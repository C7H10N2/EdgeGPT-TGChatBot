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

    def search_message(self, key_word, chat_id, usr_id=None, start_time=None, end_time=None):
        # 查询消息
        search_query = 'SELECT * FROM messages WHERE message LIKE ?'
        parameters = ('%' + key_word + '%',)

        if chat_id:
            search_query += ' AND chat_id = ?'
            parameters += (chat_id,)
        if usr_id:
            search_query += ' AND usr_id = ?'
            parameters += (usr_id,)
        if start_time:
            search_query += ' AND time >= ?'
            parameters += (start_time,)
        if end_time:
            search_query += ' AND time <= ?'
            parameters += (end_time,)

        self.cursor.execute(search_query, parameters)
        rows = self.cursor.fetchall()
        
        # 获取列名，用作字典的键
        column_names = [desc[0] for desc in self.cursor.description]
        
        # 准备以字典格式输出的数据
        output_data = {}
        for idx, row in enumerate(rows, start=1):
            row_data = {}
            for i, value in enumerate(row):
                row_data[column_names[i]] = value
            output_data[f"Row {idx}"] = row_data
        
        result = output_data
        return result
