from Crypto.Cipher import AES
import base64
from Crypto import Random
from format import *

# Separate a string or a list into dispersed elements, limited by LENGTH
spc = lambda x,LENGTH:[x[i:i + LENGTH:] for i in range(0, len(x) - LENGTH, LENGTH)] + [x[-(len(x)%LENGTH):-1]+ x[-1]]

class Asymmetric(object):
    '''RSA class, using for encryption and decryption'''
    def __init__(self, key):
        '''Initialize the key into special format '''
        key = key.split(b' ')
        self.key = str64decode(key[0]), str64decode(key[1])
        self.MAX_KEY_LEN = len(str(self.key[0]))//3 - 1
    
    def encrypt(self,text):
        '''Encrypt the plaintext into ciphertext. Argument "text" should be string. The output is a bytes array'''
        text = spc(text, self.MAX_KEY_LEN)
        en = []
        for elem in text:
            elem = intEncode(elem)
            en.append(str(pow(elem,self.key[1],self.key[0])))

        return ' '.join(en).encode()

    def decrypt(self, text):
        '''Decrypt the ciphertext into plaintext. Argument "text" should be a list of string. The output is a string'''
        text = [int(i) for i in text.decode().split()]
        de = ''
        for elem in text: 
            de += intDecode(pow(elem, self.key[1],self.key[0]))
        
        return de.encode()

BS = AES.block_size #The length of plaintext to encrypted should be the multiple of block_size
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) # Append the length of inputed string into the multiple of block_size
unpad = lambda s : s[:-ord(s[len(s)-1:])] #return the orginal text that is appended

class Symmetric(object):
    '''AES class, using for encryption and decryption'''
    def __init__(self, key, mode = AES.MODE_CBC):
        '''Initialize key, mode of AES'''
        self.key = key
        self.mode = mode

    def encrypt(self, plaintext):
        '''Encrypt the plaintext into ciphertext. Argument "plaintext" should be string. The output is a bytes array'''
        en = pad(plaintext).encode()
        iv = Random.new().read(AES.block_size)
        cryptor = AES.new(self.key, self.mode, iv)
        ciphertext = cryptor.encrypt(en)

        return base64.b64encode(iv + ciphertext)

    def decrypt(self, ciphertext):
        '''Decrypt the ciphertext into plaintext. Argument "ciphertext" should be a bytes array. The output is a string'''
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        cryptor = AES.new(self.key, self.mode, iv)
        plaintext = cryptor.decrypt(ciphertext[AES.block_size:])

        return unpad(plaintext).decode()

    def getKey(self):
        '''Return the AES key'''
        return self.key.decode()