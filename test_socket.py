import socket 

localPort = 20005
bufferSize = 1024 
address = '192.168.43.17'

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
UDPServerSocket.bind((address, localPort))

print('UDP Server is On')

while True:

    bytesSenderPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesSenderPair[0]

    sender = bytesSenderPair[1]

    # response = str.encode('OK')
    UDPServerSocket.sendto(message, sender)