from MessageHandlers.ClientMessageParser import *
from Definitions.Protocol import ClientMessages
import Communicators.RobotCommunicator
from Definitions.Directions import *
from MessageHandlers.ServerMessageGenerator import *


"""
VERY IMPORTANT NOTE: call recv_msg function after every message received from the client !!!

class fields:
    websocket - websocket to communicate through
    robot_comm - robot communicator (there is a single robot, so a single communicator too)
    msg - last received message (in bytes)
    parser - client parser that parses the current message
"""
class ClientCommunicator:
    def __init__(self, websocket, robot_comm):
        self.websocket = websocket
        self.robot_comm = robot_comm
    
    # This function has to be called after every message received from the client!
    def recv_msg(self, msg):
        self.msg = msg
        self.parser = ClientMessageParser(msg)
        # no need to handle ACK
        if self.parser.type != ClientMessages.ACK:
            self.__handle_msg()
    
    def __handle_msg(self):
        if self.parser.type == ClientMessages.CONNECT:
            self.__send_msg(ServerMessages.ACK)
        elif self.parser.type == ClientMessages.ORDER:
            # TODO: check in the DB if all the items are available and return a list of not_available_items
            not_available_items = []
            # some items are not available
            if not_available_items:
                self.__send_msg(ServerMessages.ITEM_NOT_AVAILABLE, not_available_items)
                self.__recv()           # receive the ACK
            # all items are available
            else:
                self.__send_msg(ServerMessages.ACK)
            
            # any way, we proceed the available items
            # TODO: calculate the route for the robot and send it as a list of lists of Directions 
            # (inner list for every item in the order).
            # put it in items_steps
            items_steps = []
            for steps in items_steps:
                self.robot_comm.handle_order(steps)
            # send DONE when the order is ready
            self.__send_msg(ServerMessages.DONE)
        elif self.parser.type == ClientMessages.STOCK:
            # TODO: get items in stock from the DB and return them in a list
            items = []
            self.__send_msg(ServerMessages.STOCK, items)

    
    def __send_msg(self, msg_type, param=''):
        msg = None
        if msg_type == ServerMessages.ACK:
            msg = ServerMessageGenerator.client_ack_msg()
        elif msg_type == ServerMessages.DONE:
            msg = ServerMessageGenerator.done_msg()
        elif msg_type == ServerMessages.ITEM_NOT_AVAILABLE:
            msg = ServerMessageGenerator.item_not_available_msg(param)
        elif msg_type == ServerMessages.STOCK:
            msg = ServerMessageGenerator.stock_msg(param)

        if msg != None:
            self.__send(msg_type)
    

    async def __send(self, msg):
        # TODO: The msg is of type JSON, so it should be sent in a binary format. 
        #       If the client has problems with that, send as string and the client will parse it to JSON by itself
        await self.websocket.send(msg)
    
    async def __recv(self):
        return await self.websocket.recv()
