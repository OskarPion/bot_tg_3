from aiogram.fsm.state import State, StatesGroup


class RequestStates(StatesGroup):
    name = State()
    description = State()
    email = State()


class JobsStates(StatesGroup):
    jobs_name = State()
    classification = State()
    money = State()
    somestate = State()


class PhotoStates(StatesGroup):
    send_photo = State()
    send_video = State()


class DocumentStates(StatesGroup):
    document = State()


