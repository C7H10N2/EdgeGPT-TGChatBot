import logging
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler
from config import set_proxy_url, set_token
from command_start import start
from command_ping import ping
from message_handler_text import handle_text_message
from message_handler_media import handle_media_message

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(set_token).proxy_url(set_proxy_url).get_updates_proxy_url(set_proxy_url).build()

    # Set handlers
    start_handler = CommandHandler('start', start)
    caps_handler = CommandHandler('ping', ping)
    text_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text_message)
    media_filters = filters.ALL & (~filters.COMMAND) & (~filters.TEXT)
    media_handler = MessageHandler(media_filters, handle_media_message)

    # Add handlers to the application
    application.add_handler(start_handler)
    application.add_handler(caps_handler)
    application.add_handler(text_handler)
    application.add_handler(media_handler)

    # Run the application
    application.run_polling()
