import sys

sys.path.append(...)

from aiogram import Dispatcher, types
from tgbot.services.fontifier import fontify
from tgbot.fonts_list import fonts_list


async def try_inline(m: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text='Выбрать', switch_inline_query=''))
    keyboard.add(types.InlineKeyboardButton(text='Этот чат', switch_inline_query_current_chat=''))
    await m.answer('Выберите чат ', reply_markup=keyboard)


async def inline_fontify(query: types.InlineQuery):
    text = query.query or None
    if text is None:
        return await query.answer(results=[types.InlineQueryResultArticle(id='1', title='Пустое сообщение',
                                                                          input_message_content=types.InputTextMessageContent(
                                                                              message_text='Пустое сообщение'))])

    fontified_lst = [fontify(text, i) for i in fonts_list]
    results = []
    for index, value in enumerate(fontified_lst):
        result = types.InlineQueryResultArticle(id=str(index), title=value,
                                                input_message_content=types.InputTextMessageContent(message_text=value))
        results.append(result)

    return await query.answer(results=results)


def register_inline(dp: Dispatcher):
    dp.register_message_handler(try_inline, commands='try_inline')
    dp.register_inline_handler(inline_fontify)
