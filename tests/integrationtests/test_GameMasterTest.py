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
        self.TEST_MIN_PLAYERS = 2
        self.gameMaster = GameMaster(self.TEST_HOST, self.TEST_PORT, self.TEST_MIN_PLAYERS)
        self.gameMasterThread = threading.Thread(target = self.gameMaster.start)
        
        
    def setUp(self):
        self.gameMasterThread.start()

    def tearDown(self):
        self.gameMaster.stop()
        self.gameMasterThread.join()

    def atest_player_connection(self):
        # connect to plyerListener
        try:  
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except:  
            self.fail()
        
        s.connect((self.TEST_HOST, self.TEST_PORT))
        time.sleep(2)
        s.close()

        self.assertEqual(self.gameMaster.getPlayerCount(), 1)

    def test_start_game_room(self):
        players = []
        for i in range(self.TEST_MIN_PLAYERS):
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TEST_HOST, self.TEST_PORT))
                players.append(s)
            except:  
                self.fail()

        time.sleep(5)

        for i in range(self.TEST_MIN_PLAYERS):
            res = players[i].recv(1024).decode("utf-8")
            self.assertTrue("Game started" in res)

    def test_start_player_answer_question(self):
        players = []
        for i in range(self.TEST_MIN_PLAYERS):
            try:  
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.TEST_HOST, self.TEST_PORT))
                players.append(s)
            except:  
                self.fail()

        time.sleep(5)

        for i in range(self.TEST_MIN_PLAYERS):
            players[i].send("A".encode())
            players[i].send("B".encode())

        time.sleep(5)

        for i in range(self.TEST_MIN_PLAYERS):
            res = players[i].recv(1024).decode("utf-8")
            self.assertTrue("Correct" in res or "Wrong Answer" in res)

if __name__ == '__main__':
    unittest.main()