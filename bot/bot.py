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
    def register(message):
        if db.check_user(message.chat.id):
            bot.set_state(message.from_user.id, states.RandomStates.register, message.chat.id)
            bot.send_message(message.chat.id,"Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп\n"
                         "Пожалуйста,введите свое имя для продолжения работы")
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
        bot.set_state(message.from_user.id, states.RandomStates.chooseaction, message.chat.id)
        bot.send_message(message.chat.id, "Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников группы. Создайте группу, добавьте участников и побликуйте задачи, которые участники смогут выбрать и решить самостоятельно! Устанавливайте крайние даты решения, добавьте описание задач и работайте с другими функциями Taskmatic!\n"
                                          "Выберите раздел",
                         reply_markup= buttons.chooseactioon_markup)
        
    @bot.message_handler(state=states.RandomStates.register)
    def register(message):
        db.register_user(message.chat.id,message.text)
        bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
        

    @bot.message_handler(state=states.RandomStates.chooseaction)
    def choseact(message):
        bot.send_message(message.chat.id,'kfivnoinismcf')
        
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

