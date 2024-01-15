from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dictionar.oge_tasks import oge_list_physics, oge_list_informatics
from handlers.db import users_db_condition

class IKB:


    @staticmethod
    async def create_keyboard_menu_start():
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню📋', callback_data='menu'),
                InlineKeyboardButton(text='Помощь🙏', callback_data='help')
            ]
        ])
    
    @staticmethod
    async def create_kb_help() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню📋', callback_data='menu')
            ]
        ])

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
    async def create_keyboard_oge_task(task_number: str, task_count: int, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"{users_db_condition[user_id]['object']}:tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"{users_db_condition[user_id]['object']}:tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="📝Решение",callback_data=f"{users_db_condition[user_id]['object']}:decision_{task_number}_{task_count}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"{users_db_condition[user_id]['object']}_task")
            ]
        ])
    
    @staticmethod
    async def create_keyboard_oge_decision(task_number: str, task_count: int, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"{users_db_condition[user_id]['object']}:tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"{users_db_condition[user_id]['object']}:tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"{users_db_condition[user_id]['object']}:task_{task_number}")
            ]
        ])
    
    @staticmethod
    async def create_kb_oge_task(task_number: str, task_count: int, user_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=f"{users_db_condition[user_id]['object']}:tasks_back_{task_number}"),
                InlineKeyboardButton(text=f"{task_count}/60",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=f"{users_db_condition[user_id]['object']}:tasks_next_{task_number}")
            ],
            [
                InlineKeyboardButton(text="📝Решение",callback_data=f"{users_db_condition[user_id]['object']}:decision_{task_number}_{task_count}")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"{users_db_condition[user_id]['object']}_task")
            ]
        ])
    
    @staticmethod
    async def create_kb_task_physics() -> InlineKeyboardMarkup:
        buttons_rows = []
        buttons_all = [InlineKeyboardButton(text=f"{item}", callback_data=f"physics:task_{index+1}") for index, item in enumerate(oge_list_physics)]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"menu"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    
    
    @staticmethod
    async def create_kb_tasks_informatics() -> InlineKeyboardMarkup:
        buttons_rows = []
        buttons_all = [InlineKeyboardButton(text=f"{item}", callback_data=f"informatics:task_{index+1}") for index, item in enumerate(oge_list_informatics)]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"menu"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    @staticmethod
    async def create_keyboard_physics() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Теория🌌", callback_data=f"physics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data=f"physics_task")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="menu")
            ]
        ])
    
    @staticmethod
    async def create_kb_informatics() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Теория🌌", callback_data="informatics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data="informatics_task")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="menu")
            ]
        ])
    
    @staticmethod
    async def create_profil() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Статистика📊", callback_data="statistics")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="menu")
            ]
            
        ])
    
    @staticmethod
    async def create_keybord_theory() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Конспекты ОГЭ📑", callback_data="physics:themes")
            ],
            [
                InlineKeyboardButton(text="Плейлист📺", url="https://www.youtube.com/playlist?list=PLLb2QnIP-fSUiDDjHkaStEJCj0CWJbLVE")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="menu")
            ]
        ])


    @staticmethod
    async def create_kb_themes_physics() -> InlineKeyboardMarkup:
        themes = ['МЕХАНИЧЕСКИЕ ЯВЛЕНИЯ Ч-1','МЕХАНИЧЕСКИЕ ЯВЛЕНИЯ Ч-2','ТЕПЛОВЫЕ ЯВЛЕНИЯ', 'ЭЛЕКТРОМАГНИТНЫЕ ЯВЛЕНИЯ','КВАНТОВЫЕ ЯВЛЕНИЯ']
        buttons_rows = []
        buttons_all = [InlineKeyboardButton(text=f"{item}", callback_data=f"physics:themes_{index+1}") for index, item in enumerate(themes)]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"physics:section"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    @staticmethod
    async def create_keybord_themes_physics_url() -> InlineKeyboardMarkup:
        #https://telegra.ph/MEHANICHESKIE-YAVLENIYA-01-12
        #https://telegra.ph/MEHANICHESKIE-YAVLENIYA-CHAST-2-01-13
        pass
    
    @staticmethod
    async def create_kb_informatics_url() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Плейлист", url="https://www.youtube.com/watch?v=mUY00El5fZQ&list=PLs2IpQwiXpT130p7XYe9JJ0KN8aFEROdK")
            ],
            [
                InlineKeyboardButton(text="Иван Викторович", url="https://www.youtube.com/@plugar_inf")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"informatics:section")
            ]

        ])
    
    




