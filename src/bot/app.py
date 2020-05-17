import os
import time
import requests
import logging
import torch
import fastai
from fastai.text import *
from dotenv import load_dotenv

# Import utility classes
from utils.bot import TeleBot


# Configure logger
logging.basicConfig(level=logging.INFO)

logging.info("Loading the application")


#TOKENS
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
encryption_key = os.getenv('ENCRYPTION_KEY')

model = None

fastai.torch_core.default_device = torch.device('cpu')
model = load_learner('./models/')

if model is not None:
    #Initializing instance of the bot
    argos = TeleBot(bot_token, model, encryption_key)
    argos.activate()
else:
    exit()