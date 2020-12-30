from MessageHandlers.RobotMessageParser import *
from MessageHandlers.ServerMessageGenerator import ServerMessageGenerator
from Servers.FTP_Server import FTP_Server


"""
VERY IMPORTANT NOTE: call recv_msg function after every message received from the robot !!!

class fields:
    buffer_size - max buffer size can receive
    sock - socket to communicate through
    msg - last received message (in bytes)
    parser - robot parser that parses the current message
"""
class RobotCommunicator:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

    def set_socket(self, sock):
        self.sock = sock
    
    # This function has to be called after every message received from the robot!
    def recv_msg(self, msg):
        self.msg = msg
        self.parser = RobotMessageParser(msg)
        # send ACK as a reply for any non-ACK message
        if self.parser.type != RobotMessages.ACK:
            self.__send_msg(ServerMessages.ACK)
    
    def handle_order(self, steps):
        for step in steps:
            self.__send_msg(ServerMessages.MOVE, step)
            self.__recv()    # receive the ACK
            FTP_Server(self.parser).start()     # TODO: maybe it would be better to start the FTP connection once earlier - check it
            # TODO: the current robot's location is now updated in self.parse - validate it
            self.__send_msg(ServerMessages.ACK)
        self.__send_msg(ServerMessages.DROP)
        self.__recv()        # receive the ACK
    

    def __send_msg(self, msg_type, param=''):
        msg = None
        if msg_type == ServerMessages.ACK:
            msg = ServerMessageGenerator.robot_ack_msg()
        elif msg_type == ServerMessages.MOVE:
            msg = ServerMessageGenerator.move_msg(param)
        elif msg_type == ServerMessages.DROP:
            msg = ServerMessageGenerator.drop_msg()
        
        if msg != None:
            self.__send(msg)


    def __send(self, msg):
        self.sock.send(msg)
    
    def __recv(self):
        return self.sock.recv(self.buffer_size)
