import yt_dlp
import os
from config import DOWNLOAD_PATH, TEMP_PATH
from logger import logger
from utils import sanitize_filename

class VideoDownloader:
    def __init__(self, progress_hook=None):
        self.progress_hook = progress_hook
        self.ydl_opts = {
            'format': 'bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]',
            'outtmpl': os.path.join(TEMP_PATH, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'progress_hooks': [self.progress_hook] if self.progress_hook else [],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'logger': logger,
            'cookiefile': 'cookies.txt', # Placeholder for potential future use
        }

    def get_video_info(self, url):
        try:
            with yt_dlp.YoutubeDL({'noplaylist': True, 'logger': logger}) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except Exception as e:
            logger.error(f"Error extracting video info for {url}: {e}")
            return None

    def download_video(self, url):
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)
                # yt-dlp might add .mp4 even if it's already there, or merge to .mp4
                # We need to find the actual merged file.
                if info.get('requested_downloads'):
                    for f in info['requested_downloads']:
                        if f.get('filepath') and os.path.exists(f['filepath']):
                            filepath = f['filepath']
                            break
                elif info.get('_filename') and os.path.exists(info['_filename']):
                    filepath = info['_filename']
                
                # Ensure the file has a .mp4 extension if it was merged
                if not filepath.endswith('.mp4') and os.path.exists(filepath + '.mp4'):
                    filepath = filepath + '.mp4'

                # Move the downloaded file to the DOWNLOAD_PATH and sanitize filename
                original_filename = os.path.basename(filepath)
                sanitized_name = sanitize_filename(info.get('title', 'video')) + os.path.splitext(original_filename)[1]
                final_path = os.path.join(DOWNLOAD_PATH, sanitized_name)
                
                os.rename(filepath, final_path)
                logger.info(f"Downloaded and moved: {final_path}")
                return final_path
        except Exception as e:
            logger.error(f"Error downloading video from {url}: {e}")
            return None

    def download_audio(self, url):
        audio_ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(TEMP_PATH, '%(title)s.%(ext)s'),
            'extractaudio': True,
            'audioformat': 'mp3',
            'noplaylist': True,
            'progress_hooks': [self.progress_hook] if self.progress_hook else [],
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': logger,
            'cookiefile': 'cookies.txt', # Placeholder for potential future use
        }
        try:
            with yt_dlp.YoutubeDL(audio_ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filepath = ydl.prepare_filename(info)
                # yt-dlp often renames the file to .mp3 after postprocessing
                if not filepath.endswith('.mp3') and os.path.exists(os.path.splitext(filepath)[0] + '.mp3'):
                    filepath = os.path.splitext(filepath)[0] + '.mp3'

                original_filename = os.path.basename(filepath)
                sanitized_name = sanitize_filename(info.get('title', 'audio')) + os.path.splitext(original_filename)[1]
                final_path = os.path.join(DOWNLOAD_PATH, sanitized_name)
                
                os.rename(filepath, final_path)
                logger.info(f"Downloaded and moved audio: {final_path}")
                return final_path
        except Exception as e:
            logger.error(f"Error downloading audio from {url}: {e}")
            return None
