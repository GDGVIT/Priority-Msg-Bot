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

    
    def get_date_string(self, date_object):
        '''
        This function returns a string representation
        of a datetime object
        Parameters:
        date_object (datetime): The date extracted from message
        Return:
        string : Date in form "dd/mm/yyyy"
        '''

        date_string = str(date_object.year) + '-'
        date_string += str(date_object.month) + '-'
        date_string += str(date_object.day)

        return date_string
    
    def scheduled_send(self):
        '''
        This function send scheduled reminders
        Parameters:
        None
        Return:
        None
        '''
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            cur_date = self.get_date_string(datetime.now())
            next_date = self.get_date_string(datetime.now() + timedelta(days=4)) 

            select_query = "SELECT * FROM events WHERE "
            select_query += " date between '"+cur_date+"' and '"+next_date+"' ;"
            
            logging.info("Querying from database")
            cursor.execute(select_query)

            records = cursor.fetchall()

            for row in records:
                # Decrypt messages here
                event_type = self.goblin.decrypt(row[2])
                event_desc = self.goblin.decrypt(row[3])
                date_string = self.get_date_string(row[4])

                text = event_type + " on *"+date_string+"* at *"+row[5]+"*\n"+"_"+event_desc+"_"
                self.bot.send_message(row[1],text,parse_mode="Markdown")
            
            cursor.close()
            connection.close()

        except Exception as error:
            logging.info(error)
        
        finally:
            print("finally")
            # Delete all expired reminders

def job():
    print("Hey mofo")




if __name__ == "__main__":

    # Configure logger
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading the application")

    #TOKENS
    load_dotenv()

    bot_token = os.getenv('REMINDER_BOT_TOKEN')
    encryption_key = os.getenv('ENCRYPTION_KEY')


    bot = TeleBot(bot_token, encryption_key)

    bot.scheduled_send()

    #schedule.every().minute.at(":10").do(job)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)  



