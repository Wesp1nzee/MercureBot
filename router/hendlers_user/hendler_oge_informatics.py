from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from lexicon.dict_task_number_inf import container_inf
from keyboards.inlain_users import ikb
from fsm import StateMachine
from callback_factory import FactoryTask
from database.datacoonect import db


router = Router()

@router.callback_query(F.data == "back_informatics_task")
@router.callback_query(F.data == "informatics", (StateMachine.informatics or StateMachine.leaf_task_physics))
async def callback_informatics_task(callback: CallbackQuery, state: FSMContext):

    await callback.message.answer(
        "Выбери тип задачи:",    
        reply_markup = await ikb.create_kb_tasks_informatics()
    )
    await callback.message.delete()
    await state.set_state(StateMachine.task_selection_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics"), StateMachine.task_selection_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    task_number = callback_data.task_number
    await state.update_data(task_number = task_number)
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)
    object = callback_data.object
    await state.update_data(object=object)
    
    image_id = await db.get_task(object="informatics", id=task_count, task_number=task_number)
    await callback.message.answer_photo(
        photo=image_id,
        # protect_content=True,
        reply_markup = await ikb.create_kb_pagination_inf(
            task_number=task_number,
            task_count = task_count,
            )
    )

    await callback.message.delete()
    await state.set_state(StateMachine.leaf_task_informatics)


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.direction == "Next"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)

    if task_count+1 < await container_inf.get_item(task_number):
        await db.update_user_task(callback.from_user.id, 'informatics', task_number, sign="+")
        task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)

        image_id = await db.get_task(object="informatics", id=task_count, task_number=task_number)  

        await callback.message.edit_media(
        media=InputMediaPhoto( 
            media=image_id,
            ),
        reply_markup = await ikb.create_kb_pagination_inf(
            task_number=task_number,
            task_count=task_count,
            )
        )
        
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

        image_id = await db.get_task(object="informatics", id=task_count, task_number=task_number)
        
        await callback.message.edit_media(
        media=InputMediaPhoto( 
            media=image_id,
            ),
        reply_markup = await ikb.create_kb_pagination_inf(
            task_number=task_number, 
            task_count=task_count,
            )
        )

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "informatics" and F.decision == "yes"), StateMachine.leaf_task_informatics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'informatics',task_number)

    await callback.answer(
        text= f'Ответ: {await db.get_task_decision(id=task_count,task_number=task_number, object="informatics")}',
        show_alert=True
        )
    
    