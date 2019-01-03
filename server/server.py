__author__      = "Iman Lee ST22639"
__copyright__   = "Copyright 2018-2019, UNITEN"

import os
from socket import *
serverIP = '127.0.0.1'
serverPort = 9999
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind((serverIP,serverPort))
serverSocket.listen(1)


#read file and return it's object
def readfile(filename):
    try:
        statinfo = os.stat(filename)
        if(statinfo.st_size >= 1024): # check if the file is > or = to 1k bytes
            print('file is to big')
            return 'ERR' #error message
        file = open(filename, 'r') # open file
        content = file.read()
        file.close()
        return content # return the content of the file
    except:
        print('can\'t open the file')
        return 'ERR' # error message

# create/open file and put content inside
def writefile(filename,content):
    try:
        file = open(filename,'w+')
        file.write(content)
        file.close()
        return 'OK' # ok message
    except:
        return 'ERR'#error message

print '\n\nWelcome to Server Application by Iman Lee ST22639\n'
print 'The server is running...'
while 1:
    connectionSocket, addr = serverSocket.accept()
    print 'server is connected to a client'
    loop = True
    while loop:
        command = connectionSocket.recv(1024)
        connectionSocket.send('OK')
        if(command == 'upload'):
            print('upload sections running')
            filename = connectionSocket.recv(1024)
            connectionSocket.send('OK')
            content = connectionSocket.recv(1024)
            connectionSocket.send('OK')
            writefile('upload_'+ filename +'.txt',content)
            connectionSocket.send('OK')
        elif (command == 'download'):
            print('download sections running')
            filename = connectionSocket.recv(1024)
            content = readfile('upload_'+ filename +'.txt')
            connectionSocket.send(content)
            print connectionSocket.recv(1024)
        elif (command == 'quit'):
            print('quit sections running')
            loop = False

    connectionSocket.send('OK') #quiting message
    connectionSocket.close()
    print 'server closed a connection from a client'
