import requests
import json
import re
import telebot
from telebot import types
import os
import time
from dotenv import load_dotenv

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
        
        

    def activate(self):
        '''
        This function activates the bot and listens to messages

        Parameters:
        None

        Returns:
        None
        '''

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
            print('Showing messages')

            self.item_ptr = 0
            self.show_one_event()
            

        @self.bot.message_handler(func = lambda message : True)
        def track_messages(message):

            if message.reply_to_message is None:
                if self.is_event_notification(message.text):
                    event_type = self.extract_event(message.text)
                    
                    print('Event detected')

                    #Incase event not found
                    if event_type is None:
                        event_type = 'some event'

                    item = self.get_tracker_item(message,event_type)
                    self.tracker.append(item)

            elif message.reply_to_message.message_id == self.fb_req_id:

                if (message.text == 'Yes'):

                    print('Positive feedback')
                    #Create event object and start form action
                    self.event = Event(self.tracker[self.item_ptr]['event_type'])
                    
                    #Start collecting event details
                    # Get missing detail
                    
                    question = self.entity_to_request()

                    sent_message = self.bot.send_message(self.chat_id, question)

                    self.ent_req_id = sent_message.message_id

                else:

                    print('Negative feedback')
                    #Update pointer and show another item

                    if self.item_ptr < len(self.tracker)-1:
                        print('Events remaining')
                        self.item_ptr+=1
                        self.show_one_event()
                    
                    elif self.item_ptr == (len(self.tracker)-1):
                        print('All caught up')
                        # Clear the tracker
                        self.tracker = []
                        self.bot.send_message(self.chat_id, 'You are all caught up :)')
            
            elif message.reply_to_message.message_id == self.ent_req_id:

                print('Form action in progress')

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

            #Inline keyboard
            markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton('Yes')
            btn2 = types.KeyboardButton('No')
            markup.add(btn1,btn2)

            print('Markup complete')
            sent_message = self.bot.send_message(self.chat_id, text,
                        reply_markup=markup, parse_mode="Markdown")

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

        print('Event notification being checked')
        #Make request to backend
        body = json.dumps({"text":message_text})

        response = requests.post(self.parser_url, body)
        response = response.json()

        if response['intent']['name'] == 'event_notification':
            print('Its an event')
            print('Entities are:')
            print(response['entities'])
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


class Event:
    '''
    This is the event class
    '''

    def __init__(self, event_type):
        '''
        This is the constructor for the event class
        '''

        self.details = {
            #'name':None,
            'event_type':event_type,
            'date': None,
            'time':None
        }
        
  

    def is_details_complete(self):
        '''
        This function returns if all event details are completed or not

        Return:
        boolean : True if details are complete else False
        '''
        for entity in self.details:
            if self.details[entity] is None:
                return False
        return True

    def get_event_details(self):
        '''
        This function returns the event details

        Return:
        dictionary: The event details
        '''

        return self.details

    def get_missing_detail(self):
        '''
        This function returns the event detail which is missing
        
        Return:
        string: Name of event which is missing
        '''

        for event_key in self.details:
            if self.details[event_key] is None:
                return event_key
        return None     
    
    def add_event_detail(self, event_key, event_value):
        '''
        This function add an event detail to the event details dictionary

        Parameters:
        event_key (string) : Event detail name
        event_value (string) : Event detail value
        '''

        self.details[event_key] = event_value

#TOKENS
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
parser_url = os.getenv('PARSER_URL')

#Initializing instance of the bot
argos = TeleBot(bot_token, parser_url)
argos.activate()