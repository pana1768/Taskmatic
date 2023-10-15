import telebot
from telebot import types
choosepoint_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
sozdatgr_1 = types.KeyboardButton('Группы')
mygroups_1 = types.KeyboardButton('Задания')
choosepoint_markup.add(sozdatgr_1, mygroups_1)

chooserole_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки"Задания"
rukovoditel_2 = types.KeyboardButton('Я руководитель')
uchastnik_2 = types.KeyboardButton('Я участник')
zhopa = types.KeyboardButton('Назад')
chooserole_markup.add(rukovoditel_2, uchastnik_2, zhopa)

chooseaction_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "Группы"
actgr1 = types.KeyboardButton('Мои группы')
actgr2 = types.KeyboardButton('Создать группу')
chooseaction_markup.add(actgr1, actgr2, zhopa)

zadacha_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо посое вывода задачи, составленной руководителем
okzad = types.KeyboardButton('Сохранить')
changezad = types.KeyboardButton('Изменить')
zadacha_markup.add(okzad, changezad, zhopa)

changing_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "изменить" для задачи
changename = types.KeyboardButton('Название')
changedis = types.KeyboardButton('Описание')
# changedd = types.KeyboardButton('Дедлайн')
changing_markup.add(changename, changedis, zhopa)

otchet_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после отправки отчета
yes = types.KeyboardButton('Принять')
no = types.KeyboardButton('Отклонить')
otchet_markup.add(yes, no, zhopa)

chesdelat_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после того, как мы выбираем одну из задач из списка задач
sdat = types.KeyboardButton('Сдать')
kspisku = types.KeyboardButton('К списку') #после этой кнопки предыдущее сообщение удаляется
chesdelat_markup.add(sdat, kspisku, zhopa) #эта жопа возвращает к списку задач

dlyagrupp_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это создание группы
dobavit = types.KeyboardButton('Добавить участника')
saving = types.KeyboardButton('Сохранить') #после этого пользователь возвращается на этап выбора "Группы" или "Задания"
dlyagrupp_markup.add(dobavit, saving, zhopa)

zadruk_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после кнопки "Я руководитель" в разделе "Задания"(!)
active = types.KeyboardButton('В процессе')
zadruk_markup.add(active, zhopa)

changegr_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это изменение группы
dp = types.KeyboardButton('Удалить участника')
dg = types.KeyboardButton('Удалить группу')
zhopa = types.KeyboardButton('Назад')
changegr_markup.add(dp, dg, zhopa)

yarukoblud_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после руководителя в группах
redact = types.KeyboardButton('Редактировать')
prosmotr = types.KeyboardButton('Просмотр')
yarukoblud_markup.add(redact, prosmotr, zhopa)

uchastchange_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после кнопки редактировать у руководителя в группах
exite = types.KeyboardButton('Выйти из группы')
uchastchange_markup.add(exite, zhopa)

areyousure_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после "Вы уверены, что хотите выйти из группы?"
yes1 = types.KeyboardButton('Да')
no1 = types.KeyboardButton('Нет') #после этого возвращается к списку групп
areyousure_markup.add(yes1, no1, zhopa)

sozdrab_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
sozdrab_markup.add(okzad, changezad)

chtomenyaemusebya_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
chtomenyaemusebya_markup.add(changename, changedis)
def inline_get_list(list_groups:list)->types.InlineKeyboardMarkup():
    for group in list_groups:
        group['role'] = 'admin'
    
    adminlistgroups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='admin_'+str(group['Group id']))
        adminlistgroups.add(but)
    return adminlistgroups

def inline_get_list_edit(list_groups:list)->types.InlineKeyboardMarkup():
    for group in list_groups:
        group['role'] = 'admiedit'
    adminlistgroups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='adminedit_'+str(group['Group id']))
        adminlistgroups.add(but)
    return adminlistgroups

def inline_get_list_executor(list_groups:list)->types.InlineKeyboardMarkup():
    list_of_groups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='executor_'+str(group['Group id']))
        list_of_groups.add(but)
    return list_of_groups

def inline_get_list_executor_tasks(list_groups:list)->types.InlineKeyboardMarkup():
    list_of_groups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='executortasks_'+str(group['Group id']))
        list_of_groups.add(but)
    return list_of_groups

def inline_get_list_executor_free_tasks(list_groups:list)->types.InlineKeyboardMarkup():
    list_of_groups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='executorfreetasks_'+str(group['Group id']))
        list_of_groups.add(but)
    return list_of_groups

def inline_get_list_admin_process(list_groups:list)->types.InlineKeyboardMarkup():
    list_of_groups = types.InlineKeyboardMarkup()
    for group in list_groups:
        but = types.InlineKeyboardButton(text = group['Group name'], callback_data='adminprocesstasks_'+str(group['Group id']))
        list_of_groups.add(but)
    return list_of_groups
backup_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
backup_markup.add(zhopa)