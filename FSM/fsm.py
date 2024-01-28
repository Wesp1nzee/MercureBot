from aiogram.fsm.state import StatesGroup, State


class StateMachine(StatesGroup):
    start = State()
    menu = State()
    informatics = State()
    physics = State()