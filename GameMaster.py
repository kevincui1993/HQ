from GameRoom import GameRoom
from PlayerSocketListener import PlayerSocketListener
import logging
import time
import threading
import sys
import signal
from logger import *
"""
This class is responsible for establishing connection with players
"""

class GameMaster:
    '''
    This is the main class for starting game server and open up connection 
    for players to connect. 

    Attributes
    ----------
    players : list(socket)
        players pool
    minPlayersCount : int
        minimum number of players to start a game room
    playersLatch : Semaphore
        protects accesss to player pool
    runGame: boolean
        controls whether game server should be running
    playerConnListener: PlayerSocketListener
        opens up socket for players to connect to
    playerConnListenerThread: Thread
        threads for playerConnListener
    gamePlayThread: Thread
        threads for running a game
    '''

    def __init__(self, addr="0.0.0.0", port=3000, minPlayers=2):
        self.players = []
        self.minPlayersCount = minPlayers
        self.playersLatch = threading.Semaphore(1)
        self.runGame = True
        self.playerConnListener = PlayerSocketListener(addr, port, self.addPlayer)
        self.playerConnListenerThread = threading.Thread(target = self.playerConnListener.start)
        self.gamePlayThread = threading.Thread(target = self.gameplay)

        logging.basicConfig(filename='hqgame.log', level=logging.INFO)

    def __del__(self):
        self.cleanup()

    def start(self):
        ''' 
        Starts the GamesMaster server and open up sockets for players to connect

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        self.gamePlayThread.start()
        self.playerConnListenerThread.start()
        print("HQ game server successfully started! Press CTRL + C to stop")

    def stop(self):
        ''' 
        Closes player sockets and connections then stop the GamesMaster server

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        self.playerConnListener.stop()
        log(self.__class__.__name__).info("Exit playerConnListenerThread: waiting")
        self.playerConnListenerThread.join()
        log(self.__class__.__name__).info("Exit playerConnListenerThread: success")
        self.runGame = False

        log(self.__class__.__name__).info("Exit gamePlayThread: waiting")
        self.gamePlayThread.join()
        log(self.__class__.__name__).info("Exit gamePlayThread: success")
        
    def gameplay(self):
        ''' 
        This function constanly looks at the player pool and starts a game 
        room once the number of players in the pool exceeds minimium players 

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        log(self.__class__.__name__).info("starting GameMaster")
        while self.runGame:

            time.sleep(0.5)
            # start a game once the minimum amount of players is reached
            if len(self.players) >= self.minPlayersCount:
                try:
                    # sleep for 1.5 seconds to let more players in 
                    time.sleep(1.5)
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

    def addPlayer(self, conn):
        ''' 
        This function add a player connection to the players pool

        Parameters:
            conn (socket): a socket connection

        Returns:
            Nothing
        '''

        try:
            log(self.__class__.__name__).info("Waiting to aquire the lock: player {}".format(conn))
            self.playersLatch.acquire()
            log(self.__class__.__name__).info("lock aquired: player {}".format(conn))

            self.players.append(conn)

            playersNeeded = self.minPlayersCount - len(self.players)
            if playersNeeded > 0:
                conn.send("Waiting for {} player(s) to join the game!\n".format(playersNeeded).encode())
            log(self.__class__.__name__).info("successfully added to the player pool: Player {}".format(conn))

        except:
            log(self.__class__.__name__).warning("Unexpected error: {} Player {}".format(sys.exc_info()[0], conn))
        finally:
            self.playersLatch.release()
            log(self.__class__.__name__).info("lock released: player {}".format(conn))
            log(self.__class__.__name__).info("number of players in the pool: {}".format(len(self.players)))

    def getPlayerCount(self):
        ''' 
        Returns the number of players in the pool

        Parameters:
            Nothing

        Returns:
            len(self.players) (int): number of players in the player pool
        '''

        try:
            self.playersLatch.acquire()
            return len(self.players)
        finally:
            self.playersLatch.release()

    def getPlayers(self):
        ''' 
        Returns the the players pool, testing purpose only

        Parameters:
            Nothing

        Returns:
            self.players (list(socket)): player pool
        '''

        return self.players

    def cleanup(self):
        ''' 
        Closes any active connection in the player pool

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        for conn in self.players:
            conn.close()

    def signal_handler(self, sig, frame):
        ''' 
        Stop the game server if CTRL+C is received

        Parameters:
            Nothing

        Returns:
            Nothing
        '''
        print("stopping running services...")
        self.stop()
        sys.exit(0)

def printHelpPage():
    print("HQ players is an online multiplayer trivia questions contest")
    print("to start the HQ server: python3 ./GameMaster.py [address] [port] [roomMinPlayers]")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        printHelpPage()
    else: 
        addr,port,minPlayers = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
        gameMaster = GameMaster()
        gameMaster.start()
        signal.signal(signal.SIGINT, gameMaster.signal_handler)

        # keep running until CTRL + C is received
        while True:
            continue
    