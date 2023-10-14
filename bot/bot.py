import telebot
import states.states as states
import buttons.buttons as buttons
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

state_storage = StateMemoryStorage()
bot = telebot.TeleBot('6652605107:AAFLxE_GAkvr-HC4AKW3h_WotvYYiOBrSdk',state_storage=state_storage)

def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.set_state(message.from_user.id, states.RandomStates.chooseaction, message.chat.id)
        bot.send_message(message.chat.id, "Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и хз придумайте описание пж. Выберите действие",
                         reply_markup= buttons.chooseactioon_markup)
        
        
        
    @bot.message_handler(state=states.RandomStates.chooseaction)
    def choseact(message):
        bot.send_message(message.chat.id,'kfivnoinismcf')
        
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

