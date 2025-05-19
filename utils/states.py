from aiogram.fsm.state import State, StatesGroup


class RequestStates(StatesGroup):
    name = State()
    description = State()
    email = State()


class JobsStates(StatesGroup):
    jobs_name = State()
    classification = State()
    money = State()
