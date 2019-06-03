import base64

def str64decode(s):
    return int(base64.b64decode(s).decode('utf8'))

def str64encode(it):
    return base64.b64encode(str(it).encode('utf8'))


def intEncode(text):
    enText = ['1'] + [(3 - len(str(ord(i)))) * '0' + str(ord(i)) for i in text]

    return int(''.join(enText))

def intDecode(text):
    deText = [chr(int(str(text)[i + 1:i + 4])) for i in range(0, len(str(text)) - 3, 3)]

    return ''.join(deText)