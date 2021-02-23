import unittest
from unittest.mock import Mock
import socket
from GameRoom import GameRoom

class GameRoomTestU(unittest.TestCase):

    def test_sendMessage_empty_message(self):
        gameRoom = GameRoom([])
        mock = Mock()
        gameRoom.sendMessage(mock, "")

        self.assertEqual(mock.send.call_count, 1)

    def test_sendMessage_short_message(self):
        gameRoom = GameRoom([])
        mock = Mock()
        gameRoom.sendMessage(mock, "short message")

        self.assertEqual(mock.send.call_count, 1)

    def test_sendMessage_long_message(self):
        gameRoom = GameRoom([])
        mock = Mock()
        gameRoom.sendMessage(mock, "this is a long message" * 100)

        self.assertEqual(mock.send.call_count, 1)

    def test_setResponseFromPlayer_invalid_message(self):
        mock = Mock()
        mock.recv.return_value = ""
        gameRoom = GameRoom([mock])

        gameRoom.setResponseFromPlayer(0)

        self.assertEqual(mock.recv.call_count, 1)
        self.assertEqual(gameRoom.response[0], "")

    def test_setResponseFromPlayer_valid_message(self):
        mock = Mock()
        mock.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock])

        gameRoom.setResponseFromPlayer(0)

        self.assertEqual(mock.recv.call_count, 1)
        self.assertEqual(gameRoom.response[0], "A")

    def test_setResponseFromPlayer_long_message_take_first_character(self):
        mock = Mock()
        mock.recv.return_value = "A RANDOM MESSAGE".encode()
        gameRoom = GameRoom([mock])

        gameRoom.setResponseFromPlayer(0)

        self.assertEqual(mock.recv.call_count, 1)
        self.assertEqual(gameRoom.response[0], "A")

    def test_eliminatePlayers_empty_game(self):
        gameRoom = GameRoom([])

        gameRoom.eliminatePlayers("A")

        self.assertEqual(gameRoom.getPlayerCount(), 0)

    def test_eliminatePlayers_correct_answer(self):
        mock = Mock()
        mock.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock])
        gameRoom.setResponseFromPlayer(0)

        gameRoom.eliminatePlayers("A")

        self.assertEqual(gameRoom.getPlayerCount(), 1)

    def test_eliminatePlayers_incorrect_answer(self):
        mock = Mock()
        mock.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock])
        gameRoom.setResponseFromPlayer(0)

        gameRoom.eliminatePlayers("D")

        self.assertEqual(gameRoom.getPlayerCount(), 0)

    def test_eliminatePlayers_correct_answer_lowercase(self):
        mock = Mock()
        mock.recv.return_value = "d".encode()
        gameRoom = GameRoom([mock])
        gameRoom.setResponseFromPlayer(0)

        gameRoom.eliminatePlayers("D")

        self.assertEqual(gameRoom.getPlayerCount(), 1)

    def test_eliminatePlayers_two_players_winner(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        mock2 = Mock()
        mock2.recv.return_value = "D".encode()
        gameRoom = GameRoom([mock1, mock2])
        gameRoom.setResponseFromPlayer(0)
        gameRoom.setResponseFromPlayer(1)

        gameRoom.eliminatePlayers("D")

        self.assertEqual(gameRoom.getPlayerCount(), 1)

    def test_eliminatePlayers_two_players_all_eliminated(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        mock2 = Mock()
        mock2.recv.return_value = "D".encode()
        gameRoom = GameRoom([mock1, mock2])
        gameRoom.setResponseFromPlayer(0)
        gameRoom.setResponseFromPlayer(1)

        gameRoom.eliminatePlayers("B")

        self.assertEqual(gameRoom.getPlayerCount(), 0)

    def test_eliminatePlayers_two_players_tie(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        mock2 = Mock()
        mock2.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock1, mock2])
        gameRoom.setResponseFromPlayer(0)
        gameRoom.setResponseFromPlayer(1)

        gameRoom.eliminatePlayers("A")

        self.assertEqual(gameRoom.getPlayerCount(), 2)

    def test_broadcast_empty_message(self):
        mock = Mock()
        gameRoom = GameRoom([mock])

        gameRoom.broadcast("")

        self.assertEqual(mock.send.call_count, 1)

    def test_broadcast_valid_message(self):
        mock = Mock()
        gameRoom = GameRoom([mock])

        gameRoom.broadcast("game started!")

        self.assertEqual(mock.send.call_count, 1)

    def test_broadcast_two_players(self):
        mock1 = Mock()
        mock2 = Mock()
        gameRoom = GameRoom([mock1, mock2])

        gameRoom.broadcast("game started!")

        self.assertEqual(mock1.send.call_count, 1)
        self.assertEqual(mock2.send.call_count, 1)

    def test_calculateStatistics_no_player(self):
        gameRoom = GameRoom([])

        res = gameRoom.calculateStatistics("A")

        self.assertEqual(res, "")

    def test_calculateStatistics_one_player_correct(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock1])
        gameRoom.setResponseFromPlayer(0)

        res = gameRoom.calculateStatistics("A")

        self.assertEqual(res, "Answer is A (A: 100.0% B: 0.0% C: 0.0% D: 0.0% Skipped: 0.0%)")

    def test_calculateStatistics_one_player_incorrect(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        gameRoom = GameRoom([mock1])
        gameRoom.setResponseFromPlayer(0)

        res = gameRoom.calculateStatistics("D")

        self.assertEqual(res, "Answer is D (A: 100.0% B: 0.0% C: 0.0% D: 0.0% Skipped: 0.0%)")
        
    def test_calculateStatistics_one_player_invalid_input(self):
        mock1 = Mock()
        mock1.recv.return_value = "123124adfad".encode()
        gameRoom = GameRoom([mock1])
        gameRoom.setResponseFromPlayer(0)

        res = gameRoom.calculateStatistics("D")

        self.assertEqual(res, "Answer is D (A: 0.0% B: 0.0% C: 0.0% D: 0.0% Skipped: 100.0%)")

    def test_calculateStatistics_two_players_incorrect(self):
        mock1 = Mock()
        mock1.recv.return_value = "A".encode()
        mock2 = Mock()
        mock2.recv.return_value = "B".encode()
        gameRoom = GameRoom([mock1, mock2])
        gameRoom.setResponseFromPlayer(0)
        gameRoom.setResponseFromPlayer(1)

        res = gameRoom.calculateStatistics("D")

        self.assertEqual(res, "Answer is D (A: 50.0% B: 50.0% C: 0.0% D: 0.0% Skipped: 0.0%)")

    def test_calculateStatistics_two_players_correct(self):
        mock1 = Mock()
        mock1.recv.return_value = "D".encode()
        mock2 = Mock()
        mock2.recv.return_value = "D".encode()
        gameRoom = GameRoom([mock1, mock2])
        gameRoom.setResponseFromPlayer(0)
        gameRoom.setResponseFromPlayer(1)

        res = gameRoom.calculateStatistics("D")

        self.assertEqual(res, "Answer is D (A: 0.0% B: 0.0% C: 0.0% D: 100.0% Skipped: 0.0%)")

if __name__ == '__main__':
    unittest.main()