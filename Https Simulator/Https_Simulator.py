from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
from Crypto.Cipher import AES

def main():
    '''
    publicKey,privateKey = generateRSAkey(1024)

    text = input("String:")

    en = encrypt(publicKey, text)

    de = decrypt(privateKey, en)

    print(de)'''
    demo = Symmetric(b'keyven__keyven__')
    string_ex = "AAA"
    e = demo.encrypt(string_ex.encode("utf8"))
    d = demo.decrypt(e)



if __name__ == "__main__":

    main()