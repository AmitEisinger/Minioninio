from Servers.SocketServer import SocketServer
from Servers.WebSocketServer import WebSocketServer
import threading
import time


if __name__ == "__main__":
    socket_server = SocketServer()
    socket_server.connect()
    # at this point, the robot is connected
    websocket_server = WebSocketServer(socket_server.robot_comm)
    socket_server_thraed = threading.Thread(target=socket_server.serve)
    socket_server_thraed.start()
    websocket_server.serve()
