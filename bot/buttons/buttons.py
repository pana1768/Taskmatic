import telebot
from telebot import types
choosepoint_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
sozdatgr_1 = types.KeyboardButton('Группы')
mygroups_1 = types.KeyboardButton('Задания')
choosepoint_markup.add(sozdatgr_1, mygroups_1)

chooserole_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки"Задания"
rukovoditel_2 = types.KeyboardButton('Я руководитель')
uchastnik_2 = types.KeyboardButton('Я участник')
zhopa_2 = types.KeyboardButton('Назад')
chooserole_markup.add(rukovoditel_2, uchastnik_2, zhopa_2)

chooseaction_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "Группы"
actgr1 = types.KeyboardButton('Мои группы')
actgr2 = types.KeyboardButton('Создать группу')
zhopa_2 = types.KeyboardButton('Назад')
chooseaction_markup.add(actgr1, actgr2,zhopa_2)

zadacha_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо посое вывода задачи, составленной руководителем
okzad = types.KeyboardButton('Сохранить')
changezad = types.KeyboardButton('Изменить')
zadacha_markup.add(okzad, changezad)

changing_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "изменить" для задачи
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

zadrab_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это после кнопки "Я участник" в разделе "Задания"
free1 = types.KeyboardButton('Свободные')
create1 = types.KeyboardButton('Создать свою')
active1 = types.KeyboardButton('В процессе')
zadrab_markup.add(free1, active1, create1)

changegr_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это изменение группы
dp = types.KeyboardButton('Удалить участника')
zhopa = types.KeyboardButton('Назад')
changegr_markup.add(dp, zhopa)

