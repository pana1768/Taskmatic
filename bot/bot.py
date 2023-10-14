import telebot
import states.states as states
import buttons.buttons as buttons
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import db.db as db
import logging
logging.basicConfig(level=logging.WARNING, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

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
            bot.send_message(message.chat.id,"Этот бот поможет вам удобно управлять задачами и\n"
                             "быстро распределять их среди участников группы.\n"
                             "Создайте группу, добавьте участников и побликуйте задачи,\n" 
                             "которые участники смогут выбрать и решить самостоятельно!\n"
                             "Устанавливайте крайние даты решения, добавьте описание задач и\n" 
                             "работайте с другими функциями Taskmatic!\n",reply_markup=buttons.choosepoint_markup)
        
    @bot.message_handler(state=states.RandomStates.register)
    def register(message):
        a = "@" + message.from_user.username
        db.register_user(message.chat.id,message.text,a)
        bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
        bot.send_message(message.chat.id, "Выберите действие:",reply_markup=buttons.choosepoint_markup)

    @bot.message_handler(state=states.RandomStates.start_work)
    def start_work(message):
        if message.text == 'Группы':
            bot.set_state(message.from_user.id, states.Groups.choosertype, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие:",reply_markup=buttons.chooseaction_markup)
        else:
            pass
    @bot.message_handler(state=states.Groups.choosertype)
    def choosetype(message):
        if message.text == "Создать группу":
            bot.set_state(message.from_user.id, states.CreateGroup.entername)
            bot.send_message(message.chat.id, "Введите название группы:")
        elif message.text == 'Мои группы':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль",reply_markup=buttons.chooseaction_markup)
            
    # @bot.message_handler(state=states.CreateGroup.entername)
    # def choserole(message):
    #     pass       
    #     #доделать

    @bot.message_handler(state=states.CreateGroup.entername)
    def entername(message):
        if not db.check_doubled_name(message.chat.id,message.text):
            bot.send_message(message.chat.id,'У вас уже есть группа с таким названием, пожалуйста, придумайте новое')
            print('')
        else:
            db.create_group(message.text,message.chat.id)
            invite_id = message.text +"_"+ db.get_id_group(message.chat.id,message.text)
            bot.send_message(message.chat.id,"Твой id группы: " + invite_id,buttons.choosepoint_markup)
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
            #Проверить!!!
    
    

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

