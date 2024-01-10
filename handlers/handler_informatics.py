from keyboards.inlain import IKB
from dictionar.dictionaries import glavu, lesson_content_dict
from handlers.db import users_db_condition
from lexicon.lexicon import generate_tasks_string

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode 
from aiogram.utils.markdown import hide_link 