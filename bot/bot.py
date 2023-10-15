import telebot
import states.states as states
import buttons.buttons as buttons
from telebot.storage import StateMemoryStorage
from telebot import custom_filters
import db.db as db
import logging
import telebot.types as types
logging.basicConfig(level=logging.WARNING, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
msg_id = None
state_storage = StateMemoryStorage()
bot = telebot.TeleBot('6652605107:AAFLxE_GAkvr-HC4AKW3h_WotvYYiOBrSdk',state_storage=state_storage)

def main():
    
    @bot.message_handler(state='*',commands=['jointogroup'])
    def join(message):
        bot.send_message(message.chat.id, "Введите идентификатор группы")
        bot.register_next_step_handler(message,join_to_group)
    def join_to_group(message):
        db.join_group(message.text, message.chat.id)
        bot.send_message(message.chat.id, "Вы успешно добавились в группу")
    
    
    
    
    @bot.message_handler(commands=['start'])
    def check_register(message):
        if db.check_user(message.chat.id):
            bot.set_state(message.from_user.id, states.RandomStates.register, message.chat.id)
            bot.send_message(message.chat.id,"Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп.\n"
                         "Пожалуйста, введите свое имя для продолжения работы")
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
            bot.set_state(message.from_user.id, states.Tasks.choserole, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие:",reply_markup=buttons.chooserole_markup)
        #таски
        
        
    @bot.message_handler(state=states.Groups.choosertype)
    def choosetype(message):
        if message.text == "Создать группу":
            bot.set_state(message.from_user.id, states.CreateGroup.entername)
            bot.send_message(message.chat.id, "Введите название группы:")
        elif message.text == 'Мои группы':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль:",reply_markup=buttons.chooserole_markup)
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие:",reply_markup=buttons.choosepoint_markup)
            
    @bot.message_handler(state=states.Groups.chooserole)
    def choserole(message):
        if message.text == 'Я руководитель':
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            #добавить просмотр/редактировать
            bot.send_message(message.chat.id,"Выберите действие:",reply_markup=buttons.yarukoblud_markup)
        elif message.text == 'Я участник':
            list_of_groups = db.get_executor_group(message.chat.id)
            if len(list_of_groups) == 0:
                bot.send_message(message.chat.id,'Вы не состоите не в одной группе',reply_markup=buttons.chooserole_markup)
            else:
                inline_groups_markup = buttons.inline_get_list_executor(list_of_groups)
                bot.send_message(message.chat.id,'Выберите группу:', reply_markup=inline_groups_markup)
            
            
        else:
            bot.set_state(message.from_user.id, states.Groups.choosertype)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.chooseaction_markup)
        #доделать

    @bot.message_handler(state=states.Groups.chooseactionadmin)
    def chooseactionadmin(message):
        if message.text == "Просмотр":
            grouplist = db.get_admin_groups(message.chat.id)
            keylist_markup = buttons.inline_get_list(grouplist)
            bot.send_message(message.chat.id,"Ваши группы",reply_markup=keylist_markup)
        elif message.text == 'Назад':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
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

    

    
    
    
    
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'executor')
    def chose_group_executor(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
        bot.set_state(call.from_user.id, states.RandomStates.chose_leave)
        bot.send_message(call.message.chat.id,"Выберите действие",reply_markup=buttons.uchastchange_markup)
        
    @bot.message_handler(state= states.RandomStates.chose_leave)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        if message.text == 'Выйти из группы':
            db.leave_group(group_id,message.chat.id)
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Вы успешно вышли из группы",reply_markup=buttons.chooserole_markup)
        else:
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль",reply_markup=buttons.chooserole_markup)
    
    
    
    
    
    @bot.message_handler(state= states.Tasks.choserole)
    def chsrole(message):
        if message.text == 'Я участник':
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.zadruk_markup)
        elif message.text == 'Я руководитель':
            pass
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.choosepoint_markup)
            
    @bot.message_handler(state= states.Tasks.choseactionmember)
    def yahz(message):
        if message.text == 'Создать':
            list_of_groups = db.get_executor_group(message.chat.id)
            if len(list_of_groups) == 0:
                bot.send_message(message.chat.id,'Вы не состоите не в одной группе',reply_markup=buttons.chooserole_markup)
            else:
                inline_groups_markup_tasks = buttons.inline_get_list_executor_tasks(list_of_groups)
                bot.send_message(message.chat.id,'Выберите группу:', reply_markup=inline_groups_markup_tasks)
        elif message.text == 'Свободные':
            pass
        elif message.text == 'В процессе':
            a = db.get_tasks_user(message.chat.id)
            with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
                data['all_pages'] = len(a)
                data['page'] = 1
                pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelist')
                send = types.InlineKeyboardButton('Сдать',callback_data='send_inlinelist')
                right = types.InlineKeyboardButton('->',callback_data='right_inlinelist')
                left = types.InlineKeyboardButton('<-',callback_data='left_inlinelist')
                markup_pages = types.InlineKeyboardMarkup()
                markup_pages.row(send)
                markup_pages.row(left,pagination,right)
                bot.send_message(message.chat.id,a[data['page']-1], reply_markup=markup_pages,parse_mode="HTML")
        else:
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль",reply_markup=buttons.chooserole_markup)
    
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[1] == 'inlinelist')
    def chose_group_executor(call):
        cmd = call.data.split('_')[0]
        a = db.get_tasks_user(call.message.chat.id)
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            all_pages = data['all_pages']
            cur_page = data['page']
            if cmd == 'right':
                if data['page'] + 1 <= data['all_pages']:
                    data['page']+=1
                    pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelist')
                    send = types.InlineKeyboardButton('Сдать',callback_data='send_inlinelist')
                    right = types.InlineKeyboardButton('->',callback_data='right_inlinelist')
                    left = types.InlineKeyboardButton('<-',callback_data='left_inlinelist')
                    markup_pages = types.InlineKeyboardMarkup()
                    markup_pages.row(send)
                    markup_pages.row(left,pagination,right)
                    bot.edit_message_text(a[data['page']-1]['string'], reply_markup = markup_pages, chat_id=call.message.chat.id, message_id=call.message.message_id,parse_mode="HTML")
            elif cmd == 'left':
                if data['page'] - 1 > 0:
                    data['page'] -= 1
                    pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelist')
                    send = types.InlineKeyboardButton('Сдать',callback_data='send_inlinelist')
                    right = types.InlineKeyboardButton('->',callback_data='right_inlinelist')
                    left = types.InlineKeyboardButton('<-',callback_data='left_inlinelist')
                    markup_pages = types.InlineKeyboardMarkup()
                    markup_pages.row(send)
                    markup_pages.row(left,pagination,right)
                    bot.edit_message_text(a[data['page']-1]['string'], reply_markup = markup_pages, chat_id=call.message.chat.id, message_id=call.message.message_id,parse_mode="HTML")
            elif cmd == 'send':
                bot.set_state(call.from_user.id, states.Tasks.createreview)
                bot.send_message(call.message.chat.id,"Введите отчёт.\n" 
                    "Отчёт должен содержать:\n" 
                    "1. Здачу\n"
                    "2. Цель\n"
                    "3. Процесс выполнения\n"
                    "4. Итог\n")
                page = int(data['page'])-1
                data['cur_task_id'] = a[page]['task_id']
            elif data['all_pages'] == 0:
                bot.send_message(call.message.chat.id,'У вас нет активных заданий',reply_markup=buttons.zadruk_markup)
                bot.set_state(call.from_user.id, states.Tasks.choseactionmember)
        
    @bot.message_handler(state= states.Tasks.createreview)
    def vlxijvbf(message):
            with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
                    task = data['cur_task_id']
                    db.send_review(task, message.text)
                    bot.send_message(message.chat.id,'Вы успешно сдали отчет',reply_markup=buttons.zadruk_markup)
                    bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
                    
    
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'executortasks')
    def chose_group_executor(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
        bot.set_state(call.from_user.id, states.Tasks.name)
        bot.send_message(call.message.chat.id,"Введите имя таска")
        
    @bot.message_handler(state= states.Tasks.name)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['task_name'] = message.text
        bot.set_state(message.from_user.id, states.Tasks.description)
        bot.send_message(message.chat.id,"Введите описание")
        
    @bot.message_handler(state= states.Tasks.description)
    def chose_executor_reaction(message):
        data_task = {}
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data_task['task_description'] = message.text
            data_task['task_name'] = data['task_name']
            data_task['task_group'] = data['group_id']
            data_task['user_id'] = message.chat.id
            data['full_dict'] = data_task
        # db.add_task_user(data_task)
        string = ''
        for key,item in data_task.items():
            string += str(key) + "=" + str(item) + "\n"
        bot.send_message(message.chat.id,string,reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
        
    @bot.message_handler(state= states.Tasks.wait)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data_parse = data['full_dict']
        if message.text == "Сохранить":
            db.add_task_user(data_parse)
            bot.send_message(message.chat.id,'Вы успешно добавили таск',reply_markup=buttons.zadruk_markup)
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
        elif message.text == "Изменить":
            bot.set_state(message.from_user.id, states.Tasks.choosechange)
            bot.send_message(message.chat.id,'Выберите куда хотите внести изменения',reply_markup=buttons.changing_markup)
        else:
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.zadruk_markup)
            
            
            
    @bot.message_handler(state= states.Tasks.choosechange)
    def chose_executor_reaction(message):
        if message.text == "Название":
            bot.set_state(message.from_user.id, states.Tasks.changename)
            bot.send_message(message.chat.id,'Введите новое имя',reply_markup=None)
            
        else:
            bot.set_state(message.from_user.id, states.Tasks.changedesc)
            bot.send_message(message.chat.id,'Введите новое описание',reply_markup=None)
            
    @bot.message_handler(state= states.Tasks.changename)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['full_dict']['task_name'] = message.text
        bot.send_message(message.chat.id,"Выберите действие",reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
        
            
    @bot.message_handler(state= states.Tasks.changedesc)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['full_dict']['task_description'] = message.text
        bot.send_message(message.chat.id,"Выберите действие",reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
            
    
        
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

