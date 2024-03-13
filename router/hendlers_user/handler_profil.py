from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.inlain_users import ikb
from lexicon.lexicon import LEXICON, generate_tasks_string
from fsm import StateMachine

router = Router()


@router.callback_query(F.data == 'profile', StateMachine.menu)
async def callbacks_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Это профиль и тут вам предлагается просмотреть статистику по вашим решеным задачкам.📊\n\n"
        f"Ваш id:",
        reply_markup= await ikb.create_profil()
     )    
    await callback.answer()
    await state.set_state(StateMachine.profile)

    
@router.callback_query(F.data == 'statistics', StateMachine.profile)
async def statistics_profile(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Это профиль и тут вам предлагается просмотреть статистику по вашим решеным задачкам.📊\n\n"
        f"Вот ваша статистика по задачам:\n\n{await generate_tasks_string(callback.from_user.id)}",
        reply_markup= await ikb.create_profil()
     )
    await callback.answer()
    await state.set_state(StateMachine.statistics)