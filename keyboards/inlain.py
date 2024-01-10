from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from typing import Union, Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dictionar.dictionaries import class_len
from dictionar.oge_tasks import oge_list

class IKB:

    @staticmethod
    async def create_keyboard_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Информатика👨‍💻", callback_data="informatics:section"),
                InlineKeyboardButton(text="Физика☢️", callback_data=f"physics:section")
            ],
            [
                InlineKeyboardButton(text="Профиль🙎🏻‍♂️", callback_data=f"profile")
            ]
        ])
    
    @staticmethod
    async def create_keyboard_oge_task(task_number: str, task_count: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="📝Решение",callback_data=f"decision_{task_number}_{task_count}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data="oge")
            ]
        ])
    
    @staticmethod
    async def create_keyboard_oge_decision(task_number: str, task_count: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"task_{task_number}")

            ]
        ])
    
    @staticmethod
    async def create_keyboard_oge_decision(task_number: str, task_count: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"task_{task_number}")
            ]
        ])
    
    @staticmethod
    async def create_keyboard_tasks() -> InlineKeyboardMarkup:
        buttons_rows = []
        buttons_all = [InlineKeyboardButton(text=f"{item}", callback_data=f"task_{index+1}") for index, item in enumerate(oge_list)]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"Back"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []
        if row:
            buttons_rows.append(row)

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    @staticmethod
    async def create_keyboard_physics() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Конспекты", callback_data=f"physics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data=f"physics_task")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="Back")
            ]
        ])
    
    @staticmethod
    async def create_keyboard_informatics() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Конспекты", callback_data=f"informatics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data=f"informatics_task")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="Back")
            ]
        ])
    
    @staticmethod
    async def create_profil() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="Back")
            ]
        ])

    
    




