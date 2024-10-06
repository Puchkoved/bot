from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

BOT_TOKEN = '7373643217:AAF4gysa7xKtkRkDuupkWbtJEmkGFNy2s_w'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')


@dp.message()
async def all_massages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    dp.run_polling(bot)
