from copy import deepcopy

from aiogram import Router
from aiogram.filters import  CommandStart
from aiogram.types import Message

from keyboards.for_command import menu
from lexicon.lexicon import LEXICON
from handlers.db import users_db, dict_tack_count, users_db_condition, condition


router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! {LEXICON['/start']}",
        reply_markup=menu()
    )
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(dict_tack_count)

    if message.from_user.id not in users_db_condition:
        users_db_condition[message.from_user.id] = deepcopy(condition)




