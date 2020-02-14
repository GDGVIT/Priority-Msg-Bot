import telebot
import time

bot_token = '1006827845:AAGhqvI__6q7BYGOUwlKYLHlLpXaO-SoUYI'

bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Welcome')

@bot.message_handler(func = lambda message: test_function(message))
def echo_all(message):
    bot.reply_to(message, message.text)

while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)