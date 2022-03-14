# !/usr/bin/python
# -*- coding: UTF-8 -*-


import os
import socket
import sys
import threading
import _thread
import time
import hashlib

conac = 0


def setup():
    """
    usage:set up the server
    input:(null)
    output:(null)
    """
    print('Hi!Welcome to User-Authenticator Server!\n'
          'Before using,you must accept our licence.(GPL-3.0)\n'
          'Click here to view:https://github.com/ArthurZhou/User-Authenticator/blob/main/LICENSE')
    acc = input('Type "accept" to accept our licence:')
    if acc == 'accept':
        mk = open('key.lock', 'w')
        mk.write('<hashcode storage>')
        mk.close()
        print('Your server setup successfully!')
        sys.exit(0)
    else:
        sys.exit(0)


def signup(connf, addrf, rt):
    time.sleep(0.2)
    cliHash = connf.recv(1024).decode('utf-8')
    time.sleep(0.2)
    cliSalt = connf.recv(1024).decode('utf-8')
    hashCode = hashlib.sha256((cliHash + cliSalt).encode('utf-8')).hexdigest()
    print('{0} sign up as {1}'.format(addr, hashCode))
    kf = open('key.lock', 'a+')
    kf.write('\n' + hashCode)
    oldKeys = kf.read()
    kf.close()
    keys = oldKeys.split('\n')
    ch = list.count(keys, hashCode)
    if ch == 0:
        time.sleep(0.1)
        connf.send('ready!'.encode('utf-8'))
        print('{0} account ready: {1}'.format(addr, hashCode))
        rt = 'NEWACCOUNT|' + hashCode
        return rt
    else:
        connf.send('ex!'.encode('utf-8'))
        print('{0} account already in used: {1}'.format(addr, hashCode))
        signup(connf, addrf, rt)


def login(connf, addrf, rt):
    """
    usage:main process,use to verify users
    input:(null)
    output(global statements):s, nm, psw, login
    """
    if conac == 1:
        sys.exit(0)
    kf = open('key.lock', 'r')
    oldKeys = kf.read()
    kf.close()
    time.sleep(0.2)
    cliHash = connf.recv(1024).decode('utf-8')
    if cliHash == 'setup':
        signup(connf, addrf, rt)
    time.sleep(0.2)
    cliSalt = connf.recv(1024).decode('utf-8')
    if cliHash and cliSalt:
        hashCode = hashlib.sha256((cliHash + cliSalt).encode('utf-8')).hexdigest()  # use SHA256 to encrypt usr and psw
        keys = oldKeys.split('\n')
        ch = list.count(keys, hashCode)
        time.sleep(0.5)
        if ch == 1:
            print('{0} logged in as {1}. Find {2} account named {1}'.format(addrf, hashCode, ch))
            connf.send('True'.encode('utf-8'))
            rt = 'True|' + hashCode
            return rt
        else:
            print('{0} wrong username or password: {1}'.format(addrf, hashCode))
            connf.send('False'.encode('utf-8'))
            login(connf, addrf, rt)
            rt = 'False'
            return rt
    else:
        print('{0} connection close'.format(addrf))
        pass


def wait():
    """
    usage:waiting user to enter 'stop'.If true, stop the server
    input:(null)
    output:(null)
    """
    print('Type "stop" to stop it')
    st = input()
    while st != 'stop':
        st = input()
    else:
        global conac
        conac = 1
        print('Server stopped.You can kill the process now.')
        sys.exit(0)


def start():
    try:
        if str(os.path.exists('key.lock')) == 'False':
            setup()
        else:
            pass

        global addr, t, rt
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # avoid (socket.error: [Error 98] Address already in use) error
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # host_name = socket.gethostname()
        # host = socket.gethostbyname(host_name)
        host = '127.0.0.1'
        port = int(12323)
        s.bind((host, int(port)))
        s.listen(10)
        print('Server opened on:', host, ':', port)
        _thread.start_new_thread(wait, ())
        while 1:
            if conac == 1:
                sys.exit(0)
            connf, addrf = s.accept()
            print('Accept new connection from {0}'.format(addrf))
            nOs = connf.recv(1024).decode('utf-8')
            rt = 'return'  # default return value
            if nOs == 'setup':
                signup(connf, addrf, rt)
            else:
                t = threading.Thread(target=login, args=(connf, addrf, rt))
                t.start()
    except BrokenPipeError or ConnectionResetError:
        print('{0} connection close'.format(addr))
        pass


# This is the main process
if __name__ == '__main__':
    start()
