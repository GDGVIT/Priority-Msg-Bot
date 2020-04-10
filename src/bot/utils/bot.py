import time
import telebot
import json
import re
import requests
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

            logging.info("Showing messages")

            self.item_ptr = 0
            self.show_one_event()
            

        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):

            if message.reply_to_message is None:
                if self.is_event_notification(message.text):
                    event_type = self.extract_event(message.text)
                    
                    logging.info("Event detected")

                    #Incase event not found
                    if event_type is None:
                        event_type = 'some event'

                    item = self.get_tracker_item(message,event_type)
                    self.tracker.append(item)
            
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
                
                question = self.entity_to_request()

                sent_message = self.bot.send_message(self.chat_id, question, parse_mode="Markdown")

                self.ent_req_id = sent_message.message_id


                if self.event.is_details_complete():
                    if self.item_ptr < len(self.tracker)-1:
                        self.item_ptr+=1
                        self.show_one_event()
                    
                    elif self.item_ptr == (len(self.tracker)-1):
                        
                        # Clear the tracker
                        self.tracker = []
                        self.bot.send_message(self.chat_id, 'You are all caught up :)')


          
        while True:
            try:
                self.bot.polling()
            except Exception:
                time.sleep(15)
    
    def process_feedback(self,positive):
        '''
        This function processes feedback given for events
        '''
        logging.info("Processing feedback")
        if positive is True:

            logging.info("Feedback is positive")
            #Create event object and start form action
            self.event = Event(self.tracker[self.item_ptr]['event_type'])
            
            #Start collecting event details
            # Get missing detail
            
            question = self.entity_to_request()

            sent_message = self.bot.send_message(self.chat_id, question)

            self.ent_req_id = sent_message.message_id

        else:

            logging.info("Feedback is negative")
            #Update pointer and show another item

            if self.item_ptr < len(self.tracker)-1:
                logging.info("Events remaining")
                self.item_ptr+=1
                self.show_one_event()
            
            elif self.item_ptr == (len(self.tracker)-1):
                logging.info("All caught up")
                # Clear the tracker
                self.tracker = []
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
        else:
            event_details = self.event.get_event_details()
            question = 'The details are \n'
            for event_key in event_details:
                question+='\n '+'*'+event_key+'*'+' : '+event_details[event_key]
            question+='\n Stored sucessfully!'
            
        return question

    
        
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
    
    def get_tracker_item(self, message, event_type):
        '''
        This function adds a message to the conversation tracker

        Parameters:
        message (dictionary) : The message object returned by telegram

        Returns:
        dictionary : The item to be added to tracker
        '''
      
        item = {
            'id': message.message_id,
            'text': message.text,
            'event_type':event_type
        }

        return item

