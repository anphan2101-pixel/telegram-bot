import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from deep_translator import GoogleTranslator

# ===== CONFIG =====
BOT_TOKEN = os.getenv("8680535248:AAHimCrwwr6_7exbtMFP8q8K6NhbXD_iqZ4")

# ===== INIT =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== MODE =====
user_mode = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇨🇳 → 🇻🇳"), KeyboardButton(text="🇻🇳 → 🇨🇳")]
    ],
    resize_keyboard=True
)

# ===== START =====
@dp.message(Command("start"))
async def start(message: Message):
    user_mode[message.from_user.id] = "CN_VI"
    await message.answer("Chọn chế độ dịch 👇", reply_markup=keyboard)

# ===== CHANGE MODE =====
@dp.message(lambda message: message.text in ["🇨🇳 → 🇻🇳", "🇻🇳 → 🇨🇳"])
async def change_mode(message: Message):
    if message.text == "🇨🇳 → 🇻🇳":
        user_mode[message.from_user.id] = "CN_VI"
    else:
        user_mode[message.from_user.id] = "VI_CN"

    await message.answer(f"Đã chuyển mode: {message.text}")

# ===== TEXT TRANSLATE =====
@dp.message(lambda message: message.text is not None)
async def translate_text(message: Message):
    try:
        text = message.text
        mode = user_mode.get(message.from_user.id, "CN_VI")

        if mode == "CN_VI":
            result = GoogleTranslator(source='zh-CN', target='vi').translate(text)
            title = "🇨🇳 → 🇻🇳"
        else:
            result = GoogleTranslator(source='vi', target='zh-CN').translate(text)
            title = "🇻🇳 → 🇨🇳"

        await message.answer(
            f"✨ {title}\n\n"
            f"📝 Gốc:\n{text}\n\n"
            f"🌍 Dịch:\n{result}"
        )

    except Exception as e:
        print("ERROR:", e)
        await message.answer("Lỗi dịch rồi 😅")

# ===== RUN =====
async def main():
    print("Bot running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
