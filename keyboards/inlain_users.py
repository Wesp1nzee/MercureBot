from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.dict_task_number_inf import container_inf
from lexicon.dict_task_number_phy import container_phy
from lexicon.lexicon import oge_list_physics, oge_list_informatics
from callback_factory import FactoryTask, FactoryError

class IKB:
    """Клавиатура пользователей"""

    async def create_keyboard_menu_start(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text='Меню📋', callback_data='menu')
            ]
        ])

    async def create_kd_menu(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Информатика👨‍💻", callback_data="informatics:section"),
                InlineKeyboardButton(text="Физика☢️", callback_data=f"physics:section")
            ],
            [
                InlineKeyboardButton(text="Профиль🙎🏻‍♂️", callback_data=f"profile")
            ]
        ])
    
    async def create_kb_pagination_inf(self, task_number: str, task_count: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=FactoryTask(object="informatics", task_number=task_number, task_count=task_count, direction="Back").pack()),
                InlineKeyboardButton(text=f"{task_count}/{await container_inf.get_item(task_number)}",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=FactoryTask(object="informatics", task_number=task_number, task_count=task_count, direction="Next").pack())
            ],
            [
                InlineKeyboardButton(text="✅Ответ",callback_data=FactoryTask(object="informatics", task_number=task_number, task_count=task_count, decision=True).pack())
            ],
            [
                InlineKeyboardButton(text="🚨Сообщить об ошибке🚨",callback_data=FactoryError(object="error_message", task_number=task_number, task_count=task_count).pack())
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"back_informatics_task")
            ]
        ])
    
    async def create_kb_pagination_phy(self, task_number: str, task_count: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="«",callback_data=FactoryTask(object='physics', task_number=task_number, task_count=task_count, direction="Back").pack()),
                InlineKeyboardButton(text=f"{task_count}/{await container_phy.get_item(task_number)}",callback_data="plug"),
                InlineKeyboardButton(text="»",callback_data=FactoryTask(object='physics', task_number=task_number, task_count=task_count, direction="Next").pack())
            ],
            [
                InlineKeyboardButton(text="✅Ответ",callback_data=FactoryTask(object='physics', task_number=task_number, task_count=task_count, decision=True).pack())
            ],
            [
                InlineKeyboardButton(text="🚨Сообщить об ошибке🚨",callback_data=FactoryError(object='error_message', task_number=task_number, task_count=task_count).pack())
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"back_physics_task")
            ]
        ])

    async def create_kb_task_physics(self) -> InlineKeyboardMarkup:
        buttons_rows = []
        buttons_all = [
            InlineKeyboardButton(text=f"{item}",
                                callback_data=FactoryTask(object="physics", task_number = index+1 ).pack()) for index, item in enumerate(oge_list_physics)
                                ]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"back_physics"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    async def create_kb_tasks_informatics(self) -> InlineKeyboardMarkup:
        buttons_rows = []
        buttons_all = [
            InlineKeyboardButton(text=item,
                                callback_data=FactoryTask(object="informatics", task_number = index+1 ).pack()) for index, item in enumerate(oge_list_informatics)
                                ]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"back_informatics"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []

        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)
    
    async def create_keyboard_physics(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Теория🌌", callback_data=f"physics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data="physics")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")
            ]
        ])
    

    async def create_kb_informatics(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Теория🌌", callback_data="informatics_theory")
            ],
            [
                InlineKeyboardButton(text="ОГЭ🆘", callback_data="informatics")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")
            ]
        ])
    

    async def create_profil(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Статистика📊", callback_data="statistics")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")
            ]
        ])
    
    async def back_statistics(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="statistics")
            ]
        ])
    
    async def create_statistics(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Информатика", callback_data="statistics:inf"),
                InlineKeyboardButton(text="Физика", callback_data="statistics:phy")
            ],
            [
                InlineKeyboardButton(text="🔙Назад", callback_data="profile")
            ]    
        ])
    

    async def create_keybord_theory(self) -> InlineKeyboardMarkup:
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



    async def create_kb_themes_physics(self) -> InlineKeyboardMarkup:
        # themes = ['МЕХАНИЧЕСКИЕ ЯВЛЕНИЯ Ч-1','МЕХАНИЧЕСКИЕ ЯВЛЕНИЯ Ч-2','ТЕПЛОВЫЕ ЯВЛЕНИЯ', 'ЭЛЕКТРОМАГНИТНЫЕ ЯВЛЕНИЯ','КВАНТОВЫЕ ЯВЛЕНИЯ']
        # buttons_rows = []
        # buttons_all = [InlineKeyboardButton(text=f"{item}", callback_data=f"physics:themes_{index+1}") for index, item in enumerate(themes)]
        # buttons_all.append(InlineKeyboardButton(text="🔙Назад",callback_data=f"back_physics"))
        # row = []
        # for button in buttons_all:
        #     row.append(button)
        #     buttons_rows.append(row)
        #     row = []

        # return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Плейлист", url="https://www.youtube.com/playlist?list=PLLb2QnIP-fSUiDDjHkaStEJCj0CWJbLVE")
            ],
            [
                InlineKeyboardButton(text="Эмиль Исмаилов", url="https://www.youtube.com/@globalee_physics")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"back_physics")
            ]
        ])
    

    # async def create_keybord_themes_physics_url(self) -> InlineKeyboardMarkup:
    #     #https://telegra.ph/MEHANICHESKIE-YAVLENIYA-01-12
    #     #https://telegra.ph/MEHANICHESKIE-YAVLENIYA-CHAST-2-01-13
    #     pass

    async def create_kb_informatics_url(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Плейлист", url="https://www.youtube.com/watch?v=mUY00El5fZQ&list=PLs2IpQwiXpT130p7XYe9JJ0KN8aFEROdK")
            ],
            [
                InlineKeyboardButton(text="Иван Викторович", url="https://www.youtube.com/@plugar_inf")
            ],
            [
                InlineKeyboardButton(text="🔙Назад",callback_data=f"back_informatics")
            ]
        ])
    
    async def back_mistake(self, object, task_number) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙Назад", callback_data=FactoryTask(object=object, task_number = task_number).pack())
            ]
        ])
        
    
    

ikb = IKB()