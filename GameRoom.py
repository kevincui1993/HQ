class GameRoom:
    def __init__(self, players):
        self.players = players

    def getPlayerCount(self):
        return len(self.players)