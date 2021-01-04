from Servers.SocketServer import SocketServer
from Servers.WebSocketServer import WebSocketServer


if __name__ == "__main__":
    #socket_server = SocketServer()
    #socket_server.connect()
    # at this point, the robot is connected
    #websocket_server = WebSocketServer(socket_server.robot_comm)
    websocket_server = WebSocketServer(None)
    websocket_server.serve()
    #socket_server.serve()
