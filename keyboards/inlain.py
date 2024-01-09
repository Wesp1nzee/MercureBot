from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from dictionar.dictionaries import class_len
from dictionar.oge_tasks import oge_list

def create_keyboard_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(7,10):
        builder.button(text=f"{i} класс📚", callback_data=f"class_{i}")
    builder.button(text="ОГЭ🆘", callback_data=f"oge")
    builder.button(text="Профиль👩🏻‍💻", callback_data=f"profile")
    builder.adjust(3,1,1)
    return builder.as_markup()

#Оге задачи кнопки
def create_keyboard_tasks() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, item in enumerate(oge_list):
        builder.button(text=f"{item}", callback_data=f"task_{index+1}")
    builder.button(text="🔙Назад", callback_data=f"Back")
    builder.adjust(1)
    return builder.as_markup()

#Создаем кнопки lesson
def create_keyboard_lesson(class_data: str, type_work: str ) -> InlineKeyboardMarkup:
    len_lesson = int(class_len[class_data][type_work])
    builder = InlineKeyboardBuilder()
    for i in range(1,len_lesson+1):
        builder.button(text=f"{i} урок", callback_data=f"lesson_{i}")
    builder.adjust(3)
    return builder.as_markup()

def create_keyboard_theory_practice() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Теория", callback_data="theory")
    builder.button(text="Практика", callback_data="practice")
    builder.button(text="🔙Назад", callback_data="Back")
    builder.adjust(2)
    return builder.as_markup()

def create_keyboard_oge_task(task_number: str, task_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="<<",callback_data=f"tasks_back_{task_number}" )
    builder.button(text=f"{task_count}/60",callback_data="plug" )
    builder.button(text=">>",callback_data=f"tasks_next_{task_number}")
    builder.button(text="📝Решение",callback_data=f"decision_{task_number}_{task_count}")
    builder.button(text="🔙Назад",callback_data="oge")
    builder.adjust(3,1,1)
    return builder.as_markup()

def create_keyboard_oge_decision(task_number: str, task_count: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="<<",callback_data=f"tasks_back_{task_number}" )
    builder.button(text=f"{task_count}/60",callback_data="plug" )
    builder.button(text=">>",callback_data=f"tasks_next_{task_number}")
    builder.button(text="🔙Назад",callback_data=f"task_{task_number}")
    builder.adjust(3,1)
    return builder.as_markup()



