# !/usr/bin/python
# -*- coding: UTF-8 -*-


"""
This is a demo for User-Authenticator Client.
This demo tells you how to import UAC in your own project
"""


import socket
import tkinter as tk
import tkinter.messagebox

from client import signup
from client import check


def run():
    getReturn = check(login, nm, psw, s)  # get return value
    print(getReturn)  # print return value


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
    bt = tk.Button(login, text='Login', font=('', 15), command=run)   # show login button
    bt.grid(row=3, column=0, columnspan=2)
    sg = tk.Button(login, text='No account?', font=('', 15), fg='blue', command=sg_clickon)  # show login button
    sg.grid(row=4, column=0, columnspan=2)
    login.mainloop()    # mainloop


# This is the main process
if __name__ == '__main__':
    try:
        # connect to the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ipaddr = '127.0.0.1'  # set ip
        port = int(12323)  # set port
        s.connect((ipaddr, int(port)))  # connect
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
