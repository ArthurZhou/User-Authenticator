# !/usr/bin/python
# -*- coding: UTF-8 -*-


"""
This is a demo for User-Authenticator Server.
This demo tells you how to import UAS in your own project
"""


import socket
import _thread
from server import login
from server import signup


def run(connf, addrf):
    getReturn = login(connf, addrf)     # get return value
    print(getReturn)    # print return value


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'  # set ip
    port = int(12323)   # set port
    s.bind((host, int(port)))
    s.listen(10)
    print('Server opened on:', host, ':', port)
    while 1:
        connf, addrf = s.accept()   # accept connection
        print('Accept new connection from {0}'.format(addrf))
        nOs = connf.recv(1024).decode('utf-8')  # is this a setup connection
        if nOs == 'setup':
            signup(connf, addrf)
        else:
            _thread.start_new_thread(run, (connf, addrf))     # normal connection


if __name__ == '__main__':
    start()
