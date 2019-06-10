from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
import socket
from random import randint
from hashlib import sha256
import threading

def handShake(ssl_client):
    
    CLIENT_INT = str(randint(2 ** 32, 2 ** 33)).encode()

    ssl_client.sendall(CLIENT_INT + b'/' + b'ClientHello')
    serverHello = ssl_client.recv(1024)

    if serverHello == b'ServerHello':
        #Hankshake begins
        signed_packet = ssl_client.recv(2 ** 14)
        signed_packet = signed_packet.split(b'/')
        caDeSign = Asymmetric(CA_ROOT_KEY)

        serverPublicKey_CA = caDeSign.decrypt(signed_packet[0]).encode()
        serverDeSign = Asymmetric(serverPublicKey_CA)
        serverSign = serverDeSign.decrypt(signed_packet[1])
        serverSign = serverSign.encode().split(b'/')


        if serverSign[0] == CLIENT_INT:

            serverPublicKey = serverSign[1]

            dec = Asymmetric(serverPublicKey)

            clientAesKey = sha256(str(randint(2 ** 16, 2 ** 17)).encode()).hexdigest()[:32]
            
            CLIENT_INT = str(randint(2 ** 32, 2 ** 33))
            signed_packet = dec.encrypt(clientAesKey + ' ' + CLIENT_INT)

            ssl_client.sendall(signed_packet)

            commu = Symmetric(clientAesKey.encode())

            if commu.decrypt(ssl_client.recv(1024).decode()) == CLIENT_INT:
                return True, commu
            else:
                ssl_client.sendall(b'Refuse Connection')


def main():
    
    global CA_ROOT_KEY
    CA_ROOT_KEY = b'NTY3NDkxODM5NTE0NjMyNTc0NzYwOTI3MDA2NTM4NjQyMzY1MzM5Njg0MjAwODc4NDc4ODk1MzQ3MzEwNjc4MjI2NDE0NDc2MjkzOTY1MjE5MzUyNTI2MzQxNzU0NDMyNzc2NDg5MDM2Nzk3MDIwMzA3NzQ1NDY3NjA0MzQyODkzODMzOTU5MTIxNzM4MjQzOTQwNTE0ODkwODg1NTMxMjk0Mzc5MTA5MTU5Nzc3MzczNTI2OTM0NTEwMTU0NTQzMzI1Nzg4MDgxODg2NDQ1MjIzMDkyMDk2MzY2NDY0NTU3NDE3NTIwMDU0MTQ4MDE5MzAyODcxNzgxNjk3NTY5Njk3ODEyNTI0MjYxNjgxODU4ODg5NzAxNTI3MDE5ODk2ODUxMzM1MTE2NDYwMzczNzIyNDU2MDE4MTE4NDc5ODg4NzI2NDIzMzg0MTc5NzgzNTAzMzgwOTkyNjA0ODY0MjE5MDc3NzU0NjAyNjU3ODQzMDcyMzIxMzQ3MTMyMDU0MDQyMTkxOTU0MDAyNTgyNjUyMjU1MzY1Mjg0MjEyNjA2NjkzNTE1MDYwMzEyMTE2ODEzMDE0ODUyOTU1Nzk1NDU5MDc4Mjg1Mjg3Mzk0MDc3MjExNTU2NDU1NTY2NTU3OTQ0MTQyMjMwOTM4OTgyMTE3ODkyMTU3NzczMjI3MjI5MDE3MDU1MzQyMTA4MzYxNDU1MjkwNTExOTY2NDE3MzIyMDA0NzI4MTY5NDEzOTYzNzc0NjYzNjE0MTA1NzU3MzMzODM3NTg0NzE3NDMwNzI5MTUzMTY0NTc3NDk1MDc2MDg3OTkyNTg1MjYwNDIwODQwOTYzMDUxMzA0NzAyNjA4NDg2NTQ1MjYzMjU4NzA1MTUzMzc5ODQzMzY5NTE1OTk4ODYxMTM3MjA3NTk3Mzk2NDYxMjA0NjAzMDg1OTY3ODU2Njk3MTI0NDY2NDc3MjYwOTExMTI5MTQ1NzkzMTU2MjgzNzE1OTA2NTM5MjU2MjM2ODQ5ODEyNDI2MDAxMDM4NTg3NDcxMTc0OTAxNTE3MzY5MzE5NjM0NjI2NDY2ODcyNTg1MzExMjE0NDUxMTE3MTk3MjY2MTY4MDUyNzY1NjEzMjgzMDgwMTg0Nzk0ODQ1Nzc1MzU2ODk0MDk2NjU4MDY1MzQ3OTkxOTM2NDI5Mjc1NDY0NDQxOTA3OTc4NDY1Mzc4ODM4Njc3NDAyMTYyNDgyNDY4MzcyNzg0MDY0MzU1MzY5MzMzOTI3NjYwMDU1MjI4NTMxNzEzMTQ5Mzk1ODA2NTM2NzY5NDY2MDg1Mzc2OTE2MTEzNTkwOTU0OTMwODQxODU4ODMwMjE0MjM4NTA2MjU0NDk3MTAyNzM1NTA3ODk5NTk5MTE3NDMzMTc0ODI4MjczMjEwODQ3NjE4NzMyNTE0MDE1ODMyMTE1MDgyNzk1MTU0ODI5NjczMzg0Mzg3ODgxNzYyMzgzOTE5NzE1NDMzOTc1NDIxMTAxMDIxNjc0NDgzMTQyNzExOTc5MDAyNDAwMzg2NTk5NDEzMDU1MDkwNDM2NzI1MTQxMzI1NDE4MDM0MzE1NDM3MTgzOTE0MTk5ODg0OTUxMzI2NjgxMDA3Mjk1MjIyNTk2MDIzOTMxNDM0NDYyNjM3 NjU1Mzc='

    HOST = 'localhost' #'35.243.232.136'
    PORT = 61563
    
    

    ssl_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_client.connect((HOST, PORT))

    def sendThreadFunc():
        while True:

            myword = input()
            ssl_client.send(crypt.encrypt(myword))
    
    def recvThreadFunc():
        while True:
            otherword = ssl_client.recv(1024)
            if otherword:
                print(crypt.decrypt(otherword))
    
    status, crypt = handShake(ssl_client)

    if status:
        print(crypt.decrypt(ssl_client.recv(1024)))
        while True:
            nickName = input('Input your nickname: ')
            passw = input('Input your password: ')
            #ssl_client.send(crypt.encrypt(nickName))
            ssl_client.send(crypt.encrypt(nickName + ' ' + passw))
            loginStatus = crypt.decrypt(ssl_client.recv(1024))
            if loginStatusnot == 'NF False':
                print('Nickname already be used')
            elif loginStatus == 'WPU False':
                print('Nickname or password is wrong')
            else: break
            #if loginStatus != 'False':
                #break
            #print('Nickname used')

        th1 = threading.Thread(target=sendThreadFunc)
        th2 = threading.Thread(target=recvThreadFunc)
        threads = [th1, th2]
 
        for t in threads :
            t.setDaemon(True)
            t.start()
        t.join()
        



if __name__ == "__main__":

    main()