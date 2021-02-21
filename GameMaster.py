from GameRoom import GameRoom
from PlayerSocketListener import PlayerSocketListener
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
        self.runGame = True
        self.playerConnListener = PlayerSocketListener("127.0.0.1", 8080, self.addPlayer)
        self.playerConnListenerThread = threading.Thread(target = self.playerConnListener.start)

    def start(self):
        self.gameplay()
        self.playerConnListenerThread.start()

    def stop(self):
        self.playerConnListener.stop()
        logging.info("Exit playerConnListenerThread: waiting")
        self.playerConnListenerThread.join()
        logging.info("Exit playerConnListenerThread: success")
        self.runGame = False
        
    def gameplay(self):
        logging.info("starting GameMaster")
        while self.runGame:

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

        self.cleanup()

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

    def cleanup(self):
        for conn in self.players:
            conn.close()
