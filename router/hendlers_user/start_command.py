from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.inlain import ikb
from lexicon.lexicon import LEXICON
from fsm import StateMachine
from database.datacoonect import db


router = Router()

# Этот хэндлер будет срабатывать на команду "/start"
@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await message.answer(
        f"Привет, {message.from_user.full_name}! {LEXICON['/start']}",
        reply_markup= await ikb.create_keyboard_menu_start()
    )
    #Проверка есть ли пользоваетль в БД если нет, то добовляет
    if not await db.count_user(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.username)

    await state.set_state(StateMachine.start)



