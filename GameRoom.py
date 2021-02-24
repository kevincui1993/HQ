from logger import *
import socket
import time
import threading
import sys
from QuestionMaster import QuestionMaster

class GameRoom:
    '''
    This class is responsible for sending questions to players, receiving their responses,
    and generate statistics

    Attributes
    ----------
    players : list(socket)
        players pool
    response : list(str)
        list of response from the player for one round
    '''

    # static question master class
    questionMaster = QuestionMaster()

    def __init__(self, players):
        self.players = players
        self.response = ["" for i in range(len(self.players))]

        for pconn in players:
            #set a timeout value of 10s to align with how long we should wait a response for a question
            pconn.settimeout(10)

    def __del__(self):
        for pconn in self.players:
            pconn.close()

    def broadcast(self, message):
        ''' 
        broadcast a message to all players in this game room

        Parameters:
            message (str) : message to be broadcasted

        Returns:
            Nothing
        '''

        for conn in self.players:
            try:
                conn.send((message + "\n").encode())
            except:
                log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))

    def getPlayerCount(self):
        ''' 
        Returns the number of players in the room

        Parameters:
            Nothing

        Returns:
            len(self.players) (int): number of players in the room
        '''

        return len(self.players)

    def sendMessage(self, conn, message):
        ''' 
        Sends a message to a socket

        Parameters:
            conn (socket) : a player connection
            message (str) : message to be sent


        Returns:
            Nothing
        '''

        try:
            conn.send((message + "\n").encode())
        except:
            log(self.__class__.__name__).warning("Unexpected error: {}".format(sys.exc_info()[0]))

    def setResponseFromPlayer(self, playerIndex):
        ''' 
        Records the resopnse from player

        Parameters:
            playerIndex (int) : the index of the player in the curretn room

        Returns:
            Nothing
        '''

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
        ''' 
        This function is responsible for starting the game room, sending questions and receiving
        response from the players

        Parameters:
            Nothing

        Returns:
            Nothing
        '''

        log(self.__class__.__name__).info("Started game in game room")
        self.broadcast("Game started! You have 10 seconds to answer each question!")
        numRound = 1
        while len(self.players) > 1:
            log(self.__class__.__name__).info("Progress: round {}".format(numRound))

            ques, ans, numChoices = GameRoom.questionMaster.generateQwithA()
            self.broadcast(ques)

            log(self.__class__.__name__).info("Question: {}".format(ques))
            # asyc threads are used here to get player input
            responseThreads = []
            for j in range(len(self.players)):
                responseThreads.append(threading.Thread(target = self.setResponseFromPlayer, args=(j, )))
                responseThreads[-1].start()
            
            # wait to collect response for all players, timeout is 10 seconds
            for t in responseThreads:
                t.join()

            # sending statistics and eliminate players
            stats = self.calculateStatistics(ans, numChoices)
            self.broadcast(stats)
            self.eliminatePlayers(ans)
            numRound += 1

        if len(self.players) == 1:
            log(self.__class__.__name__).info("Winner player {}".format(self.players[0]))
            self.sendMessage(self.players[0], "Winner!")
            self.players[0].close()
        else:
            log(self.__class__.__name__).info("No Winner!")

    def calculateStatistics(self, answer, numChoices):
        ''' 
        Preparing the statistics for the most recent finished question. The statistics includes 
        the correct answer, and the percentage of each choice selected by all the players in the 
        game room

        Parameters:
            answer (str): the answer for the current question
            numChoices (int): number of choices in the question

        Returns:
            stats (str): statistics
        '''

        percentages = [0 for i in range(numChoices+1)]
        total = len(self.response)
        if total <= 0:
            log(self.__class__.__name__).warning("there is no player to calculate statistics on")
            return ""
        for r in self.response:
            if r != "":
                index = ord(r.lower()) - ord('a')
                if index >= 0 and index < len(percentages):
                    percentages[index] +=1
                else:
                    percentages[-1] += 1 
            else:
                percentages[-1] += 1 

        stats = "Answer is {} (".format(answer)

        for i in range(numChoices):
            stats += "{}: {:.1%} ".format(chr(ord('A')+i), float(percentages[i])/total)
        stats += "Skipped: {:.1%})".format(float(percentages[-1])/total)
        return stats

    def eliminatePlayers(self, answer):
        ''' 
        Removes the eliminated players from the room 

        Parameters:
            answer (str): the answer for the current question

        Returns:
            Nothing
        '''

        i = 0 
        while i < len(self.response):
            if self.response[i].lower() != answer.lower():
                log(self.__class__.__name__).info("Eliminated player {}".format(self.players[i]))
                self.sendMessage(self.players[i], "Wrong Answer! Better luck next time!")
                self.players[i].close()
                log(self.__class__.__name__).info("Closed connection for player {}".format(self.players[i]))
                self.players.pop(i)
                self.response.pop(i)
            else:
                self.sendMessage(self.players[i], "Correct!")
                i+=1
