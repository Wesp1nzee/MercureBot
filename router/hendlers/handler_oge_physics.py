from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from FSM.fsm import StateMachine
from keyboards.inlain import ikb
from dictionar.decision_dict import decision_db
from callback_factory import FactoryTask
from database.datacoonect import db

router = Router()


@router.callback_query(F.data == "back_physics_task")
@router.callback_query(F.data == "physics", StateMachine.physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выбери задачу:",    
        reply_markup = await ikb.create_kb_task_physics()
    )
    await callback.message.delete()
    await state.set_state(StateMachine.task_selection_physics)

@router.callback_query(FactoryTask.filter(F.object == "physics"), StateMachine.task_selection_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    task_number = callback_data.task_number
    await state.update_data(task_number=task_number)
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")

    await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await ikb.create_keyboard_oge_task(
            task_number=task_number, 
            task_count=task_count,
            object="physics"
            )
    )
    await callback.message.delete()
    await state.set_state(StateMachine.leaf_task_physics)

@router.callback_query(FactoryTask.filter(F.object == "physics" and F.direction == "Next") , StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    
    if  task_count+1 < 60:
        await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="+")
        task_count = await db.chek_count(callback.from_user.id,'physics',task_number)
        image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")

        await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await ikb.create_keyboard_oge_task(
            task_number=task_number, 
            task_count=task_count,
            object="physics"
        )
        )
        await callback.message.delete()

    else:
        await callback.answer(
            text="Извините, но больше нельзя!",
            show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "physics" and F.direction == "Back"), StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    if task_count-1 > 0:
            await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="-")
            task_count = await db.chek_count(callback.from_user.id,'physics',task_number)
            image_from_pc = FSInputFile(f"img/physics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")

            await callback.message.answer_photo(
            image_from_pc,
            reply_markup = await ikb.create_keyboard_oge_task(
                task_number=task_number, 
                task_count=task_count,
                object="physics")
            )
            await callback.message.delete()

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )

@router.callback_query(FactoryTask.filter(F.object == "physics" and F.decision == "yes"), StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = str(user_data["task_number"])
    task_count = str(await db.chek_count(callback.from_user.id,'physics',task_number))

    await callback.message.answer(
         f"Ответ: {decision_db[task_number][task_count]}",
         reply_markup= await ikb.create_keyboard_oge_decision(
            task_number=task_number, 
            task_count=task_count,
            object="physics"
            )
    )
    await callback.message.delete()
    
     