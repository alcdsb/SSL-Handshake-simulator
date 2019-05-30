from Crypto.Cipher import AES
import base64
from Crypto import Random

class Asymmetric(object):

    def __init__(self, key):

        self.key = key
    
    def encrypt(self,text):

        text = text.encode('ascii')
        text = base64.b64encode(text)
        text = list(text)
        en = []
        for e in text:
            en.append(pow(e,self.key[1],self.key[0]))

        return en#base64.b64encode(bytes(en))

    def decrypt(self,text):

        #text = base64.b64decode(text)
        de = []
        text = list(text)
        for c in text:
            de.append(pow(c, self.key[1],self.key[0]))

        text = bytes(de).decode('ascii')
        text = base64.b64decode(text)
    
        return text

BS = AES.block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(0) 

class Symmetric(object):

    def __init__(self, key, mode = AES.MODE_CBC):
        self.key = key
        self.mode = mode

    def encrypt(self, plaintext):
        iv = Random.new().read(AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv)
        ciphertext = cryptor.encrypt(pad(plaintext))
        return base64.encodebytes(iv + ciphertext)

    def decrypt(self, ciphertext):
        ciphertext = base64.encodebytes(ciphertext)
        iv = ciphertext[0:AES.block_size]
        ciphertext = ciphertext[AES.block_size:len(ciphertext)]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext.rstrip(chr(0))