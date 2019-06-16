from chat import SslClient, socket

def main():
    HOST = 'localhost' #server ip
    PORT = 61563 # server port
    

    ssl_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_server.bind((HOST, PORT))
    ssl_server.listen()

    while True:

        conn, addr = ssl_server.accept()
        print('Accept a new connection', conn.getsockname(), conn.fileno())
        newThread = SslClient(conn)
        newThread.setDaemon(True)
        newThread.start()
    

if __name__ == "__main__":
    
    main()
