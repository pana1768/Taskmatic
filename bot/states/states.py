from telebot.handler_backends import State, StatesGroup


class MyGroups(StatesGroup):
    chooserole = State()
    manager = State()
    executor = State()
    
    
class RandomStates(StatesGroup):
    chooseaction = State()