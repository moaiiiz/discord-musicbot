import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from datetime import datetime
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

# YouTube DL options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'ytsearch',
    'quiet': False,
    'no_warnings': False,
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('webpage_url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url']
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class MusicQueue:
    def __init__(self):
        self.queue = []
        self.now_playing = None
    
    def add(self, item):
        self.queue.append(item)
    
    def get_next(self):
        if self.queue:
            return self.queue.pop(0)
        return None
    
    def clear(self):
        self.queue.clear()
    
    def is_empty(self):
        return len(self.queue) == 0

# Create a music queue for the guild
guild_queues = {}

def get_queue(guild_id):
    if guild_id not in guild_queues:
        guild_queues[guild_id] = MusicQueue()
    return guild_queues[guild_id]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('------')

@bot.command(name='join', help='Joins the voice channel')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send('You are not connected to a voice channel.')
        return
    
    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()
    
    await ctx.send(f'Joined {channel.name}')  

@bot.command(name='leave', help='Leaves the voice channel')
async def leave(ctx):
    if ctx.voice_client is None:
        await ctx.send('Not connected to a voice channel.')
        return
    
    queue = get_queue(ctx.guild.id)
    queue.clear()
    await ctx.voice_client.disconnect()
    await ctx.send('Left the voice channel')

@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, *, query):
    if not ctx.author.voice:
        await ctx.send('You must be in a voice channel to use this command.')
        return
    
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    
    async with ctx.typing():
        try:
            player = await YTDLSource.from_url(query, loop=bot.loop)
            queue = get_queue(ctx.guild.id)
            
            if ctx.voice_client.is_playing():
                queue.add(player)
                await ctx.send(f'Added to queue: **{player.title}**')
            else:
                ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(
                    play_next(ctx), bot.loop))
                await ctx.send(f'Now playing: **{player.title}**')
        except Exception as e:
            await ctx.send(f'Error: {str(e)}')

async def play_next(ctx):
    queue = get_queue(ctx.guild.id)
    next_player = queue.get_next()
    
    if next_player:
        ctx.voice_client.play(next_player, after=lambda e: asyncio.run_coroutine_threadsafe(
            play_next(ctx), bot.loop))
        await ctx.send(f'Now playing: **{next_player.title}**')

@bot.command(name='pause', help='Pauses the current song')
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send('Music paused')
    else:
        await ctx.send('No music is playing')

@bot.command(name='resume', help='Resumes the paused song')
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send('Music resumed')
    else:
        await ctx.send('No music is paused')

@bot.command(name='stop', help='Stops the current song')
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        queue = get_queue(ctx.guild.id)
        queue.clear()
        await ctx.send('Music stopped')
    else:
        await ctx.send('No music is playing')

@bot.command(name='queue', help='Shows the current queue')
async def queue(ctx):
    queue = get_queue(ctx.guild.id)
    
    if queue.is_empty():
        await ctx.send('Queue is empty')
        return
    
    queue_list = '\n'.join([f'{i+1}. {player.title}' for i, player in enumerate(queue.queue)])
    await ctx.send(f'**Queue:**\n{queue_list}') 

@bot.command(name='volume', help='Changes the volume (0-100)')
async def volume(ctx, vol: int):
    if not 0 <= vol <= 100:
        await ctx.send('Volume must be between 0 and 100')
        return
    
    if ctx.voice_client and ctx.voice_client.source:
        ctx.voice_client.source.volume = vol / 100
        await ctx.send(f'Volume set to {vol}%')
    else:
        await ctx.send('No music is playing')

@bot.command(name='help', help='Shows all available commands')
async def help_command(ctx):
    embed = discord.Embed(title='Music Bot Commands', color=discord.Color.blue())
    embed.add_field(name='!join', value='Joins your voice channel', inline=False)
    embed.add_field(name='!leave', value='Leaves the voice channel', inline=False)
    embed.add_field(name='!play <query>', value='Plays a song from YouTube', inline=False)
    embed.add_field(name='!pause', value='Pauses the current song', inline=False)
    embed.add_field(name='!resume', value='Resumes the paused song', inline=False)
    embed.add_field(name='!stop', value='Stops the current song', inline=False)
    embed.add_field(name='!queue', value='Shows the current queue', inline=False)
    embed.add_field(name='!volume <0-100>', value='Changes the volume', inline=False)
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == '__main__':
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print('Error: DISCORD_TOKEN not found in .env file')
    else:
        bot.run(TOKEN)
