from enum import Enum
import Utils


class RobotMessages(Enum):
    CONNECT = 0
    ACK = 1
    # in any other case it is a file

    @staticmethod
    def get_robot_message_type(msg_type):
        return Utils.get_enum_of_val(msg_type, RobotMessages)


class ServerMessages(Enum):
    ACK = 0
    MOVE = 1
    DROP = 2
    DONE = 3
    
    @staticmethod
    def get_server_message_type(msg_type):
        return Utils.get_enum_of_val(msg_type, ServerMessages)


class ClientMessages(Enum):
    CONNECT = 0
    ORDER = 1
    ACK = 2

    @staticmethod
    def get_client_message_type(msg_type):
        return Utils.get_enum_of_val(msg_type, ClientMessages)
