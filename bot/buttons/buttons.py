import telebot
from telebot import types
choosepoint_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
sozdatgr_1 = types.KeyboardButton('Группы')
mygroups_1 = types.KeyboardButton('Задания')
chooseactioon_markup.add(sozdatgr_1, mygroups_1)

chooserole_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопок "Мои группы", "Создать группу", "Задания"
rukovoditel_2 = types.KeyboardButton('Я руководитель')
uchastnik_2 = types.KeyboardButton('Я участник')
zhopa_2 = types.KeyboardButton('Назад')
chooserole_markup.add(rukovoditel_2, uchastnik_2, zhopa_2)

chooseaction_markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #это надо после кнопки "Группы"
actgr1 = types.KeyboardButton('Мои группы')
actgr2 = types.KeyboardButton('Создать группу')
chooseaction_markup.add(actgr1, actgr2)

chooserole_markup.add(rukovoditel_2, rabotnik_2)


