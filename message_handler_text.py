from telegram import Update
from telegram.ext import ContextTypes
from database import DatabaseHandler

# Create a database handler object
db_handler = DatabaseHandler()

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get the message and save it to the database"""
    if update.message is not None:
        timestamp = update.message.date
        chat_id = update.effective_chat.id
        usr_full_name = update.message.from_user.full_name
        usr_id = update.message.from_user.id
        message_text = update.message.text
        message_id = update.message.message_id
        db_handler.insert_message(timestamp, chat_id, usr_full_name, usr_id, message_text, message_id)

    # [DEBUG]Send the message
    # await context.bot.send_message(
    #     chat_id=update.effective_chat.id,
    #     text= '已保存'+ '"' + message_text + '"'
    #     )
    