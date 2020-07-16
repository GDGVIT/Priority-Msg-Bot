import os
import logging
import spacy
import onnxruntime
from dotenv import load_dotenv

# Import utility classes
from core.bot import TeleBot


# Configure logger
logging.basicConfig(level=logging.INFO)

logging.info("Loading the application")


#TOKENS
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
encryption_key = os.getenv('ENCRYPTION_KEY')

if __name__ == "__main__":
    logging.info("Load Spacy model")
    nlp = spacy.load('en_core_web_sm')
    logging.info("Load onnx classifier")
    model = onnxruntime.InferenceSession("./models/message_classifier-192A.onnx")
    argos = TeleBot(bot_token, encryption_key, nlp, model)
    argos.activate()
else:
    exit()