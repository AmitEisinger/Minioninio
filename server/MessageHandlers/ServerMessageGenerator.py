from Definitions.Protocol import *
from Definitions.Components import Components
from Definitions.Directions import Directions


S = Components.SERVER.value

class ServerMessageGenerator:
    def robot_ack_msg():
        return S + Utils.zero_padding(ServerMessages.ACK.value, 2)
    
    # param dir of type Directions
    def move_msg(dir):
        msg_type = Utils.zero_padding(ServerMessages.MOVE.value, 2)
        return S + msg_type + dir.value
    
    def drop_msg():
        return S + Utils.zero_padding(ServerMessages.DROP.value, 2)
    
    
    def client_ack_msg():
        return Utils.dict_to_json(
            {
                ClientMessageFields.SOURCE : S,
                ClientMessageFields.TYPE : ServerMessages.ACK.value
            }
        )
    
    def done_msg(row, col):
        return Utils.dict_to_json(
            {
                ClientMessageFields.SOURCE : S,
                ClientMessageFields.TYPE : ServerMessages.DONE.value,
                ClientMessageFields.LOCATION : {
                    ClientMessageFields.ROW : row,
                    ClientMessageFields.COL : col
                }
            }
        )

    # param items is a list of dictionaries (according to the protocol)
    def item_not_available_msg(items):
        return Utils.dict_to_json(
            {
                ClientMessageFields.SOURCE : S,
                ClientMessageFields.TYPE : ServerMessages.ITEM_NOT_AVAILABLE.value,
                ClientMessageFields.ITEMS : items
            }
        )

    # param items is a list of dictionaries (according to the protocol)
    def stock_msg(items):
        return Utils.dict_to_json(
            {
                ClientMessageFields.SOURCE : S,
                ClientMessageFields.TYPE : ServerMessages.STOCK.value,
                ClientMessageFields.ITEMS : items
            }
        )
