from aiogram import Router, F
from aiogram.types import CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from lexicon.dict_task_number_phy import container_phy
from fsm import StateMachine
from keyboards.inlain_users import ikb
from callback_factory import FactoryTask
from database.datacoonect import db
from database.conteiner_fileid import container_fileid
from log import logger

router = Router()


@router.callback_query(F.data == "back_physics_task")
@router.callback_query(F.data == "physics", StateMachine.physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext):
    if callback.data == "physics":
        await callback.message.edit_text(
            "Выбери тип задачи:",    
            reply_markup = await ikb.create_kb_task_physics()
        )
    else:
        await callback.message.answer(
            "Выбери тип задачи:",    
            reply_markup = await ikb.create_kb_task_physics()
        )
        try:
            await callback.message.delete()
            
        except TelegramBadRequest:
            await callback.answer()
            logger.error(TelegramBadRequest)

    await state.set_state(StateMachine.task_selection_physics)

@router.callback_query(FactoryTask.filter(F.object == "physics"), StateMachine.task_selection_physics)
@router.callback_query(FactoryTask.filter(F.object == "physics"), StateMachine.error_message)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    task_number = callback_data.task_number
    await state.update_data(task_number=task_number)
    await state.update_data(object="physics")
    task_count = await db.chek_count(callback.from_user.id,'physics',task_number)

    try:
        image_id = await container_fileid.get_item_phy(task_number, task_count)

        await callback.message.answer_photo(
                photo=image_id,
                protect_content=True,
                reply_markup = await ikb.create_kb_pagination_phy(
                                task_number=task_number, 
                                task_count=task_count,
                            )   
            )
        try:
            await callback.message.delete()
            
        except TelegramBadRequest:
            await callback.answer()
            logger.error(TelegramBadRequest)

        await state.set_state(StateMachine.leaf_task_physics)

    except KeyError:
        await callback.answer(
        text='Этот раздел ещё не готов:0',
        show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "physics" and F.direction == "Next") , StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count

    if  task_count+1 < await container_phy.get_item(task_number):
        await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="+")
        image_id = await container_fileid.get_item_phy(task_number, task_count+1)
        await callback.message.edit_media(
            media=InputMediaPhoto( 
            media=image_id,
            ),
            reply_markup = await ikb.create_kb_pagination_phy(
                            task_number=task_number, 
                            task_count=task_count+1,
                        )   
        )

    else:
        await callback.answer(
            text="Извините, но больше нельзя!",
            show_alert=True
        )


@router.callback_query(FactoryTask.filter(F.object == "physics" and F.direction == "Back"), StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count

    if task_count-1 > 0:
        await db.update_user_task(callback.from_user.id, 'physics', task_number, sign="-")
        image_id = await container_fileid.get_item_phy(task_number, task_count-1)
        
        await callback.message.edit_media(
            media=InputMediaPhoto( 
            media=image_id,
            ),
            reply_markup = await ikb.create_kb_pagination_phy(
                            task_number=task_number, 
                            task_count=task_count-1,
                        )   
        )

    else:
        await callback.answer(
            text="Извините, но меньше нельзя!",
            show_alert=True
        )

@router.callback_query(FactoryTask.filter(F.object == "physics" and F.decision == True), StateMachine.leaf_task_physics)
async def message_with_text(callback: CallbackQuery, state: FSMContext, callback_data: FactoryTask):
    user_data = await state.get_data()
    task_number = user_data["task_number"]
    task_count = callback_data.task_count
    answer = await db.get_task_decision(id=task_count,task_number=task_number, object="physics")
    if answer:
        await callback.answer(
            text=f'Ответ: {answer}',
            show_alert=True
            )
    else:
        await callback.answer(
            text='Извините, но у нас нет ответа на эту задачку:((',
            show_alert=True
            )
     