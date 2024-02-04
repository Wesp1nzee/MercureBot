from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from keyboards.inlain import ikb
from FSM.fsm import StateMachine
from callback_factory import FactoryTask
from database.datacoonect import db


router = Router()

@router.callback_query(F.data == "back_informatics_task")
@router.callback_query(F.data == "informatics", (StateMachine.informatics or StateMachine.leaf_task_physics))
async def callback_informatics_task(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "Выбери задачу:",    
        reply_markup = await ikb.create_kb_tasks_informatics()
    )
    await callback.message.delete()
    await state.set_state(StateMachine.task_selection_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics"), StateMachine.task_selection_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):

    await state.update_data(task_number = callback_data.task_number)
    task_number = callback_data.task_number
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)
    
    image_from_pc = FSInputFile(f"img/informatics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")
    await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await ikb.create_keyboard_oge_task(
            task_number=task_number,
            task_count = task_count,
            object = "informatics"
            )
    )
    await callback.message.delete()
    await state.set_state(StateMachine.leaf_task_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.direction == "Next"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)

    if task_count+1 < 60:
        await db.update_user_task(callback.from_user.id, 'informatics', task_number, sign="+")
        task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)
        image_from_pc = FSInputFile(f"img/informatics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")

        await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await ikb.create_keyboard_oge_task(
            task_number=task_number,
            task_count=task_count,
            object='informatics'
            )
        )
        await callback.message.delete()

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.direction == "Back"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)

    if task_count-1 >= 1:
        await db.update_user_task(callback.from_user.id, 'informatics', task_number, sign="-" )
        task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)
        image_from_pc = FSInputFile(f"img/informatics/taskpapka_{task_number}/task_{task_number}_{task_count}.png")

        await callback.message.answer_photo(
        image_from_pc,
        reply_markup = await ikb.create_keyboard_oge_task(
            task_number=task_number, 
            task_count=task_count,
            object='informatics'
            )
        )

        await callback.message.delete()

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.decision == "yes"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)
    image_from_pc = FSInputFile(f"img/decision_informatics/decision_1/decision_{task_number}_{task_count}.png")
    await callback.message.answer_photo(
        image_from_pc,
        reply_markup= await ikb.create_keyboard_oge_decision(
            task_number=task_number, 
            task_count=task_count,
            object="informatics"
            )
    )
    await callback.message.delete()
    