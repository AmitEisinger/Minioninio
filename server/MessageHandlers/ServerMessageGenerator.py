from Definitions.Protocol import *
from Definitions.Components import Components
from Definitions.Directions import Directions


class ServerMessageGenerator:
    S = Components.SERVER.value
    
    @staticmethod
    def ack_msg():
        return S + Utils.zero_padding(ServerMessages.ACK.value, 2)
    
    # param dir of type Directions
    @staticmethod
    def move_msg(dir):
        msg_type = Utils.zero_padding(ServerMessages.MOVE.value, 2)
        return S + msg_type + dir.value
    
    @staticmethod
    def drop_msg():
        return S + Utils.zero_padding(ServerMessages.DROP.value, 2)
    
    @staticmethod
    def done_msg():
        # TODO: implement it when the client-server protocol will be known
        pass
