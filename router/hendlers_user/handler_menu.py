from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from keyboards.inlain_users import ikb
from lexicon.lexicon import LEXICON, MENU
from fsm import StateMachine

router = Router()


@router.message(Command(commands = "menu"))
@router.callback_query(F.data == "back_menu")
@router.callback_query(F.data == "menu", StateMachine.start)
async def message_menu(query_message: Union[CallbackQuery, Message], state: FSMContext):
    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            text=MENU,        
            reply_markup= await ikb.create_kd_menu()
            )
        
    if isinstance(query_message, Message):
        await query_message.answer(
            text=MENU,    
            reply_markup= await ikb.create_kd_menu()
            )
    
    await state.set_state(StateMachine.menu)

@router.callback_query(F.data == 'plug')
async def callbacks_profile(callback: CallbackQuery):
    await callback.answer("Не нажимай на меня:)")


@router.message()
async def send_echo(message: Message):
    try:
        await message.answer("Я не знаю что на это ответить🤷:")
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(
            text='Я не знаю что на это ответить🤷'
        )