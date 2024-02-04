from aiogram.filters.callback_data import CallbackData
from typing import Optional


class FactoryTask(CallbackData, prefix='task'):
    object: str 
    task_number:Optional[int] = None
    task_count:Optional[int] = None
    direction:Optional[str] = None
    decision:Optional[str] = None