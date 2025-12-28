import sqlite3
import logging
import random
import os
from datetime import datetime
from pyrogram import Client, filters, types
from pyrogram.errors import UserNotParticipant
from flask import Flask
from threading import Thread
import telebot

# --- ၁။ Web Server ဆောက်တဲ့အပိုင်း (Keep Alive) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Koyeb သို့မဟုတ် Render အတွက် Port 8080 ကို အသုံးပြုပါ
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
    
# --- ၃။ Bot ကို စတင်နှိုးစက်ပေးတဲ့အပိုင်း ---
if __name__ == "__main__":
    # Web Server ကို နောက်ကွယ်မှာ အရင် Run ခိုင်းပါမယ်
    keep_alive()
    print("Web Server Started")
    
    # Bot ကို အမြဲတမ်း Polling လုပ်နေအောင် ထားပါမယ်
    bot.infinity_polling()

# Koyeb Health Check အောင်မြင်ရန်အတွက် Port တစ်ခု ဖွင့်ပေးခြင်း
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is Alive!"

def run():
    # Koyeb က ပေးတဲ့ Port ကို သုံးမယ်၊ မရှိရင် 8000 ကို သုံးမယ်
    port = int(os.environ.get("PORT", 8000))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# သင့်ရဲ့ Bot code တွေ မစခင် ဒါကို အရင်ခေါ်ထားပါ
keep_alive()

# --- ၁။ Configuration ---
# Koyeb မှာ Environment Variables အဖြစ် ထည့်သွင်းရပါမယ်
API_ID = int(os.environ.get("API_ID", "27855043"))
API_HASH = os.environ.get("API_HASH", "e6dea5d571e0d9bab219026211ef54b6")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8443357375:AAF5AvWe_RHVjU-K4S7K6mGklPHLHoGrpBU")

OWNER_ID = 7481946766
CHANNEL_ID = -1002428771168
CHANNEL_URL = "https://t.me/DongHuaFan"

