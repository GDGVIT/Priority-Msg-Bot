import os
import time
import requests
import logging
from dotenv import load_dotenv

# Import utility classes
from utils.bot2 import TeleBot


# Configure logger
logging.basicConfig(level=logging.INFO)

logging.info("Loading the application")

#TOKENS
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
parser_url = os.getenv('PARSER_URL')
encryption_key = os.getenv('ENCRYPTION_KEY')



# Waking up the server
resp = requests.get(parser_url[:-11])
logging.info("NLU Engine Status : {}".format(resp.content))

#Initializing instance of the bot
argos = TeleBot(bot_token, parser_url)
argos.activate()
