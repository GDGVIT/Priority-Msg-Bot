from bot.tele_bot import TeleBot 

#Bot Token
bot_token = '1006827845:AAGhqvI__6q7BYGOUwlKYLHlLpXaO-SoUYI'

#Initialize Argos
argos = TeleBot(bot_token=bot_token)

#Activate the bot
argos.activate()