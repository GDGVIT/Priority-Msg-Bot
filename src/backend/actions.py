# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


#This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

class EventDetails(FormAction):
    '''
    This is the form action class for extracting event details
    '''

    def name(self):
        '''
        Unique identifier of the form
        '''
        return "event_details_form"
    
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        '''
        A list of required slots that the form has to fill
        '''

        return ["event", "date", "time"]

    # def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
    #     """A dictionary to map required slots to
    #     - an extracted entity
    #     - intent: value pairs
    #     - a whole message
    #     or a list of them, where a first match will be picked"""
    #     intent_list = ["event_notification","inform_event","inform_time","inform_date","inform_standard_date"]
    #     return {
    #         "event": self.from_entity(entity='event', intent=intent_list),
    #         "date":  self.from_entity(entity='date', intent=intent_list),
    #         "time":  self.from_entity(entity='time', intent=intent_list)
    #     }

    # def validate(self, dispatcher, tracker, domain):
    #     try:
    #         return super().validate(dispatcher, tracker, domain)
    #     except ActionExecutionRejection as e:
    #         # could not extract entity
    #         dispatcher.utter_message(
    #             "Sorry, I could not parse the value correctly. \n"
    #             "Please double check your entry otherwise I will ask you this forever"
    #         )
    #     return []

    def submit(self,
     dispatcher: CollectingDispatcher,
     tracker: Tracker,
     domain: Dict[Text, Any],) -> List[Dict]:
        '''
        Define what the form has to do after all slots are filled
        '''
        print('This invoked')
        #utter show slots template
        dispatcher.utter_message(template='utter_show_slots')

        return []



class AcrtionEventSubmission(Action):

    def name(self) -> Text:
        return "action_event_submission"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('CustomAction called')

        event = tracker.get_slot("event")

        date = tracker.get_slot("event")

        time = tracker.get_slot("time")

        message = "The event has been added to your calendar"

        dispatcher.utter_message(text=message)

        return [SlotSet("event", None),SlotSet("date",None),SlotSet("time", None)]

