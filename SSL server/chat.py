import threading
import socket
from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
from key import *
from random import randint



class SslClient(threading.Thread):

    clientDict = []
    clientList = []
    chatHistory = open('chatHistory.txt', 'r').read()
    loginDict = dict([info.split() for info in open('loginDict.txt','r').read().split('\n')])

    def __init__(self, conn):

        threading.Thread.__init__(self)
        status, self.symmetric = self.__handShake(conn)
        self.connection = conn

    def __handShake(self, conn):

        data = conn.recv(1024).decode().split('/')

        if data[1] == 'ClientHello':
            conn.sendall(b'ServerHello')
            
            publicKey, privateKey = generateRSAkey()

            sign = Asymmetric(PRIVATE_KEY_CA)
            server_signed = sign.encrypt(data[0] + '/' + publicKey.decode())

            toSend = CA_SIGNED + b'/' + server_signed

            conn.sendall(toSend)
            clientPacket = conn.recv(1024)
            server_unsign = Asymmetric(privateKey)
            clientPacket = server_unsign.decrypt(clientPacket)
            commKey, clientInt = clientPacket.split(b' ')
            
            commu = Symmetric(commKey)
            conn.sendall(commu.encrypt(clientInt.decode()))
            return True, commu
    
    def send(self, message):

        self.connection.sendall(self.symmetric.encrypt(message))

    def recv(self, size = 2048):

        return self.symmetric.decrypt(self.connection.recv(size).decode())

    def sendEveryone(self, message):
        for conn in SslClient.clientList:
            if conn.connection.fileno() != self.connection.fileno():
                conn.send(message)
    
    def Userlogin(self, username, passw):
        if username in SslClient.loginDict:
            if SslClient.loginDict[username]== passw:
                return True
        return False

    def run(self):

        self.send('Welcome to the server')

        while True:
            self.nickName, passw = self.recv().split()
            if self.Userlogin(self.nickName, passw):

                if self.nickName not in SslClient.clientDict:
                    print(6)
                    SslClient.clientDict.append(self.nickName)
                    self.send('Nickname :'+ self.nickName)
                    print(7)
                    break

                self.send('NF False')
            else:
                print(8)
                self.send('WPU False')
                print(9)
        '''
        while True:
            self.nickName = self.recv()
            if self.nickName not in SslClient.clientDict:
                SslClient.clientDict.append(self.nickName)
                self.send('Nickname :'+ self.nickName)
                break

            self.send('False')
        '''

        SslClient.clientList.append(self)
        self.sendEveryone('System notice: ' + self.nickName + ' enter the chat room')
        self.send(SslClient.chatHistory)

        while True:
            try:
                recvedMsg = self.recv()
                if recvedMsg == 'getKey':
                    self.send(self.symmetric.getKey())
                elif recvedMsg :
                    message = self.nickName + ' : ' + recvedMsg
                    print(message)
                    self.sendEveryone(message)
                    SslClient.chatHistory += message + '\n'
                          

            except (OSError, ConnectionResetError):
                
                try: SslClient.clientList.remove(self)

                except:pass

                print(self.nickName, 'exit, ', len(SslClient.clientList), ' person left')
                self.sendEveryone('System notice: ' + self.nickName + ' left the chat room. ' + str(len(SslClient.clientList)) + ' person left')
                if len(SslClient.clientList) == 0:
                    open('chatHistory.txt','w').write(SslClient.chatHistory)

                self.connection.close()

                return None
      