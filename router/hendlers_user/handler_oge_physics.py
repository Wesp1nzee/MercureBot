from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from database.cache import cache
from lexicon.dict_task_number import container
from fsm import StateMachine
from keyboards.inlain import ikb
from callback_factory import FactoryTask
from database.datacoonect import db

router = Router()


@router.callback_query(F.data == "back_physics_task")
@router.callback_query(F.data == "physics", StateMachine.physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Выбери тип задачи:",    
        reply_markup = await ikb.create_kb_task_physics()
    )
    await callback.message.delete()
    await state.set_state(StateMachine.task_selection_physics)

@router.callback_query(FactoryTask.filter(F.object == "physics"), StateMachine.task_selection_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    task_number = callback_data.task_number
    await state.update_data(task_number=task_number)
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    if await cache.check_key(task_number, task_count):
        image_id = await cache.check_key(task_number, task_count)

    else:
        await cache.update_val(key_1=task_number,
                               key_2=task_count,
                               val=await db.get_task(object="physics", id=task_count, task_number=task_number))
        image_id = await cache.check_key(task_number, task_count)

    await callback.message.answer_photo(
            photo=image_id,
            protect_content=True,
            reply_markup = await ikb.create_kb_pagination(
                            task_number=task_number, 
                            task_count=task_count,
                            object='physics'
                        )   
        )
    await callback.message.delete()
    await state.set_state(StateMachine.leaf_task_physics)

@router.callback_query(FactoryTask.filter(F.object == "physics" and F.direction == "Next") , StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    if await cache.check_key(task_number, task_count):
        image_id = await cache.check_key(task_number, task_count)

    else:
        await cache.update_val(key_1=task_number,
                               key_2=task_count,
                               val=await db.get_task(object="physics", id=task_count, task_number=task_number))
        image_id = await cache.check_key(task_number, task_count)
    
    if  task_count+1 < await container.get_item(task_number):
        await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="+")
        task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

        await callback.message.edit_media(
            media=InputMediaPhoto( 
            media=image_id,
            ),
            reply_markup = await ikb.create_kb_pagination(
                            task_number=task_number, 
                            task_count=task_count,
                            object='physics'
                        )   
        )

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

    if await cache.check_key(task_number, task_count):
        image_id = await cache.check_key(task_number, task_count)

    else:
        await cache.update_val(key_1=task_number,
                               key_2=task_count,
                               val=await db.get_task(object="physics", id=task_count, task_number=task_number))
        image_id = await cache.check_key(task_number, task_count)

    if task_count-1 > 0:
            await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="-")
            task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

            await callback.message.edit_media(
            media=InputMediaPhoto( 
            media=image_id,
            ),
            reply_markup = await ikb.create_kb_pagination(
                            task_number=task_number, 
                            task_count=task_count,
                            object='physics'
                        )   
        )

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )

@router.callback_query(FactoryTask.filter(F.object == "physics" and F.decision == "yes"), StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)
    
    await callback.answer(
        text=f'Ответ: {await db.get_task_decision(id=task_count,task_number=task_number, object="physics")}',
        show_alert=True
        )
    
     