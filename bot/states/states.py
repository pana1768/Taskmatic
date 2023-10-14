from telebot.handler_backends import State, StatesGroup


class Groups(StatesGroup):
    chooserole = State()
    manager = State()
    executor = State()
    
class Tasks(StatesGroup):
    chooserole = State()


    
class RandomStates(StatesGroup):
    chooseaction = State()
    register = State()
    start_work = State()