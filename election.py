from threading import Thread
from process import Process
import socket 
import time

class Election(Thread):

    def __init__(self, proc: Process):
        self.proc = proc
        Thread.__init__(self)

    def run(self):
        print('Election Setup')
        msgFromClient = "ELECTION"
        bytesToSend   = str.encode(msgFromClient)
        bufferSize    = 1024
        while True:
            if self.proc.last_alive > 15 and self.proc.status == 'FOLLOWER':
                print('Starting Election')
                self.proc.status = 'CANDIDATE'
                self.proc.last_alive = 0
                self.proc.election_time = 0

                for node in self.proc.proc_list:
                    if node[1] > self.proc.id:
                        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                        UDPClientSocket.sendto(bytesToSend, (node[0], self.proc.defaultPort))
                        # msgFromServer = UDPClientSocket.recvfrom(bufferSize)


                        # if msgFromServer:
                        #     message = msgFromServer[0].decode('utf-8')                        
                        #     print('Received ', message, ' from ', msgFromServer[1])
                        #     if(message == 'OK'):
                        #         self.proc.status = 'WAITING-ELECTION'
                        #         self.proc.last_alive = 0
                        #         self.proc.election_time = 0
                        #         break

            if self.proc.election_time > 10 and self.proc.status == 'CANDIDATE':
                bytesToFollowers = str.encode('LEADER')
                print('I am the new LEADER')
                for node in self.proc_list:
                    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                    UDPClientSocket.sendto(bytesToFollowers, (node[0], self.proc.defaultPort))
                    self.proc.election_time = 0
                    self.proc.status = 'LEADER'
            
            time.sleep(1)
            if self.proc.status == 'WAITING_ELECTION':
                self.proc.election_time += 1
            
            if self.proc.status == 'FOLLOWER':
                self.proc.last_alive += 1