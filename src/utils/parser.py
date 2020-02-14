import spacy
import en_core_web_sm
import re
nlp = en_core_web_sm.load()

'''
Parser functions are defined below
'''

def time_parser(ents):
    return [ent for ent in ents if ent.label_ == 'TIME']

def date_parser(ents):
    return [ent for ent in ents if ent.label_ == 'DATE']

def location_parser(message):
    
    
    places_list = ['SJT','TT','SMV'] #List of possible location meetings

    tokens = [str(token) for token in nlp.tokenizer(message)]

    location = (None, None) #Workaround for unbound local variable
    location_found = False
    
    for place in places_list:
        for index in range(len(tokens)):
            if place == tokens[index]:
                location_found = True
                location = (index, tokens[index])

                if(re.search(r'\d\d\d|\w\d\d', tokens[location[0]+1])):
                    new_location = location[1]+' '+tokens[location[0]+1]
                    location = (location[0], new_location)

    if location_found:
        return location
    else:
        return None, None

def extract_information(message):
    message = ' '.join([str(token).upper() for token in nlp.tokenizer(message)])


    ents = nlp(message).ents

    time = time_parser(ents)[0] if len(time_parser(ents))>0 else None 

    date = date_parser(ents)[0] if len(date_parser(ents))>0 else None

    location = location_parser(message)[1] 

    return {
        'time': time,
        'date': date,
        'location': location
    }