app = Client("ultra_movie_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- ၂။ Database Setup ---
def init_db():
    conn = sqlite3.connect("movies.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, last_seen TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS movies (name TEXT PRIMARY KEY, link1 TEXT, link2 TEXT, likes INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

init_db()

# --- ၃။ Helper Functions ---
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

# --- ၄။ Callback Handlers ---
@app.on_callback_query()
async def cb_handler(client, cb):
    conn = sqlite3.connect("movies.db")
    data = cb.data

    if data == "back":
        await cb.message.edit_text("👋 **မင်္ဂလာပါ Donghua Fan တို့ရေ...**\n\n"
    "ကျွန်တော်ကတော့ သင်ကြည့်ချင်တဲ့ Donghua ဇာတ်ကားတွေကို အမြန်ဆုံး ရှာဖွေပေးမယ့် **DonghuaFan Official Bot** ပါ။ 🐉\n\n"
    "🔹 **အသုံးပြုနည်း-**\n"
    "ဇာတ်ကားနာမည်ကို Chat box ထဲမှာ ရိုက်ပို့ပြီး ရှာဖွေနိုင်ပါတယ်။\n\n"
    "💡 အောက်က Menu ခလုတ်တွေကို အသုံးပြုပြီးတော့လည်း ဇာတ်ကားစာရင်းတွေကို စစ်ဆေးနိုင်ပါတယ်ခင်ဗျာ။", reply_markup=main_menu())
    
    elif data == "help":
        await cb.message.edit_text("🆘 **အကူအညီ**\n\n၁။ ဇာတ်ကားရှာရန် ဇာတ်ကားနာမည်ရေး‌ပို့ပါ\n၂။ Like ပေးရန် Like ခလုတ်ကိုနှိပ်ပါ။\n၃။ ဘာကားကြည့်ရမလဲ မသိရင် ကျပန်းကြည့်ရန် နှိပ်ပါ\n၄။ Like များတဲ့ကားကြည့်ချင်ရင် Trading ကိုနှိပ်ပါ\n၅။ ဘာကားတွေတင်ထားလဲသိချင်ရင် ဇာတ်ကားစာရင်း ကိုနှိပ်ပါ\n\nBy @DongHuaFan", 
            reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("🏠 Back", callback_data="back")]]))

    elif data == "rand":
        movie = conn.execute("SELECT name, link1, link2, likes, rowid FROM movies ORDER BY RANDOM() LIMIT 1").fetchone()
        if movie:
            t = f"🎬 **{movie[0].upper()}**\n\n🔗 Link 1: {movie[1]}\n👍 Likes: {movie[3]}"
            kb = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(f"👍 Like This", callback_data=f"lk_{movie[4]}")],
                                             [types.InlineKeyboardButton("🏠 Back", callback_data="back")]])
            await cb.message.edit_text(t, reply_markup=kb)
        else: await cb.answer("ဇာတ်ကားမရှိသေးပါ။", show_alert=True)

    elif data == "trend":
        top = conn.execute("SELECT name, likes FROM movies WHERE likes > 0 ORDER BY likes DESC LIMIT 10").fetchall()
        if top:
            t = "🔥 **Trending Top 10**\n\n" + "\n\n".join([f"{i+1}. {m[0].upper()} ({m[1]} likes)" for i, m in enumerate(top)])
            await cb.message.edit_text(t, reply_markup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("🏠 Back", callback_data="back")]]))
        else: await cb.answer("Trending မရှိသေးပါ။", show_alert=True)

    elif data.startswith("lk_"):
        m_id = data.split("_")[1]
        conn.execute("UPDATE movies SET likes = likes + 1 WHERE rowid = ?", (m_id,))
        conn.commit()
        new_l = conn.execute("SELECT likes FROM movies WHERE rowid = ?", (m_id,)).fetchone()[0]
        await cb.answer(f"Liked! အခု {new_l} ဖြစ်သွားပါပြီ 👍", show_alert=True)
        try:
            await cb.message.edit_reply_markup(reply_markup=types.InlineKeyboardMarkup([
                [types.InlineKeyboardButton(f"✅ Liked ({new_l})", callback_data="done")],
                [types.InlineKeyboardButton("🏠 Back", callback_data="back")]
            ]))
        except: pass

    elif data.startswith("list_"):
        page = int(data.split("_")[1])
        offset = (page - 1) * 10
        movies = conn.execute("SELECT name FROM movies LIMIT 10 OFFSET ?", (offset,)).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
        if movies:
            t = f"📜 **ဇာတ်ကားစာရင်း (Page {page})**\n\n" + "\n\n".join([f"{offset+i+1}. {m[0].upper()}" for i, m in enumerate(movies)])
            btns = []
            if page > 1: btns.append(types.InlineKeyboardButton("⬅️ Prev", callback_data=f"list_{page-1}"))
            if offset + 10 < total: btns.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"list_{page+1}"))
            await cb.message.edit_text(t, reply_markup=types.InlineKeyboardMarkup([btns, [types.InlineKeyboardButton("🏠 Back", callback_data="back")]]))

    elif data == "stats":
        u = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        m = conn.execute("SELECT COUNT(*) FROM movies").fetchone()[0]
        await cb.answer(f"👥 Users: {u} | 🎬 Movies: {m}", show_alert=True)
    
    conn.close()

