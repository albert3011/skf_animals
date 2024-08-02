import asyncio
import pandas as pd
import json
from random import choices
from aiogram import Bot, Dispatcher, types
import aiohttp
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from functions import send_question, create_answer, starting
from token_data import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
questions = pd.read_excel('data.xlsx', sheet_name='Вопросы')


class TestInfo(StatesGroup):
    rating = State()


@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await starting(message, state, 'Добро пожаловать в викторину, созданную для того, чтобы рассказать Вам о программе "Возьми животное под опеку" в Московском зоопарке!\nПройди викторину, узнай на какое животное из Московского зоопарка ты больше всего похож, и, возможно, Вам захочется взять его под свою опеку!', questions)


@dp.message()
async def echo(message: types.Message, state: FSMContext):
    if 'Попробовать ещё раз' in message.text:
        await starting(message, state, 'Ответьте на вопросы снова! Удачи!', questions)
    curr_data = await state.get_data()
    answers = ['Да', 'Нет']
    if 'start' in curr_data:
        if curr_data['start']:
            if message.text in answers:
                if message.text == "Да":
                    await state.set_data({'points': curr_data['points'] + 1,
                                          'question_num': curr_data['question_num'] + 1,
                                          'start': True})
                elif message.text == "Нет":
                    await state.set_data({'points': curr_data['points'],
                                          'question_num': curr_data['question_num'] + 1,
                                          'start': True})
                result = await state.get_data()
                if curr_data['question_num'] < len(questions) - 1 and curr_data['start']:
                    await send_question(questions, curr_data['question_num'] + 1, message)
                else:
                    await create_answer(questions, result["points"], message, bot)
                    await state.set_data({'start': False})
            else:
                await message.answer('Вам нужно ответить "Да" или "Нет".')
        else:
            await message.answer('Начните игру командой /start')
    else:
        await message.answer('Начните игру командой /start')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
