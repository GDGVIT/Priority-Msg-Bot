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
            'description':None,
            'date': None,
            'time':None,
        }

        self.req_entity = None
        
        self.valid = False
  

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
                self.req_entity = event_key
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

    def get_req_entity(self):
        '''
        This function returns the entity being currently processed

        Parameters:
        None
        Return:
        string : The entity being requested
        '''

        return self.req_entity

    def is_prev_req_complete(self):
        '''
        This function checks if the current entity being 
        processed has been collected
        Parameters:
        None
        Return:
        bool : Whether collected (True) or not (False)
        '''

        if self.req_entity is not None:
            if self.details[self.req_entity] is None:
                return False

        
        return True 
    
    def are_details_valid(self):
        '''
        This function returns if details are valid
        Parameters:
        None
        Return:
        bool : True if valid else False
        '''

        return self.valid
    
    def make_valid(self):
        '''
        This function sets valid to True
        Parameters:
        None
        Return:
        None
        '''
        self.valid = True