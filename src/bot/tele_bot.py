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

        @self.bot.message_handler(func = lambda message: identify(message.text)) #Identify event in message
        def send_event_info(message):
            event_info = extract_information(message.text)
            reply_message = 'Event detected => '
            for ent in event_info:
                if event_info[ent]:
                    reply_message+=ent+' : '+str(event_info[ent])+' ;'
            
    
            self.bot.reply_to(message, reply_message)

        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)


