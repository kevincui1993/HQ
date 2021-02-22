import unittest
import threading
from GameMaster import GameMaster

class GameMasterTestU(unittest.TestCase):

    def test_addPlayer_single(self):
        gameMaster = GameMaster()
        playerId = 1

        gameMaster.addPlayer(playerId)

        self.assertEqual(gameMaster.getPlayerCount(), 1)

    def test_addPlayer_multiple(self):
        gameMaster = GameMaster()
        playerIds = [2,5,7,1,3]

        for pid in playerIds:
            gameMaster.addPlayer(pid)

        self.assertEqual(gameMaster.getPlayerCount(), len(playerIds))

    def test_addPlayer_multiple_parallel(self):
        gameMaster = GameMaster()
        playerIds = [2,5,7,1,3]

        threads = []
        for pid in playerIds:
            t = threading.Thread(target = gameMaster.addPlayer, args=(pid, ))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.assertEqual(gameMaster.getPlayerCount(), len(playerIds))
        self.assertEqual(list(set(gameMaster.getPlayers())).sort(), playerIds.sort())
        
    def test_addPlayer_duplicate(self):
        gameMaster = GameMaster()
        playerIds = [2,2]

        for pid in playerIds:
            gameMaster.addPlayer(pid)

        self.assertEqual(gameMaster.getPlayerCount(), 1)

if __name__ == '__main__':
    unittest.main()