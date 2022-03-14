# !/usr/bin/python
# -*- coding: UTF-8 -*-

"""
User-Authenticator Alpha0.1
By ArthurZhou
This project follows GPL-3.0 License
"""
import os.path
import sys
import tkinter as tk
import tkinter.messagebox
import socket
import time
import hashlib
import uuid


ipaddr = '127.0.0.1'
port = 12323


def signup():
    """
    usage:sign up
    input:s
    output:(null)
    """
    def wriUP():
        askyn = tkinter.messagebox.askokcancel('Yes or no',
                                               'username:{0}\npassword:{1}\nYou can never change it after you click '
                                               '"OK".'.format(usr.get(), psw.get()), parent=swin)
        if str(askyn) == 'True':
            s.send('setup'.encode('utf-8'))     # tell server this is a setup
            time.sleep(0.1)
            salt = str(uuid.uuid4())    # spawn random uuid
            wriSalt = open('salt.lock', 'w')
            wriSalt.write(salt)     # write it in salt.lock
            wriSalt.close()
            # send hash of username and password
            s.send(str(hashlib.sha256((usr.get() + psw.get()).encode('utf-8')).hexdigest()).encode('utf-8'))    #
            time.sleep(0.1)
            s.send(salt.encode('utf-8'))    # send salt
            time.sleep(0.1)
            back = s.recv(1024).decode('utf-8')     # receive statue(ready! or ex!(duplicate account))
            if back == 'ready!':
                tkinter.messagebox.showinfo('Message', 'Your account is ready!Restart to use it.',
                                            parent=swin)
                sys.exit(0)
            elif back == 'ex!':
                tkinter.messagebox.showerror('Error', 'Your account is already used!', parent=swin)
        else:
            pass

    swin = tk.Tk()
    swin.title('Sign-up')
    swin.geometry('500x500')
    # show the elements
    usrt = tk.Label(swin, text='Set your username', font=('Arial', 20), width=25, height=2)
    pswt = tk.Label(swin, text='Set your password', font=('Arial', 20), width=25, height=2)
    con = tk.Button(swin, text='OK', font=('Arial', 20), bg='grey', width=25, height=2, command=wriUP)
    usr = tk.Entry(swin)
    psw = tk.Entry(swin)
    usrt.pack()
    usr.pack()
    pswt.pack()
    psw.pack()
    con.pack()

    swin.mainloop()


def check():
    """
    usage:check your usr and psw with the server
    input(global statements):s, nm, psw, login
    output:(null)
    """
    hashCode = hashlib.sha256((nm.get() + psw.get()).encode('utf-8')).hexdigest()   # use SHA256 to encrypt usr and psw
    sl = open('salt.lock', 'r')     # get salt
    salt = sl.read()
    sl.close()
    s.send(hashCode.encode('utf-8'))  # send hash code to the server
    time.sleep(0.1)     # refresh socket channel
    s.send(salt.encode('utf-8'))    # send salt to the server
    time.sleep(0.1)
    tf = s.recv(1024).decode('utf-8')  # receive password statue(True or False)
    if tf == 'True':  # correct password
        tkinter.messagebox.showinfo('Message',
                                    'Logged in as {0}\n'
                                    'Press "OK" to continue...'.format(nm.get()),
                                    parent=login)   # show a messagebox
        login.destroy()  # hide login window
        return 'True'   # return true or false
    elif tf == 'False':  # wrong password
        tkinter.messagebox.showwarning('Warning',
                                       'Wrong username or password.', parent=login)     # show a messagebox
        return 'False'  # return true or false
    elif not tf:
        tkinter.messagebox.showwarning('Warning', 'Connection lost!\n')
        pass


def main():
    """
    usage:main process,use to create a login window
    input:(null)
    output(global statements):s, nm, psw, login
    """
    def sg_clickon():
        login.destroy()
        signup()

    global nm, psw, login
    login = tk.Tk()
    login.title('Login')    # window title
    # show the elements
    tit = tk.Label(login, text='Login window', font=('', 20))  # show title
    tit.grid(row=0, column=0, columnspan=2)
    uti = tk.Label(login, text='Username:', font=('', 15))  # show 'Username:'
    uti.grid(row=1, column=0)
    nm = tk.Entry(login)    # show usr input box
    nm.grid(row=1, column=1)
    pti = tk.Label(login, text='Password:', font=('', 15))  # show 'Password:'
    pti.grid(row=2, column=0)
    psw = tk.Entry(login, show='*')     # show psw input box(input will be shown as '*')
    psw.grid(row=2, column=1)
    bt = tk.Button(login, text='Login', font=('', 15), command=check)   # show login button
    bt.grid(row=3, column=0, columnspan=2)
    sg = tk.Button(login, text='No account?', font=('', 15), fg='blue', command=sg_clickon)  # show login button
    sg.grid(row=4, column=0, columnspan=2)
    login.mainloop()    # mainloop


# This is the main process
if __name__ == '__main__':
    try:
        # connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ipaddr, int(port)))  # connect
        if str(os.path.exists('salt.lock')) == 'False':
            signup()
        else:
            s.send('normal'.encode('utf-8'))  # tell server this is a normal login
            main()  # run main()
    except BrokenPipeError or ConnectionResetError or ConnectionRefusedError as errmsg:
        if BrokenPipeError:
            tkinter.messagebox.showwarning('Warning', 'BrokenPipe!\n' + errmsg)
        if ConnectionResetError:
            tkinter.messagebox.showwarning('Warning', 'Connection lost!\n' + errmsg)
        if ConnectionRefusedError:
            tkinter.messagebox.showwarning('Warning', 'The server refused your connection!\n' + errmsg)
        pass
