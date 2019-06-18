import threading
import socket
from rsa import generateRSAkey
from crypto import Asymmetric, Symmetric
from key import *
from random import randint



class SslClient(threading.Thread):
    '''Public access data'''
    clientDict = [] # List of nickName that connecting to the server 
    clientList = [] # List of SslClient instances
    chatHistory = open('chatHistory.txt', 'r').read() #The chat history
    loginDict = dict([info.split() for info in open('loginDict.txt','r').read().split('\n')]) # Username and password dict

    def __init__(self, conn):
        '''Get AES key from ssl handshake protocol, inherit some methods from threading class'''
        threading.Thread.__init__(self)
        status, self.symmetric = self.__handShake(conn)
        self.connection = conn

    def __handShake(self, conn):
        '''A private method. The method should run only once for each instance
           Return if handshake is success, and A Symmetirc instance 
        '''
        data = conn.recv(1024).decode().split('/')

        if data[1] == 'ClientHello':
            # represent the starting of hankshake
            conn.sendall(b'ServerHello') 
            
            publicKey, privateKey = generateRSAkey() 

            sign = Asymmetric(PRIVATE_KEY_CA)
            #The server signed packet for client to verify the idenity of server, the size of the packet is limited by length of 2^14 bytes
            server_signed = sign.encrypt(data[0] + '/' + publicKey.decode())
            # The format is split by b'/'
            toSend = CA_SIGNED + b'/' + server_signed

            conn.sendall(toSend)
            # AES key and a random integer from client
            clientPacket = conn.recv(1024)
            server_unsign = Asymmetric(privateKey)
            clientPacket = server_unsign.decrypt(clientPacket)
            # The format is split by b' '
            commKey, clientInt = clientPacket.split(b' ')
            
            commu = Symmetric(commKey)
            #Send to client the encrypted random integer, for client to verify
            conn.sendall(commu.encrypt(clientInt.decode()))
            return True, commu
    
    def send(self, message):
        '''Send the encrypted message to the client that this instance connect to'''
        self.connection.sendall(self.symmetric.encrypt(message))

    def recv(self, size = 2048):
        '''Receive the encrypted message from the client that this instance connect to
           return the decryted message       
        '''
        return self.symmetric.decrypt(self.connection.recv(size).decode())

    def sendEveryone(self, message):
        '''Send message to all client that connect to the server'''
        for conn in SslClient.clientList:
            if conn.connection.fileno() != self.connection.fileno():
                conn.send(message)
    
    def userlogin(self, username, passw):
        '''Verify if the username's password is true'''
        if username in SslClient.loginDict:
            if SslClient.loginDict[username]== passw:
                return True
        return False

    def userSignUp(self, username, passw):
        '''Sign up for a new user'''
        if username not in SslClient.loginDict:
            SslClient.loginDict[username] = passw
            return True
        return False

    def run(self):
        '''The method inherit from threading. When the (Sslclient instance).start() is called
           the run method will be called
        '''
        #Tell client that connection and hankshake is succefully done
        self.send('Welcome to the server')
        #(1) Login 
        try:
            while True:
                self.nickName, passw = self.recv().split()
                if self.userlogin(self.nickName, passw):

                    if self.nickName not in SslClient.clientDict:
                        SslClient.clientDict.append(self.nickName)
                        self.send('Welcome!'+'\n'+'Nickname :'+ self.nickName)
                        break
                    self.send('NF False')
                else:
                    self.send('WPU False')
        except:self.connection.close()
        #(1)
        
        
        try:
            # Add the instance to the clientList for public access
            SslClient.clientList.append(self)
            self.sendEveryone('System notice: ' + self.nickName + ' enter the chat room')

            self.send(SslClient.chatHistory)
        except:self.connection.close()
        
        
        while True:
            #(2)Continously receiving message
            try:
                recvedMsg = self.recv()
                if recvedMsg == 'getKey':
                    # Send the AES key of the instance to only the client
                    self.send(self.symmetric.getKey())
                elif recvedMsg == 'signUp':
                    if self.userSignUp(*self.recv().split()):
                        self.send('S')
                    else:
                        self.send('US')
                elif recvedMsg :
                    message = self.nickName + ' : ' + recvedMsg
                    #print(message)
                    self.sendEveryone(message)
                    # Add message to the chat history
                    SslClient.chatHistory += message + '\n'
             #(2)      

            except (OSError, ConnectionResetError):
                # if the connection is lost
                try: 
                    # remove the nickName and the instance from public access data
                    SslClient.clientList.remove(self)
                    SslClient.clientDict.remove(self.nickName)

                except:pass

                #print(self.nickName, 'exit, ', len(SslClient.clientList), ' person left')
                self.sendEveryone('System notice: ' + self.nickName + ' left the chat room. ' + str(len(SslClient.clientList)) + ' person left')
                if len(SslClient.clientList) == 0:
                    # if no one is connecting to server, write login data and chat history to local file
                    open('chatHistory.txt','w').write(SslClient.chatHistory)
                    open('loginDict.txt', 'w').write('\n'.join([username +' '+SslClient.loginDict[username] for username in SslClient.loginDict]))

                self.connection.close()

                return None
      