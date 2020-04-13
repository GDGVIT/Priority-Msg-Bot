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

        # Track time to avoid deadlock
        self.start = time.monotonic()
        
        # Tracker list to store event notification 
        self.tracker = []
        
        # Chat ID of the chat
        self.chat_id = None

        # Feedback request tracker
        self.fb_req_id = 0

        # Entity request tracker
        self.ent_req_id = 0
        
        # Pointer for item
        self.item_ptr = None

        # Current object
        self.event = None

        # Current requested event key
        self.event_key = None

        self.markup = self.gen_markup()

        #self.connection = self.get_connection()

        # if self.connection:
        #     logging.info("Successfully connected to the database")
        # else:
        #     logging.info("Failed to connect to the database")

        self.mutex = False
        
        

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
            self.chat_id = message.chat.id
            
            self.bot.reply_to(message, 'Bot is active and listening')
        
        @self.bot.message_handler(commands=['show'])
        def show_all_events(message):
            '''
            This function is shows all important messages

            Parameters:
            message (dictionary) : Message object returned by telegram

            Return:
            None
            '''


            self.chat_id = message.chat.id

            # logging.info("Long polling unread messages")
            # updates = self.bot.get_updates()

            # for update in updates:
            #     text = update.message.text
            #     if self.is_event_notification(text):
            #         event_type = self.extract_event(text)

            #         logging.info(event_type + " Detected")

            #         # Incase event type not found
            #         if event_type is None:
            #             event_type = 'Some event'
                    
            #         item = self.get_tracker_item(text, event_type)
            #         self.tracker.append(item)

            # Debugging mutex status
            self.mutex_status()

            # Overcome race condition
            cur = time.monotonic()

            if cur - self.start > 120:
                self.mutex = False

            if self.mutex is False:
                logging.info("Showing messages")

                # Lock the mutex
                self.mutex = True
                
                # Track time variable
                self.start = time.monotonic()

                # Clear state
                self.clear_state()

                # Set chat id
                self.chat_id = message.chat.id
                
                # Retrive records
                select_query = "SELECT * FROM tracker where chat_id="+str(self.chat_id)+";"

                connection = self.get_connection()

                # Acquire cursor
                cursor = connection.cursor()
                
                # Execute query
                cursor.execute(select_query)
                records = cursor.fetchall()

                cursor.close()
                connection.close()
                
                for row in records:
                    #Populate tracker list

                    item = self.get_tracker_item(row)
                    self.tracker.append(item)

                self.item_ptr = 0
                self.show_one_event()

            
            else:
                self.bot.reply_to(message, 'Bot is currently busy, try again in a minute')
            

        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):

            logging.info("Being replied to : {}".format(self.ent_req_id))

            if message.reply_to_message is None:
                if self.is_event_notification(message.text):
                    event_type = self.extract_event(message.text)
                    
                    logging.info("Event detected")

                    #Incase event not found
                    if event_type is None:
                        event_type = 'some event'
                    
                    connection = self.get_connection()

                    cursor = connection.cursor()
                    
                    try:
                        if cursor:
                            logging.info("Cursor opened")
                        
                        

                            # Insert the message into postgres
                            insert_query = """INSERT INTO tracker (chat_id, message, event_type) VALUES (%s,%s, %s);"""
                            record_to_insert = (message.chat.id, message.text, event_type)

                            cursor.execute(insert_query, record_to_insert)

                            #Commit the insert
                            connection.commit()

                            #Close the cursor
                            cursor.close()
                            connection.close()
                            logging.info("Cursor closed")

                        else:
                            raise Exception('Cursor could not be opened')

                    except (Exception, psycopg2.Error) as error:
                            logging.info(error)                    
                    
            

            elif message.reply_to_message.message_id == self.ent_req_id:

                logging.info("Form action in progress")

                

                #Make request to backend
                body = json.dumps({'text': message.text})

                response = requests.post(self.parser_url, body)

                response = response.json()

                if len(response['entities']) > 0:
                    for event in response['entities']:

                        #Validate the value later
                        self.event.add_event_detail(event['entity'], event['value'])
                
                elif self.event_key == 'description':
                    self.event.add_event_detail('description', message.text)
                
                question = self.entity_to_request()

                sent_message = self.bot.send_message(self.chat_id, question, parse_mode="Markdown")

                self.ent_req_id = sent_message.message_id


                if self.event.is_details_complete():
                    if self.item_ptr < len(self.tracker)-1:
                        self.item_ptr+=1
                        self.show_one_event()
                    
                    elif self.item_ptr == (len(self.tracker)-1):
                        self.release_bot()
                        
          
        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)
    
    def mutex_status(self):
        if self.mutex:
            logging.info("CS Locked")
        else:
            logging.info("CS Open")

    def get_connection(self):

        try:
            connection = psycopg2.connect(
               os.environ['DATABASE_URL'],
                sslmode = 'require'
            )

            return connection
        
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
    
    def process_feedback(self,positive):
        '''
        This function processes feedback given for events
        '''

        logging.info("Processing feedback")
        if positive is True:

            logging.info("Feedback is positive")
            #Create event object and start form action
            self.event = Event(self.tracker[self.item_ptr]['event_type'])
            
            
            question = self.entity_to_request()

            sent_message = self.bot.send_message(self.chat_id, question)

            self.ent_req_id = sent_message.message_id

        else:

            logging.info("Feedback is negative")
            # Update pointer and show another item

            if self.item_ptr < len(self.tracker)-1:
                logging.info("Events remaining")
                self.item_ptr+=1
                self.show_one_event()
            
            elif self.item_ptr == (len(self.tracker)-1):
               self.release_bot()

    def release_bot(self):
        '''
        This function sends the last message that tracker is empty
        '''
        # Clear the tracker
        self.tracker = []

        # Clear tracked messages
        delete_query = "DELETE FROM tracker where chat_id="+str(self.chat_id)+";"
        
        connection = self.get_connection()

        # Execute
        cursor = sconnection.cursor()
        try:
            cursor.execute(delete_query)
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
        
        # Commit changes
        connection.commit()
        cursor.close()
        connection.close()

        logging.info("Cleared tracked messages")

        #Release lock
        self.mutex = False
        self.bot.send_message(self.chat_id, 'You are all caught up :)')

    def gen_markup(self):
        logging.info("Markup being generated")
        markup = types.InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
                    types.InlineKeyboardButton("No", callback_data="cb_no"))
        
        return markup
    
    def entity_to_request(self):
        '''
        This function finds out the entity to be collected in event object
        Parameters:
        None
        Return:
        None
        '''

        event_key = self.event.get_missing_detail()


        if event_key is not None:
            question = 'Please enter event '+event_key
            self.event_key = event_key
        else:
            event_details = self.event.get_event_details()
            question = 'The details are \n'
            for event_key in event_details:
                question+='\n '+'*'+event_key+'*'+' : '+event_details[event_key]
            question+='\n Stored sucessfully!'

            
            connection = self.get_connection()
            cursor = connection.cursor()

            try:
                
                if cursor:
                    logging.info("Cursor Opened")
                
                    # Storing the event to database
                    insert_query = """INSERT INTO events (chat_id, type, description, date, time) VALUES (%s, %s, %s, %s, %s);"""

                    record_to_insert = tuple([event_details[key] for key in event_details])
                    record_to_insert = (self.chat_id, )+record_to_insert


                    cursor.execute(insert_query, record_to_insert)

                    # Commit
                    connection.commit()

                else: 
                    raise Exception("Cursor could not be opened")
            
            except (Exception,psycopg2.Error) as error:
                logging.info(error)

            finally:
                # Close the cursor
                cursor.close()
                connection.close()
                logging.info("Cursor closed")
        

        return question

    def clear_state(self):
        '''
        This function clears the state of bot
        '''

        print("State being wiped")

        self.tracker = []
        self.chat_id = None
        self.fb_req_id = None
        self.ent_req_id = None
        self.item_ptr = None
        self.event = None
    
        
    def show_one_event(self):
        '''
        This function displays an event being tracked

        Parameters:
        None
        Return:
        None
        '''
        
        if (self.item_ptr < len(self.tracker)):
            text = self.tracker[self.item_ptr]['event_type']+' detected \n'
            text+= '_'+self.tracker[self.item_ptr]['text']+'_'+'\n'

            text+='Store this?'

            # #Inline keyboard
            # markup = types.ReplyKeyboardMarkup()
            # btn1 = types.KeyboardButton('Yes')
            # btn2 = types.KeyboardButton('No')
            # markup.add(btn1,btn2)

            # #print('Markup complete')
            # sent_message = self.bot.send_message(self.chat_id, text,
            #             reply_markup=markup, parse_mode="Markdown")

            self.bot.send_message(self.chat_id, text,reply_markup=self.markup)

            # Tracking feedback request ID

            self.fb_req_id = sent_message.message_id

        else:
            self.bot.send_message(self.chat_id, 'No important messages were detected')



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

        if response['intent']['name'] == 'event_notification':
            return True
        
        return False
    
    def get_tracker_item(self, row):
        '''
        This function adds a message to the conversation tracker

        Parameters:
        message (dictionary) : The message object returned by telegram

        Returns:
        dictionary : The item to be added to tracker
        '''
      
        item = {
            'id': row[0],
            'chat_id': row[1],
            'text': row[2],
            'event_type':row[3]
        }

        return item

