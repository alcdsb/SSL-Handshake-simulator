import base64

def str64decode(s):
    return int(base64.b64decode(s).decode('utf8'))

def str64encode(it):
    return base64.b64encode(str(it).encode('utf8'))
