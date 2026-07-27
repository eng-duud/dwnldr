from telegram import Update
from telegram.ext import ContextTypes
from config import OWNER_ID, DOWNLOAD_PATH, TEMP_PATH
from logger import logger
from utils import is_valid_url, clean_up_files, create_directories
from downloader import VideoDownloader
import os
import asyncio

# Dictionary to store download progress for each user/message
DOWNLOAD_PROGRESS = {}

async def check_owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("❌ This bot is private.")
        logger.warning(f"Unauthorized access attempt by user ID: {update.effective_user.id}")
        return False
    return True

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update, context):
        return
    await update.message.reply_text("مرحباً بك! أنا بوت تحميل الفيديوهات الخاص بك. أرسل لي رابط فيديو لبدء التحميل.")
    logger.info(f"User {update.effective_user.id} started the bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update, context):
        return
    help_text = (
        "أوامر البوت المتاحة:\n"
        "/start - بدء البوت ورسالة الترحيب\n"
        "/help - عرض قائمة الأوامر\n"
        "/info - عرض معلومات الخادم\n"
        "/audio <URL> - تحميل الصوت فقط\n"
        "/video <URL> - تحميل الفيديو\n"
        "أو أرسل الرابط مباشرة."
    )
    await update.message.reply_text(help_text)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner(update, context):
        return
    await update.message.reply_text("خادم البوت يعمل وجاهز لاستلام طلباتك.")

async def download_progress_hook(d, update: Update, message_id: int, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if d["status"] == "downloading":
        _percent_str = d.get("_percent_str", "0%")
        _speed_str = d.get("_speed_str", "N/A")
        _eta_str = d.get("_eta_str", "N/A")
        
        current_progress = f"التقدم: {_percent_str}\nالسرعة: {_speed_str}\nالوقت المتبقي: {_eta_str}"
        
        if chat_id not in DOWNLOAD_PROGRESS:
            DOWNLOAD_PROGRESS[chat_id] = {}
            
        if DOWNLOAD_PROGRESS[chat_id].get(message_id) != current_progress:
            try:
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"جاري التحميل...\n{current_progress}"
                )
                DOWNLOAD_PROGRESS[chat_id][message_id] = current_progress
            except Exception:
                pass
    elif d["status"] == "finished":
        if chat_id in DOWNLOAD_PROGRESS and message_id in DOWNLOAD_PROGRESS[chat_id]:
            del DOWNLOAD_PROGRESS[chat_id][message_id]

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE, download_type: str = "video"):
    if not await check_owner(update, context):
        return

    url = context.args[0] if context.args else update.message.text
    if not url or not is_valid_url(url):
        await update.message.reply_text("الرجاء إرسال رابط صحيح.")
        return

    status_message = await update.message.reply_text("جاري تحليل الرابط...")
    message_id = status_message.message_id

    downloader = VideoDownloader(progress_hook=lambda d: asyncio.create_task(download_progress_hook(d, update, message_id, context)))
    file_path = None
    try:
        info = await asyncio.to_thread(downloader.get_video_info, url)
        if not info:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text="❌ تعذر الحصول على معلومات الفيديو.")
            return

        title = info.get("title", "video")
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=f"تم البدء في تحميل: {title[:50]}...")

        if download_type == "video":
            file_path = await asyncio.to_thread(downloader.download_video, url)
        else:
            file_path = await asyncio.to_thread(downloader.download_audio, url)

        if file_path and os.path.exists(file_path):
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text="جاري الرفع إلى تليجرام...")
            if download_type == "video":
                await update.message.reply_video(video=open(file_path, 'rb'), caption=title)
            else:
                await update.message.reply_audio(audio=open(file_path, 'rb'), caption=title)
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text="✅ تم التحميل بنجاح.")
        else:
            await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text="❌ فشل التحميل.")

    except Exception as e:
        logger.error(f"Error: {e}")
        await context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=message_id, text=f"❌ خطأ: {str(e)}")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Removed file: {file_path}")
        clean_up_files(TEMP_PATH)

async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_url(update, context, download_type="video")

async def audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_url(update, context, download_type="audio")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if is_valid_url(update.message.text):
        await handle_url(update, context, download_type="video")
    else:
        await update.message.reply_text("أرسل رابط فيديو صحيح.")

async def post_init(application):
    create_directories()

async def shutdown(application):
    pass
