from copy import deepcopy

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.inlain import IKB
from lexicon.lexicon import LEXICON
from handlers.db import users_db_physics, dict_tack_count_physics, users_db_condition, condition, users_db_informatics, dict_tack_count_informatics


router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}! {LEXICON['/start']}",
        reply_markup= await IKB.create_keyboard_menu_start()
    )
    if message.from_user.id not in users_db_physics:
        users_db_physics[message.from_user.id] = deepcopy(dict_tack_count_physics)

    if message.from_user.id not in users_db_condition:
        users_db_condition[message.from_user.id] = deepcopy(condition)

    if message.from_user.id not in users_db_informatics:
        users_db_informatics[message.from_user.id] = deepcopy(dict_tack_count_informatics)



