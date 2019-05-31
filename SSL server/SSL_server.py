from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket

def main():
    SERVER_ADDRESS = 'localhost'

    ssl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server.bind((SERVER_ADDRESS, 23492))
    ssl_server.listen(5)

    while True:
        connection, address = ssl_server.accept()
        try:
            connection.settimeout(50)
            buf = connection.recv(1024)
            print(buf)
            if buf=="1":
                connection.send("False")
        except:
             print("Unable to connect with slient")
    connection.close()
if __name__ == "__main__":

    main()