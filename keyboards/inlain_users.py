from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.dict_task_number import container_inf
from lexicon.dict_task_number import container_phy
from lexicon.lexicon import oge_list_physics, oge_list_informatics
from callback_factory import FactoryTask, FactoryMistake


class IKB:
    """Inlain Button for users"""

    async def create_keyboard_menu_start(self) -> InlineKeyboardMarkup:
        """
        /start
        1 row: Меню📋
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Меню📋", callback_data="menu")]
            ]
        )

    async def create_kd_menu(self) -> InlineKeyboardMarkup:
        """
        'Меню'
        1 row: Информатика👨‍💻 Физика☢️
        2 row: Профиль🙎🏻‍♂️
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Информатика👨‍💻", callback_data="informatics:section"
                    ),
                    InlineKeyboardButton(
                        text="Физика☢️", callback_data=f"physics:section"
                    ),
                ],
                [InlineKeyboardButton(text="Профиль🙎🏻‍♂️", callback_data=f"profile")],
            ]
        )

    async def create_kb_pagination_inf(
        self, task_number: str, task_count: int
    ) -> InlineKeyboardMarkup:
        """
        'Информатика👨‍💻' -> 'ОГЭ🆘' -> 'Задание n'
        1 row: « (task count user)/(max task count) »
        2 row: ✅Ответ
        3 row: 🚨Сообщить об ошибке🚨
        4 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="«",
                        callback_data=FactoryTask(
                            object="informatics",
                            task_number=task_number,
                            task_count=task_count,
                            direction="Back",
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text=f"{task_count}/{await container_inf.get_item(task_number)}",
                        callback_data="plug",
                    ),
                    InlineKeyboardButton(
                        text="»",
                        callback_data=FactoryTask(
                            object="informatics",
                            task_number=task_number,
                            task_count=task_count,
                            direction="Next",
                        ).pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✅Ответ",
                        callback_data=FactoryTask(
                            object="informatics",
                            task_number=task_number,
                            task_count=task_count,
                            decision=True,
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨Сообщить об ошибке🚨",
                        callback_data=FactoryMistake(
                            object="error_message",
                            task_number=task_number,
                            task_count=task_count,
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_informatics_task"
                    )
                ],
            ]
        )

    async def create_kb_pagination_phy(
        self, task_number: str, task_count: int
    ) -> InlineKeyboardMarkup:
        """
        'Физика☢️' -> 'ОГЭ🆘' -> 'Задание n'
        1 row: « (task count user)/(max task count) »
        2 row: ✅Ответ
        3 row: 🚨Сообщить об ошибке🚨
        4 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="«",
                        callback_data=FactoryTask(
                            object="physics",
                            task_number=task_number,
                            task_count=task_count,
                            direction="Back",
                        ).pack(),
                    ),
                    InlineKeyboardButton(
                        text=f"{task_count}/{await container_phy.get_item(task_number)}",
                        callback_data="plug",
                    ),
                    InlineKeyboardButton(
                        text="»",
                        callback_data=FactoryTask(
                            object="physics",
                            task_number=task_number,
                            task_count=task_count,
                            direction="Next",
                        ).pack(),
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="✅Ответ",
                        callback_data=FactoryTask(
                            object="physics",
                            task_number=task_number,
                            task_count=task_count,
                            decision=True,
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🚨Сообщить об ошибке🚨",
                        callback_data=FactoryMistake(
                            object="error_message",
                            task_number=task_number,
                            task_count=task_count,
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_physics_task"
                    )
                ],
            ]
        )

    async def create_kb_task_physics(self) -> InlineKeyboardMarkup:
        """
        'Физика' -> 'ОГЭ🆘'
        1 row: Задание 1 Физические величины
        n row: ...
        21 row: Задания 24-25 Расчетные задачи
        22 row: 🔙Назад
        """
        buttons_rows = []
        buttons_all = [
            InlineKeyboardButton(
                text=f"{item}",
                callback_data=FactoryTask(
                    object="physics", task_number=index + 1
                ).pack(),
            )
            for index, item in enumerate(oge_list_physics)
        ]
        buttons_all.append(
            InlineKeyboardButton(text="🔙Назад", callback_data=f"back_physics")
        )
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []
        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    async def create_kb_tasks_informatics(self) -> InlineKeyboardMarkup:
        """
        'Информатика' -> 'ОГЭ🆘'
        1 row: Задание 1 Биты, байты
        n row: ...
        10 row: Задание 10 Перевод чисел
        11 row: 🔙Назад
        """
        buttons_rows = []
        buttons_all = [
            InlineKeyboardButton(
                text=item,
                callback_data=FactoryTask(
                    object="informatics", task_number=index + 1
                ).pack(),
            )
            for index, item in enumerate(oge_list_informatics)
        ]
        buttons_all.append(InlineKeyboardButton(text="🔙Назад", callback_data=f"back_informatics"))
        row = []
        for button in buttons_all:
            row.append(button)
            buttons_rows.append(row)
            row = []
        return InlineKeyboardMarkup(inline_keyboard=buttons_rows)

    async def create_keyboard_physics(self) -> InlineKeyboardMarkup:
        """
        'Физика'
        1 row: Теория🌌
        2 row: ОГЭ🆘
        3 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Теория🌌", callback_data=f"physics_theory")],
                [InlineKeyboardButton(text="ОГЭ🆘", callback_data="physics")],
                [InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")],
            ]
        )

    async def create_kb_informatics(self) -> InlineKeyboardMarkup:
        """
        'Информатика'
        1 row: Теория🌌
        2 row: ОГЭ🆘
        3 row: 🔙Назад
        """

        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Теория🌌", callback_data="informatics_theory")],
                [InlineKeyboardButton(text="ОГЭ🆘", callback_data="informatics")],
                [InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")],
            ]
        )

    async def create_profil(self) -> InlineKeyboardMarkup:
        """
        'Профиль'
        1 row: Статистика📊
        2 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Статистика📊", callback_data="statistics")],
                [InlineKeyboardButton(text="🔙Назад", callback_data="back_menu")],
            ]
        )

    async def back_statistics(self) -> InlineKeyboardMarkup:
        """
        'Профиль' -> 'Статистика' -> 'Информатика' or 'Физика'
        1 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙Назад", callback_data="statistics")]
            ]
        )

    async def create_statistics(self) -> InlineKeyboardMarkup:
        """
        'Профиль' -> 'Статистика'
        1 row: Информатика Физика
        2 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Информатика", callback_data="statistics:inf"
                    ),
                    InlineKeyboardButton(text="Физика", callback_data="statistics:phy"),
                ],
                [InlineKeyboardButton(text="🔙Назад", callback_data="profile")],
            ]
        )

    async def create_kb_themes_physics(self) -> InlineKeyboardMarkup:
        """
        'Физика -> теория'
        1 row: Плейлист
        2 row: Эмиль Исмаилов
        3 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Плейлист",
                        url="https://www.youtube.com/playlist?list=PLLb2QnIP-fSUiDDjHkaStEJCj0CWJbLVE",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Эмиль Исмаилов",
                        url="https://www.youtube.com/@globalee_physics",
                    )
                ],
                [InlineKeyboardButton(text="🔙Назад", callback_data=f"back_physics")],
            ]
        )

    async def create_kb_informatics_url(self) -> InlineKeyboardMarkup:
        """
        'Информатика'- 'Теория'
        1 row: Плейлист
        2 row: Иван Викторович
        3 row: 🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Плейлист",
                        url="https://www.youtube.com/watch?v=mUY00El5fZQ&list=PLs2IpQwiXpT130p7XYe9JJ0KN8aFEROdK",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Иван Викторович",
                        url="https://www.youtube.com/@plugar_inf",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔙Назад", callback_data=f"back_informatics"
                    )
                ],
            ]
        )

    async def back_mistake(self, object, task_number) -> InlineKeyboardMarkup:
        """
        mistake
        1 row :🔙Назад
        """
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔙Назад",
                        callback_data=FactoryTask(
                            object=object, task_number=task_number
                        ).pack(),
                    )
                ]
            ]
        )

    async def create_phenomenon_selection_kd(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Механические явления",
                        callback_data=FactoryTask(
                            object="physics", task_number="18_1"
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Тепловые явления",
                        callback_data=FactoryTask(
                            object="physics", task_number="18_2"
                        ).pack(),
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Электрические явления",
                        callback_data=FactoryTask(
                            object="physics", task_number="18_3"
                        ).pack(),
                    )
                ],
                [InlineKeyboardButton(text="🔙Назад", callback_data=f"back_physics_task")],
            ]
        )


ikb = IKB()
