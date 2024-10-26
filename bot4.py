from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncio

BOT_TOKEN = '7373643217:AAGvqKG0fAF-QOpsi3-MNrjA24NYoePJ9wM'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

calories_btn = KeyboardButton(text='Рассчитать калории')
info_btn = KeyboardButton(text='Информация')
markup = ReplyKeyboardMarkup(keyboard=[[calories_btn, info_btn]], resize_keyboard=True)
m_btn = KeyboardButton(text='Мужской')
w_btn = KeyboardButton(text='Женский')
markup1 = ReplyKeyboardMarkup(keyboard=[[m_btn, w_btn]], resize_keyboard=True)

r_btn = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
f_btn = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
markup2 = InlineKeyboardMarkup(inline_keyboard=[[r_btn, f_btn]])


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message(Command(commands=["start"]))
async def start(message: Message):
    await message.answer(text='Привет! Я бот помогающий твоему здоровью.', reply_markup=markup)


@dp.message(F.text == 'Информация')
async def info(message: Message):
    await message.answer(text='Этот бот может посчитать суточную норму калорий')


@dp.message(F.text == 'Рассчитать калории')
async def start(message: Message):
    await message.answer('Выберите опцию:', reply_markup=markup2)


@dp.callback_query(F.data == 'formulas')
async def get_formulas(call: CallbackQuery):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + k (коэфицент зависящий от пола)')
    await call.answer()


@dp.callback_query(F.data == 'calories')
async def set_age(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите свой возраст')
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


@dp.message()
async def all_massages(message: Message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    dp.run_polling(bot)
