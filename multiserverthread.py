from socket import *
import sys, threading # In order to terminate the program

class ConsumerThread(threading.Thread):

    def __init__(self, addr,connectionSocket):
        threading.Thread.__init__(self)
        self.address = addr
        self.csocket = connectionSocket
        
    def run(self):    
        try:
            message = connectionSocket.recv(1024)
            filename = message.split()[1]
            f = open(filename[1:], "rb")
            outputdata = f.read()
            
            #Send one HTTP header line into socket
            header = '\nHTTP/1.1 200 OK\n\n'
            connectionSocket.send(header.encode())
       
            #Send the content of the requested file to the client
            for i in range(2, len(outputdata)):
                connectionSocket.send(outputdata[i:i+1])
            connectionSocket.send(b'\r\n\r\n')
    
            connectionSocket.close()
        except IOError:
            #Send response message for file not found 
            connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
            errorMessage = '<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'
            connectionSocket.send(errorMessage.encode())
            connectionSocket.send(b'\r\n\r\n')
            #Close client socket
            connectionSocket.close()
    
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789

#Prepare a sever socket
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    #pass clientsock to the ConsumerThread thread object being created
    newthread = ConsumerThread(addr , connectionSocket)
    newthread.start()    

serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data 