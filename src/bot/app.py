import os
import time
import requests
import logging
from fastai.text import *
from dotenv import load_dotenv

# Import utility classes
from utils.bot import TeleBot


# Configure logger
logging.basicConfig(level=logging.INFO)

logging.info("Loading the application")

#TOKENS
load_dotenv()

parser_url = os.getenv('PARSER_URL')
encryption_key = os.getenv('ENCRYPTION_KEY')

model = load_learner('./models/')

#Initializing instance of the bot
argos = TeleBot(bot_token, model, encryption_key)
argos.activate()
