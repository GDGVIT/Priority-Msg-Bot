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

        # Initialize a dictionary
        self.bricks = {}
    
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

        @self.bot.message_handler(commands=['show'])
        def show_messages(message):
            '''
            This function is used to test if bot is active

            Parameters:
            message (dictionary) : Message object returned by telegram

            Return:
            None
            '''
            
            self.bot.reply_to(message, 'Brb with your messages')

            # Allocate a brick to chat
            if message.chat.id not in self.bricks:

                try:
                    self.bricks[message.chat.id] = self.generate_brick()

                    # Populate the brick with relevant data

                    # Get tracked messages
                    tracker = self.retrieve_tracker(message.chat.id)
                    if len(tracker) == 0:
                        raise ValueError("Tracker is empty")
                  
                    self.bricks[message.chat.id]['tracker'] = tracker

                    # Get the generator object
                    gen_event = self.get_event_generator(tracker)
                    self.bricks[message.chat.id]['gen_event'] = gen_event

                    # List tracked events
                except ValueError as error:
                    logging.info(error)
                    self.bot.send_message(message.chat.id, "No imp messages were detected")
                

        
        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):

            if message.reply_to_message is None:
                if self.is_event_notification(message.text):

                    # Message is an event
                    # Store it!

                    logging.info("Event detected")
                    self.store_message(message)
            else:
                # Message is possibly a reponse to bot
                logging.info("Probably a response")
                
                # Check if a brick has been allocated to this chat
                # Note that a brick is only allocated when the bot
                # Is interacting , and after interaction 
                # The brick is destroyed
                if message.chat.id in self.bricks:
                    
                    # Check if reply is being given to correct query
                    condition = message.reply_to_message.message_id == self.bricks[message.chat.id]['req_id']

                    if condition :
                        # Check what was the entity being requested
                        

        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)  
    
    def store_message(self, message):
        '''
        This function stores a message in database
        Parameters:
        chat_id (int): Chat ID of the telegram group
        message (string): The message to be stored
        Return:
        None
        '''
        event_type = self.extract_event(message.text)

        if event_type is None:
            event_type = 'Some event'
        
        
        try: 
            connection = self.get_connection()
            cursor = connection.cursor()   

            # Insert the message into postgres
            insert_query = """INSERT INTO tracker (chat_id, message, event_type) VALUES (%s,%s, %s);"""
            # Encrypt here
            record_to_insert = (message.chat.id, message.text, event_type)

            cursor.execute(insert_query, record_to_insert)

            #Commit the insert
            connection.commit()

            #Close the cursor
            cursor.close()
            connection.close()
            logging.info("Cursor closed")

        except (Exception, psycopg2.Error) as error:
                logging.info(error)            

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

        for key in ['event', 'req_id', 'gen_event', 'tracker']:
            brick[key] = None
        
        return brick
    
    def get_event_generator(self, tracker):
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

            
            for row in records:
                item = self.get_tracker_item(row)
                tracker.append(item)
    
        except Exception as error:
            logging.info(error)
        
        finally:
            return tracker

    def get_tracker_item(self, row):
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

    def extract_event(self, message_text):
        '''
        This function extracts events from the message
        NER not able to parse the message

        Parameters:
        message_text (string) : The text message that was given

        Return:
        None
        '''

        events = ['Meeting', 'Party', 'DA', 'Exam', 'Assignement']

        for event in events:
            if re.search(event, message_text, re.IGNORECASE):
                return event
        return None
        
    def is_event_notification(self, message_text):
        '''
        This function checks if message is important or not
        Parameters:
        message_text (string) : The message from user
        Return:
        bool : True if message is important else False
        '''

        logging.info('Event notification being checked')
        #Make request to backend
        body = json.dumps({"text":message_text})

        response = requests.post(self.parser_url, body)
        response = response.json()

        cond1 = float(response['intent']['confidence']) >= 0.8
        cond2 = response['intent']['name'] == 'event_notification'
        if cond1 and cond2:
            return True