import socket
from Communicators.RobotCommunicator import RobotCommunicator
from Communicators.ClientCommunicator import ClientCommunicator
from Servers.Details import *


"""
class fields:
    robot_comm - robot communicator (there is a single robot, so a single communicator too)
    conn - the socket that the robot has been connected with
"""
class SocketServer:
    def __init__(self):
        self.robot_comm = RobotCommunicator(BUFFER_SIZE)

    def connect(self):
        with socket.socket() as s:
            s.bind((IP, SOCKET_PORT))
            s.listen()
            self.conn, addr = s.accept()
            self.robot_comm.set_socket(self.conn)
    
    def is_connected(self):
        return hasattr(self, 'conn')
    
    def serve(self):
        if self.is_connected():
            with self.conn:
                msg = self.conn.recv(BUFFER_SIZE)
                self.robot_comm.recv_msg(msg)
                while True:
                    continue
