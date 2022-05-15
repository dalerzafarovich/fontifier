import sys

sys.path.append(...)
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import MessageNotModified

from tgbot.services.fontifier import fontify
from tgbot.fonts_list import fonts_list
from aiogram.utils.callback_data import CallbackData
from contextlib import suppress

cb = CallbackData('text', 'font')


def get_keyboard():
    keyboard = types.InlineKeyboardMarkup()

    buttons = [types.InlineKeyboardButton(text=value[:3], callback_data=cb.new(font=index)) for index, value in
               enumerate(fonts_list[:-1])]
    buttons.append(types.InlineKeyboardButton(text='Regular', callback_data=cb.new(font=-1)))
    keyboard.add(*buttons)
    return keyboard


class ChangeFont(StatesGroup):
    waiting_for_text = State()
    waiting_for_font = State()


async def start(m: types.Message):
    await m.answer('Пожалуйста, введите текст: ')
    await ChangeFont.waiting_for_text.set()


async def text_entered(m: types.Message, state: FSMContext):
    bot_m_id = (await m.answer(m.text, reply_markup=get_keyboard())).message_id
    await m.answer('<i>Примечание: </i> если в тексте есть опечатка, вы можете отредактировать сообщение',
                   parse_mode='HTML')
    await state.update_data(user_text=m.text, user_m_id=m.message_id, bot_m_id=bot_m_id, font='0')
    await ChangeFont.next()


async def font_chosen(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    font = callback_data['font']
    await state.update_data(font=font)
    text = (await state.get_data()).get('user_text')
    with suppress(MessageNotModified):
        await call.message.edit_text(fontify(text, fonts_list[int(font)]),
                                     reply_markup=get_keyboard())
    await call.answer()


async def message_edited(m: types.Message, state: FSMContext):
    data: dict = await state.get_data()
    user_m_id: types.Message = data.get('user_m_id')
    if user_m_id != m.message_id:
        return
    bot_m_id: int = data.get('bot_m_id')
    font = data.get('font')
    await state.update_data(user_text=m.text)
    await m.bot.edit_message_text(fontify(m.text, fonts_list[int(font)]), m.from_user.id, bot_m_id,
                                  reply_markup=get_keyboard())


def register_fontify(dp: Dispatcher):
    dp.register_message_handler(start, state='*', commands='fontify')
    dp.register_message_handler(text_entered, state=ChangeFont.waiting_for_text)
    dp.register_callback_query_handler(font_chosen, cb.filter(), state=ChangeFont.waiting_for_font)
    dp.register_edited_message_handler(message_edited, state=ChangeFont.waiting_for_font)
