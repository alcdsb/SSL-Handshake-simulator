import base64

def str64decode(s):
    '''Decode bytes array into an integer'''
    return int(base64.b64decode(s).decode('utf8'))

def str64encode(it):
    '''Encode a positive integer into a bytes array '''
    return base64.b64encode(str(it).encode('utf8'))

global BYTE_LENGTH # The max length for ord(byte)
BYTE_LENGTH = 3 

def intEncode(text):
    '''Encode a string into a list of postive integers, the argument "text" should be a string'''
    enText = ['1'] + [(BYTE_LENGTH - len(str(ord(i)))) * '0' + str(ord(i)) for i in text]

    return int(''.join(enText))

def intDecode(text):
    '''Decode a list of positve integers into a string, the argument "text" should be a list of integers'''
    deText = [chr(int(str(text)[i + 1:i + 1 + BYTE_LENGTH])) for i in range(0, len(str(text)) - BYTE_LENGTH, BYTE_LENGTH)]

    return ''.join(deText)