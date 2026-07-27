# Private Telegram Video Downloader Bot

This is a personal Telegram bot designed to download videos and audio from various platforms using `yt-dlp` and `FFmpeg`.

## Features

- Download videos and audio from supported URLs.
- Supports a wide range of websites (YouTube, TikTok, Instagram, Facebook, X, Reddit, Vimeo, Dailymotion, Twitch, Pinterest, etc.).
- Personal use only: verifies `OWNER_ID` for all interactions.
- Command-based downloads (`/video`, `/audio`) and automatic URL detection.
- Progress updates during download and upload.
- Automatic cleanup of temporary files.
- Logging of bot activities and errors.

## Project Structure

```
telegram_downloader_bot/
├── bot.py
├── handlers.py
├── downloader.py
├── config.py
├── utils.py
├── logger.py
├── requirements.txt
├── README.md
├── .env.example
├── downloads/
├── temp/
└── logs/
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/telegram_downloader_bot.git
cd telegram_downloader_bot
```

### 2. Create a virtual environment

It\'s highly recommended to use a virtual environment to manage dependencies.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install FFmpeg

`yt-dlp` requires `FFmpeg` to merge audio and video streams. Follow the instructions for your operating system:

- **Ubuntu/Debian:**
  ```bash
sudo apt update
sudo apt install ffmpeg
  ```
- **Fedora:**
  ```bash
sudo dnf install ffmpeg
  ```
- **macOS (using Homebrew):**
  ```bash
brew install ffmpeg
  ```
- **Windows:**
  Download the latest FFmpeg build from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` directory to your system\'s PATH environment variable.

### 5. Create your Telegram Bot and obtain `BOT_TOKEN`

1. Open Telegram and search for `@BotFather`.
2. Start a chat with `@BotFather` and send `/newbot`.
3. Follow the instructions to choose a name and username for your bot.
4. `@BotFather` will provide you with an API token (e.g., `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`). This is your `BOT_TOKEN`.

### 6. Obtain your `OWNER_ID`

1. Open Telegram and search for `@userinfobot`.
2. Start a chat with `@userinfobot` and send `/start`.
3. The bot will reply with your user ID (a numerical value). This is your `OWNER_ID`.

### 7. Configure environment variables

Create a `.env` file in the root of your project directory (e.g., `telegram_downloader_bot/.env`) and add the following:

```ini
BOT_TOKEN=YOUR_BOT_TOKEN
OWNER_ID=YOUR_TELEGRAM_USER_ID
DOWNLOAD_PATH=downloads
LOG_PATH=logs
TEMP_PATH=temp
```

Replace `YOUR_BOT_TOKEN` with the token obtained from `@BotFather` and `YOUR_TELEGRAM_USER_ID` with your ID from `@userinfobot`.

## Running Locally

After completing the installation and configuration steps:

```bash
source venv/bin/activate # Activate your virtual environment
python bot.py
```

The bot should now be running and accessible via Telegram.

## Deployment

This section provides basic deployment guides for various platforms. Remember to set up environment variables (`BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`) on your chosen platform.

### Railway

- **Environment Variables:** Set `BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`.
- **Build Command:** `pip install -r requirements.txt && sudo apt update && sudo apt install -y ffmpeg`
- **Start Command:** `python bot.py`

### Render

- **Environment Variables:** Set `BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`.
- **Build Command:** `pip install -r requirements.txt && sudo apt update && sudo apt install -y ffmpeg`
- **Start Command:** `python bot.py`

### Koyeb

- **Environment Variables:** Set `BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`.
- **Build Command:** `pip install -r requirements.txt && sudo apt update && sudo apt install -y ffmpeg`
- **Start Command:** `python bot.py`

### Northflank

- **Environment Variables:** Set `BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`.
- **Build Command:** `pip install -r requirements.txt && sudo apt update && sudo apt install -y ffmpeg`
- **Start Command:** `python bot.py`

### Fly.io

For Fly.io, you\'ll typically use a `Dockerfile`. Here\'s a basic example:

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.12-slim-bookworm

# Set the working directory in the container
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
# EXPOSE 8000 # Not strictly needed for Telegram bots as they use long polling

# Run bot.py when the container launches
CMD ["python", "bot.py"]
```

- **Environment Variables:** Set `BOT_TOKEN`, `OWNER_ID`, `DOWNLOAD_PATH`, `LOG_PATH`, `TEMP_PATH`.
- **Build Command:** (Handled by Dockerfile)
- **Start Command:** (Handled by Dockerfile `CMD`)

## Troubleshooting

- **Bot not responding:**
  - Check your `.env` file for correct `BOT_TOKEN` and `OWNER_ID`.
  - Ensure the bot is running (`python bot.py`).
  - Check the `logs/bot.log` file for errors.
- **Download failures:**
  - Verify the URL is valid and supported by `yt-dlp`.
  - Ensure `FFmpeg` is correctly installed and accessible in your system\'s PATH.
  - Check `logs/bot.log` for `yt-dlp` specific errors.
- **`OWNER_ID` issue:**
  - Make sure your `OWNER_ID` in `.env` is correct and is an integer.
  - If you\'re getting "❌ This bot is private." message, it means your `OWNER_ID` is not matching the sender\'s ID.

---

**Author:** Manus AI
