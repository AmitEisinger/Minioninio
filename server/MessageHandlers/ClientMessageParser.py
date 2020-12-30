from Definitions.Components import *
from Definitions.Protocol import *

"""
class fields:
    msg - the original message as dictionary
    src - message sender (value of Component enum)
    type - message type (value of ClientMessages enum)
    items - client's order as list of dictionaries
"""
class ClientMessageParser():
    def __init__(self, msg):
        self.msg = Utils.json_to_dict(msg)
        self.src = get_component(self.msg[ClientMessageFields.SOURCE])
        self.type = ClientMessages.get_client_message_type(self.msg[ClientMessageFields.TYPE])
        if self.type == ClientMessages.ORDER:
            self.items = self.msg[ClientMessageFields.ITEMS]
