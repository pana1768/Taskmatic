import telebot
from telebot import types
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

sozdatgr_1 = types.KeyboardButton('Создать группу')
mygroups_1 = types.KeyboardButton('Мои группы')
markup.add(sozdatgr_markup, mygroups_markup)

markup = typesReplyKeyboardMarkup(resize_keyboard=True)

rukovoditel_2 = types.KeyboardButton('Я руководитель')
rabotnik_2 = types.KeyboardButton('Я работник')
markup.add(rukovoditel_2, rabotnik_2)
