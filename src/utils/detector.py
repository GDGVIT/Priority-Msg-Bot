def identify(text):
    keywords = ['meeting', 'party']
    for word in text:
        if word in keywords:
            return True
    return False