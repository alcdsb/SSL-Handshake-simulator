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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('localhost', 23492))  
    import time  
    time.sleep(2)  
    sock.send(b'1')  
    print(sock.recv(1024))
    sock.close()  





if __name__ == "__main__":

    main()