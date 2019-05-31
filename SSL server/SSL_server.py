from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket

def main():
    HOST = 'localhost'
    PORT = 65432

    ssl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server.bind((HOST, PORT))
    ssl_server.listen()
    conn, addr = ssl_server.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            print(repr(data))
            if repr(data) == b'ClientHello':
                print(1)
                conn.sendall('Handshake begin')

if __name__ == "__main__":

    main()