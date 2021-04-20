from MessageHandlers.ClientMessageParser import *
from Definitions.Protocol import ClientMessages
import Communicators.RobotCommunicator
from Definitions.Directions import *
from MessageHandlers.ServerMessageGenerator import *
from Firebase.DB_Items import DB_Items
from Definitions.Grid import *


"""
VERY IMPORTANT NOTE: call recv_msg function after every message received from the client !!!

class fields:
    websocket - websocket to communicate through
    robot_comm - robot communicator (there is a single robot, so a single communicator too)
    msg - last received message (as string)
    parser - client parser that parses the current message
    dst_row, dst_col - the location from which the client should pick the orders
"""
class ClientCommunicator:
    def __init__(self, websocket, robot_comm):
        self.websocket = websocket
        self.robot_comm = robot_comm
        self.dst_row, self.dst_col = Grid.get_empty_dst()
        print('Destination: (', self.dst_row, self.dst_col, ')')
    
    # This function has to be called after every message received from the client!
    async def recv_msg(self, msg):
        self.msg = msg
        self.parser = ClientMessageParser(msg)
        # no need to handle ACK
        if self.parser.type != ClientMessages.ACK:
            await self.__handle_msg()
    
    async def __handle_msg(self):
        if self.parser.type == ClientMessages.CONNECT:
            await self.__send_msg(ServerMessages.ACK)
        
        elif self.parser.type == ClientMessages.ORDER:
            not_available_items = DB_Items.get_not_available_items(self.parser.items)
            # some items are not available
            if not_available_items:
                await self.__send_msg(ServerMessages.ITEM_NOT_AVAILABLE, not_available_items)
                await self.__recv()       # receive the ACK
            # all items are available
            else:
                await self.__send_msg(ServerMessages.ACK)
            
            # any way, we provide the available items
            available_items = DB_Items.get_available_items(self.parser.items)
            # calculate the route for the robot
            for item in available_items:
                # steps: current -> dispenser -> destination
                steps = Grid.calculate_route(self.robot_comm.parser.curr_row, self.robot_comm.parser.curr_col, DISPENSER_ROW, DISPENSER_COL) + Grid.calculate_route(DISPENSER_ROW, DISPENSER_COL, self.dst_row, self.dst_col)
                print('Steps: ', steps)
                self.robot_comm.handle_order(steps)
            # update the stock in the DB
            DB_Items.update_items_amount(available_items)
            # send DONE when the order is ready
            await self.__send_msg(ServerMessages.DONE, self.dst_row, self.dst_col)
        
        elif self.parser.type == ClientMessages.STOCK:
            items = DB_Items.get_all_items()
            await self.__send_msg(ServerMessages.STOCK, items)

    
    async def __send_msg(self, msg_type, *args):
        msg = None
        if msg_type == ServerMessages.ACK:
            msg = ServerMessageGenerator.client_ack_msg()
        elif msg_type == ServerMessages.DONE:
            msg = ServerMessageGenerator.done_msg(args[0], args[1])
        elif msg_type == ServerMessages.ITEM_NOT_AVAILABLE:
            msg = ServerMessageGenerator.item_not_available_msg(args[0])
        elif msg_type == ServerMessages.STOCK:
            msg = ServerMessageGenerator.stock_msg(args[0])

        if msg != None:
            await self.__send(msg)
    

    async def __send(self, msg):
        await self.websocket.send(msg)
    
    async def __recv(self):
        return await self.websocket.recv()
