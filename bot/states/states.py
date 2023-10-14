from telebot.handler_backends import State, StatesGroup

class TemplateState(StatesGroup):
    first = State()