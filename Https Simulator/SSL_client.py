from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket
import timeit

def main():

    '''text = input("String:")

    start = timeit.default_timer()
    publicKey, privateKey = generateRSAkey()
    en = Asymmetric(publicKey)
    enText = en.encrypt(text)

    de = Asymmetric(privateKey)
    deText = de.decrypt(enText)

    stop = timeit.default_timer()

    print('Time: ', stop - start)
    print(deText)
'''


    HOST = 'localhost'
    PORT = 65432

    ssl_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client.connect((HOST, PORT))

    ssl_client.sendall('ClientHello'.encode('utf8'))
    data = ssl_client.recv(1024)
    if data == b'ServerHello':
        print('Received', str(data))




if __name__ == "__main__":

    main()