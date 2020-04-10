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
