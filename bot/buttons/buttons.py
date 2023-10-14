import telebot
from telebot import types
chooseactioon_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

sozdatgr_1 = types.KeyboardButton('Создать группу')
mygroups_1 = types.KeyboardButton('Мои группы')
chooseactioon_markup.add(sozdatgr_1, mygroups_1)

chooserole_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

rukovoditel_2 = types.KeyboardButton('Я руководитель')
rabotnik_2 = types.KeyboardButton('Я работник')
chooserole_markup.add(rukovoditel_2, rabotnik_2)
