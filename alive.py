
from threading import Thread
from process import Process
import socket 
import time

class Alive(Thread):

    def __init__(self, proc: Process):
        Thread.__init__(self)
        self.proc = proc


    def run(self):
        print('Alive Setup')
        msgFromClient = "ALIVE"
        bytesToSend   = str.encode(msgFromClient)
        bufferSize    = 1024
        while True:
            if self.proc.status == 'LEADER':
                print('Sending ALIVE to ', node[1], ' at port ', self.proc.defaultPort)
                for node in self.proc.proc_list:
                    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                    UDPClientSocket.sendto(bytesToSend, (node[1], self.proc.defaultPort))
                time.sleep(5)