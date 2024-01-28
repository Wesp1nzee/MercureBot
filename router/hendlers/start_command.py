from copy import deepcopy
import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from keyboards.inlain import IKB
from lexicon.lexicon import LEXICON
from router.db import users_db_physics, dict_tack_count_physics, users_db_condition, condition, users_db_informatics, dict_tack_count_informatics
from FSM.fsm import StateMachine
from database.datacoonect import db


router = Router()


# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        f"Привет, {message.from_user.full_name}! {LEXICON['/start']}",
        reply_markup= await IKB.create_keyboard_menu_start()
    )
    #Проверка есть ли пользоваетль в БД если нет, то добовляет
    if not await db.count_user(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.username)

    if message.from_user.id not in users_db_physics:
        users_db_physics[message.from_user.id] = deepcopy(dict_tack_count_physics)

    if message.from_user.id not in users_db_condition:
        users_db_condition[message.from_user.id] = deepcopy(condition)

    if message.from_user.id not in users_db_informatics:
        users_db_informatics[message.from_user.id] = deepcopy(dict_tack_count_informatics)

    await state.set_state(StateMachine.start)
    



