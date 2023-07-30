from telegram import Update
from telegram.ext import ContextTypes
from database import DatabaseHandler

# Create a database handler object
db_handler = DatabaseHandler()

async def handle_media_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the message type and save it to the database"""
    if update.message.caption:
        message = update.message.caption
    else:
        message = ''
    
    timestamp = update.message.date
    chat_id = update.effective_chat.id
    usr_full_name = update.message.from_user.full_name
    usr_id = update.message.from_user.id
    message_type = str(get_message_type(update.message))+message
    message_id = update.message.message_id
    db_handler.insert_message(timestamp, chat_id, usr_full_name, usr_id, message_type, message_id)

def get_message_type(message):
    # Get the message type
    if message.photo:
        return '[图片]'
    elif message.sticker:
        return '[贴纸]'+message.sticker.emoji
    elif message.video: 
        return '[视频]'
    elif message.document: 
        return '[文件'+message.document.mime_type+']'
    elif message.voice:
       return '[语音]'
    else:
        return '[其他类型'+message.content_type+']'
