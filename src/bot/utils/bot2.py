import time
import telebot
import json
import re
import os
import time
import requests
import psycopg2
import logging
from telebot import types

# Import utility class
from utils.event import Event

class TeleBot: 
    '''
    This is the class which initializes a telegram bot
    '''

    def __init__(self, bot_token, parser_url):
        '''
        The constructor for TeleBot class

        Parameters:
        bot_token (string) : The secret token for Telegram bot
        parser_url (string) : The API endpoint for calling Rasa

        Returns:
        None
        '''

        # Initialize bot
        self.bot = telebot.TeleBot(token=bot_token, threaded=False)
        
        # Rasa API endpoint
        self.parser_url = parser_url
        logging.info("URL parser set : {}".format(self.parser_url))

        self.markup = self.gen_markup()
    
    def activate(self):
        '''
        This function activates the bot and listens to messages

        Parameters:
        None

        Returns:
        None
        '''       
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            logging.info("Callback triggered")
            if call.data == "cb_yes":
                #self.bot.answer_callback_query(call.id, "Answer is Yes")
                self.process_feedback(True)
            elif call.data == "cb_no":
                #self.bot.answer_callback_query(call.id, "Answer is No")
                self.process_feedback(False)

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            '''
            This function is used to test if bot is active

            Parameters:
            message (dictionary) : Message object returned by telegram

            Return:
            None
            '''
            
            self.bot.reply_to(message, 'Bot is active and listening')

        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)  
    
    def store_message(self, chat_id, message):
        '''
        This function stores a message in database
        Parameters:
        chat_id (int): Chat ID of the telegram group
        message (string): The message to be stored
        Return:
        None
        '''
    
    def show_event(self, chat_id):
        '''
        This function returns an event being tracked
        Parameters:
        chat_id (int) : The Chat ID of a telegram group
        Return:
        string : The message to be returned
        '''
        message = ""
        try: 
            message = next(bricks[chat_id][generate_event])
        except StopAsyncIteration:
            message = "You are all caught up :)"
        finally:
            return message
        
    def generate_brick(self):
        '''
        This function generates a dictionary 
        '''

        brick = {}

        for key in ['event', 'req_id', 'generate_event', 'tracker']:
            brick[key] = None
        
        return brick
    
    def event_generator(self, tracker):
        '''
        This function is a generator which yields tracked messages
        Parameters:
        tracker (list) : List of messages being tracke
        Return:
        None
        '''

        for message in tracker:
            yield(message)
                  
    def gen_markup(self):
        '''
        This function generates markup for inline keyboard
        Parameters:
        None
        Return:
        None
        '''
        logging.info("Markup being generated")
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
                    types.InlineKeyboardButton("No", callback_data="cb_no"))
        
        return markup

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
    
    def retrieve_tracker(self, chat_id):
        '''
        This function retrieves the tracked messages from database
        Parameters:
        chat_id (int) : Chat ID of telegram group
        Return:
        list : A list of tracked messages from database
        '''

        tracker = []

        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            select_query = "SELECT * FROM tracker WHERE chat_id="+str(chat_id)

            cursor.execute(select_query)

            records = cursor.fetchall()

            cursor.close()
            connection.close()

            else:
                for row in records:
                    item = self.get_tracker_item(row)
                    tracker.append(item)
        
        except Exception as error:
            logging.info(error)
        
        finally:
            return tracker

    def get_tracker_item(self, message):
        '''
        This function generates the item stored in tracker
        Parameters:
        message (string): The message to be processed
        Return:
        dictionary: The item to be added to tracker
        '''

        item = {
            'id':row[0],
            'chat_id':row[1],
            'text':row[2],
            'event_type':row[3]
        }

        return item
