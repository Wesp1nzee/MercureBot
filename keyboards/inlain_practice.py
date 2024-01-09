from aiogram.utils.keyboard import  InlineKeyboardMarkup, InlineKeyboardBuilder
from dictionar.dictionaries import glavu



def create_keyboard_pract(class_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, element in glavu[class_data].items():
        builder.button(text=element, callback_data=f"glava:P_{class_data}_{i}")
    builder.button(text="🔙Назад", callback_data=f"class_{class_data}")
    builder.adjust(1)
    return builder.as_markup()

