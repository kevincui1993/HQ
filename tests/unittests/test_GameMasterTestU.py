import unittest
import threading
from GameMaster import GameMaster
from unittest.mock import Mock

class GameMasterTestU(unittest.TestCase):

    def test_addPlayer_single(self):
        gameMaster = GameMaster()
        mockConnection = Mock()

        gameMaster.addPlayer(mockConnection)

        self.assertEqual(gameMaster.getPlayerCount(), 1)

    def test_addPlayer_multiple(self):
        gameMaster = GameMaster()
        mockConnections = [Mock(),Mock(),Mock(),Mock(),Mock()]

        for conn in mockConnections:
            gameMaster.addPlayer(conn)

        self.assertEqual(gameMaster.getPlayerCount(), len(mockConnections))

    def test_addPlayer_multiple_parallel(self):
        gameMaster = GameMaster()
        mockConnections = [Mock(),Mock(),Mock(),Mock(),Mock()]

        threads = []
        for conn in mockConnections:
            t = threading.Thread(target = gameMaster.addPlayer, args=(conn, ))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEquals(gameMaster.getPlayerCount(), len(mockConnections))

if __name__ == '__main__':
    unittest.main()