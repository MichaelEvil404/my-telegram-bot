import sqlite3
import os
import logging
from datetime import datetime
from threading import Thread
from flask import Flask
from pyrogram import Client, filters, types
from pyrogram.errors import UserNotParticipant

# --- ၁။ Web Server (Keep Alive) အပိုင်း ---
# Koyeb က Health Check လုပ်ဖို့ Port 8080 ကို သုံးရပါမယ်
web_app = Flask('')

@web_app.route('/')
def home():
    return "DonghuaFan Bot is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

# --- ၂။ Configuration ---
# Koyeb ရဲ့ Environment Variables မှာ သွားထည့်ပေးရမယ့် အချက်များ
API_ID = int(os.environ.get("API_ID", "27855043"))
API_HASH = os.environ.get("API_HASH", "e6dea5d571e0d9bab219026211ef54b6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8443357375:AAF5AvWe_RHVjU-K4S7K6mGklPHLHoGrpBU")

OWNER_ID = 7481946766
CHANNEL_ID = -1002428771168
CHANNEL_URL = "https://t.me/DongHuaFan"

app = Client("ultra_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- ၃။ Database Setup ---
def init_db():
    conn = sqlite3.connect("movies.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, last_seen TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS movies (name TEXT PRIMARY KEY, link1 TEXT, link2 TEXT, likes INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

# --- ၄။ Helper Functions ---
async def is_subscribed(client, message):
    if message.from_user.id == OWNER_ID: return True
    try:
        await client.get_chat_member(CHANNEL_ID, message.from_user.id)
        return True
    except UserNotParticipant:
        kb = types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Join Channel", url=CHANNEL_URL)]])
        await message.reply_text("⚠️ ရှေ့ဆက်ရန် Channel အရင် Join ပေးပါ။ ပြီးရင် /start ကို ပြန်နှိပ်ပါ။", reply_markup=kb)
        return False
    except: return True

def main_menu():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("📜 ဇာတ်ကားစာရင်း", callback_data="list_1"),
         types.InlineKeyboardButton("🎲 ကျပန်းကြည့်ရန်", callback_data="rand")],
        [types.InlineKeyboardButton("🔥 Trending", callback_data="trend"),
         types.InlineKeyboardButton("📊 စာရင်းဇယား", callback_data="stats")],
        [types.InlineKeyboardButton("🆘 အကူအညီ", callback_data="help")]
    ])

# --- ၅။ Handlers (Callback & Commands) ---
# (သင်ပေးထားတဲ့ CallbackQuery နဲ့ Message Handler တွေ ဒီကြားထဲမှာ ရှိနေရပါမယ်)
# မှတ်ချက် - စာမျက်နှာအကန့်အသတ်ကြောင့် သင့်ရဲ့ Handler အားလုံးကို ဒီမှာ ပြန်မကူးတော့ပါဘူး၊ 
# ဒါပေမဲ့ app.on_callback_query() နဲ့ app.on_message() အပိုင်းတွေကို ဒီကြားထဲမှာ ထည့်ပေးပါ။

# --- ၆။ Bot Run အပိုင်း (အရေးကြီးသည်) ---
# --- ၆။ Bot Run အပိုင်း ---
if __name__ == "__main__":
    init_db()      # Database ဆောက်မယ်
    keep_alive()   # Flask Web Server ကို အရင်နှိုးမယ်
    print("Web Server is up. Starting Pyrogram Bot...")
    
    try:
        app.run()  # Pyrogram Bot ကို စတင် Polling လုပ်ခိုင်းမယ်
    except Exception as e:
        print(f"Bot Error: {e}")
