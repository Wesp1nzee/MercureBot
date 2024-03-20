from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.inlain_users import ikb
from lexicon.lexicon import generate_tasks_string
from fsm import StateMachine
from database.datacoonect import db

router = Router()


@router.callback_query(F.data == 'profile', StateMachine.menu)
@router.callback_query(F.data == 'profile', StateMachine.statistics)
async def callbacks_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Это профиль здесь вы можете просмотреть статистику по задачкам.📊\n\n"
        f"Ваш id: {callback.from_user.id}\n\n"
        f"Дата регестрации: {await db.get_data(callback.from_user.id)}",
        reply_markup= await ikb.create_profil()
     )
    
    await callback.answer()
    await state.set_state(StateMachine.profile)


@router.callback_query(F.data == 'statistics', StateMachine.profile)
@router.callback_query(F.data == 'statistics', StateMachine.statistics_phy)
@router.callback_query(F.data == 'statistics', StateMachine.statistics_inf)
async def statistics_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Выбери по какому предмету ходешь увидить статистику:",
        reply_markup= await ikb.create_statistics()
    )
    await callback.answer()
    await state.set_state(StateMachine.statistics)

@router.callback_query(F.data == 'statistics:phy', StateMachine.statistics)
async def statistics_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Статистика по физики:📊\n\n"
        f"{await generate_tasks_string(callback.from_user.id, 'physics')}",
        reply_markup= await ikb.back_statistics()
    )
    await callback.answer()
    await state.set_state(StateMachine.statistics_phy)

@router.callback_query(F.data == 'statistics:inf', StateMachine.statistics)
async def statistics_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Статистика по информатики:📊\n\n"
        f"{await generate_tasks_string(callback.from_user.id, 'informatics')}",
        reply_markup= await ikb.back_statistics()
    )
    await callback.answer()
    await state.set_state(StateMachine.statistics_inf)