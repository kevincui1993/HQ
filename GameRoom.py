from logger import *
import socket
import time
import threading
import sys
from QuestionMaster import QuestionMaster

class GameRoom:

    # static question master class
    questionMaster = QuestionMaster()

    def __init__(self, players):
        self.players = players
        self.response = ["" for i in range(len(self.players))]

        for pconn in players:
            #set a timeout value of 10s to align with how long we should wait a response for a question
            pconn.settimeout(10)

    def getPlayerCount(self):
        return len(self.players)

    def sendMessage(self, conn, message):
        try:
            conn.send(message.encode())
        except:
            log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))

    def setResponseFromPlayer(self, playerIndex):
        conn = self.players[playerIndex]
        res = ""
        try: 
            # timeout is 10 seconds
            res = conn.recv(1024).decode("utf-8")
            log(self.__class__.__name__).info("Response from player {}: {}".format(conn, res))
        except socket.timeout:
            log(self.__class__.__name__).info("Failed to receive response from player {}".format(conn))
        except:
            log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))
        finally:
            self.response[playerIndex] = res[0] if len(res) > 0 else ""

    def startGame(self):
        log(self.__class__.__name__).info("Started game in game room")
        numRound = 1
        while len(self.players) > 1:
            log(self.__class__.__name__).info("Progress: round {}".format(numRound))

            # asyc threads are used here to get player input
            responseThreads = []
            ques, ans = GameRoom.questionMaster.generateQwithA()
            for j in range(len(self.players)):
                self.sendMessage(self.players[j], ques)
                responseThreads.append(threading.Thread(target = self.setResponseFromPlayer, args=(j, )))
                responseThreads[-1].start()
            
            # wait to collect response for all players, timeout is 10 seconds
            for t in responseThreads:
                t.join()

            self.eliminatePlayers(ans)
            numRound += 1

        if len(self.players) == 1:
            log(self.__class__.__name__).info("Winner player {}".format(self.players[0]))
            self.sendMessage(self.players[0], "Winner!\n")
            self.players[0].close()
        else:
            log(self.__class__.__name__).info("No Winner!")


    def eliminatePlayers(self, answer):
        i = 0 
        while i < len(self.response):
            if self.response[i].lower() != answer.lower():
                log(self.__class__.__name__).info("Eliminated player {}".format(self.players[i]))
                self.sendMessage(self.players[i], "Wrong Answer! Better luck next time!\n")
                self.players[i].close()
                log(self.__class__.__name__).info("Closed connection for player {}".format(self.players[i]))
                self.players.pop(i)
                self.response.pop(i)
            else:
                self.sendMessage(self.players[i], "Correct!\n")
                i+=1
