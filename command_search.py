from telegram import Update
from telegram.ext import ContextTypes
from database import DatabaseHandler
import re, json

# Create a database handler object
db_handler = DatabaseHandler()

# Define functions to process input commands
def parse_command(text):
    # Def a function to parse the command arguments
    pattern = r'(?P<key_word>\S+)(?:\s+-id\s+(?P<usr_id>\S+))?(?:\s+-st\s+(?P<start_time>\S+))?(?:\s+-et\s+(?P<end_time>\S+))?'
    match = re.match(pattern, text)

    if match:
        # Get the arguments
        key_word = match.group('key_word')
        usr_id = match.group('usr_id')
        start_time = match.group('start_time')
        end_time = match.group('end_time')
        return key_word, usr_id, start_time, end_time
    else:
        # If not match, return None
        return None, None, None, None

# Define a function to format the message data
def format_message_data(data):
    formatted_data = {}
    for key, value in data.items():
        row_number = key.split()[-1]
        usr_full_name = value["usr_full_name"]
        message = value["message"]
        date = value["date"]
        chat_id = str(abs(value["chat_id"]))[3:]
        message_id = value["message_id"]

        # Truncate the usr_full_name and message fields.
        max_usr_full_name_length = 8
        max_message_length = 15
        usr_full_name = usr_full_name[:max_usr_full_name_length] + "..." if len(
            usr_full_name) > max_usr_full_name_length else usr_full_name
        message = message[:max_message_length] + \
            "..." if len(message) > max_message_length else message

        # Formatted date
        date = "/".join(date.split("-")[1:])  # MM/DD

        # Escape the "." character
        usr_full_name = usr_full_name.replace(".", "\.")
        message = message.replace(".", "\.")

        formatted_data[
            row_number] = f"{row_number}．{usr_full_name}：{message} {date} [-->](https://t.me/c/{chat_id}/{message_id})"
    return formatted_data



async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Search the message./search key_word -id <usr-id> -st <start-time> -et <end-time>"""
    # Get the command arguments
    message_text = str(update.message.text)
    text = message_text[8:]

    if text == '':
        await update.message.reply_text('请输入关键词')
    else:
        chat_id = update.effective_chat.id
        key_word, usr_id, start_time, end_time = parse_command(text)

        sent_message = await update.message.reply_text('正在搜索，请稍后')
        # Search the message
        results = db_handler.search_message(
            key_word, chat_id, usr_id, start_time, end_time)
        # Send the message
        # Format the message data in Markdown format
        formatted_data = format_message_data(results)

        # Convert formatted_data to Markdown format
        markdown_output = "\n".join(formatted_data.values())
        print(markdown_output)

        await context.bot.edit_message_text(
            chat_id = update.effective_chat.id,
            message_id = sent_message.message_id,
            text = markdown_output,
            parse_mode = 'Markdown'
        )
