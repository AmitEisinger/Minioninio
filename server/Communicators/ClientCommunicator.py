from MessageHandlers.ClientMessageParser import *
from Definitions.Protocol import ClientMessages
import RobotCommunicator
from Definitions.Directions import *
from MessageHandlers.ServerMessageGenerator import *


class ClientCommunicator:
    def __init__(self, sock):
        self.sock = sock
    
    def recv_msg(self, msg):
        self.msg = msg
        self.parser = ClientMessageParser(msg)
        self.parser.parse()
        # send ACK as a reply for any non-ACK message
        if self.parser.type != ClientMessages.ACK:
            self.send_ack()
    
    def handle_msg(self, robot_comm):
        if self.parser.type == ClientMessages.ORDER:
            # TODO: calculate the route for the robot and send it as a list of Directions
            directions = []
            robot_comm.handle_order(directions)
            # send DONE when the order is ready
            self.send_done()
    
    def send_done(self):
        msg = ServerMessageGenerator.done_msg()
        self.__send(msg)
    
    def __send(self, msg):
        self.sock.send(msg)
