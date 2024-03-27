#import socket module
from socket import *
import sys # In order to terminate the program

#Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM) 
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    print('Ready to serve...') 
    connectionSocket, addr = serverSocket.accept()   #Establish the connection 
    try:
        message = connectionSocket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:], "rb")
        outputdata = f.read()
        #Send one HTTP header line into socket
        header = '\nHTTP/1.1 200 OK\n\n'
        connectionSocket.send(header.encode())

        for i in range(2, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1]) 
        connectionSocket.send("\r\n".encode()) 
        
        connectionSocket.close() 

    except IOError:
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        errorMessage = '<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'
        connectionSocket.send(errorMessage.encode())
        connectionSocket.send(b'\r\n')

        connectionSocket.close()

    serverSocket.close()
    sys.exit()#Terminate the program after sending the corresponding data