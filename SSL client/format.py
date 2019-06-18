'''See documentation from SSL server, the crypto,  cryptomath, format, and rsa library used in client and server are the same'''

import base64

def str64decode(s):
    return int(base64.b64decode(s).decode('utf8'))

def str64encode(it):
    return base64.b64encode(str(it).encode('utf8'))

global BYTE_LENGTH
BYTE_LENGTH = 3

def intEncode(text):
    enText = ['1'] + [(BYTE_LENGTH - len(str(ord(i)))) * '0' + str(ord(i)) for i in text]

    return int(''.join(enText))

def intDecode(text):
    deText = [chr(int(str(text)[i + 1:i + 1 + BYTE_LENGTH])) for i in range(0, len(str(text)) - BYTE_LENGTH, BYTE_LENGTH)]

    return ''.join(deText)