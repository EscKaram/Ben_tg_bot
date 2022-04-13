from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import json
import random

import config

Token = config.API_TOKEN

bot = Bot(token=Token)
dp = Dispatcher(bot, storage=MemoryStorage())

answers = ["Yes", "No"]
reactions = ["Ohhohoho...", "😜"]


class caller(StatesGroup):
    answer = State()


@dp.message_handler(commands="start")
async def starter(message: types.Message):
    if str(message.from_user.id) == "1282778486":
        await message.answer("Hi, Karam!")
    else:
        with open("Data.json") as Data_json:
            Data = dict(json.load(Data_json))
        Data[str(message.from_user.id)] = str(message.from_user.username)
        with open("Data.json", 'w') as Data_json:
            json.dump(Data, Data_json)
        await message.answer("Hi, I'm Ben. If you want to know what I can, write /help.")


@dp.message_handler(commands="help")
async def helper(message: types.Message):
    await message.answer(
        "Send any message and I will repeat it.\n\n"
        "Send /start_call to start a call and send /end_call to end it.\n\n"
        "Send /author to find out who created this bot.\n\n"
        "Have fun!")


@dp.message_handler(commands="author")
async def who_me(message: types.Message):
    await message.answer("Oops... It's a secret.")


@dp.message_handler(commands="start_call")
async def start_call(message: types.Message):
    await message.answer("Ben")
    await caller.answer.set()


@dp.message_handler(state=caller.answer)
async def call(message: types.Message, state: FSMContext):
    if message.text == "/end_call":
        await state.finish()
    else:
        if message.is_command():
            await message.reply("...")
        elif '?' in message.text:
            await message.reply(random.choice(answers))
        else:
            await message.reply(random.choice(reactions))
        await caller.answer.set()


@dp.message_handler(content_types="text")
async def echo(message: types.Message):
    if message.is_command():
        await message.reply("...")
    else:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
