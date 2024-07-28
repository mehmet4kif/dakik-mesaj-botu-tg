from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import os

# Bot token
TOKEN = 'telegram api'

# Logging configuration
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and application
bot = Bot(TOKEN)
application = Application.builder().token(TOKEN).build()

# Scheduler for message sending
scheduler = AsyncIOScheduler()
scheduler.start()

# In-memory storage for scheduled messages and groups
scheduled_tasks = []
known_groups = {}  # Using dictionary to store group IDs and names
short_ids = {}  # Mapping short IDs to full chat IDs
admin_chat_id = None  # Admin chat ID to notify about message status

# Start command handler
async def start(update: Update, context: CallbackContext):
    global admin_chat_id
    admin_chat_id = update.message.chat_id  # Store admin chat ID for notifications
    help_text = (
        "Merhaba! Bu bot belirli aralıklarla belirli gruplara mesaj atabilir.\n\n"
        "Kullanım Kılavuzu:\n"
        "/start - Botu başlatır ve bu mesajı gösterir.\n"
        "/add_group <kısa_id> <grup_id> <grup_ismi> - Bir grubu ekler. Örnek: /add_group k1 123456789 Grup İsmi\n"
        "/schedule <kısa_id> <dakika> <mesaj> - Belirli bir gruba belirli aralıklarla mesaj gönderilmesini ayarlar. "
        "Örnek: /schedule k1 30 Merhaba\n"
        "/schedule_photo <kısa_id> <dakika> <resim_url> - Belirli bir gruba belirli aralıklarla resim gönderilmesini ayarlar. "
        "Örnek: /schedule_photo k1 30 https://example.com/image.jpg\n"
        "/list_scheduled - Zamanlanmış mesajları listeler.\n"
        "/list_groups - Bilinen grupları listeler.\n\n"
        "Grup mesajları otomatik olarak tespit edilir ve bilinen gruplar listesine eklenir. "
        "Komutlarda uzun grup ID'si yerine kısa ID kullanabilirsiniz."
    )
    await update.message.reply_text(help_text)

# Add group command handler
async def add_group(update: Update, context: CallbackContext):
    try:
        short_id = context.args[0]
        chat_id = int(context.args[1])
        group_name = ' '.join(context.args[2:])
        known_groups[chat_id] = group_name
        short_ids[short_id] = chat_id
        await update.message.reply_text(f'Grup eklendi: {group_name} (ID: {chat_id}, Kısa ID: {short_id})')
    except (IndexError, ValueError):
        await update.message.reply_text('Komut formatı: /add_group <kısa_id> <grup_id> <grup_ismi>')

# Schedule text message command handler
async def schedule(update: Update, context: CallbackContext):
    try:
        short_id = context.args[0]
        interval_minutes = int(context.args[1])
        message = ' '.join(context.args[2:])
        
        chat_id = short_ids.get(short_id)
        if not chat_id:
            await update.message.reply_text('Geçersiz kısa ID.')
            return
        
        group_name = known_groups.get(chat_id, "Bilinmeyen Grup")
        scheduler.add_job(send_message, 'interval', minutes=interval_minutes, args=[chat_id, group_name, message])
        scheduled_tasks.append((chat_id, interval_minutes, message, group_name))
        await update.message.reply_text(f'Her {interval_minutes} dakikada bir {group_name} ({chat_id}) grubuna mesaj gönderilecek: {message}')
    except (IndexError, ValueError):
        await update.message.reply_text('Komut formatı: /schedule <kısa_id> <dakika> <mesaj>')

# Schedule photo message command handler
async def schedule_photo(update: Update, context: CallbackContext):
    try:
        short_id = context.args[0]
        interval_minutes = int(context.args[1])
        photo_url = context.args[2]
        
        chat_id = short_ids.get(short_id)
        if not chat_id:
            await update.message.reply_text('Geçersiz kısa ID.')
            return
        
        group_name = known_groups.get(chat_id, "Bilinmeyen Grup")
        scheduler.add_job(send_photo, 'interval', minutes=interval_minutes, args=[chat_id, group_name, photo_url])
        scheduled_tasks.append((chat_id, interval_minutes, photo_url, group_name))
        await update.message.reply_text(f'Her {interval_minutes} dakikada bir {group_name} ({chat_id}) grubuna resim gönderilecek: {photo_url}')
    except (IndexError, ValueError):
        await update.message.reply_text('Komut formatı: /schedule_photo <kısa_id> <dakika> <resim_url>')

# Send message function
async def send_message(chat_id, group_name, message):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        if admin_chat_id:
            await bot.send_message(chat_id=admin_chat_id, text=f'Mesaj başarıyla gönderildi: {group_name} ({chat_id}) - {message}')
    except Exception as e:
        if admin_chat_id:
            await bot.send_message(chat_id=admin_chat_id, text=f'Mesaj gönderimi başarısız oldu: {group_name} ({chat_id}) - {message}\nHata: {e}')

# Send photo function
async def send_photo(chat_id, group_name, photo_url):
    try:
        await bot.send_photo(chat_id=chat_id, photo=photo_url)
        if admin_chat_id:
            await bot.send_message(chat_id=admin_chat_id, text=f'Resim başarıyla gönderildi: {group_name} ({chat_id}) - {photo_url}')
    except Exception as e:
        if admin_chat_id:
            await bot.send_message(chat_id=admin_chat_id, text=f'Resim gönderimi başarısız oldu: {group_name} ({chat_id}) - {photo_url}\nHata: {e}')

# List scheduled tasks command handler
async def list_scheduled(update: Update, context: CallbackContext):
    if scheduled_tasks:
        task_list = '\n'.join([f'Her {interval_minutes} dakikada bir - {group_name} ({chat_id}) - {message}' for chat_id, interval_minutes, message, group_name in scheduled_tasks])
        await update.message.reply_text(f'Zamanlanmış Görevler:\n{task_list}')
    else:
        await update.message.reply_text('Henüz zamanlanmış görev yok.')

# List known groups command handler
async def list_groups(update: Update, context: CallbackContext):
    if known_groups:
        group_list = '\n'.join([f'Grup ID: {group_id}, Grup İsmi: {known_groups[group_id]}, Kısa ID: {short_id}' for short_id, group_id in short_ids.items()])
        await update.message.reply_text(f'Bilinen Gruplar:\n{group_list}')
    else:
        await update.message.reply_text('Henüz bilinen grup yok.')

# Message handler to capture group IDs and names
async def message_handler(update: Update, context: CallbackContext):
    chat = update.message.chat
    if chat.type in ['group', 'supergroup']:
        known_groups[chat.id] = chat.title

# Command handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('add_group', add_group))
application.add_handler(CommandHandler('schedule', schedule))
application.add_handler(CommandHandler('schedule_photo', schedule_photo))
application.add_handler(CommandHandler('list_scheduled', list_scheduled))
application.add_handler(CommandHandler('list_groups', list_groups))
application.add_handler(MessageHandler(filters.ALL, message_handler))

# Start the Bot
application.run_polling()

# Keep the scheduler running
scheduler.start()
