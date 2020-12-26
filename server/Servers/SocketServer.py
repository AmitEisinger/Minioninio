import socket
from MessageHandlers.SourceIdentifier import SourceIdentifier
from Communicators.RobotCommunicator import RobotCommunicator
from Communicators.ClientCommunicator import ClientCommunicator

# TODO: fix these values
IP = '127.0.0.1'
PORT = 8080
BUFFER_SIZE = 4096

class SocketServer:
    def serve():
        robot_communicator = RobotCommunicator(BUFFER_SIZE)
        with socket.socket() as s:
            s.bind((IP, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                client_communicator = ClientCommunicator(conn, BUFFER_SIZE, robot_communicator)
                while True:
                    msg = conn.recv(BUFFER_SIZE)
                    if SourceIdentifier.is_robot(msg):
                        robot_communicator.set_socket(conn)
                        robot_communicator.recv_msg(msg)
                    elif SourceIdentifier.is_client(msg):
                        client_communicator.recv_msg(msg)
