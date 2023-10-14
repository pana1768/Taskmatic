import telebot
import states.states as states
import buttons.buttons as buttons
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import db.db as db
import logging
logging.basicConfig(level=logging.WARNING, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
msg_id = None
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
        #таски
    @bot.message_handler(state=states.Groups.choosertype)
    def choosetype(message):
        if message.text == "Создать группу":
            bot.set_state(message.from_user.id, states.CreateGroup.entername)
            bot.send_message(message.chat.id, "Введите название группы:")
        elif message.text == 'Мои группы':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль",reply_markup=buttons.chooserole_markup)
            
    @bot.message_handler(state=states.Groups.chooserole)
    def choserole(message):
        if message.text == 'Я руководитель':
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            #добавить просмотр/редактировать
            bot.send_message(message.chat.id,"Выберите действие",reply_markup=buttons.yarukoblud_markup)
        #доделать

    @bot.message_handler(state=states.Groups.chooseactionadmin)
    def chooseactionadmin(message):
        if message.text == "Просмотр":
            grouplist = db.get_admin_groups(message.chat.id)
            keylist_markup = buttons.inline_get_list(grouplist)
            bot.send_message(message.chat.id,"Ваши группы:",reply_markup=keylist_markup)
        elif message.text == 'Назад':
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            bot.send_message(message.chat.id, "Выберите роль",reply_markup=buttons.chooserole_markup)
        else:
            grouplist = db.get_admin_groups(message.chat.id)
            keylist_markup = buttons.inline_get_list_edit(grouplist)
            bot.send_message(message.chat.id,"Выберите группу:",reply_markup=keylist_markup)
            
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'adminedit')
    def get_group_info(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
        bot.set_state(call.from_user.id, states.Groups.edit)
        bot.send_message(call.message.chat.id,"Выберите действие",parse_mode='HTML',reply_markup=buttons.changegr_markup)
        
    
    @bot.message_handler(state=states.Groups.edit)
    def editGroup(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        if message.text == 'Удалить группу':
            db.delete_group(group_id)
            bot.send_message(message.chat.id, "Вы удалили группу")
        elif message.text == 'Удалить участника':
            bot.send_message(message.chat.id,'Введите никнейм участника в формате @username')
            bot.set_state(message.from_user.id, states.Groups.wait_username)
        else:
            bot.send_message(message.chat.id,"Выберите действие",reply_markup=buttons.yarukoblud_markup)
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            
    @bot.message_handler(state=states.Groups.wait_username)
    def user_delete(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        rez = db.delete_member(message.text,group_id)
        if rez == 0:
            bot.send_message(message.chat.id,'Пользователь не найден')
        else:
            bot.send_message(message.chat.id,'Пользователь успешно удален')
            bot.set_state(message.from_user.id, states.Groups.edit)
            bot.send_message(message.chat.id,"Выберите действие",parse_mode='HTML',reply_markup=buttons.changegr_markup)
        
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'admin')
    def get_group_info(call):
        group_id = call.data.split('_')[1]
        text_group = db.info_groups(group_id)
        bot.send_message(call.message.chat.id,text_group,parse_mode='HTML',reply_markup=buttons.backup_markup)
        
        
        
    @bot.message_handler(state=states.CreateGroup.entername)
    def entername(message):
        if not db.check_doubled_name(message.chat.id,message.text):
            bot.send_message(message.chat.id,'У вас уже есть группа с таким названием, пожалуйста, придумайте новое')
        else:
            db.create_group(message.text,message.chat.id)
            invite_id = "Твой идентификатор группы: " + message.text +"_"+ str(db.get_id_group(message.chat.id,message.text))
            bot.send_message(message.chat.id,invite_id,reply_markup=buttons.choosepoint_markup)
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)

    

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

