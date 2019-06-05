from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket
from random import randint


def main():
    '''
    
    
    esa = Symmetric(b'm0rm00m011m10r298mc9r0muc09u8r18')
    a = input('string: ')
    start = timeit.default_timer()
    en = esa.encrypt(a)
    print(en)
    de = esa.decrypt(en)
    print(de)

    stop = timeit.default_timer()
    
    print('Time: ', stop - start)
    
    import timeit'''
    import base64
    
    publicKey, privateKey = generateRSAkey(128)
    en = Asymmetric(publicKey)
    enText = en.encrypt(input('string: '))
    de = Asymmetric(privateKey)
    deText = de.decrypt(enText)

    print(deText)


    '''
    HOST = 'localhost'
    PORT = 65432
    
    CLIENT_INT = randint(2**32, 2**33)

    ssl_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client.connect((HOST, PORT))

    ssl_client.sendall((str(CLIENT_INT) + '/' + 'ClientHello').encode('utf8'))
    data = ssl_client.recv(1024)
    if data == b'ServerHello':
        print('Hankshake begins')'''
        




if __name__ == "__main__":

    main()