
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
        msgToClient = "ALIVE-"+str(self.proc.id)
        bytesToSend   = str.encode(msgToClient)
        bufferSize    = 1024
        while True:
            if self.proc.status == 'LEADER':                
                for node in self.proc.proc_list:
                    print('Sending ALIVE to ', node[0], ' at port ', self.proc.defaultPort)
                    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                    UDPClientSocket.sendto(bytesToSend, (node[0], self.proc.defaultPort))
                time.sleep(5)