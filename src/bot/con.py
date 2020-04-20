def get_event(tracker):
    
    for event in tracker:
        yield(event)


tracker = ['Hey','Fuck', 'Off']
index = get_event(tracker)
index2 = get_event(['hola','amigos'])

while True:
    try:
        print(next(index2))
        print(next(index))
    except StopIteration:
        print("That all folks")
        break

