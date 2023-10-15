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
    
    @bot.message_handler(commands=['jointogroup'])
    def join(message):
        if db.check_user(message.chat.id):
            bot.set_state(message.from_user.id, states.RandomStates.register, message.chat.id)
            bot.send_message(message.chat.id,"Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп.\n"
                         "Пожалуйста, введите свое имя для продолжения работы, а после снова вызовите")
        else:
            bot.send_message(message.chat.id, "Введите идентификатор группы🆔")
            bot.register_next_step_handler(message,join_to_group)
    def join_to_group(message):
        if db.join_group(message.text, message.chat.id):
            bot.send_message(message.chat.id, "Вы успешно добавились в группу✅")
        else:
            bot.send_message(message.chat.id, "Неверный идентефикатор группы")
    
    
    
    @bot.message_handler(commands=['start'])
    def check_register(message):
        if db.check_user(message.chat.id):
            bot.set_state(message.from_user.id, states.RandomStates.register, message.chat.id)
            bot.send_message(message.chat.id,"Добро пожаловать в Taskmatic!❤\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп.\n"
                         "\n"
                         "Вот инструкция по использованию бота!\n"
                         "1)/start – базовая команда, позволяющая запустить бот. Сначала Вам нужно будет пройти регистрацию, если она уже пройдена, команда позволит сразу перейти к выбору раздела\n"
                         "\n"
                         "2)/joingroup  - команда, с помощью которой Вы можете присоединяться к группе. Помните, что для присоединения Вам нужен ID группы! Его вы можете узнать у Вашего руководителя\n"
                         '\n'
                         "А теперь немного информации и работе с группами💬\n"
                         "Нажав на кнопку «Группы», Вы сможете выбрать раздел «Мои группы» или создать новую группу. В разделе «Мои группы» Вы сможете обозначить, руководитель Вы или участник. В зависимости от этого Вы сможете редактировать списки Ваших групп.\n"
                         "\n"  
                         "Помимо раздела «Группы» есть раздел «Задания». В нём Вы сможете сразу обозначить свою роль (руководитель или участник). Выбирая роль участника, у Вас будет возможность просмотреть список заданий, над которыми Вы работаете в данный момент, а также создать новое задание. Если же Вы выберете роль руководителя, то сможете просмотреть задания, над которыми работают участники Ваших групп.\n"
                         "\n"
                         "Надеемся, вам будет приятно работать с нашим ботом! Удачи!❤")
            bot.send_message(message.chat.id, "Пожалуйста, введите Ваше имя для продолжения работы💬")
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
            bot.send_message(message.chat.id,"Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников группы.📝\n"
                             "\n"
                             "Создайте группу, добавьте участников и побликуйте задачи, которые участники смогут выбрать и решить самостоятельно! Установите крайние даты решения, добавьте описание задач и работайте с другими функциями Taskmatic!❤\n",reply_markup=buttons.choosepoint_markup)
        
    @bot.message_handler(state=states.RandomStates.register)
    def register(message):
        a = "@" + message.from_user.username
        db.register_user(message.chat.id,message.text,a)
        bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
        bot.send_message(message.chat.id, "Выберите действие📔", reply_markup=buttons.choosepoint_markup)

    @bot.message_handler(state=states.RandomStates.start_work)
    def start_work(message):
        if message.text == 'Группы':
            bot.set_state(message.from_user.id, states.Groups.choosertype, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие📔",reply_markup=buttons.chooseaction_markup)
        else:
            bot.set_state(message.from_user.id, states.Tasks.choserole, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие📔",reply_markup=buttons.chooserole_markup)
        #таски
        
        
    @bot.message_handler(state=states.Groups.choosertype)
    def choosetype(message):
        if message.text == "Создать группу":
            bot.set_state(message.from_user.id, states.CreateGroup.entername)
            bot.send_message(message.chat.id, "Введите название группы💬")
        elif message.text == 'Мои группы':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль🎭",reply_markup=buttons.chooserole_markup)
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work, message.chat.id)
            bot.send_message(message.chat.id, "Выберите действие📔",reply_markup=buttons.choosepoint_markup)
            
    @bot.message_handler(state=states.Groups.chooserole)
    def choserole(message):
        if message.text == 'Я руководитель':
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            #добавить просмотр/редактировать
            bot.send_message(message.chat.id,"Выберите действие📔",reply_markup=buttons.yarukoblud_markup)
        elif message.text == 'Я участник':
            list_of_groups = db.get_executor_group(message.chat.id)
            if len(list_of_groups) == 0:
                bot.send_message(message.chat.id,'Вы не состоите ни в одной группе❌',reply_markup=buttons.chooserole_markup)
            else:
                inline_groups_markup = buttons.inline_get_list_executor(list_of_groups)
                bot.send_message(message.chat.id,'Выберите группу👥', reply_markup=inline_groups_markup)
            
            
        else:
            bot.set_state(message.from_user.id, states.Groups.choosertype)
            bot.send_message(message.chat.id, "Выберите действие📔",reply_markup=buttons.chooseaction_markup)
        #доделать

    @bot.message_handler(state=states.Groups.chooseactionadmin)
    def chooseactionadmin(message):
        if message.text == "Просмотр":
            grouplist = db.get_admin_groups(message.chat.id)
            if grouplist == 'You haven`t group':
                bot.send_message(message.chat.id,"У вас нет администрируемых групп",reply_markup=buttons.chooserole_markup)
                bot.set_state(message.from_user.id, states.Groups.chooserole)
            else:
                keylist_markup = buttons.inline_get_list(grouplist)
                bot.send_message(message.chat.id,"Ваши группы👥",reply_markup=keylist_markup)
        elif message.text == 'Назад':
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль🎭",reply_markup=buttons.chooserole_markup)
        else:
            grouplist = db.get_admin_groups(message.chat.id)
            if grouplist == 'You haven`t group':
                bot.send_message(message.chat.id,"У вас нет администрируемых групп",reply_markup=buttons.chooserole_markup)
                bot.set_state(message.from_user.id, states.Groups.chooserole)
            else:
                grouplist = db.get_admin_groups(message.chat.id)
                keylist_markup = buttons.inline_get_list_edit(grouplist)
                bot.send_message(message.chat.id,"Выберите группу👥",reply_markup=keylist_markup)
            
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'adminedit')
    def get_group_info(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
        bot.set_state(call.from_user.id, states.Groups.edit)
        bot.send_message(call.message.chat.id,"Выберите действие📔",parse_mode='HTML',reply_markup=buttons.changegr_markup)
        
    
    @bot.message_handler(state=states.Groups.edit)
    def editGroup(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        if message.text == 'Удалить группу':
            db.delete_group(group_id)
            bot.send_message(message.chat.id, "Вы удалили группу✅")
        elif message.text == 'Удалить участника':
            bot.send_message(message.chat.id,'Введите никнейм участника в формате @username 🆔')
            bot.set_state(message.from_user.id, states.Groups.wait_username)
        else:
            bot.send_message(message.chat.id,"Выберите действие📔",reply_markup=buttons.yarukoblud_markup)
            bot.set_state(message.from_user.id, states.Groups.chooseactionadmin)
            
    @bot.message_handler(state=states.Groups.wait_username)
    def user_delete(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        rez = db.delete_member(message.text,group_id)
        if rez == 0:
            bot.send_message(message.chat.id,'Пользователь не найден❌')
        else:
            bot.send_message(message.chat.id,'Пользователь успешно удален✅')
            bot.set_state(message.from_user.id, states.Groups.edit)
            bot.send_message(message.chat.id,"Выберите действие📔",parse_mode='HTML',reply_markup=buttons.changegr_markup)
        
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'admin')
    def get_group_info(call):
        group_id = call.data.split('_')[1]
        text_group = db.info_groups(group_id)
        bot.send_message(call.message.chat.id,text_group,parse_mode='HTML',reply_markup=buttons.backup_markup)
        
        
        
    @bot.message_handler(state=states.CreateGroup.entername)
    def entername(message):
        if not db.check_doubled_name(message.chat.id,message.text):
            bot.send_message(message.chat.id,'У вас уже есть группа с таким названием, пожалуйста, придумайте новое❌')
        elif '_' in message.text:
            bot.send_message(message.chat.id,'Название группы не должно содержать специальных символов, пожалуйста введите название заново❌')
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
        bot.send_message(call.message.chat.id,"Выберите действие📔",reply_markup=buttons.uchastchange_markup)
        
    @bot.message_handler(state= states.RandomStates.chose_leave)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            group_id = data['group_id']
        if message.text == 'Выйти из группы❌':
            db.leave_group(group_id,message.chat.id)
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Вы успешно вышли из группы✅",reply_markup=buttons.chooserole_markup)
        else:
            bot.set_state(message.from_user.id, states.Groups.chooserole)
            bot.send_message(message.chat.id, "Выберите роль🎭",reply_markup=buttons.chooserole_markup)
    
    
    
    
    
    @bot.message_handler(state= states.Tasks.choserole)
    def chsrole(message):
        if message.text == 'Я участник':
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
            bot.send_message(message.chat.id, "Выберите роль📔",reply_markup=buttons.zadruk_markup)
        elif message.text == 'Я руководитель':
            bot.set_state(message.from_user.id, states.Tasks.choseactionadmin)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.zadruk_markup)
        else:
            bot.set_state(message.from_user.id, states.RandomStates.start_work)
            bot.send_message(message.chat.id, "Выберите действие",reply_markup=buttons.choosepoint_markup)
       
       
    @bot.message_handler(state= states.Tasks.choseactionadmin)  
    def hzhz(message):
        if message.text == 'Назад':
            bot.set_state(message.from_user.id, states.Tasks.choserole, message.chat.id)
            bot.send_message(message.chat.id, "Выберите роль📔", reply_markup=buttons.chooserole_markup)
        #     list_of_groups = db.get_executor_group(message.chat.id)
        #     if len(list_of_groups) == 0:
        #         bot.send_message(message.chat.id,'Вы не состоите не в одной группе',reply_markup=buttons.chooserole_markup)
        #     else:
        #         inline_groups_markup_tasks = buttons.inline_get_list_executor_tasks(list_of_groups)
        #         bot.send_message(message.chat.id,'Выберите группу:', reply_markup=inline_groups_markup_tasks)
        # elif message.text == 'Свободные':
        #     list_of_groups = db.get_executor_group(message.chat.id)
        #     if len(list_of_groups) == 0:
        #         bot.send_message(message.chat.id,'Вы не состоите не в одной группе',reply_markup=buttons.chooserole_markup)
        elif message.text == 'В процессе':
            
            list_of_groups = db.get_admin_groups(message.chat.id)
            if list_of_groups == 'You haven`t group':
                bot.send_message(message.chat.id,"У вас нет администрируемых групп",reply_markup=buttons.chooserole_markup)
                bot.set_state(message.from_user.id, states.Tasks.choserole)
            inline_groups_markup_tasks = buttons.inline_get_list_admin_process(list_of_groups)
            bot.send_message(message.chat.id,'Выберите группу:', reply_markup=inline_groups_markup_tasks)
        else:
            bot.send_message(message.chat.id,'Функция пока недоступна... Но в скором времени она обязательно появится!')
            
            
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'adminprocesstasks')
    def sajdnnc(call):
        group_id = call.data.split('_')[1]
        string = "Активные таски:\n"
        data = db.admin_in_processing(group_id)
        if len(data) == 0:
            string += "Отсутствуют"
            bot.send_message(call.message.chat.id,string)
            bot.set_state(call.from_user.id, states.Tasks.choseactionadmin)
            bot.send_message(call.message.chat.id, "Выберите действие",reply_markup=buttons.zadruk_markup)
        else:
            for i in data:
                string += f"    {i['Название задачи']} - {i['Пользователь']}\n"
            bot.send_message(call.message.chat.id,string)
            bot.set_state(call.from_user.id, states.Tasks.choseactionadmin)
            bot.send_message(call.message.chat.id, "Выберите действие",reply_markup=buttons.zadruk_markup)
         
         
    @bot.message_handler(state= states.Tasks.choseactionmember)
    def yahz(message):
        if message.text == 'Создать':
            list_of_groups = db.get_executor_group(message.chat.id)
            if len(list_of_groups) == 0:
                bot.send_message(message.chat.id,'Вы не состоите ни в одной группе❌',reply_markup=buttons.chooserole_markup)
            else:
                inline_groups_markup_tasks = buttons.inline_get_list_executor_tasks(list_of_groups)
                bot.send_message(message.chat.id,'Выберите группу👥', reply_markup=inline_groups_markup_tasks)
        elif message.text == 'Свободные':
            list_of_groups = db.get_executor_group(message.chat.id)
            if len(list_of_groups) == 0:
                bot.send_message(message.chat.id,'Вы не состоите ни в одной группе❌',reply_markup=buttons.chooserole_markup)
            else:
                inline_groups_markup_tasks = buttons.inline_get_list_executor_free_tasks(list_of_groups)
                bot.send_message(message.chat.id,'Выберите группу👥', reply_markup=inline_groups_markup_tasks)
        
        
    
        
        
        elif message.text == 'В процессе':
            a = db.get_tasks_user(message.chat.id)
            if len(a) == 0:
                bot.send_message(message.chat.id,"У вас нет активных задач",reply_markup=buttons.zadruk_markup)
            else:
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
                    bot.send_message(message.chat.id,a[data['page']-1]['string'], reply_markup=markup_pages,parse_mode="HTML")
        else:
            bot.set_state(message.from_user.id, states.Tasks.choserole)
            bot.send_message(message.chat.id, "Выберите роль🎭",reply_markup=buttons.chooserole_markup)
    
    
    
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'executorfreetasks')
    def chose_group_executor(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
            a = db.get_free_task(group_id)
            if len(a) != 0:
                data['all_pages'] = len(a)
                data['page'] = 1
                pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelistfree')
                settask = types.InlineKeyboardButton('взять',callback_data='settask_inlinelistfree')
                right = types.InlineKeyboardButton('->',callback_data='right_inlinelistfree')
                left = types.InlineKeyboardButton('<-',callback_data='left_inlinelistfree')
                markup_pages = types.InlineKeyboardMarkup()
                markup_pages.row(settask)
                markup_pages.row(left,pagination,right)
                bot.send_message(call.message.chat.id,a[data['page']-1]['string'], reply_markup=markup_pages,parse_mode="HTML")
            else:
                bot.send_message(call.message.chat.id,'В этой группе нет свободных заданий❌',reply_markup=buttons.zadruk_markup)
                bot.set_state(call.from_user.id, states.Tasks.choseactionmember)

    @bot.callback_query_handler(func=lambda call: call.data.split('_')[1] == 'inlinelistfree')
    def chose_group_executor(call):
        cmd = call.data.split('_')[0]
        
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            a = db.get_free_task(data['group_id'])
            print(a)
            all_pages = data['all_pages']
            cur_page = data['page']
            if cmd == 'right':
                if data['page'] + 1 <= data['all_pages']:
                    data['page']+=1
                    pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelistfree')
                    settask = types.InlineKeyboardButton('взять',callback_data='settask_inlinelistfree')
                    right = types.InlineKeyboardButton('->',callback_data='right_inlinelistfree')
                    left = types.InlineKeyboardButton('<-',callback_data='left_inlinelistfree')
                    markup_pages = types.InlineKeyboardMarkup()
                    markup_pages.row(settask)
                    markup_pages.row(left,pagination,right)
                    bot.edit_message_text(a[data['page']-1]['string'], reply_markup = markup_pages, chat_id=call.message.chat.id, message_id=call.message.message_id,parse_mode="HTML")
            elif cmd == 'left':
                if data['page'] - 1 > 0:
                    data['page'] -= 1
                    pagination = types.InlineKeyboardButton(f'{data["page"]}/{data["all_pages"]}',callback_data='send_inlinelistfree')
                    settask = types.InlineKeyboardButton('взять',callback_data='settask_inlinelistfree')
                    right = types.InlineKeyboardButton('->',callback_data='right_inlinelistfree')
                    left = types.InlineKeyboardButton('<-',callback_data='left_inlinelistfree')
                    markup_pages = types.InlineKeyboardMarkup()
                    markup_pages.row(settask)
                    markup_pages.row(left,pagination,right)
                    bot.edit_message_text(a[data['page']-1]['string'], reply_markup = markup_pages, chat_id=call.message.chat.id, message_id=call.message.message_id,parse_mode="HTML")
            elif cmd == 'settask':
                db.take_free_task(call.message.chat.id,a[data['page']-1]['task_id'])
                bot.send_message(call.message.chat.id,"Вы стали исполнителем задания✅")
            elif data['all_pages'] == 0:
                bot.send_message(call.message.chat.id,'У вас нет активных заданий❌',reply_markup=buttons.zadruk_markup)
                bot.set_state(call.from_user.id, states.Tasks.choseactionmember)
        
    
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
                bot.send_message(call.message.chat.id,"Введите отчёт📔.\n" 
                    "Отчёт должен содержать:\n" 
                    "1. Здачу\n"
                    "2. Цель\n"
                    "3. Процесс выполнения\n"
                    "4. Итог\n")
                page = int(data['page'])-1
                data['cur_task_id'] = a[page]['task_id']
            elif data['all_pages'] == 0:
                bot.send_message(call.message.chat.id,'У вас нет активных заданий❌',reply_markup=buttons.zadruk_markup)
                bot.set_state(call.from_user.id, states.Tasks.choseactionmember)
        
        
        
    
    @bot.message_handler(state= states.Tasks.createreview)
    def vlxijvbf(message):
            with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
                    task = data['cur_task_id']
                    db.send_review(task, message.text)
                    bot.send_message(message.chat.id,'Вы успешно сдали отчет✅',reply_markup=buttons.zadruk_markup)
                    bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
                    
    
    @bot.callback_query_handler(func=lambda call: call.data.split('_')[0] == 'executortasks')
    def chose_group_executor(call):
        group_id = call.data.split('_')[1]
        with bot.retrieve_data(call.from_user.id,call.message.chat.id) as data:
            data['group_id'] = group_id
        bot.set_state(call.from_user.id, states.Tasks.name)
        bot.send_message(call.message.chat.id,"Введите название задания💬")
        
    @bot.message_handler(state= states.Tasks.name)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['task_name'] = message.text
        bot.set_state(message.from_user.id, states.Tasks.description)
        bot.send_message(message.chat.id,"Введите описание задания💬")
        
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
        string = "Ваша задача:\n" + f"Имя - {data_task['task_name']}\n" + f"Описание - {data_task['task_description']}\n"
        bot.send_message(message.chat.id,string,reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
        
    @bot.message_handler(state= states.Tasks.wait)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data_parse = data['full_dict']
        if message.text == "Сохранить":
            db.add_task_user(data_parse)
            bot.send_message(message.chat.id,'Вы успешно добавили задание✅',reply_markup=buttons.zadruk_markup)
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
        elif message.text == "Изменить":
            bot.set_state(message.from_user.id, states.Tasks.choosechange)
            bot.send_message(message.chat.id,'Выберите, куда хотите внести изменения💬',reply_markup=buttons.changing_markup)
        else:
            bot.set_state(message.from_user.id, states.Tasks.choseactionmember)
            bot.send_message(message.chat.id, "Выберите действие📔",reply_markup=buttons.zadruk_markup)
            
            
            
    @bot.message_handler(state= states.Tasks.choosechange)
    def chose_executor_reaction(message):
        if message.text == "Название":
            bot.set_state(message.from_user.id, states.Tasks.changename)
            bot.send_message(message.chat.id,'Введите новое название💬',reply_markup=None)
            
        else:
            bot.set_state(message.from_user.id, states.Tasks.changedesc)
            bot.send_message(message.chat.id,'Введите новое описание💬',reply_markup=None)
            
    @bot.message_handler(state= states.Tasks.changename)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['full_dict']['task_name'] = message.text
        bot.send_message(message.chat.id,"Выберите действие📔",reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
        
            
    @bot.message_handler(state= states.Tasks.changedesc)
    def chose_executor_reaction(message):
        with bot.retrieve_data(message.from_user.id,message.chat.id) as data:
            data['full_dict']['task_description'] = message.text
        bot.send_message(message.chat.id,"Выберите действие📔",reply_markup=buttons.zadacha_markup)
        bot.set_state(message.from_user.id, states.Tasks.wait)
            
    
        
    
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
if __name__ == "__main__":
    main()

