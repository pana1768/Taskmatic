import telebot
from telebot import types
choosepoint_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
sozdatgr_1 = types.KeyboardButton('Группы')
mygroups_1 = types.KeyboardButton('Задания')
choosepoint_markup.add(sozdatgr_1, mygroups_1)

chooserole_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопок "Мои группы", "Создать группу", "Задания"
rukovoditel_2 = types.KeyboardButton('Я руководитель')
uchastnik_2 = types.KeyboardButton('Я участник')
nazad_2 = types.KeyboardButton('Назад')
chooserole_markup.add(rukovoditel_2, uchastnik_2, zhopa_2)

chooseaction_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "Группы"
actgr1 = types.KeyboardButton('Мои группы')
actgr2 = types.KeyboardButton('Создать группу')
chooseaction_markup.add(actgr1, actgr2)

zadacha_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо посое вывода задачи, составленной руководителем
okzad = types.KeyboardButton('Сохранить')
changezad = types.KeyboardButton('Изменить')
zadacha_markup.add(okzad, changezad)

changing_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "изменить"
changename = types.KeyboardButton('Название')
changedis = types.KeyboardButton('Описание')
changedd = types.KeyboardButton('Дедлайн')
changing_markup.add(changename, changedis, changedd)

otchet_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после отправки отчета
yes = types.KeyboardButton('Принять')
no = types.KeyboardButton('Отклонить')
otchet_markup.add(yes, no)

chesdelat_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после того, как мы выбираем одну из задач из списка задач
sdat = types.KeyboardButton('Сдать')
kspisku = types.KeyboardButton('К списку') #после этой кнопки предыдущее сообщение удаляется
chesdelat_markup.add(sdat, kspisku)

dlyagrupp_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это создание группы
dobavit = types.KeyboardButton('Добавить участника')
saving = types.KeyboardButton('Сохранить') #после этого пользователь возвращается на этап выбора "Группы" или "Задания"
dlyagrupp_markup.add(dobavit, saving)

zadruk_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после кнопки "Я руководитель" в разделе "Задания"(!)
create = types.KeyboardButton('Создать')
free = types.KeyboardButton('Свободные')
active = types.KeyboardButton('В процессе')
zadruk_markup.add(create, free, active)



