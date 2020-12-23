import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

import MessageHandlers.RobotMessageParser


class FTP_Server:
    def __init__(self, robot):
        self.robot = robot

        # Instantiate a dummy authorizer for managing 'virtual' users
        self.authorizer = DummyAuthorizer()

        # anonymous user
        self.authorizer.add_anonymous(os.getcwd())

        # Instantiate FTP handler class
        self.handler = FileReceiverHandler #FTPHandler - (TODO: it was the original code. remove it when we sure the new one is correct)
        self.handler.authorizer = authorizer
        self.handler.permit_foreign_addresses = True

        # Instantiate FTP server class and listen on 0.0.0.0:21 (TODO: check it)
        self.address = ('', 21)
    

    def start(self):
        with FTPServer(self.address, self.handler) as server:
            # start ftp server
            server.serve_forever()


    class FileReceiverHandler(FTPHandler):
        def on_file_received(self, file):
            # TODO: get the location from the file (which is an image of a barcode)
            # use self.robot.set_location()
            # TODO: find a way to return to the main loop after receiving a file (do not stuck on serve_forever)
            pass
