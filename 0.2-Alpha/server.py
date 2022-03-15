# !/usr/bin/python
# -*- coding: UTF-8 -*-


"""
User-Authenticator Alpha0.2 Server
By ArthurZhou
This project follows GPL-3.0 License
"""


import os
import socket
import sys
import _thread
import time
import hashlib
import uuid

conac = 0   # use 1 to stop the server to start
host_name = socket.gethostname()
host = socket.gethostbyname(host_name)
port = int(12323)


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
    rtPsw = input('Set password for user "root":')
    if acc == 'accept':
        mk = open('key.lock', 'w')
        salt = str(uuid.uuid4())
        preHash = hashlib.sha256(('root' + rtPsw).encode('utf-8')).hexdigest()  # mix usr and psw
        hashCode = hashlib.sha256((preHash + salt).encode('utf-8')).hexdigest()     # mix prehash and salt
        mk.write('root|{0}|{1}'.format(salt, hashCode))
        mk.close()
        print('Your server setup successfully!')
        sys.exit(0)
    else:
        sys.exit(0)


def signup(connf, addrf):
    try:
        time.sleep(0.2)
        cliHash = connf.recv(1024).decode('utf-8')
        time.sleep(0.2)
        cliUsr = connf.recv(1024).decode('utf-8')
        salt = str(uuid.uuid4())
        hashCode = hashlib.sha256((cliHash + salt).encode('utf-8')).hexdigest()
        print('{0} sign up as {1}'.format(addrf, hashCode))
        kf = open('key.lock', 'r')
        oldKeys = kf.read()
        kf.close()
        keys = oldKeys.split('\n')
        for index in keys:
            splitKeys = index.split('|')
            if str(splitKeys[0]) == cliUsr:
                time.sleep(0.3)
                connf.send('ex!'.encode('utf-8'))
                print('{0} account already used: {1}'.format(addrf, hashCode))
                print('{0} connection close'.format(addrf))
                return 'EXACCOUNT'
        else:
            time.sleep(0.1)
            connf.send('ready!'.encode('utf-8'))
            print('{0} account ready: {1}'.format(addrf, hashCode))
            kf = open('key.lock', 'a')
            kf.write('\n{0}|{1}|{2}'.format(cliUsr, salt, hashCode))
            kf.close()
            print('{0} connection close'.format(addrf))
            return 'NEWACCOUNT|' + hashCode
    except BrokenPipeError or ConnectionResetError:
        print('{0} connection close'.format(addrf))
        pass


def login(connf, addrf):
    """
    usage:main process,use to verify users
    input:(null)
    output(global statements):s, nm, psw, login
    """
    global rt
    if conac == 1:  # is the server stopped
        sys.exit(0)

    kf = open('key.lock', 'r')  # open storage
    oldKeys = kf.read()
    kf.close()
    time.sleep(0.2)
    cliHash = connf.recv(1024).decode('utf-8')
    if cliHash == 'setup':
        signup(connf, addrf)
    time.sleep(0.2)
    cliUsr = connf.recv(1024).decode('utf-8')
    if cliHash and cliUsr:
        keys = oldKeys.split('\n')
        for index in keys:
            splitKeys = index.split('|')
            if splitKeys[0] == cliUsr:
                print('{0} find account named {1}'.format(addrf, cliUsr))
                break
        else:
            print('{0} wrong username: {1}'.format(addrf, cliUsr))

        salt = splitKeys[1]
        hashCode = hashlib.sha256((cliHash + salt).encode('utf-8')).hexdigest()     # spawn hash code
        time.sleep(0.2)
        if hashCode == splitKeys[2]:
            print('{0} logged in as {1}'.format(addrf, hashCode))
            connf.send('True'.encode('utf-8'))
            rt = 'True|' + hashCode
        else:
            print('{0} wrong password: {1}'.format(addrf, hashCode))
            connf.send('False'.encode('utf-8'))
            rt = 'False'
            login(connf, addrf)
        return rt
    else:
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
    """
    usage:build-in starter
    input:(null)
    output:(null)
    """
    try:
        if str(os.path.exists('key.lock')) == 'False':  # is this the first time to use
            setup()     # yes
        else:   # no
            count = 0   # reset counter
            keysNum = open('key.lock', 'r')
            while True:
                buffer = keysNum.read()     # read the file
                if not buffer:  # reach the bottom of the file
                    break
                count += buffer.count('\n')     # count '\n'
            print('{0} account(s) loaded.'.format(count))

        global conn, addr, t, rt
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # avoid (socket.error: [Error 98] Address already in use) error
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, int(port)))
        s.listen(10)
        print('Server opened on:', host, ':', port)
        _thread.start_new_thread(wait, ())

        while 1:
            connf, addrf = s.accept()
            print('Accept new connection from {0}'.format(addrf))
            nOs = connf.recv(1024).decode('utf-8')
            rt = 'return'  # default return value
            if nOs == 'setup':
                signup(connf, addrf)
            else:
                _thread.start_new_thread(login, (connf, addrf, rt))
    except BrokenPipeError or ConnectionResetError or KeyboardInterrupt:
        if BrokenPipeError or ConnectionResetError:
            print('{0} connection close'.format(addr))
        pass


# This is the main process
if __name__ == '__main__':
    start()
