import unittest
from PlayerSocketListener import PlayerSocketListener
import threading
import socket
import warnings
import time

class PlayerSocketListenerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerSocketListenerTest, self).__init__(*args, **kwargs)
        self.TEST_PORT = 8088
        self.TEST_HOST = '127.0.0.1'
        self.playerListener = PlayerSocketListener(self.TEST_HOST, self.TEST_PORT, self.mockPlayerCB)
        self.mockPlayerCBCallCount = 0

    def startTestRun(self):
        self.mockPlayerCBCallCount = 0

    def mockPlayerCB(self, player):
        self.mockPlayerCBCallCount += 1

    def test_startSocket(self):
        # create a thread to start the playerListener
        connThread = threading.Thread(target = self.playerListener.start)
        connThread.start()

        # connect to plyerListener
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
        # create a thread to start the playerListener
        connThread = threading.Thread(target = self.playerListener.start)
        connThread.start()

        self.playerListener.stop()
        connThread.join()
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()