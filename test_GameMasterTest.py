import unittest
from GameMaster import GameMaster
import threading
import socket
import warnings
import time
import time

class GameMasterTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GameMasterTest, self).__init__(*args, **kwargs)
        self.TEST_PORT = 8088
        self.TEST_HOST = '127.0.0.1'
        self.gameMaster = GameMaster(self.TEST_HOST, self.TEST_PORT)
        self.gameMasterThread = threading.Thread(target = self.gameMaster.start)
        
        
    def setUp(self):
        self.gameMasterThread.start()

    def tearDown(self):
        self.gameMaster.stop()
        self.gameMasterThread.join()

    def test_player_connection(self):
        # connect to plyerListener
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except:  
            self.fail()
        
        s.connect((self.TEST_HOST, self.TEST_PORT))
        time.sleep(2)
        s.close()

        self.assertEqual(self.gameMaster.getPlayerCount(), 1)

if __name__ == '__main__':
    unittest.main()