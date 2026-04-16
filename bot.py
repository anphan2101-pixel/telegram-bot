import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from deep_translator import GoogleTranslator

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN")

# ===== INIT =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== MODE =====
user_mode = {}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇨🇳 → 🇻🇳"), KeyboardButton(text="🇻🇳 → 🇨🇳")],
        [KeyboardButton(text="🇻🇳 → 🇬🇧 (QA)")],
    ],
    resize_keyboard=True
)

# ===== START =====
@dp.message(Command("start"))
async def start(message: Message):
    user_mode[message.from_user.id] = "CN_VI"
    await message.answer("Chọn chế độ dịch 👇", reply_markup=keyboard)

# ===== CHANGE MODE =====
@dp.message(lambda message: message.text in ["🇨🇳 → 🇻🇳", "🇻🇳 → 🇨🇳", "🇻🇳 → 🇬🇧 (QA)"])
async def change_mode(message: Message):
    if message.text == "🇨🇳 → 🇻🇳":
        user_mode[message.from_user.id] = "CN_VI"
    elif message.text == "🇻🇳 → 🇨🇳":
        user_mode[message.from_user.id] = "VI_CN"
    else:
        user_mode[message.from_user.id] = "VI_EN_QA"

    await message.answer(f"Đã chuyển mode: {message.text}")

# ===== TEXT TRANSLATE =====
@dp.message(lambda message: message.text is not None)
async def translate_text(message: Message):
    try:
        text = message.text
        mode = user_mode.get(message.from_user.id, "CN_VI")

        # CN -> VI
        if mode == "CN_VI":
            result = GoogleTranslator(source='zh-CN', target='vi').translate(text)
            title = "🇨🇳 → 🇻🇳"

        # VI -> CN
        elif mode == "VI_CN":
            result = GoogleTranslator(source='vi', target='zh-CN').translate(text)
            title = "🇻🇳 → 🇨🇳"

        # VI -> EN (QA)
        else:
            # dịch thường trước
            raw = GoogleTranslator(source='vi', target='en').translate(text)

            # tối ưu lại theo ngữ cảnh testing
            result = f"(QA Context)\n{raw}"
            title = "🇻🇳 → 🇬🇧 (QA)"

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