__author__      = "Iman Lee ST22639"
__copyright__   = "Copyright 2018-2019, UNITEN"

import datetime
import time
import os
from socket import *

# defining the server IP Address & Port
serverName = '127.0.0.1' # IP Address
serverPort = 9999 # Port Number

# connecting to the server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


#------------ Helper Funtions -------------#
#read file and return it's object
def readfile(filename):
    try:
        statinfo = os.stat(filename+'.txt')
        if(statinfo.st_size >= 1024): # check if the file is > or = to 1k bytes
            msg('The selected file is more then 1kbytes !!')#error message
            return None
        file = open(filename+'.txt', 'r') # open file
        content = file.read()
        file.close()
        return content # return the content of the file
    except:
        msg('file cant be found !!') # error message

# create/open file and put content inside
def writefile(filename,content):
    try:
        file = open(filename,'w+')
        file.write(content)
        file.close()
    except:
        return 'file can\'t create file ' + filename
#display message to the user
def msg(message):
    print "\n++++++++++++++++++++++++++++++++++"
    if(message != ''):
        print message
    else:
        print "Please enter a valid command suck as following: "
    print "UPLOAD <filename> |  uploads a file to the server"
    print "DOWNLOAD <filename> |  downloads a file from the server"
    print "QUIT |  will terminates the client connection and quit the app"
    print "++++++++++++++++++++++++++++++++++\n"
    pass

#------------ Welcome Message --------------#
# welcoming message when you start the application
print '\n\nWelcome to Client Application by Iman Lee ST22639'
msg('Please Be informed that you can use the following commands')


#------------ Commands Functions ------------#
# command that upload the document to the server
def upload(filename):
    if (filename != ''):
        print "UPLOADING "+ filename + "....."
        content = readfile(filename)
        if(content != None ):
            clientSocket.send('upload') #send command name
            print clientSocket.recv(1024)
            clientSocket.send(filename)
            print clientSocket.recv(1024)
            clientSocket.send(content)
            print clientSocket.recv(1024)
            serverMessage = clientSocket.recv(1024)
            print serverMessage
            if(serverMessage == 'OK'):
                print('File Uploaded Successfully')
            else:
                print('something went wrong while uploading!')
                print('please try again later')
    else:
        msg('filename can\'t be empty')
    pass

# command that download the document from the server
def download(filename):
    clientSocket.send('download') #send command name
    print clientSocket.recv(1024)
    clientSocket.send(filename)
    content = clientSocket.recv(1024)
    clientSocket.send('OK')
    if(content != "ERR"):
        ts = time.time()
        name = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        writefile(name+".txt",content)
        print('File Downloaded Successfully!')
    else:
        print('Something went wrong while downloading!')
        print('it could be that the file was not found')
    pass

# command that quit the application
def quit(message):
    clientSocket.send('quit') #send command name
    serverMessage = clientSocket.recv(1024)
    global loop
    if( serverMessage == 'OK'):
        print 'quiting now ' + message
        clientSocket.close()
        loop = False
    else:
        print('something went worng while closing the socket connection')

# adding the commands/functions into a list
commandsList = {
    'UPLOAD'    :   upload,
    'DOWNLOAD'  :   download,
    'QUIT'      :   quit,
}

# caller function it will return the funtion that is be called
def caller(command): # commands caller
    cmd = command.upper()
    try:
        return commandsList[cmd]
    except:
        return msg

#------------ Main Application Loop  ------------#
loop = True # keeps the application running
while loop :
    input = raw_input('Please Enter Your Command:').split(' ')
    command = ''
    arg = ''
    if ( len(input) > 0 ):
        command = input[0].rstrip() #command
        if( len(input) > 1 ):
            arg = input[1].rstrip() #one arg only
    if(command != '' and arg != ''):
        caller(command)(arg)
    elif (command != ''):
        caller(command)('')
    else:
        msg('You Did Not Input Any Command !!') # display error message
