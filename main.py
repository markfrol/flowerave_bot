import aiogram
from aiogram import Dispatcher, types
import random
import asyncio
from aiogram.filters import CommandStart, Command
from db_init import prepare_database
from config import ADMIN_CHAT_ID, API_TOKEN, DB_RESTORE
from crud import send_csv, add_message, add_user


bot = aiogram.Bot(token=API_TOKEN)
dp = Dispatcher()


responses = [
    "Хорошая погода",
    "Как дела?",
    "Hala Madrid",
    "Марк хочет работать в Flowerave",
    "До свидания!",
]


@dp.message(CommandStart())
async def start(message: types.Message):
    await add_user(message.from_user)
    await message.answer("Поехали!")


@dp.message(Command("csv"))
async def send_csv_command(message: types.Message):
    user_id = message.from_user.id
    file = await send_csv(user_id)
    if file:
        await bot.send_document(chat_id=ADMIN_CHAT_ID, document=file)

    await message.answer("Выгрузка отправлена!")


@dp.message()
async def handle_message(message: types.Message):
    await add_user(message.from_user)
    await add_message(message.from_user, message)
    response = random.choice(responses)
    await message.answer(response)


async def main():
    if DB_RESTORE:
        await prepare_database()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
