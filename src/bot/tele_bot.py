import telebot
import time
from utils.parser import extract_information
from utils.detector import identify


class TeleBot():
    def __init__(self, bot_token):
        self.bot = telebot.TeleBot(token=bot_token)

    def activate(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, 'Welcome')

        @self.bot.message_handler(func = lambda message: identify(message.text))
        def echo_all(message):
            self.bot.reply_to(message, message.text)

        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)


