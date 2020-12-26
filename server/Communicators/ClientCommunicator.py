from MessageHandlers.ClientMessageParser import *
from Definitions.Protocol import ClientMessages
import RobotCommunicator
from Definitions.Directions import *
from MessageHandlers.ServerMessageGenerator import *


"""
VERY IMPORTANT NOTE: call recv_msg function after every message received from the robot !!!

class fields:
    sock - socket to communicate through
    buffer_size - max buffer size can receive
    robot_comm - robot communicator (there is a single robot, so a single communicator too)
    msg - last received message (in bytes)
    parser - client parser that parses the current message
"""
class ClientCommunicator:
    def __init__(self, sock, buffer_size, robot_comm):
        self.sock = sock
        self.buffer_size = buffer_size
        self.robot_comm = robot_comm
    
    # This function has to be called after every message received from the robot!
    def recv_msg(self, msg):
        self.msg = msg
        self.parser = ClientMessageParser(msg)
        self.parser.parse()
        # no need to handle ACK
        if self.parser.type != ClientMessages.ACK:
            self.__handle_msg()
    
    def __handle_msg(self):
        if self.parser.type == ClientMessages.CONNECT:
            self.send_ack()
        elif self.parser.type == ClientMessages.ORDER:
            # TODO: check in the DB if all the items are available and return a list of not_available_items
            not_available_items = []
            # some items are not available
            if not_available_items:
                self.send_item_not_available(not_available_items)
                self.sock.recv(self.buffer_size)    # receive the ACK
            # all items are available
            else:
                self.send_ack()
            
            # any way, we proceed the available items
            # TODO: calculate the route for the robot and send it as a list of lists of Directions 
            # (inner list for every item in the order).
            # put it in items_steps
            items_steps = []
            for steps in items_steps:
                self.robot_comm.handle_order(steps)
            # send DONE when the order is ready
            self.send_done()
        elif self.parser.type == ClientMessages.STOCK:
            # TODO: get items in stock from the DB and return them in a list
            items = []
            self.send_stock_msg(items)
            self.sock.recv(self.buffer_size)    # receive the ACK
        elif self.parser.type == ClientMessages.DISCONNECT:
            if self.send_ack():
                self.sock.close()

    
    
    def send_ack(self):
        msg = ServerMessageGenerator.client_ack_msg()
        return self.__send(msg)
    
    def send_done(self):
        msg = ServerMessageGenerator.done_msg()
        return self.__send(msg)
    
    def send_item_not_available(self, items):
        msg = ServerMessageGenerator.item_not_available_msg(items)
        return self.__send(msg)
    
    def send_stock_msg(self, items):
        msg = ServerMessageGenerator.stock_msg(items)
        return self.__send(msg)
    
    def __send(self, msg):
        # TODO: check if its a correct way to send JSON
        return self.sock.send(msg)
