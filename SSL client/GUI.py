'''
Negligible parts are modified by Jingyu in order to connect to the client interface, and create multi-threads

By Leo
'''

from tkinter import *
from tkinter.messagebox import *
import threading

def RegistationPage(login):
        root = Tk()#creat the Tk loop
        root.title = ("register page")#give the page title
        #name the two stringVars
        username = StringVar(root)
        password = StringVar(root)

        #get the input and doing the register check
        def registerCheck():
            name = username.get()
            secret = password.get()
            if login(name,secret) == 1:
                L1 = Label(root,text = "register successful").grid(row = 3,stick = W,pady =10)
                root.destroy()
            elif login(name,secret) == 2:
                L1 = Label(root,text = "the username had be used by someone").grid(row = 3,stick = W,pady =10)

        #create the small things in the page, two Entry and a button with command
        Label(root).grid(row = 0,stick = W,pady = 10)
        Label(root,text = "username:").grid(row = 1,stick = W,pady =10)
        E1 = Entry(root ,textvariable = username)
        E1.grid(row=1, column = 1,stick = E)
        Label(root,text = "password:").grid(row = 2,stick = W,pady=10)
        E2 = Entry(root, textvariable = password)
        E2.grid(row = 2,column = 1,stick = E)
        L1 = Label(root,text = "").grid(row = 3,stick = W,pady =10)
        Button(root,text = "register",command = registerCheck).grid(row =4,stick = W,pady =10)

#The gui for the chat room
def chatRoom(ssl_client,crypt):
    ssl_client =ssl_client
    crypt =crypt
    def msgsend():
            msg = txt_msgsend.get('0.0', END)
            txt_msglist.insert(END, '\nMe : ' +msg)
            ssl_client.send(crypt.encrypt(msg))
            txt_msgsend.delete('0.0',END)

    def msgrecv():
        '''A Thread for recieving message'''
        while True:
            otherword = ssl_client.recv(1024)
            if otherword:
                txt_msglist.insert(END,crypt.decrypt(otherword))


    tk = Tk()#make a Tk loop
    tk.title('chat room')# The title
    f_msglist = Frame(height = 300,width = 300) #The size for msglist part
    f_msgsend = Frame(height = 100,width = 300)#The size for msgsend part
    f_floor = Frame(height = 100,width = 300)#the size for button part
    txt_msglist = Text(f_msglist) 
    txt_msglist.tag_config('green',foreground = 'blue')#charge the text colour
    txt_msgsend = Text(f_msgsend)
    button_send = Button(f_floor,text = 'Send',command = msgsend)#give the command to button
    #grid all things
    f_msglist.grid(row = 0,column = 0)
    f_msgsend.grid(row = 1,column = 0)
    f_floor.grid(row = 2,column = 0)
    txt_msglist.grid()
    txt_msgsend.grid()
    button_send.grid(row = 0,column = 0,sticky = W)
    th2 = threading.Thread(target=msgrecv)
    th2.start()
    tk.mainloop()#main loop end

#login page
def loginPage(login, ssl_client, crypt):
    ssl_client =ssl_client
    crypt =crypt
    root = Tk() #start the loop
    root.title("login page")#give a title
    #name of two stringVar we will used
    username = StringVar(root)
    password = StringVar(root)
    #get the input and have a login check
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

    #grid all things in the Tk page
    Label(root).grid(row = 0,stick = W,pady = 10)
    Label(root,text = "username:").grid(row = 1,stick = W,pady =10)
    E1 = Entry(root ,textvariable = username)
    E1.grid(row=1, column = 1,stick = E)
    Label(root,text = "password:").grid(row = 2,stick = W,pady=10)
    E2 = Entry(root, textvariable = password)
    E2.grid(row = 2,column = 1,stick = E)
    L1 = Label(root,text = "").grid(row = 3,stick = W,pady =10)
    Button(root,text = "login",command = loginCheck).grid(row =4,stick = W,pady =10)
    root.mainloop()#end of loop
