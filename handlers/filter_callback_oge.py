from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inlain import create_keyboard_tasks, create_keyboard_oge_task, create_keyboard_oge_decision
from handlers.db import users_db, users_db_condition
from aiogram.types import FSInputFile
from dictionar.decision_dict import decision_db

router = Router()

@router.callback_query(F.data.startswith('oge'))
async def message_with_text(callback: CallbackQuery):
    await callback.message.answer(
        "Выбери какой класс тебе интересен:",    
        reply_markup = create_keyboard_tasks()
    )
    await callback.message.delete()

@router.callback_query((F.data.startswith('task_')) )
async def message_with_text(callback: CallbackQuery):
    users_db_condition[callback.from_user.id].update({"task_number":f"{callback.data.split('_')[1]}"})
    task_number = users_db_condition[callback.from_user.id]['task_number']
    
    image_from_pc = FSInputFile(f"img/taskpapka_{task_number}/task_{task_number}_{str(users_db[callback.from_user.id][f'task_{task_number}']+1)}.png")
    await callback.message.answer_photo(
        image_from_pc,
        reply_markup = create_keyboard_oge_task(task_number,users_db[callback.from_user.id][f'task_{task_number}']+1)
    )
    await callback.message.delete()

@router.callback_query(((F.data.startswith('tasks_back_')) | (F.data.startswith('tasks_next_'))))
async def message_with_text(callback: CallbackQuery):
        tasks_action = callback.data.split("_")[1]
        task_number = users_db_condition[callback.from_user.id]['task_number']
        if tasks_action == "next":
            users_db[callback.from_user.id][f'task_{task_number}']+= 1
            image_from_pc = FSInputFile(f"img/taskpapka_{task_number}/task_{task_number}_{str(users_db[callback.from_user.id][f'task_{task_number}']+1)}.png")
            await callback.message.answer_photo(
            image_from_pc,
            reply_markup = create_keyboard_oge_task(task_number, users_db[callback.from_user.id][f'task_{task_number}']+1)
            )
            await callback.message.delete()

        if users_db[callback.from_user.id][f'task_{task_number}'] != 0:
            if tasks_action == "back":
                users_db[callback.from_user.id][f'task_{task_number}']-= 1
                image_from_pc = FSInputFile(f"img/taskpapka_{task_number}/task_{task_number}_{str(users_db[callback.from_user.id][f'task_{task_number}']+1)}.png")
                await callback.message.answer_photo(
                image_from_pc,
                reply_markup = create_keyboard_oge_task(task_number, users_db[callback.from_user.id][f'task_{task_number}']+1)
                )
                await callback.message.delete()
        else:
            await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
            )
             
@router.callback_query((F.data.startswith('decision_')) )
async def message_with_text(callback: CallbackQuery):
    task_number = users_db_condition[callback.from_user.id]['task_number']
    await callback.message.answer(
         f"Ответ: {decision_db[task_number][str(users_db[callback.from_user.id][f'task_{task_number}']+1)]}",
         reply_markup=create_keyboard_oge_decision(task_number, users_db[callback.from_user.id][f'task_{task_number}']+1)
    )
    await callback.message.delete()
    
     