import os
import time
import requests
import logging
from dotenv import load_dotenv

# Import utility classes
from utils.bot import TeleBot 
from utils.brick import Brick 

# Configure logger
logging.basicConfig(level=logging.INFO)