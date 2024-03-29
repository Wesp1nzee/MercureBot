from aiogram.fsm.state import StatesGroup, State


class StateMachine(StatesGroup):
    start = State()
    menu = State()

    profile = State()
    informatics = State()
    physics = State()

    theory_informatics = State()
    task_selection_informatics = State()
    leaf_task_informatics = State()

    theory_physics = State()
    task_selection_physics = State()
    task_18_selection_physics = State()
    leaf_task_physics = State()

    statistics = State()
    statistics_phy = State()
    statistics_inf = State()
    
    error_message = State()
    