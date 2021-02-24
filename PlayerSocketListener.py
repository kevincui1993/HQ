import socket
import sys
from logger import *

class PlayerSocketListener:
    '''
    This class is responsible for establishing connections with the players

    Attributes
    ----------
    serverSocket : list(socket)
        server socket for players to connect to
    enable : boolean
        controls whether we should start/stop listenning for connections
    addPlayercb: cb
        callbacks to add players to GameMaster
    '''

    def __init__(self, host, port, callback):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(5)
        self.serverSocket.settimeout(4)
        self.enable = True
        self.addPlayercb = callback

    def __del__(self):
        self.cleanup()

    def start(self):
        ''' 
        Starts to listen for connections from players

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        log(self.__class__.__name__).info("PlayerSocketListener: started")
        while self.enable:
            try: 
                conn,addr = self.serverSocket.accept()
                log(self.__class__.__name__).info("PlayerSocketListener: received a connection from {}".format(addr))
                conn.send("Welcome to HQ game server!\n".encode())
                self.addPlayercb(conn)
            except socket.timeout:
                continue
            except:
                log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))
        
        self.cleanup()
        log(self.__class__.__name__).info("PlayerSocketListener: stopped")


    def stop(self):
        ''' 
        Stops listening for player connections

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        log(self.__class__.__name__).info("stoppping PlayerSocketListener")
        self.enable = False

    def cleanup(self):
        ''' 
        Cleans up the class. Closes socket if opened

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        self.serverSocket.close()