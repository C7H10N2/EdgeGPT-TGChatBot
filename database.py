import sqlite3

class DatabaseHandler:
    def __init__(self, db_name='chat_messages.db'):
        # Connect to the database
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        # Create table if not exists
        self.create_table()

    def __del__(self):
        # Close the connection
        self.conn.close()

    def create_table(self):
        # Create table of messages
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               date TEXT,
                               time TEXT,
                               chat_id INTEGER,
                               usr_full_name TEXT,
                               usr_id INTEGER,
                               message TEXT,
                               message_id INTEGER)''')
        self.conn.commit()

    def insert_message(self, timestamp, chat_id, usr_full_name, usr_id, message_text, message_id):
        # Convert the timestamp to date and time strings
        date = timestamp.strftime('%Y-%m-%d')  # Format as year-month-day
        time = timestamp.strftime('%H:%M:%S')  # Format as hour:minute:second

        # Include the message in the database
        self.cursor.execute('INSERT INTO messages (date, time, chat_id, usr_full_name, usr_id, message, message_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (date, time, chat_id, usr_full_name, usr_id, message_text, message_id))
        self.conn.commit()
