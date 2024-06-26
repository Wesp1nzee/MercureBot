from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from lexicon.dict_task_number import container_inf
from keyboards.inlain_users import ikb
from fsm import StateMachine
from callback_factory import FactoryTask
from database.dataclass import db


router = Router()


@router.callback_query(F.data == "back_informatics_task")
@router.callback_query(F.data == "informatics", StateMachine.informatics)
async def callback_informatics_task(callback: CallbackQuery, state: FSMContext):
    if callback.data == "informatics":
        await callback.message.edit_text(
            "Выбери тип задачи:", reply_markup=await ikb.create_kb_tasks_informatics()
        )
    else:
        await callback.message.answer(
            "Выбери тип задачи:", reply_markup=await ikb.create_kb_tasks_informatics()
        )
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            await callback.answer()
    await state.set_state(StateMachine.task_selection_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics"),StateMachine.task_selection_informatics)
@router.callback_query(FactoryTask.filter(F.object == "informatics"), StateMachine.error_message)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    task_number = callback_data.task_number
    await state.update_data(task_number=task_number)
    task_count = await db.chek_count(callback.from_user.id, "informatics", task_number)
    await state.update_data(object="informatics")

    image_id = await db.get_task_inf(task_number, task_count)
    await callback.message.answer_photo(
        photo=image_id,
        protect_content=True,
        reply_markup=await ikb.create_kb_pagination_inf(
            task_number=task_number,
            task_count=task_count,
        ),
    )
    try:
        await callback.message.delete()

    except TelegramBadRequest:
        await callback.answer()

    await state.set_state(StateMachine.leaf_task_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.direction == "Next"),StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count

    if task_count + 1 <= await container_inf.get_item(task_number):
        await db.update_user_task(callback.from_user.id, "informatics", task_number, sign="+")
        image_id = await db.get_task_inf(task_number, task_count + 1)

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=image_id,
            ),
            reply_markup=await ikb.create_kb_pagination_inf(
                task_number=task_number,
                task_count=task_count + 1,
            ),
        )
    else:
        await callback.answer(text="Извините, но больше нельзя!", show_alert=True)


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.direction == "Back"),StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count

    if task_count - 1 > 0:
        await db.update_user_task(callback.from_user.id, "informatics", task_number, sign="-")
        image_id = await db.get_task_inf(task_number, task_count-1)

        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=image_id,
            ),
            reply_markup=await ikb.create_kb_pagination_inf(
                task_number=task_number,
                task_count=task_count - 1,
            ),
        )
    else:
        await callback.answer(text="Извините, но меньше нельзя!", show_alert=True)


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.decision == True),StateMachine.leaf_task_informatics,)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count

    await callback.answer(
        text=f'Ответ: {await db.get_task_decision(user_id=task_count,task_number=task_number, object="informatics")}',
        show_alert=True,
    )
