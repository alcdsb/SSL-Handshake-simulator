'''JiaCheng Zhou'''


def  sign_up(username, password):
    sn = open("userdata.txt","a")
    while True:
        if len(password) < 12:
            print ("The password is too short")
        elif len(password) > 20:
            print ("The password is too long")
        else:
            break
    while True:
        password2 = str(input("confirm password1"))
        if password2 ==password:
            break
        else:
            print ("the passwords are not same")
    sn.write(username+"\t"+password+"\n")
    sn.close()

def login(username, password):
    sn=open("userdata.txt","r")
    userdata = username +"\t"+ password +"\n"
    while True:
        data = sn.readline()
        if data == "":
            print("The username or the password is wrong")
            return False
            break
        elif data ==userdata:
            print("welcome back",username)
            return True
            break
    sn.close()