from Crypto.Cipher import AES
import base64
from Crypto import Random

class Asymmetric(object):

    def __init__(self, key, text):

        self.key = key
        self.text = text
    
    def encrypt(self):

        self.text = base64.encode(self.text)
        self.text = self.text.encode('ascii')
        self.text = list(self.text)
        en = []
        for e in self.text:
            en.append(pow(e,self.key[1],self.key[0]))

        return en

    def decrypt(self):

        de = []
        self.text = list(self.text)
        for c in self.text:
            de.append(pow(c, self.key[1],self.key[0]))
        
        text = bytes(de).decode('ascii')
        text = base64.decode(text)
    
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
        return base64.encodestring(iv + ciphertext)

    def decrypt(self, ciphertext):
        ciphertext = base64.decodestring(ciphertext)
        iv = ciphertext[0:AES.block_size]
        ciphertext = ciphertext[AES.block_size:len(ciphertext)]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext)
        return plaintext.rstrip(chr(0))