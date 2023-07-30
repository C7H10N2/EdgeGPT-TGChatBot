from telegram import Update
from telegram.ext import ContextTypes
import time

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ping the bot and get a response."""
    receive_time = time.time()
    text_ping = 'pong!'

    # Send the initial message
    sent_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_ping
        )
    
    # Calculate the delay
    send_time = time.time()
    delay = (send_time - receive_time) * 1000
    text_delay = f'({delay:.1f} ms)'

    # Edit the initial message
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=sent_message.message_id,
        text=f'{text_ping}\n{text_delay}'
        )
