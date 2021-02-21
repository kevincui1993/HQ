import unittest
from PlayerSocketListener import PlayerSocketListener
import threading
import socket
import warnings
import time

class PlayerSocketListenerTestU(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerSocketListenerTestU, self).__init__(*args, **kwargs)
        self.TEST_PORT = 3000
        self.TEST_HOST = '127.0.0.1'
        self.playerListener = PlayerSocketListener(self.TEST_HOST, self.TEST_PORT, self.mockPlayerCB)
        self.mockPlayerCBCallCount = 0

    def startTestRun(self):
        self.mockPlayerCBCallCount = 0

    def mockPlayerCB(self, player):
        self.mockPlayerCBCallCount += 1

    def test_startSocket(self):
        connThread = threading.Thread(target = self.playerListener.start)
        connThread.start()

        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except:  
            self.fail()
        
        s.connect((self.TEST_HOST, self.TEST_PORT))  
        s.close()

        self.playerListener.stop()
        connThread.join()
        self.assertEqual(self.mockPlayerCBCallCount, 1)

    def test_stopSocket(self):
        connThread = threading.Thread(target = self.playerListener.start)
        connThread.start()

        self.playerListener.stop()

        connThread.join()
        self.assertTrue(True)
        self.assertEqual(self.mockPlayerCBCallCount, 0)


if __name__ == '__main__':
    unittest.main()