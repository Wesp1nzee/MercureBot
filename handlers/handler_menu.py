from typing import Union

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from keyboards.inlain import IKB
from lexicon.lexicon import LEXICON, generate_tasks_string

router = Router()

@router.message(F.text == "⚡️Меню")
@router.message(Command(commands="menu"))
async def message_with_text(query_message: Union[CallbackQuery, Message]):
    if isinstance(query_message, CallbackQuery):
        await query_message.message.answer(
            "⬇️Выбери что тебе интересно⬇️",    
            reply_markup= await IKB.create_keyboard_menu()
            )
        
    if isinstance(query_message, Message):
        await query_message.answer(
            "⬇️Выбери что тебе интересно⬇️",    
            reply_markup= await IKB.create_keyboard_menu()
            )
        
@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(
        LEXICON["/help"]
    )

@router.callback_query(F.data == 'Back')
async def message_with_text(callback: CallbackQuery):
    await callback.message.edit_text(
        "⬇️Выбери что тебе интересно⬇️",    
        reply_markup = await IKB.create_keyboard_menu()
    )
    await callback.answer()

@router.callback_query(F.data == 'profile')
async def callbacks_profile(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Это профиль и тут вам предлагается просмотреть статистику по вашим решеным задачкам.👨🏻‍🎓\n\n"
        f"Вот ваша статистика по задачам:\n\n{generate_tasks_string(callback.from_user.id)}",
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