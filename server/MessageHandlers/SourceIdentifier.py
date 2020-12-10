# TODO: implelment the functions when we know how to distinguish between robot and client messages.
# This might be done by the type of the message (robot is string and client is JSON) 
# or using the Components enum.
class SourceIdentifier:
    @staticmethod
    def get_src_type(msg):
        pass

    @staticmethod
    def is_robot(msg):
        pass

    @staticmethod
    def is_client(msg):
        pass
