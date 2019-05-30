from rsa import *

def main():
    publicKey,privateKey = generateRSAkey(1024)

    text = input("String:")

    en = encrypt(publicKey, text)

    de = decrypt(privateKey, en)

    print(de)


if __name__ == "__main__":

    main()