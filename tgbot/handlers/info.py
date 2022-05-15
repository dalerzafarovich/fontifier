from aiogram import types, Dispatcher
from pathlib import Path

path = Path(__file__).parent.parent / 'messages' / 'info.html'

with open(path, 'r', encoding='utf-8') as f:
    INFO_TEXT = f.read()


async def info(m: types.Message):
    await m.answer(INFO_TEXT, parse_mode='HTML')


def register_info(dp: Dispatcher):
    dp.register_message_handler(info, commands='info', state='*')
