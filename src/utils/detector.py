def identify(text):
    keywords = ['meeting', 'party']
    for keyword in keywords:
        if keyword in text:
            return True
    return False
