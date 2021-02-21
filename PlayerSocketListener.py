import socket
import logging
import sys

class PlayerSocketListener:

    def __init__(self, host, port, callback):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(5)
        self.serverSocket.settimeout(4)
        self.enable = True
        self.addPlayercb = callback

    def start(self):
        logging.info("PlayerSocketListener: started")
        while self.enable:
            try: 
                conn,addr = self.serverSocket.accept()
                self.addPlayercb(conn)
            except socket.timeout:
                continue
            except:
                logging.warning("Unexpected error: {}".format(sys.exc_info()[0]))
        
        self.cleanup()
        logging.info("PlayerSocketListener: stopped")


    def stop(self):
        logging.info("stoppping PlayerSocketListener")
        self.enable = False

    def cleanup(self):
        self.serverSocket.close()