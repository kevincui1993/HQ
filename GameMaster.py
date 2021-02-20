from GameRoom import GameRoom
import logging
import time
import threading
import sys
"""
This class is responsible for establishing connection with players
"""
class GameMaster:

    def __init__(self):
        self.players = []
        self.minPlayersCount = 5
        self.playersLatch = threading.Semaphore(1)

    def start(self):
        self.gameplay()

    def gameplay(self):
        
        runGame = True
        while runGame:

            time.sleep(0.5)
            # check if we can start a game
            if len(self.players) > self.minPlayersCount:
                try:
                    self.playersLatch.acquire()

                    logging.info("added {} players to game room".format(len(self.players)))
                    gameRoom = GameRoom(self.players[::])

                    self.players.clear()
                except:
                    logging.warning("Unexpected error: {}".format(sys.exc_info()[0]))
                finally:
                    self.playersLatch.release()


    def addPlayer(self, playerId):
        try:
            logging.info("Waiting to aquire the lock: player {}".format(playerId))
            self.playersLatch.acquire()
            logging.info("lock aquired: player {}".format(playerId))

            if playerId not in self.players:
                self.players.append(playerId)
                logging.info("successfully added to the player pool: Player {}".format(playerId))
            else:
                logging.warning("Failed to add player as there exists a player with the same Id: Player {}".format(playerId))
        except:
            logging.warning("Unexpected error: {} Player {}".format(sys.exc_info()[0], playerId))
        finally:
            self.playersLatch.release()
            logging.info("lock released: player {}".format(playerId))

    def getPlayerCount(self):
        try:
            self.playersLatch.acquire()
            return len(self.players)
        finally:
            self.playersLatch.release()