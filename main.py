from aiogram import Bot, Dispatcher, types, executor
import sqlite3

API_TOKEN = "8028594734:AAEcjgn83x892UaCRIYvnZtTzI7qfcEL6u8"
ADMIN_IDS = [1210901314]  # Admin user_id lar ro'yxati

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# SQLite baza ulash
db = sqlite3.connect('kino.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS kino (id INTEGER PRIMARY KEY, code TEXT, title TEXT, file_id TEXT, info TEXT)''')
db.commit()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Assalomu alaykum! Kino kodini kiriting:")

@dp.message_handler(lambda message: message.text and message.text.startswith("/add") and message.from_user.id in ADMIN_IDS)
async def add_kino(message: types.Message):
    try:
        _, code, title, file_id, info = message.text.split("|", 4)
        cursor.execute("INSERT INTO kino (code, title, file_id, info) VALUES (?, ?, ?, ?)", (code, title, file_id, info))
        db.commit()
        await message.reply("Kino qo'shildi!")
    except Exception as e:
        await message.reply(f"Xatolik: {e}")

@dp.message_handler(lambda message: message.text)
async def find_kino(message: types.Message):
    code = message.text.strip()
    cursor.execute("SELECT title, file_id, info FROM kino WHERE code=?", (code,))
    kino = cursor.fetchone()
    if kino:
        title, file_id, info = kino
        await message.answer(f"Kino: {title}\nMa'lumot: {info}")
        await message.answer_video(file_id)
    else:
        await message.reply("Bunday kodda kino mavjud emas!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)