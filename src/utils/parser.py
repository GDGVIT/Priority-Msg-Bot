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
    
    for place in places_list:
        for index in range(len(tokens)):
            if place == tokens[index]:
                location = (index, tokens[index])

    if(re.search(r'\d\d\d|\w\d\d', tokens[location[0]+1])):
        new_location = location[1]+' '+tokens[location[0]+1]
        location = (location[0], new_location)
    return location

def extract_information(message):
    message = ' '.join([str(token).upper() for token in nlp.tokenizer(message)])


    ents = nlp(message).ents

    time = time_parser(ents)[0]

    date = date_parser(ents)[0]

    location = location_parser(message)[1]

    return {
        'time': time,
        'date': date,
        'location': location
    }



