import socket 
import time
from threading import Thread

class Process(Thread):
    defaultPort = 20001
    localPort = 20001
    bufferSize = 1024    
    last_alive = 0
    election_time = 0
    # leader = {'address': '192.168.1.35', 'id': 4}

    def __init__(self):
        pidf = open('status.txt', 'r')
        Thread.__init__(self)
        self.id = pidf.readline().strip()
        self.status = pidf.readline().strip()
        self.address = pidf.readline().strip()
        leader_info = pidf.readline().strip().split('-')

        self.leader = {'address': leader_info[0], 'id': leader_info[1]}

        pidf.close()

        proc_list_file = open('proc_list.txt', 'r')

        self.proc_list = []

        for line in proc_list_file:
            proc_address_id = line.strip();
            parts = proc_address_id.split('-')

            self.proc_list.append((parts[0], parts[1]))
        
        proc_list_file.close()

        


    def print_proc_info(self):

        print('My ID: {}'.format(self.id))
        print('My Status: {}'.format(self.status))
        print('Other Processes: {}'.format(self.proc_list))


    def run(self):
        # Create a datagram socket
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 

        # Bind to address and ip
        self.UDPServerSocket.bind((self.address, self.localPort))

        found_leader = False

        for proc in self.proc_list:
            if self.id < proc[1]:
                found_leader = True

        if not found_leader:
            self.status = 'LEADER'
            
            byteLeaderMessage = str.encode('LEADER')
            UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
            

            for proc in self.proc_list:
                UDPClientSocket.sendto(byteLeaderMessage, (proc[0], self.defaultPort))


        while True:

            bytesSenderPair = self.UDPServerSocket.recvfrom(self.bufferSize)

            message = bytesSenderPair[0].decode('utf-8')

            sender = bytesSenderPair[1]

            print('Received message: ', message)

            if message == 'ALIVE':
                print('ALIVE received from ', sender)
                bytesToSend = str.encode('ALIVE-ACK')
                self.last_alive = 0
                self.UDPServerSocket.sendto(bytesToSend, sender)
                

            if message == 'ELECTION':
                response = str.encode('OK')
                self.status = 'CANDIDATE'
                self.UDPServerSocket.sendto(response, (sender[0], self.defaultPort))
                self.last_alive = 0
                self.election_time = 0

                for proc in self.proc_list:
                    if proc[1] > self.id:
                        electionMessage = 'ELECTION'
                        byteMessage = str.encode(electionMessage)
                        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                        UDPClientSocket.sendto(byteMessage, (proc[0], self.defaultPort))
                print('ELECTION: I am a candidate!')
                

            if message == 'OK':
                self.status = 'WAITING-ELECTION'
                self.last_alive = 0
                self.election_time = 0

            if message == 'LEADER':
                UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
                              

                i_am_greater = False
                for proc in self.proc_list:
                    if proc[0] == sender[0]:
                        if self.id < proc[1]:
                            self.leader['id'] = proc[1]
                            self.status = 'FOLLOWER'
                            self.leader['address'] = sender[0]
                            print ('The new LEADER is ', self.leader['id'], ' at ', self.leader['address'])
                        else:
                            i_am_greater = True
                        
                        break
                
                    if i_am_greater:
                        self.status = 'LEADER'
                        print('I am the new LEADER')
                        leaderByteMessage = str.encode('LEADER')

                        for proc in self.proc_list:
                            UDPClientSocket.sendto(leaderByteMessage, (proc[0], self.proc.defaultPort)) 

    # def send_alive(self):
    #     print('Alive Setup')
    #     msgFromClient = "ALIVE"
    #     bytesToSend   = str.encode(msgFromClient)
    #     bufferSize    = 1024
    #     while True:
    #         if self.status == 'LEADER':
    #             print('Sending ALIVE')
    #             for node in self.proc_list:
    #                 self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    #                 self.UDPClientSocket.sendto(bytesToSend, node[1])
    #             time.sleep(5)
    
    # def election(self):
    #     print('Election Setup')
    #     msgFromClient = "ELECTION"
    #     bytesToSend   = str.encode(msgFromClient)
    #     bufferSize    = 1024
    #     while True:
    #         if self.last_alive > 15 :
    #             for node in self.proc_list:
    #                 if node[1] > self.id:
    #                     self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    #                     self.UDPClientSocket.sendto(bytesToSend, node[1])
    #                     msgFromServer = self.UDPClientSocket.recvfrom(bufferSize)
    #                     message = msgFromServer[0].decode('utf-8')
                        

    #                     if(message == 'OK'):
    #                         self.status = 'WAITING-ELECTION'
    #                         self.last_alive = 0
    #                         self.election_time = 0
    #                         break

    #         if self.election_time > 10 and self.status == 'WAITING-ELECTION':
    #             bytesToFollowers = str.encode('LEADER')

    #             for node in self.proc_list:
    #                 self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) 
    #                 self.UDPClientSocket.sendto(bytesToFollowers, node[1])
    #                 self.election_time = 0
    #                 self.status = 'LEADER'
            
    #         time.sleep(1)
    #         if self.status == 'WAITING_ELECTION':
    #             self.election_time += 1
            
    #         self.last_alive += 1
            


            





