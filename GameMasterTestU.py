import unittest
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
        
    def test_addPlayer_duplicate(self):
        gameMaster = GameMaster()
        playerIds = [2,2]

        for pid in playerIds:
            gameMaster.addPlayer(pid)

        self.assertEqual(gameMaster.getPlayerCount(), 1)

if __name__ == '__main__':
    unittest.main()