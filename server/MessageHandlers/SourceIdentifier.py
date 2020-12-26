import Utils
from Definitions.Components import *


class SourceIdentifier:
    def get_src_type(msg):
        if SourceIdentifier.is_robot(msg):
            return Components.ROBOT
        if SourceIdentifier.is_client(msg):
            return Components.CLIENT
        return None     # should never get here

    def is_robot(msg):
        msg_string = Utils.bytes_to_string(msg)
        src = get_component(msg_string[0])
        return isRobot(src)

    def is_client(msg):
        msg_dict = Utils.bytes_json_to_dict(msg)
        src = get_component(msg_dict[ClientMessageFields.SOURCE])
        return isClient(src)
