from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
from key import *
import socket
from random import randint
    
def main():
    HOST = 'localhost'
    PORT = 65432
    

    ssl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server.bind((HOST, PORT))
    ssl_server.listen()
    conn, addr = ssl_server.accept()
    with conn:
        print('Connected by', addr)
        data = conn.recv(1024).decode().split('/')
        print(data)
        if data[1] == 'ClientHello':
            conn.sendall(b'ServerHello')
            print('Handshake begin')
            publicKey, privateKey = generateRSAkey()



if __name__ == "__main__":

    main()