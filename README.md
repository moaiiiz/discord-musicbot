# Discord Music Bot

A fully-featured Discord music bot built with discord.py that allows you to play music from YouTube in your Discord server's voice channels.

## 🎵 Features

- **YouTube Integration**: Stream music directly from YouTube
- **Queue Management**: Add songs to a queue and play them sequentially
- **Playback Controls**: Play, pause, resume, and stop functionality
- **Volume Control**: Adjust playback volume (0-100%)
- **Voice Channel Management**: Automatic join and leave functionality
- **Queue Viewing**: See what's coming up in your queue
- **Simple Commands**: Easy-to-use command system with `!` prefix
- **Error Handling**: Robust error handling and user feedback

## 📋 Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- A Discord bot token
- discord.py library

### Installing FFmpeg

**Windows:**
```bash
# Using chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## 🚀 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/moaiiiz/discord-musicbot.git
cd discord-musicbot
```

2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your Discord bot token:**
   - Copy `.env.example` to `.env`
   - Add your Discord bot token to the `.env` file:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   ```

5. **Run the bot:**
```bash
python main.py
```

## 🔑 Getting Your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" tab and click "Add Bot"
4. Copy the token and paste it in your `.env` file
5. Enable the following intents:
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 → URL Generator
7. Select scopes: `bot`
8. Select permissions: `Send Messages`, `Connect`, `Speak`, `Use Voice Activity`
9. Copy the generated URL and open it in your browser to invite the bot to your server

## 📖 Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `!join` | `!join` | Joins your current voice channel |
| `!leave` | `!leave` | Leaves the voice channel and clears queue |
| `!play` | `!play <song name or URL>` | Plays a song from YouTube (or adds to queue if already playing) |
| `!pause` | `!pause` | Pauses the current song |
| `!resume` | `!resume` | Resumes the paused song |
| `!stop` | `!stop` | Stops playback and clears the queue |
| `!queue` | `!queue` | Shows the current queue |
| `!volume` | `!volume <0-100>` | Sets the volume (0-100%) |
| `!help` | `!help` | Shows all available commands |

## 💡 Usage Examples

```
# Join a voice channel
!join

# Play a song by name
!play Bohemian Rhapsody

# Play a song by YouTube URL
!play https://www.youtube.com/watch?v=fJ9rUzIMt7o

# Queue multiple songs
!play Song 1
!play Song 2
!play Song 3

# Control playback
!pause
!resume
!stop

# Check what's playing
!queue

# Adjust volume
!volume 50
!volume 100

# Leave the voice channel
!leave
```

## 🛠️ Technical Details

### Architecture

- **YTDLSource**: Custom class for handling YouTube downloads and audio streaming
- **MusicQueue**: Queue management system for each guild
- **Command Handler**: discord.py's command extension system

### Dependencies

- **discord.py**: Discord API wrapper
- **yt-dlp**: YouTube downloader and metadata extractor
- **python-dotenv**: Environment variable management
- **PyNaCl**: Voice support for discord.py

## 🐛 Troubleshooting

### Bot doesn't connect to voice channel
- Make sure the bot has "Connect" and "Speak" permissions in the voice channel
- Verify FFmpeg is installed: `ffmpeg -version`

### No audio or very quiet audio
- Check the volume: `!volume 100`
- Make sure FFmpeg is properly installed
- Try restarting the bot

### "DISCORD_TOKEN not found" error
- Ensure you created a `.env` file
- Make sure your Discord token is correctly placed in the `.env` file
- Restart the bot

### Songs won't play
- Check your internet connection
- Try searching with a more specific song name
- Make sure the YouTube video is not age-restricted or region-locked

### Bot is offline
- Check your Discord token is valid
- Ensure the bot has the necessary intents enabled in Developer Portal
- Check console for error messages

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created by [moaiiiz](https://github.com/moaiiiz)

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## 📞 Support

If you encounter any issues, please open an issue on the GitHub repository.

---

**Happy listening! 🎶**