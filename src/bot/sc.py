import os
import time
import logging
import schedule
import telebot
import psycopg2
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv

# Import utility class
from utils.goblin import Goblin

class TeleBot:
    '''
    This is the class which initializes a telegram bot
    '''

    def __init__(self, bot_token, encryption_key):
        '''
        The constructor for TeleBot class

        Parameters:
        bot_token (string) : The secret token for Telegram bot
        encryption_key (string) : Key for encryption

        Returns:
        None
        ''' 
        # Initialize bot
        self.bot = telebot.TeleBot(token=bot_token, threaded=True)
        
        # Initialize Goblin
        self.goblin = Goblin(bytes(encryption_key, encoding='utf-8'))
        logging.info("Goblin initialized")

    def get_connection(self):
        '''
        This function return a connection to the database
        Parameters:
        None
        Return:
        None
        '''

        try:
            connection = psycopg2.connect(
               os.environ['DATABASE_URL'],
                sslmode = 'require'
            )

            return connection
        
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
            return None
    
    def scheduled_send():
        '''
        This function send scheduled reminders
        Parameters:
        None
        Return:
        None
        '''
        pass
    
    def send_message(self, text):
        self.bot.send_message(-438751679, text)

def job():
    print("Hey mofo")




if __name__ == "__main__":

    # Configure logger
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading the application")

    #TOKENS
    load_dotenv()

    bot_token = os.getenv('BOT_TOKEN')
    encryption_key = os.getenv('ENCRYPTION_KEY')


    bot = TeleBot(bot_token, encryption_key)

    bot.send_message("Hey")

    schedule.every().minute.at(":10").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)  



