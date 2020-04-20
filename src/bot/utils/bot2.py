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
            
    def generate_brick(self):
        '''
        This function generates a dictionary 
        '''
        
        brick = {}

        for key in ['event', 'req_id', 'generate_event', 'tracker']:
            brick[key] = None
        
        return brick
                  
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