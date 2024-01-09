from keyboards.inlain import(create_keyboard_lesson,
                            create_keyboard_theory_practice,
                            create_keyboard_menu)
from keyboards.inlain_practice import(create_keyboard_pract)
from keyboards.inlain_teor import(create_keyboard_teor)
from dictionar.dictionaries import glavu, lesson_content_dict, lesson_dict_article
from handlers.db import users_db_condition
from lexicon.lexicon import generate_tasks_string

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()
#Кнопка назад
@router.callback_query(F.data.startswith('Back'))
async def message_with_text(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери какой класс тебе интересен:",    
        reply_markup = create_keyboard_menu()
    )
    await callback.answer()

# Этот хэндлер будет срабатывать на инлаин кнопку "Класс"
@router.callback_query(F.data.startswith('class_'))
async def callbacks_num_change_fab(callback: CallbackQuery ):
    users_db_condition[callback.from_user.id].update({"class":f"{callback.data.split('_')[1]}"})

    await callback.message.edit_text( 
        "Выбери, что ты хочешь изучать."
        "Теорию или сразу перейти к практике?",
        reply_markup=create_keyboard_theory_practice()
    )
    await callback.answer()

#Хендлер для теории и практики 
@router.callback_query((F.data.startswith('theory')) | (F.data.startswith('practice')))
async def callbacks_num_change_fab(callback: CallbackQuery ):
    users_db_condition[callback.from_user.id].update({"direction":f"{callback.data}"})
#Условие если выбрали теорию для определенного класса
    if users_db_condition[callback.from_user.id]['direction'] == "theory":
        await callback.message.edit_text( 
        f"Выбери главу для {users_db_condition[callback.from_user.id]['class']} класса:",
        reply_markup=create_keyboard_teor(users_db_condition[callback.from_user.id]['class'])
    )
        await callback.answer()

#Условие если выбрали практику для определенного класса 
    if users_db_condition[callback.from_user.id]['direction'] == "practice":
        await callback.message.edit_text( 
        f"Выбери главу для {users_db_condition[callback.from_user.id]['class']} класса: ",
        reply_markup= create_keyboard_pract(users_db_condition[callback.from_user.id]['class'])
        )
        await callback.answer()

#Срабатывает на выбор главы 
@router.callback_query((F.data.startswith('glava:T')) | (F.data.startswith('glava:P')))
async def callbacks_num_change_fab(callback: CallbackQuery ):
    users_db_condition[callback.from_user.id].update({"chapter":f"{callback.data.split('_')[2]}"})
    #Условие если выбрали теорию для определенной главы
    if users_db_condition[callback.from_user.id]['direction'] == "theory":
        await callback.message.edit_text(
            "Темы уроков:" 
            f"<b>\n{lesson_content_dict[users_db_condition[callback.from_user.id]['class']][users_db_condition[callback.from_user.id]['chapter']]}</b>",
            reply_markup=create_keyboard_lesson(users_db_condition[callback.from_user.id]['class'],users_db_condition[callback.from_user.id]['chapter'])
        )
        await callback.answer()
    #Условие если выбрали практику для определенной главы
    if users_db_condition[callback.from_user.id]['direction'] == "practice":
        await callback.message.edit_text( 
        f'Вот ваша практика для {users_db_condition[callback.from_user.id]["class"]} класса "{glavu[users_db_condition[callback.from_user.id]["class"]][users_db_condition[callback.from_user.id]["chapter"]]}"',
        )
        await callback.answer()

# Этот хэндлер будет срабатывать на инлаин кнопку "Уроки"
@router.callback_query(F.data.startswith('lesson_'))
async def callbacks_num_change_fab(callback: CallbackQuery ):
    lesson_data =  callback.data.split("_")[1]
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙Назад", callback_data="theory")
    await callback.message.edit_text( 
         f"{hide_link(lesson_dict_article[users_db_condition[callback.from_user.id]['class']][users_db_condition[callback.from_user.id]['chapter']][lesson_data])}"
         f"Вот ваш выбраный урок:", parse_mode=ParseMode.HTML, reply_markup=builder.as_markup()
     )    
    await callback.answer()


@router.callback_query(F.data.startswith('profile'))
async def callbacks_profile(callback: CallbackQuery ):
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙Назад", callback_data="Back")
    await callback.message.edit_text(
        f"Это профиль и тут вам предлагаетс япросмотреть статистику по вашим решеным задачкам.👨🏻‍🎓\n\n"
        f"Вот ваша статистика по задачам:\n\n{generate_tasks_string(callback.from_user.id)}",
        reply_markup=builder.as_markup()
     )    
    await callback.answer()