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
changedd = types.KeyboardButton('Дедлайн')
changing_markup.add(changename, changedis, changedd, zhopa)

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
create = types.KeyboardButton('Создать')
free = types.KeyboardButton('Свободные')
active = types.KeyboardButton('В процессе')
zadruk_markup.add(create, free, active, zhopa)

zadrab_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после кнопки "Я участник" в разделе "Задания"
free1 = types.KeyboardButton('Свободные')
create1 = types.KeyboardButton('Создать свою')
active1 = types.KeyboardButton('В процессе')
zadrab_markup.add(free1, active1, create1, zhopa)

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