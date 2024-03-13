from typing import Union

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from config import ADMIN_IDS

from keyboards.inlain_users import ikb
from lexicon.lexicon import LEXICON
from fsm import StateMachine
from callback_factory import  FactoryError
from database.datacoonect import db

router = Router()


@router.callback_query(FactoryError.filter(F.object == "error_message"), StateMachine.leaf_task_physics)
@router.callback_query(FactoryError.filter(F.object == "error_message"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryError):
    task_count = callback_data.task_count
    await state.update_data(task_count = task_count)

    await callback.message.answer(
        text="Вы нашли ошибку в задаче или в ответе?\n\n"
        "Опишите пожалуйста, где иммено содержалась ошибка(Количество слов не должно превышать 600 символов):"
            )
    await state.set_state(StateMachine.error_message)
    await callback.message.delete()

@router.message(F.text, StateMachine.error_message)
async def error_message(message: Message, state: FSMContext, bot:Bot):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = user_data["task_count"]
    object = user_data["object"]
    if len(message.text) <= 600:
        await bot.send_message(chat_id=ADMIN_IDS[0],
                             text=f'Задача: {task_number}\n\nНомер задачи:{task_count}\n\n{message.text}',)
        await message.answer(
        text='Текст был отправлен Администратору!'
            )
        
        if object == "physics":
            image_id = await db.get_task(object="physics", id=task_count, task_number=task_number)
            await message.answer_photo(
                    photo=image_id,
                    # protect_content=True,
                    reply_markup = await ikb.create_kb_pagination_phy(
                                    task_number=task_number, 
                                    task_count=task_count,
                                )   
                )
            await state.set_state(StateMachine.leaf_task_physics)

        if object == "informatics":
            image_id = await db.get_task(object="informatics", id=task_count, task_number=task_number)
            await message.answer_photo(
                    photo=image_id,
                    # protect_content=True,
                    reply_markup = await ikb.create_kb_pagination_inf(
                                    task_number=task_number, 
                                    task_count=task_count,
                                )   
                )
            await state.set_state(StateMachine.leaf_task_informatics)

    else:
        await message.answer(
        text='Ваше сообщение слишком большоее'
            )

@router.message(StateMachine.error_message)
async def error_message_exception(message: Message, state: FSMContext, bot:Bot):
    await message.answer(
        text='Пожалуйста отправьте текстовое сообщение'
            )