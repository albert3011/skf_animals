import pandas as pd
import openpyxl
from aiogram import types
from aiogram.enums import ParseMode


async def send_question(questions, question_num, message):
    kb = [[types.KeyboardButton(text="Да"), types.KeyboardButton(text="Нет")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Вопрос {question_num + 1} из {len(questions['Вопросы'])}.\n{questions['Вопросы'][question_num]}", reply_markup=keyboard)


async def create_answer(questions, yes_points, message, bot):
    animals = pd.read_excel('data.xlsx', sheet_name='Животные')
    one_point = len(animals) / len(questions)

    if yes_points == 0:
        index = 0
    elif yes_points != 0 and one_point >= 1:
        index = int((yes_points * one_point) - 1)
    else:
        index = round(yes_points * one_point) - 1

    result = []
    if len(animals) > len(questions):
        spread = int(one_point // 2 + 1)
        for i in range(1, spread + 1):
            if index + i < len(animals):
                result.append(animals['Список животных'][index + i])
            if index - i >= 0:
                result.append(animals['Список животных'][index - i])
        result.append(animals['Список животных'][index])
        similar_list = ",\n".join(result[:-1])
        await bot.send_photo(message.chat.id, photo=animals['Фото'][index], caption=f'Это интересно... Вы очень похожи на это животное:\n{result[-1]} - {animals["Описание"][index]}')
        kb = [[types.KeyboardButton(text="Попробовать ещё раз")]]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer(f'Также вы очень похожи на этих животных:\n{similar_list}.\nНажмите "Попробовать ещё раз", если хотите запусить викторину снова.\nПройдите по <a href="https://moscowzoo.ru/about/guardianship">ссылке</a>, чтобы узнать подробнее о программе опеки.', reply_markup=keyboard, parse_mode=ParseMode.HTML)
    else:
        result = animals['Список животных'][index]
        print(result)


async def starting(message, state, text, questions):
    await message.answer(text)
    await state.set_data({'points': 0, 'question_num': 0, 'start': True})
    await send_question(questions, 0, message)
