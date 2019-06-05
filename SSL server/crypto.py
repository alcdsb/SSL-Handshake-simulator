from Crypto.Cipher import AES
import base64
from Crypto import Random
from format import *

spc = lambda x,LENGTH:[x[i:i + LENGTH:] for i in range(0, len(x) - LENGTH, LENGTH)] + [x[-(len(x)%LENGTH):-1]+ x[-1]]

class Asymmetric(object):

    def __init__(self, key):
        key = key.split(b' ')
        self.key = str64decode(key[0]), str64decode(key[1])
        self.MAX_KEY_LEN = len(str(self.key[0]))//3 - 1
    
    def encrypt(self,text):

        text = spc(text, self.MAX_KEY_LEN)
        en = []
        for elem in text:
            elem = intEncode(elem)
            en.append(str(pow(elem,self.key[1],self.key[0])))

        return ' '.join(en).encode()

    def decrypt(self, text):

        text = [int(i) for i in text.split().decode()]
        de = ''
        for elem in text: 
            de += intDecode(pow(elem, self.key[1],self.key[0]))

        return de.encode()

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

class Symmetric(object):

    def __init__(self, key, mode = AES.MODE_CBC):

        self.key = key
        self.mode = mode

    def encrypt(self, plaintext):

        en = pad(plaintext).encode()
        iv = Random.new().read(AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv)
        ciphertext = cryptor.encrypt(en)

        return base64.b64encode(iv + ciphertext)

    def decrypt(self, ciphertext):

        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext[AES.block_size:])

        return unpad(plaintext).decode()