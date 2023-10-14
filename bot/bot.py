import telebot
from states.states import MyGroups


bot = telebot.TeleBot('6652605107:AAFLxE_GAkvr-HC4AKW3h_WotvYYiOBrSdk')

def main():
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "Добро пожаловать в Taskmatic!\n"
                         "Этот бот поможет вам удобно управлять задачами и быстро распределять их среди участников групп. Выберите действие",
                         reply_markup=None)

    bot.infinity_polling()
if __name__ == "__main__":
    main()

