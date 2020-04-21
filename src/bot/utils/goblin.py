class Goblin:
  '''
  This is a class used to for message encryption
  Cuz no maniac would store personal messages in a database
  '''

  def __init__(self, key):
    '''
    This is the constructor function for Goblin class
    '''
    self.f = Fernet(key)
  
  def encrypt(self, text):
    '''
    This function returns encrypted text
    Parameters:
    text (string): The message to encrypt
    Return:
    string: Encrypted message
    '''
    enc_string = None
    try:
      byte_stream = bytes(text, encoding='utf-8')
      enc_stream = self.f.encrypt(byte_stream)
      enc_string = enc_stream.decode('utf-8')
    except Exception as error:
      print(error)
    finally:
      return enc_string
  
  def decrypt(self, enc_string):
    '''
    This function returns decrypted text
    Parameters:
    text (string): The message to decrypt
    Return:
    string : The decrypted message
    '''
    dec_string = None
    try:
      enc_stream = bytes(enc_string, encoding='utf-8')
      dec_string = self.f.decrypt(enc_stream).decode('utf-8')
    except Exception as error:
      print(error)
    finally:
      return dec_string
