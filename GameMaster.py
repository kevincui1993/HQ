from GameRoom import GameRoom
from PlayerSocketListener import PlayerSocketListener
import logging
import time
import threading
import sys
from logger import *
"""
This class is responsible for establishing connection with players
"""

class GameMaster:

    def __init__(self):
        self.players = []
        self.minPlayersCount = 2
        self.playersLatch = threading.Semaphore(1)
        self.runGame = True
        self.playerConnListener = PlayerSocketListener("127.0.0.1", 8088, self.addPlayer)
        self.playerConnListenerThread = threading.Thread(target = self.playerConnListener.start)
        self.gamePlayThread = threading.Thread(target = self.gameplay)

        logging.basicConfig(filename='hqgame.log', level=logging.INFO)

    def start(self):
        self.gamePlayThread.start()
        self.playerConnListenerThread.start()

    def stop(self):
        self.playerConnListener.stop()
        log(self.__class__.__name__).info("Exit playerConnListenerThread: waiting")
        self.playerConnListenerThread.join()
        log(self.__class__.__name__).info("Exit playerConnListenerThread: success")
        self.runGame = False

        log(self.__class__.__name__).info("Exit gamePlayThread: waiting")
        self.gamePlayThread.join()
        log(self.__class__.__name__).info("Exit gamePlayThread: success")
        
    def gameplay(self):
        log(self.__class__.__name__).info("starting GameMaster")
        while self.runGame:

            time.sleep(0.5)
            # start a game once the minimum amount of players is reached
            if len(self.players) >= self.minPlayersCount:
                try:
                    self.playersLatch.acquire()

                    log(self.__class__.__name__).info("added {} players to game room".format(len(self.players)))
                    gameRoom = GameRoom(self.players[::])
                    t = threading.Thread(target = gameRoom.startGame)
                    t.start()

                    self.players.clear()
                except:
                    log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))
                finally:
                    self.playersLatch.release()

        self.cleanup()

    def addPlayer(self, playerId):
        try:
            log(self.__class__.__name__).info("Waiting to aquire the lock: player {}".format(playerId))
            self.playersLatch.acquire()
            log(self.__class__.__name__).info("lock aquired: player {}".format(playerId))

            if playerId not in self.players:
                self.players.append(playerId)
                log(self.__class__.__name__).info("successfully added to the player pool: Player {}".format(playerId))
            else:
                log(self.__class__.__name__).warning("Failed to add player as there exists a player with the same Id: Player {}".format(playerId))
        except:
            log(self.__class__.__name__).warning("Unexpected error: {} Player {}".format(sys.exc_info()[0], playerId))
        finally:
            self.playersLatch.release()
            log(self.__class__.__name__).info("lock released: player {}".format(playerId))
            log(self.__class__.__name__).info("number of players in the pool: {}".format(len(self.players)))

    def getPlayerCount(self):
        try:
            self.playersLatch.acquire()
            return len(self.players)
        finally:
            self.playersLatch.release()

    def getPlayers(self):
        return self.players

    def cleanup(self):
        for conn in self.players:
            conn.close()

if __name__ == "__main__":
    gameMaster = GameMaster()
    gameMaster.start()

    command = input()
    while command != "q":
        continue
    
    gameMaster.stop()

    