import asyncio
import websockets
from Servers.Details import *
from Communicators.ClientCommunicator import ClientCommunicator
from Communicators.RobotCommunicator import RobotCommunicator


class WebSocketServer:
    def __init__(self, robot_comm):
        self.robot_comm = robot_comm

    def serve(self):
        start_server = websockets.serve(self.__ws_handler, IP, WEBSOCKET_PORT)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
    
    async def __ws_handler(self, websocket, path):
        client_communicator = ClientCommunicator(websocket, self.robot_comm)
        while True:
            msg = await websocket.recv()
            await client_communicator.recv_msg(msg)
