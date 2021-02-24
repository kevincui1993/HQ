import unittest
from PlayerSocketListener import PlayerSocketListener
import threading
import socket
import warnings
import time

class PlayerSocketListenerTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PlayerSocketListenerTest, self).__init__(*args, **kwargs)
        self.TEST_PORT = 8089
        self.TEST_HOST = '127.0.0.1'
        self.playerListener = PlayerSocketListener(self.TEST_HOST, self.TEST_PORT, self.mockPlayerCB)
        self.playerListenerThread = threading.Thread(target = self.playerListener.start)
        self.mockPlayerCBCallCount = 0

    def setUp(self):
        self.mockPlayerCBCallCount = 0
        # create a thread to start the playerListener
        self.playerListenerThread.start()

    def tearDown(self):
        self.playerListener.stop()
        self.playerListenerThread.join()

    def mockPlayerCB(self, player):
        self.mockPlayerCBCallCount += 1

    def test_startSocket(self):
        # connect to plyerListener
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except:  
            self.fail()
        
        s.connect((self.TEST_HOST, self.TEST_PORT))
        time.sleep(2)
        s.close()

        self.assertEqual(self.mockPlayerCBCallCount, 1)

if __name__ == '__main__':
    unittest.main()