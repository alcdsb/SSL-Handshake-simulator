from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket

def main():
    '''
    publicKey,privateKey = generateRSAkey()
    text = input("String:")

    en = Asymmetric(publicKey)
    enText = en.encrypt(text)
    
    print(enText)
    de = Asymmetric(privateKey)
    deText = de.decrypt(enText)

    print(deText)'''
    HOST = 'localhost'
    PORT = 65432

    ssl_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client.connect((HOST, PORT))

    ssl_client.sendall('ClientHello'.encode('utf8'))
    data = ssl_client.recv(1024)
    if data!='':
        print('Received', repr(data))




if __name__ == "__main__":

    main()