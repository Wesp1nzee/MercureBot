from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from keyboards.inlain import IKB
from lexicon.lexicon import LEXICON, generate_tasks_string
from FSM.fsm import StateMachine

router = Router()


@router.message(Command(commands = "menu"))
@router.callback_query(F.data == "menu", StateFilter(StateMachine.start))
async def message_with_text(query_message: Union[CallbackQuery, Message], state: FSMContext):
    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            "⬇️Выбери что тебе интересно⬇️",    
            reply_markup= await IKB.create_keyboard_menu()
            )
        
    if isinstance(query_message, Message):
        await query_message.answer(
            "⬇️Выбери что тебе интересно⬇️",    
            reply_markup= await IKB.create_keyboard_menu()
            )
    
    await state.set_state(StateMachine.menu)

@router.message(Command(commands = 'help'))
@router.callback_query(F.data == 'help')
async def help_command(query_message: Union[CallbackQuery, Message]):
    if isinstance(query_message, CallbackQuery):
        await query_message.message.edit_text(
            f"{LEXICON['/help']}",    
            reply_markup= await IKB.create_kb_help()
            )
        
    if isinstance(query_message, Message):
        await query_message.answer(
            f"{LEXICON['/help']}",    
            reply_markup= await IKB.create_kb_help()
            )

@router.callback_query(F.data == 'profile', StateFilter(StateMachine.menu))
async def callbacks_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Это профиль и тут вам предлагается просмотреть статистику по вашим решеным задачкам.📊\n\n"
        f"Вот ваша статистика по задачам:\n\n{await generate_tasks_string(callback.from_user.id)}",
        reply_markup= await IKB.create_profil()
     )    
    await callback.answer()

@router.message()
async def send_echo(message: Message):
    try:
        await message.answer("Я не знаю что на это ответить🤷:")
        await message.send_copy(chat_id=message.chat.id)
        await message.answer("Если вам нужна помощь напишите команду /help")
    except TypeError:
        await message.reply(
            text='Данный тип апдейтов не поддерживается '
                 'методом send_copy'
        )