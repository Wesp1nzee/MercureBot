from aiogram import Router, F
from aiogram.types import Message
from keyboards.inlain import create_keyboard_menu

router = Router()

@router.message(F.text == "⚡️Меню")
async def message_with_text(message: Message):
    await message.answer(
        "⬇️Выбери что тебе интересно⬇️",    
        reply_markup=create_keyboard_menu()
    )

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