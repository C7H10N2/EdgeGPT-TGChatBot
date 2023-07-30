import sqlite3
import os
import re
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import logging
import jieba, jieba.analyse

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 连接数据库
def connect_to_database(db_name='chat_messages.db'):
    conn = sqlite3.connect(db_name)
    return conn

# 从数据库中查询指定日期和聊天 ID 的数据
def get_data_from_database(conn, target_date, target_chat_id):
    cursor = conn.cursor()
    cursor.execute('SELECT date, time, chat_id, usr_full_name, usr_id, message, message_id FROM messages WHERE date = ? AND chat_id = ?', (target_date, target_chat_id))
    data = cursor.fetchall()
    columns = ['date', 'time', 'chat_id', 'usr_full_name', 'usr_id', 'message', 'message_id']
    df = pd.DataFrame(data, columns=columns)

    # 清洗消息文本并存储在 'cleaned_message' 列中
    df['cleaned_message'] = df['message'].apply(clean_message)
    df['cleaned_name'] = df['usr_full_name'].apply(clean_message)

    return df

# 函数用于清洗消息文本
def clean_message(message):
    # 移除类型标签
    message = message.replace("[图片]", "").replace("[贴纸]", "").replace("[视频]", "").replace("[语音]", "").replace("[其他类型]", "")
    # 移除以 '[文件' 开头的内容
    message = re.sub(r'^\[文件.*', '', message)
    # 移除表情符号
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    message = emoji_pattern.sub(r'', message)

    return message

# 步骤 1：按用户绘制消息数量的饼图
def plot_message_counts_pie_chart(data):
    user_counts = data['cleaned_name'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(user_counts, labels=user_counts.index, autopct='%1.1f%%', startangle=140)

    plt.axis('equal')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rc

    plt.show()

# 步骤 2：生成使用 jieba 分词的清洗后消息文本的词云图
def generate_word_cloud(data):
    # 使用 jieba 进行中文文本分词
    words = ' '.join(jieba.cut(''.join(data['cleaned_message'])))

    # 过滤停用词
    stopwords_file = os.path.abspath('data/stopwords/stopwords_full.txt')
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        stopwords = set(f.read().splitlines())
    filtered_words = [word for word in words.split() if word not in stopwords]

    # 获取 Microsoft YaHei 字体的绝对路径
    font_path = os.path.abspath('data\fonts\msyh.ttc')

    # 创建一个词频计数器
    word_freq = {}
    for word in filtered_words:
        word_freq[word] = word_freq.get(word, 0) + 1

    # 生成词云图
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate_from_frequencies(word_freq)

    plt.figure(figsize=(12, 7))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    # 步骤 1：连接数据库
    conn = connect_to_database()

    # 步骤 2：查询数据库并获取指定日期和聊天 ID 的数据
    target_date = '2023-07-30'
    target_chat_id = -1001838000252  # 请用实际的聊天 ID 替换这个示例值
    data = get_data_from_database(conn, target_date, target_chat_id)

    # 步骤 3：为每个用户绘制消息数量的饼图
    #plot_message_counts_pie_chart(data)

    # 步骤 5：为消息文本生成词云图
    generate_word_cloud(data)

    # 关闭数据库连接
    conn.close()
