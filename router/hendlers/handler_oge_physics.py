from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inlain import IKB
from router.db import users_db_physics, users_db_condition
from aiogram.types import FSInputFile
from dictionar.decision_dict import decision_db

router = Router()

@router.callback_query(F.data == 'physics_task')
async def message_with_text(callback: CallbackQuery):
    users_db_condition[callback.from_user.id].update({"object":"physics"})

    await callback.message.answer(
        "Выбери задачу:",    
        reply_markup = await IKB.create_kb_task_physics()
    )
    await callback.message.delete()

@router.callback_query((F.data.startswith('physics:task_')) )
async def message_with_text(callback: CallbackQuery):
    users_db_condition[callback.from_user.id].update({"task_number":f"{callback.data.split('_')[1]}"})
    task_number = users_db_condition[callback.from_user.id]['task_number']
    image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{str(users_db_physics[callback.from_user.id][f'task_{task_number}']+1)}.png")

    await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await IKB.create_keyboard_oge_task(
            task_number=task_number, 
            task_count =  users_db_physics[callback.from_user.id][f'task_{task_number}']+1,
            user_id=callback.from_user.id
            )
    )
    await callback.message.delete()

@router.callback_query(((F.data.startswith('physics:tasks_back_')) | (F.data.startswith('physics:tasks_next_'))))
async def message_with_text(callback: CallbackQuery):
        tasks_action = callback.data.split("_")[1]
        task_number = users_db_condition[callback.from_user.id]['task_number']

        if tasks_action == "next":
            if users_db_physics[callback.from_user.id][f'task_{task_number}'] < 60:
                users_db_physics[callback.from_user.id][f'task_{task_number}']+= 1
                image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{users_db_physics[callback.from_user.id][f'task_{task_number}']+1}.png")

                await callback.message.answer_photo(
                image_from_pc,
                reply_markup = await IKB.create_keyboard_oge_task(
                    task_number=task_number, 
                    task_count =  users_db_physics[callback.from_user.id][f'task_{task_number}']+1,
                    user_id=callback.from_user.id
                )
                )
                await callback.message.delete()

            else:
                await callback.answer(
                text="Извините, но больше нельзя!",
                show_alert=True
                )

        if tasks_action == "back":
            if users_db_physics[callback.from_user.id][f'task_{task_number}'] > 0:
                users_db_physics[callback.from_user.id][f'task_{task_number}']-= 1
                image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{users_db_physics[callback.from_user.id][f'task_{task_number}']+1}.png")

                await callback.message.answer_photo(
                image_from_pc,
                reply_markup = await IKB.create_keyboard_oge_task(
                    task_number=task_number, 
                    task_count =  users_db_physics[callback.from_user.id][f'task_{task_number}']+1,
                    user_id=callback.from_user.id)
                )
                await callback.message.delete()

            else:
                await callback.answer(
                text="Извините, но меньше нельзя!",
                show_alert=True
                )
             
@router.callback_query((F.data.startswith('physics:decision_')) )
async def message_with_text(callback: CallbackQuery):
    task_number = users_db_condition[callback.from_user.id]['task_number']

    await callback.message.answer(
         f"Ответ: {decision_db[task_number][str(users_db_physics[callback.from_user.id][f'task_{task_number}']+1)]}",
         reply_markup= await IKB.create_keyboard_oge_decision(
            task_number=task_number, 
            task_count =  users_db_physics[callback.from_user.id][f'task_{task_number}']+1,
            user_id=callback.from_user.id
            )
    )
    await callback.message.delete()
    
     