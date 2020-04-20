def my_gen():
    size = 5

    index = 0

    while index < size:
        yield(index)
        index+=1


index = my_gen()

while True:
    try:
        print(next(index))
    except StopIteration:
        break
