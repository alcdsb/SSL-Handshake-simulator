'''
Negligible parts are modified by Jingyu inorder to connect to the client interface, and create multi-threads

By Leo
'''
from tkinter import *
from tkinter.messagebox import *
import threading

def RegistationPage(login):
        root = Tk()
        root.title = ("register page")
        username = StringVar(root)
        password = StringVar(root)

        def registerCheck():
            name = username.get()
            secret = password.get()
            if login(name,secret) == 1:
                L1 = Label(root,text = "register successful").grid(row = 3,stick = W,pady =10)
                root.destroy()
            elif login(name,secret) == 2:
                L1 = Label(root,text = "the username had be used by someone").grid(row = 3,stick = W,pady =10)

        Label(root).grid(row = 0,stick = W,pady = 10)
        Label(root,text = "username:").grid(row = 1,stick = W,pady =10)
        E1 = Entry(root ,textvariable = username)
        E1.grid(row=1, column = 1,stick = E)
        Label(root,text = "password:").grid(row = 2,stick = W,pady=10)
        E2 = Entry(root, textvariable = password)
        E2.grid(row = 2,column = 1,stick = E)
        L1 = Label(root,text = "").grid(row = 3,stick = W,pady =10)
        Button(root,text = "register",command = registerCheck).grid(row =4,stick = W,pady =10)

def chatRoom(ssl_client,crypt):
    ssl_client =ssl_client 
    crypt =crypt 
    def msgsend():
            msg = txt_msgsend.get('0.0', END)
            txt_msglist.insert(END, '\nMe : ' +msg)
            ssl_client.send(crypt.encrypt(msg)) #Jingyu
            txt_msgsend.delete('0.0',END)

    def msgrecv():
        '''A Thread for recieving message'''
        while True:
            otherword = ssl_client.recv(1024)
            if otherword:
                txt_msglist.insert(END,crypt.decrypt(otherword))


    tk = Tk()
    tk.title('chat room')
    f_msglist = Frame(height = 300,width = 300) 
    f_msgsend = Frame(height = 100,width = 300)
    f_floor = Frame(height = 100,width = 300)
    txt_msglist = Text(f_msglist) 
    txt_msglist.tag_config('green',foreground = 'blue')
    txt_msgsend = Text(f_msgsend)
    button_send = Button(f_floor,text = 'Send',command = msgsend)
    f_msglist.grid(row = 0,column = 0)
    f_msgsend.grid(row = 1,column = 0)
    f_floor.grid(row = 2,column = 0)
    txt_msglist.grid()
    txt_msgsend.grid()
    button_send.grid(row = 0,column = 0,sticky = W)
    th2 = threading.Thread(target=msgrecv)
    th2.start()
    tk.mainloop()

def loginPage(login, ssl_client, crypt):
    ssl_client =ssl_client
    crypt =crypt
    root = Tk()
    root.title("login page")
    username = StringVar(root)
    password = StringVar(root)

    def loginCheck():
        name = username.get()
        secret = password.get()
        if login(name,secret) == 1:
            print ("welcome back",username)
            root.destroy()
            chatRoom(ssl_client,crypt)
        elif login(name,secret) == 2:
            L1 = Label(root,text = "the username or the password are incorrect").grid(row = 3,stick = W,pady =10)
        elif login(name,secret) == 3:
            L1 = Label(root,text = "User is already online                      ").grid(row = 3,stick = W,pady =10)

    Label(root).grid(row = 0,stick = W,pady = 10)
    Label(root,text = "username:").grid(row = 1,stick = W,pady =10)
    E1 = Entry(root ,textvariable = username)
    E1.grid(row=1, column = 1,stick = E)
    Label(root,text = "password:").grid(row = 2,stick = W,pady=10)
    E2 = Entry(root, textvariable = password)
    E2.grid(row = 2,column = 1,stick = E)
    L1 = Label(root,text = "").grid(row = 3,stick = W,pady =10)
    Button(root,text = "login",command = loginCheck).grid(row =4,stick = W,pady =10)
    root.mainloop()
