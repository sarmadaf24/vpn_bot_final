import telebot
from telebot import types
import sqlite3
import qrcode
import random
import string

# تنظیمات ربات و توکن تلگرام
TOKEN = "7314186934:AAEN3XMuXkNqoDi9q-RWYU2hk2uHmKcPMLo"
bot = telebot.TeleBot(TOKEN)

# اتصال به پایگاه داده
conn = sqlite3.connect("vpn_bot.db", check_same_thread=False)
cursor = conn.cursor()

# ایجاد جدول کاربران و کانفیگ‌ها در دیتابیس
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    balance INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS configs (
    config_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    config_name TEXT,
    protocol TEXT,
    server TEXT,
    port INTEGER,
    uuid TEXT,
    expiration_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")
conn.commit()

# دستورات ربات
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, message.chat.username))
    conn.commit()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📌 لیست پلن‌ها")
    btn2 = types.KeyboardButton("💰 خرید پلن")
    btn3 = types.KeyboardButton("📊 وضعیت اکانت")
    btn4 = types.KeyboardButton("📢 پشتیبانی")
    btn5 = types.KeyboardButton("💳 پرداخت و کیف پول")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(user_id, "سلام! به ربات فروش VPN خوش آمدید! 😃", reply_markup=markup)

# راه‌اندازی ربات
bot.polling(none_stop=True)
