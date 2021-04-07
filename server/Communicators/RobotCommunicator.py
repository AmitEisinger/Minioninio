from MessageHandlers.RobotMessageParser import *
from MessageHandlers.ServerMessageGenerator import ServerMessageGenerator
from Servers.FTP_Server import FTP_Server
from Definitions.Directions import step_to_direction
from Definitions.Grid import Grid
import time


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
        face_dir = self.parser.curr_face_direction
        for i in range(len(steps)-1):
            step, face_dir = step_to_direction(steps[i], steps[i+1], face_dir)
            self.__send_msg(ServerMessages.MOVE, step)
            self.__recv()    # receive the ACK
            FTP_Server(self.parser).start()     # TODO: maybe it would be better to start the FTP connection once earlier - check it
            self.__update_position(steps[i][0], steps[i][1], face_dir)
            self.__send_msg(ServerMessages.ACK)
            # wait when reaching the dispenser
            if Grid.is_dispenser(steps[i+1]):
                time.sleep(10)
        self.__send_msg(ServerMessages.DROP)
        self.__recv()        # receive the ACK
    
    
    def __update_position(self, row, col, face_dir):
        self.parser.set_location(row, col)
        self.parser.set_face_direction(face_dir)
    

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
