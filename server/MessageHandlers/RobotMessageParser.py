from Definitions.Directions import *
from Definitions.Components import *
from Definitions.Protocol import *

"""
class fields:
    msg - the original message as string
    src - message sender (value of Component enum)
    type - message type (value of RobotMessages enum)
    curr_row - the row of current robot's position
    curr_col - the column of current robot's position
    curr_face_direction - current robot's face direction
"""
class RobotMessageParser():
    def __init__(self, bytes_msg):
        self.msg = Utils.bytes_to_string(bytes_msg)
        self.src = get_component(self.msg[0])
        self.type = RobotMessages.get_robot_message_type(msg_type)
        if self.type == RobotMessages.CONNECT:
            self.__connect_msg()
            
    def __connect_msg(self):
        self.curr_row = int(self.msg[3])
        self.curr_col = int(self.msg[4])
        self.curr_face_direction = get_direction(self.msg[5])

    def set_location(self, row, col):
        self.curr_row = row
        self.curr_col = col
