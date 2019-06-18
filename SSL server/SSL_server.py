from chat import SslClient, socket

def main():
    HOST = '' #'localhost'
    PORT = 61563 # server port for chat room
    

    ssl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server.bind((HOST, PORT))
    ssl_server.listen()

    while True:

        conn, addr = ssl_server.accept()
        print('Accept a new connection', conn.getsockname(), conn.fileno())
        #Every times a Sslclient instance is created, a thread is created
        newThread = SslClient(conn)
        newThread.setDaemon(True)
        newThread.start()
    

if __name__ == "__main__":
    
    main()
