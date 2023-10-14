import telebot
import states.states as states
import buttons.buttons as buttons
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import db.db as db


state_storage = StateMemoryStorage()
bot = telebot.TeleBot('6652605107:AAFLxE_GAkvr-HC4AKW3h_WotvYYiOBrSdk',state_storage=state_storage)

def main():
    @bot.message_handler(commands=['start'])
    def check_register(message):
        if db.check_user(message.chat.id):
            bot.set_state(message.from_user.id, states.RandomStates.register, message.chat.id)
            bot.send_message(message.chat.id,"Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп\n"
                         "Пожалуйста,введите свое имя для продолжения работы")
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
            bot.send_message(message.chat.id,'Этот бот поможет вам удобно управлять задачами и быстро\n распределять их среди участников группы. Создайте группу, добавьте участников и побликуйте задачи, \n которые участники смогут выбрать и решить самостоятельно! Устанавливайте крайние даты решения,\n добавьте описание задач и работайте с другими функциями Taskmatic!',
                             reply_markup=buttons.choosepoint_markup)
    @bot.message_handler(state=states.RandomStates.register)
    def register(message):
        a = "@"+message.from_user.username
        print(a)
        db.register_user(message.chat.id,message.text,a)
        bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
        bot.send_message(message.chat.id,'Этот бот поможет вам удобно управлять задачами и быстро\n распределять их среди участников группы. Создайте группу, добавьте участников и побликуйте задачи, \n которые участники смогут выбрать и решить самостоятельно! Устанавливайте крайние даты решения,\n добавьте описание задач и работайте с другими функциями Taskmatic!',
                             reply_markup=buttons.choosepoint_markup)
        

    @bot.message_handler(state=states.RandomStates.start_work)
    def start_work(message):
        if message.text == 'Группы':
            bot.set_state(message.from_user.id, states.Groups.choosertype, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие:",reply_markup=buttons.chooseaction_markup)
        
    @bot.message_handler(state=states.Groups.choosertype)
    def choosetype(message):
        if message.text == "Создать группу":
            
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()