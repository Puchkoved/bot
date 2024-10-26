from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import asyncio

BOT_TOKEN = ''
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

m_btn = KeyboardButton(text='Мужской')
w_btn = KeyboardButton(text='Женский')
markup1 = ReplyKeyboardMarkup(keyboard=[[m_btn, w_btn]], resize_keyboard=True)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message(F.text.lower() == 'calories')
async def set_age(message: Message, state: FSMContext):
    await message.answer('Введите свой возраст')
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def set_growth(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await state.set_state(UserState.growth)


@dp.message(UserState.growth)
async def set_weight(message: Message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def set_gender(message: Message, state: FSMContext):
    await state.update_data(weight=message.text)
    await message.answer(text='Укажите свой пол', reply_markup=markup1)
    await state.set_state(UserState.gender)


@dp.message(UserState.gender)
async def send_calories(message: Message, state: FSMContext):
    await state.update_data(gender=message.text)
    data = await state.get_data()
    if data['gender'] == 'Мужской':
        k = 5
    else:
        k = -161
    calories = 10*int(data['weight']) + 6,25*int(data['growth']) - 5*int(data['age']) + k
    await message.answer(text=f'Ваша норма каллорий {str(calories)}', reply_markup=ReplyKeyboardRemove())
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
