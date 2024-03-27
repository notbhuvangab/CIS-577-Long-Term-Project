from socket import *
import sys

serverName = sys.argv[1]
serverPort = int(sys.argv[2])
file_name = sys.argv[3]

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

message = 'GET /' + file_name
clientSocket.send(message.encode())
# header = repr(clientSocket.recv(1024))#.decode('utf-8')
# messageReceived = repr(clientSocket.recv(1024))#.decode('utf-8')
# finalMessage = ''
# while messageReceived:
#     finalMessage += messageReceived
#     messageReceived = repr(clientSocket.recv(1024)) #.decode('utf-8')

response = b" "
while True:
    part = clientSocket.recv(1024)
    if not part:
        break
    response += part
           
print(response)
clientSocket.close()