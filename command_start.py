from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when bot was started."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This bot is working!"
    )