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

if __name__ == '__main__':
    unittest.main()