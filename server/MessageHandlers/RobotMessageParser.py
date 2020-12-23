from Definitions.Directions import *
from Definitions.Components import *


class RobotMessageParser():
    def __init__(self, bytes_msg):
        self.msg = Utils.bytes_to_string(bytes_msg)
        self.src = get_component(self.msg[0])    # value from the Component's enum

        # identify message's type depending on the sender
        msg_type = int(self.msg[1:3])
        if isRobot(self.src):
            self.type = RobotMessages.get_robot_message_type(msg_type)      # value from the RobotMessages's enum
    
    
    def parse(self):
        if self.type == RobotMessages.CONNECT:
            self.__connect_msg()
            
    def __connect_msg(self):
        self.curr_row = int(self.msg[3])
        self.curr_col = int(self.msg[4])
        self.curr_face_direction = get_direction(self.msg[5])

    def set_location(self, row, col):
        self.curr_row = row
        self.curr_col = col
