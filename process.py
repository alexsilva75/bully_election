import socket 
import time
from threading import Thread

class Process(Thread):
    localPort = 20005
    bufferSize = 1024    
    last_alive = 0
    election_time = 0
    leader = {'address': '192.168.1.35', 'id': 4}

    def __init__(self):
        pidf = open('status.txt', 'r')
        Thread.__init__(self)
        self.id = pidf.readline().strip()
        self.status = pidf.readline().strip()
        self.address = pidf.readline().strip()
        pidf.close()

        proc_list_file = open('proc_list.txt', 'r')

        self.proc_list = []

        for line in proc_list_file:
            proc_address_id = line.strip();
            parts = proc_address_id.split('-')

            self.proc_list.append((parts[0], parts[1]))
        
        proc_list_file.close()

        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

        # Bind to address and ip
        self.UDPServerSocket.bind((self.address, self.localPort))


    def print_proc_info(self):

        print('My ID: {}'.format(self.id))
        print('My Status: {}'.format(self.status))
        print('Other Processes: {}'.format(self.proc_list))


    def run(self):
        while True:

            bytesSenderPair = self.UDPServerSocket.recvfrom(self.bufferSize)

            message = bytesSenderPair[0]

            sender = bytesSenderPair[1]

            if message == 'ALIVE':
                self.last_alive = 0
                self.UDPServerSocket.sendto('ALIVE-ACK', sender)
                

            if message == 'ELECTION':
                response = str.encode('OK')
                self.status = 'CANDIDATE'
                self.UDPServerSocket.sendto(response, sender)
                self.last_alive = 0
                self.election_time = 0
                print('ELECTION: I am a candidate!')
                

            # if message == 'OK':
            #     self.status = 'WAITING-ELECTION'

            if message == 'LEADER':
                self.status = 'FOLLOWER'
                self.leader['address'] = sender

                for proc in self.proc_list:
                    if proc[0] == sender:
                        self.leader['id'] = proc[1]
                        break
                
                print ('{} Is the new Leader with ID: {}'.format(sender, self.leader['id']))

    def send_alive(self):
        print('Alive Setup')
        msgFromClient = "ALIVE"
        bytesToSend   = str.encode(msgFromClient)
        bufferSize    = 1024
        while True:
            if self.status == 'LEADER':
                for node in self.proc_list:
                    self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                    self.UDPClientSocket.sendto(bytesToSend, node[1])
                time.sleep(5)
    
    def election(self):
        print('Election Setup')
        msgFromClient = "ELECTION"
        bytesToSend   = str.encode(msgFromClient)
        bufferSize    = 1024
        while True:
            if self.last_alive > 15 :
                for node in self.proc_list:
                    if node[1] > self.id:
                        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                        self.UDPClientSocket.sendto(bytesToSend, node[1])
                        msgFromServer = self.UDPClientSocket.recvfrom(bufferSize)
                        message = msgFromServer[0].decode('utf-8')
                        

                        if(message == 'OK'):
                            self.status = 'WAITING-ELECTION'
                            self.last_alive = 0
                            self.election_time = 0
                            break

            if self.election_time > 10 and self.status == 'WAITING-ELECTION':
                bytesToFollowers = str.encode('LEADER')

                for node in self.proc_list:
                    self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                    self.UDPClientSocket.sendto(bytesToFollowers, node[1])
                    self.election_time = 0
                    self.status = 'LEADER'
            
            time.sleep(1)
            if self.status == 'WAITING_ELECTION':
                self.election_time += 1
            
            self.last_alive += 1
            


            





