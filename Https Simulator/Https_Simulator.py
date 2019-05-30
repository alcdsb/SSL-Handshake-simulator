from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric

def main():
    '''publicKey,privateKey = generateRSAkey(1024)

    text = input("String:")

    en = Asymmetric(publicKey)
    enText = en.encrypt(text)

    print(len(enText))
    de = Asymmetric(privateKey)
    deText = de.decrypt(enText)

    print(deText)'''
    import base64

    print(base64.b64encode(b"AAAAAA"*256))




if __name__ == "__main__":

    main()