# --- ၅။ Admin & Search Commands ---
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    user_id = message.from_user.id
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("movies.db")
    conn.execute("INSERT OR REPLACE INTO users (user_id, last_seen) VALUES (?, ?)", (user_id, now))
    conn.commit()
    conn.close()

    if not await is_subscribed(client, message): 
        return
        
    await message.reply_text("👋 **မင်္ဂလာပါ Donghua Fan တို့ရေ...**\n\n"
    "ကျွန်တော်ကတော့ သင်ကြည့်ချင်တဲ့ Donghua ဇာတ်ကားတွေကို အမြန်ဆုံး ရှာဖွေပေးမယ့် **DonghuaFan Official Bot** ပါ။ 🐉\n\n"
    "🔹 **အသုံးပြုနည်း-**\n"
    "ဇာတ်ကားနာမည်ကို Chat box ထဲမှာ ရိုက်ပို့ပြီး ရှာဖွေနိုင်ပါတယ်။\n\n"
    "💡 အောက်က Menu ခလုတ်တွေကို အသုံးပြုပြီးတော့လည်း ဇာတ်ကားစာရင်းတွေကို စစ်ဆေးနိုင်ပါတယ်ခင်ဗျာ။", reply_markup=main_menu())

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_cmd(client, message):
    try:
        d = message.text.split(None, 1)[1].split("|")
        name, l1 = d[0].strip().lower(), d[1].strip()
        l2 = d[2].strip() if len(d) > 2 else None
        conn = sqlite3.connect("movies.db")
        conn.execute("INSERT OR REPLACE INTO movies (name, link1, link2, likes) VALUES (?, ?, ?, COALESCE((SELECT likes FROM movies WHERE name = ?), 0))", (name, l1, l2, name))
        conn.commit()
        conn.close()
        await message.reply_text(f"✅ {name.upper()} ကို ထည့်သွင်းပြီးပါပြီ။")
    except: await message.reply_text("⚠️ `/add အမည် | link1 | link2` အတိုင်းပို့ပါ။")

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ User တွေကို ပို့ချင်တဲ့ Message ကို Reply ပြန်ပြီး `/broadcast` လို့ ရိုက်ပါ။")
    
    conn = sqlite3.connect("movies.db")
    users = conn.execute("SELECT user_id FROM users").fetchall()
    conn.close()
    
    count = 0
    msg = await message.reply_text("🚀 ပို့နေပါပြီ...")
    
    for u in users:
        try:
            await message.reply_to_message.copy(u[0])
            count += 1
        except Exception:
            pass
            
    await msg.edit_text(f"✅ လူပေါင်း {count} ဦးထံ အောင်မြင်စွာ ပို့ဆောင်ပြီးပါပြီ။")

@app.on_message(filters.command("del") & filters.user(OWNER_ID))
async def delete_movie(client, message):
    try:
        name = message.text.split(None, 1)[1].lower().strip()
        conn = sqlite3.connect("movies.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM movies WHERE name = ?", (name,))
        if cursor.rowcount > 0:
            await message.reply_text(f"🗑️ {name.upper()} ကို ဖျက်လိုက်ပါပြီ။")
        else:
            await message.reply_text("❌ အဲဒီနာမည်နဲ့ ဇာတ်ကား ရှာမတွေ့ပါ။")
        conn.commit()
        conn.close()
    except:
        await message.reply_text("⚠️ `/del ဇာတ်ကားအမည်` အတိုင်းသုံးပါ။")

@app.on_message(filters.text & filters.private)
async def search_cmd(client, message):
    if message.text.startswith("/"): return
    if not await is_subscribed(client, message): return
    q = message.text.lower().strip()
    conn = sqlite3.connect("movies.db")
    res = conn.execute("SELECT name, link1, link2, likes, rowid FROM movies WHERE name LIKE ?", (f"%{q}%",)).fetchall()
    conn.close()
    if res:
        for n, l1, l2, lks, mid in res:
            kb = types.InlineKeyboardMarkup([[types.InlineKeyboardButton(f"👍 Like ({lks})", callback_data=f"lk_{mid}")]])
            t = f"🎬 **{n.upper()}**\n\n🔗 Link 1: {l1}"
            if l2: t += f"\n🔗 Link 2: {l2}"
            await message.reply_text(t, reply_markup=kb)
    else: await message.reply_text("❌ မတွေ့ပါ။ နာမည်မှန်အောင် ပြန်ရိုက်ကြည့်ပါ။")

if __name__ == "__main__":
    app.run()


