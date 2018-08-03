import os
import sys
import re

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(path, 'chess_com'))

from chess_api import chess_com_data
import process_data
import settings
import unittest



class Test_Check_and_Checkmate(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.re_list = [
			settings.PROMOTE, settings.PIECE_MOVE, settings.PAWN_MOVE, settings.PIECE_FILE_MOVE,
			settings.PIECE_RANK_MOVE, settings.PIECE_FILE_RANK_MOVE, settings.PIECE_CAPTURE,
			settings.PAWN_CAPTURE, settings.PIECE_FILE_CAPTURE, settings.PIECE_RANK_CAPTURE,
			settings.KING_CASTLE, settings.QUEEN_CASTLE
		]
		#examples of each kind of move/capture based on the order of cls.re_list
		cls.example_list = [
			'h1=Q', 'Qb3', 'e4', 'Ndf5', 'N6f4', 'Nb3d4', 'Bxf7',
			'exd4', 'Rfxd8', 'N6xd5', 'O-O', 'O-O-O',]

	def test_check_checkmat_move(self):
		for re_str, move in zip(self.re_list, self.example_list):
			new_re = process_data.check_checkmate_move(re_str)
			self.assertTrue(re.match(new_re, f'{move}'))
			self.assertTrue(re.match(new_re, f'{move}+'))
			self.assertTrue(re.match(new_re, f'{move}#'))


class Test_Find_Moves(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.no_timestamp = '1. d4 d5 2. Nc3 c6 3. e4 Nf6 4. Bd3 Bg4 5. Nf3 e6 6. e5 Nfd7 7. Bg5 f6 8. h3 Bf5 9. Bxf5 exf5 10. e6 fxg5 11. exd7+ Nxd7 12. Qe2+ Be7 13. O-O-O O-O 14. Rhe1 Bd6 15. Nxg5 Qxg5+ 16. Kb1 Qg6 17. f3 Nf6 18. Qe6+ Kh8 19. Qxd6 Rae8 20. b3 Qxg2 21. Ne2 Qxf3 22. Nf4 Ne4 23. Rxe4 Qxd1+ 24. Kb2 Rg8 25. Rxe8 Rxe8 26. Qd7 Rg8 27. Qf7 Qxd4+ 28. Ka3 0-1'
		cls.no_timestamp_lst = ['d4', 'd5', 'Nc3', 'c6', 'e4', 'Nf6', 'Bd3', 'Bg4', 'Nf3', 'e6', 'e5', 'Nfd7', 'Bg5', 'f6', 'h3', 'Bf5', 'Bxf5', 'exf5', 'e6', 'fxg5', 'exd7+', 'Nxd7', 'Qe2+', 'Be7', 'O-O-O', 'O-O', 'Rhe1', 'Bd6', 'Nxg5', 'Qxg5+', 'Kb1', 'Qg6', 'f3', 'Nf6', 'Qe6+', 'Kh8', 'Qxd6', 'Rae8', 'b3', 'Qxg2', 'Ne2', 'Qxf3', 'Nf4', 'Ne4', 'Rxe4', 'Qxd1+', 'Kb2', 'Rg8', 'Rxe8', 'Rxe8', 'Qd7', 'Rg8', 'Qf7', 'Qxd4+', 'Ka3',]
		cls.no_timestamp_dict = {1.0: {'W': 'd4', 'B': 'd5'}, 2.0: {'W': 'Nc3', 'B': 'c6'}, 3.0: {'W': 'e4', 'B': 'Nf6'}, 4.0: {'W': 'Bd3', 'B': 'Bg4'}, 5.0: {'W': 'Nf3', 'B': 'e6'}, 6.0: {'W': 'e5', 'B': 'Nfd7'}, 7.0: {'W': 'Bg5', 'B': 'f6'}, 8.0: {'W': 'h3', 'B': 'Bf5'}, 9.0: {'W': 'Bxf5', 'B': 'exf5'}, 10.0: {'W': 'e6', 'B': 'fxg5'}, 11.0: {'W': 'exd7+', 'B': 'Nxd7'}, 12.0: {'W': 'Qe2+', 'B': 'Be7'}, 13.0: {'W': 'O-O-O', 'B': 'O-O'}, 14.0: {'W': 'Rhe1', 'B': 'Bd6'}, 15.0: {'W': 'Nxg5', 'B': 'Qxg5+'}, 16.0: {'W': 'Kb1', 'B': 'Qg6'}, 17.0: {'W': 'f3', 'B': 'Nf6'}, 18.0: {'W': 'Qe6+', 'B': 'Kh8'}, 19.0: {'W': 'Qxd6', 'B': 'Rae8'}, 20.0: {'W': 'b3', 'B': 'Qxg2'}, 21.0: {'W': 'Ne2', 'B': 'Qxf3'}, 22.0: {'W': 'Nf4', 'B': 'Ne4'}, 23.0: {'W': 'Rxe4', 'B': 'Qxd1+'}, 24.0: {'W': 'Kb2', 'B': 'Rg8'}, 25.0: {'W': 'Rxe8', 'B': 'Rxe8'}, 26.0: {'W': 'Qd7', 'B': 'Rg8'}, 27.0: {'W': 'Qf7', 'B': 'Qxd4+'}, 28.0: {'W': 'Ka3', 'B': '-'}}
		cls.timestamp = '1. e4 {[%clk 0:09:59.2]} 1... c5 {[%clk 0:09:57.1]} 2. Nc3 {[%clk 0:09:55.8]} 2... Nc6 {[%clk 0:09:55.7]} 3. Nf3 {[%clk 0:09:52.2]} 3... d6 {[%clk 0:09:53.7]} 4. d4 {[%clk 0:09:46.7]} 4... cxd4 {[%clk 0:09:50]} 5. Nxd4 {[%clk 0:09:44.8]} 5... Nf6 {[%clk 0:09:14.1]} 6. Bb5 {[%clk 0:09:41.6]} 6... Bd7 {[%clk 0:08:10.7]} 7. O-O {[%clk 0:09:29.9]} 7... Qb6 {[%clk 0:08:05]} 8. Be3 {[%clk 0:09:13.6]} 8... Ng4 {[%clk 0:07:57.1]} 9. Qxg4 {[%clk 0:09:10.1]} 9... Bxg4 {[%clk 0:07:52.6]} 10. Ne6 {[%clk 0:09:02.3]} 10... Qxe3 {[%clk 0:07:30]} 11. fxe3 {[%clk 0:08:45.6]} 11... fxe6 {[%clk 0:07:28.6]} 12. Rad1 {[%clk 0:08:38.9]} 12... Bxd1 {[%clk 0:07:14.7]} 13. Rxd1 {[%clk 0:08:36.6]} 13... O-O-O {[%clk 0:07:09.3]} 14. Bc4 {[%clk 0:08:04.1]} 14... e5 {[%clk 0:06:38.9]} 15. Be6+ {[%clk 0:07:36.6]} 15... Kb8 {[%clk 0:06:34.5]} 16. g4 {[%clk 0:07:23.9]} 16... g6 {[%clk 0:06:31.3]} 17. Nb5 {[%clk 0:07:21.3]} 17... Bh6 {[%clk 0:06:23.5]} 18. Re1 {[%clk 0:07:03.1]} 18... Rhf8 {[%clk 0:06:19.6]} 19. h4 {[%clk 0:06:51.9]} 19... Rf6 {[%clk 0:06:16.8]} 20. Bd5 {[%clk 0:06:46.9]} 20... g5 {[%clk 0:06:09.6]} 21. hxg5 {[%clk 0:06:42.5]} 21... Bxg5 {[%clk 0:06:08]} 22. Nc3 {[%clk 0:06:36.1]} 22... Nb4 {[%clk 0:05:45]} 23. Bb3 {[%clk 0:06:15.8]} 23... Rdf8 {[%clk 0:05:37.9]} 24. a3 {[%clk 0:06:12]} 24... Na6 {[%clk 0:05:12.8]} 25. Re2 {[%clk 0:05:47.8]} 25... Nc5 {[%clk 0:05:00.8]} 26. Nd5 {[%clk 0:05:45.1]} 26... Rh6 {[%clk 0:04:40.4]} 27. Rh2 {[%clk 0:05:22.9]} 27... Rxh2 {[%clk 0:04:23.6]} 28. Kxh2 {[%clk 0:05:19.7]} 28... Nxe4 {[%clk 0:04:21.3]} 29. Nc3 {[%clk 0:04:53.4]} 29... Nxc3 {[%clk 0:04:15.6]} 30. bxc3 {[%clk 0:04:52.1]} 30... Bxe3 {[%clk 0:04:13.5]} 31. c4 {[%clk 0:04:49.3]} 31... Bc5 {[%clk 0:04:06.1]} 32. Ba2 {[%clk 0:04:45.8]} 32... e4 {[%clk 0:04:02.7]} 33. Bb1 {[%clk 0:04:40.7]} 33... e3 {[%clk 0:04:01.6]} 34. c3 {[%clk 0:04:39.5]} 34... e2 {[%clk 0:04:00.9]} 35. Be4 {[%clk 0:04:33.5]} 35... e1=Q {[%clk 0:03:54.4]} 36. Bf5 {[%clk 0:04:31.9]} 36... Rxf5 {[%clk 0:03:42.8]} 37. gxf5 {[%clk 0:04:30.5]} 37... Qh4+ {[%clk 0:03:41]} 38. Kg2 {[%clk 0:04:29.1]} 38... Qg4+ {[%clk 0:03:39.9]} 39. Kf1 {[%clk 0:04:27.6]} 39... Qxf5+ {[%clk 0:03:38.6]} 40. Ke2 {[%clk 0:04:26.3]} 40... h5 {[%clk 0:03:32.1]} 41. Kd1 {[%clk 0:04:22.6]} 41... h4 {[%clk 0:03:31.3]} 42. Kc1 {[%clk 0:04:20.5]} 42... h3 {[%clk 0:03:30]} 43. Kb2 {[%clk 0:04:19.7]} 43... Bxa3+ {[%clk 0:03:08]} 44. Ka2 {[%clk 0:04:18.6]} 44... Bc1 {[%clk 0:03:02.5]} 45. Kb3 {[%clk 0:04:16.1]} 45... d5 {[%clk 0:02:45.4]} 46. cxd5 {[%clk 0:04:13.7]} 46... Qxd5+ {[%clk 0:02:44]} 47. Kc2 {[%clk 0:04:12.7]} 47... h2 {[%clk 0:02:42.3]} 48. Kxc1 {[%clk 0:04:11.3]} 48... h1=Q+ {[%clk 0:02:41.1]} 49. Kc2 {[%clk 0:04:10.3]} 49... a5 {[%clk 0:02:37.7]} 50. Kb2 {[%clk 0:04:08.1]} 50... a4 {[%clk 0:02:36]} 51. Ka3 {[%clk 0:04:07.6]} 51... Qb3# {[%clk 0:02:34.4]} 0-1'
		cls.timestamp_lst = ['e4', 'c5', 'Nc3', 'Nc6', 'Nf3', 'd6', 'd4', 'cxd4', 'Nxd4', 'Nf6', 'Bb5', 'Bd7', 'O-O', 'Qb6', 'Be3', 'Ng4', 'Qxg4', 'Bxg4', 'Ne6', 'Qxe3', 'fxe3', 'fxe6', 'Rad1', 'Bxd1', 'Rxd1', 'O-O-O', 'Bc4', 'e5', 'Be6+', 'Kb8', 'g4', 'g6', 'Nb5', 'Bh6', 'Re1', 'Rhf8', 'h4', 'Rf6', 'Bd5', 'g5', 'hxg5', 'Bxg5', 'Nc3', 'Nb4', 'Bb3', 'Rdf8', 'a3', 'Na6', 'Re2', 'Nc5', 'Nd5', 'Rh6', 'Rh2', 'Rxh2', 'Kxh2', 'Nxe4', 'Nc3', 'Nxc3', 'bxc3', 'Bxe3', 'c4', 'Bc5', 'Ba2', 'e4', 'Bb1', 'e3', 'c3', 'e2', 'Be4', 'e1=Q', 'Bf5', 'Rxf5', 'gxf5', 'Qh4+', 'Kg2', 'Qg4+', 'Kf1', 'Qxf5+', 'Ke2', 'h5', 'Kd1', 'h4', 'Kc1', 'h3', 'Kb2', 'Bxa3+', 'Ka2', 'Bc1', 'Kb3', 'd5', 'cxd5', 'Qxd5+', 'Kc2', 'h2', 'Kxc1', 'h1=Q+', 'Kc2', 'a5', 'Kb2', 'a4', 'Ka3', 'Qb3#']
		cls.timestamp_dict = {1.0: {'W': 'e4', 'B': 'c5'}, 2.0: {'W': 'Nc3', 'B': 'Nc6'}, 3.0: {'W': 'Nf3', 'B': 'd6'}, 4.0: {'W': 'd4', 'B': 'cxd4'}, 5.0: {'W': 'Nxd4', 'B': 'Nf6'}, 6.0: {'W': 'Bb5', 'B': 'Bd7'}, 7.0: {'W': 'O-O', 'B': 'Qb6'}, 8.0: {'W': 'Be3', 'B': 'Ng4'}, 9.0: {'W': 'Qxg4', 'B': 'Bxg4'}, 10.0: {'W': 'Ne6', 'B': 'Qxe3'}, 11.0: {'W': 'fxe3', 'B': 'fxe6'}, 12.0: {'W': 'Rad1', 'B': 'Bxd1'}, 13.0: {'W': 'Rxd1', 'B': 'O-O-O'}, 14.0: {'W': 'Bc4', 'B': 'e5'}, 15.0: {'W': 'Be6+', 'B': 'Kb8'}, 16.0: {'W': 'g4', 'B': 'g6'}, 17.0: {'W': 'Nb5', 'B': 'Bh6'}, 18.0: {'W': 'Re1', 'B': 'Rhf8'}, 19.0: {'W': 'h4', 'B': 'Rf6'}, 20.0: {'W': 'Bd5', 'B': 'g5'}, 21.0: {'W': 'hxg5', 'B': 'Bxg5'}, 22.0: {'W': 'Nc3', 'B': 'Nb4'}, 23.0: {'W': 'Bb3', 'B': 'Rdf8'}, 24.0: {'W': 'a3', 'B': 'Na6'}, 25.0: {'W': 'Re2', 'B': 'Nc5'}, 26.0: {'W': 'Nd5', 'B': 'Rh6'}, 27.0: {'W': 'Rh2', 'B': 'Rxh2'}, 28.0: {'W': 'Kxh2', 'B': 'Nxe4'}, 29.0: {'W': 'Nc3', 'B': 'Nxc3'}, 30.0: {'W': 'bxc3', 'B': 'Bxe3'}, 31.0: {'W': 'c4', 'B': 'Bc5'}, 32.0: {'W': 'Ba2', 'B': 'e4'}, 33.0: {'W': 'Bb1', 'B': 'e3'}, 34.0: {'W': 'c3', 'B': 'e2'}, 35.0: {'W': 'Be4', 'B': 'e1=Q'}, 36.0: {'W': 'Bf5', 'B': 'Rxf5'}, 37.0: {'W': 'gxf5', 'B': 'Qh4+'}, 38.0: {'W': 'Kg2', 'B': 'Qg4+'}, 39.0: {'W': 'Kf1', 'B': 'Qxf5+'}, 40.0: {'W': 'Ke2', 'B': 'h5'}, 41.0: {'W': 'Kd1', 'B': 'h4'}, 42.0: {'W': 'Kc1', 'B': 'h3'}, 43.0: {'W': 'Kb2', 'B': 'Bxa3+'}, 44.0: {'W': 'Ka2', 'B': 'Bc1'}, 45.0: {'W': 'Kb3', 'B': 'd5'}, 46.0: {'W': 'cxd5', 'B': 'Qxd5+'}, 47.0: {'W': 'Kc2', 'B': 'h2'}, 48.0: {'W': 'Kxc1', 'B': 'h1=Q+'}, 49.0: {'W': 'Kc2', 'B': 'a5'}, 50.0: {'W': 'Kb2', 'B': 'a4'}, 51.0: {'W': 'Ka3', 'B': 'Qb3#'}}
	
	def test_no_timestamp(self):
		all_moves = re.findall(process_data.MOVE_RE, self.no_timestamp)
		self.assertEqual(len(all_moves), 55)
		self.assertEqual(all_moves, self.no_timestamp_lst)

	def test_timestamp(self):
		all_moves = re.findall(process_data.MOVE_RE, self.timestamp)
		self.assertEqual(len(all_moves), 102)
		self.assertEqual(all_moves, self.timestamp_lst)

	def test_move_index(self):
		self.assertEqual(process_data.move_index(0), 1)
		self.assertEqual(process_data.move_index(2), 2)
		self.assertEqual(process_data.move_index(4), 3)
		self.assertEqual(process_data.move_index(6), 4)

	def test_parse_chess_moves_no_timestamp(self):
		move_dict = process_data.parse_chess_moves(self.no_timestamp)
		self.assertEqual(move_dict, self.no_timestamp_dict)
		self.assertEqual(len(move_dict.keys()), 28)

	def test_parse_chess_moves_timestamp(self):
		move_dict = process_data.parse_chess_moves(self.timestamp)
		self.assertEqual(move_dict, self.timestamp_dict)
		self.assertEqual(len(move_dict.keys()), 51)



class Test_Format_Game_Data_mock(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.game_data = {   
			'url': 'https://www.chess.com/live/game/{game number}',
			'pgn': """[Event "Live Chess"]\n[Site "Chess.com"]\n[Date "2018.07.28"]\n[Round "-"]\n[White "username1"]\n[Black "username2"]\n[Result "0-1"]\n[ECO "B23"]\n[ECOUrl "https://www.chess.com/openings/{variation}"]\n[WhiteElo "1466"]\n[BlackElo "1402"]\n[TimeControl "600"]\n[Termination "username2 won by checkmate"]\n[StartTime "02:57:44"]\n[EndDate "2018.07.28"]\n[EndTime "02:57:44"]\n[Link "https://www.chess.com/live/game/{game number}"]\n\n1. e4 {[%clk 0:09:59.2]} 1... c5 {[%clk 0:09:57.1]} 2. Nc3 {[%clk 0:09:55.8]} 2... Nc6 {[%clk 0:09:55.7]} 3. Nf3 {[%clk 0:09:52.2]} 3... d6 {[%clk 0:09:53.7]} 4. d4 {[%clk 0:09:46.7]} 4... cxd4 {[%clk 0:09:50]} 5. Nxd4 {[%clk 0:09:44.8]} 5... Nf6 {[%clk 0:09:14.1]} 6. Bb5 {[%clk 0:09:41.6]} 6... Bd7 {[%clk 0:08:10.7]} 7. O-O {[%clk 0:09:29.9]} 7... Qb6 {[%clk 0:08:05]} 8. Be3 {[%clk 0:09:13.6]} 8... Ng4 {[%clk 0:07:57.1]} 9. Qxg4 {[%clk 0:09:10.1]} 9... Bxg4 {[%clk 0:07:52.6]} 10. Ne6 {[%clk 0:09:02.3]} 10... Qxe3 {[%clk 0:07:30]} 11. fxe3 {[%clk 0:08:45.6]} 11... fxe6 {[%clk 0:07:28.6]} 12. Rad1 {[%clk 0:08:38.9]} 12... Bxd1 {[%clk 0:07:14.7]} 13. Rxd1 {[%clk 0:08:36.6]} 13... O-O-O {[%clk 0:07:09.3]} 14. Bc4 {[%clk 0:08:04.1]} 14... e5 {[%clk 0:06:38.9]} 15. Be6+ {[%clk 0:07:36.6]} 15... Kb8 {[%clk 0:06:34.5]} 16. g4 {[%clk 0:07:23.9]} 16... g6 {[%clk 0:06:31.3]} 17. Nb5 {[%clk 0:07:21.3]} 17... Bh6 {[%clk 0:06:23.5]} 18. Re1 {[%clk 0:07:03.1]} 18... Rhf8 {[%clk 0:06:19.6]} 19. h4 {[%clk 0:06:51.9]} 19... Rf6 {[%clk 0:06:16.8]} 20. Bd5 {[%clk 0:06:46.9]} 20... g5 {[%clk 0:06:09.6]} 21. hxg5 {[%clk 0:06:42.5]} 21... Bxg5 {[%clk 0:06:08]} 22. Nc3 {[%clk 0:06:36.1]} 22... Nb4 {[%clk 0:05:45]} 23. Bb3 {[%clk 0:06:15.8]} 23... Rdf8 {[%clk 0:05:37.9]} 24. a3 {[%clk 0:06:12]} 24... Na6 {[%clk 0:05:12.8]} 25. Re2 {[%clk 0:05:47.8]} 25... Nc5 {[%clk 0:05:00.8]} 26. Nd5 {[%clk 0:05:45.1]} 26... Rh6 {[%clk 0:04:40.4]} 27. Rh2 {[%clk 0:05:22.9]} 27... Rxh2 {[%clk 0:04:23.6]} 28. Kxh2 {[%clk 0:05:19.7]} 28... Nxe4 {[%clk 0:04:21.3]} 29. Nc3 {[%clk 0:04:53.4]} 29... Nxc3 {[%clk 0:04:15.6]} 30. bxc3 {[%clk 0:04:52.1]} 30... Bxe3 {[%clk 0:04:13.5]} 31. c4 {[%clk 0:04:49.3]} 31... Bc5 {[%clk 0:04:06.1]} 32. Ba2 {[%clk 0:04:45.8]} 32... e4 {[%clk 0:04:02.7]} 33. Bb1 {[%clk 0:04:40.7]} 33... e3 {[%clk 0:04:01.6]} 34. c3 {[%clk 0:04:39.5]} 34... e2 {[%clk 0:04:00.9]} 35. Be4 {[%clk 0:04:33.5]} 35... e1=Q {[%clk 0:03:54.4]} 36. Bf5 {[%clk 0:04:31.9]} 36... Rxf5 {[%clk 0:03:42.8]} 37. gxf5 {[%clk 0:04:30.5]} 37... Qh4+ {[%clk 0:03:41]} 38. Kg2 {[%clk 0:04:29.1]} 38... Qg4+ {[%clk 0:03:39.9]} 39. Kf1 {[%clk 0:04:27.6]} 39... Qxf5+ {[%clk 0:03:38.6]} 40. Ke2 {[%clk 0:04:26.3]} 40... h5 {[%clk 0:03:32.1]} 41. Kd1 {[%clk 0:04:22.6]} 41... h4 {[%clk 0:03:31.3]} 42. Kc1 {[%clk 0:04:20.5]} 42... h3 {[%clk 0:03:30]} 43. Kb2 {[%clk 0:04:19.7]} 43... Bxa3+ {[%clk 0:03:08]} 44. Ka2 {[%clk 0:04:18.6]} 44... Bc1 {[%clk 0:03:02.5]} 45. Kb3 {[%clk 0:04:16.1]} 45... d5 {[%clk 0:02:45.4]} 46. cxd5 {[%clk 0:04:13.7]} 46... Qxd5+ {[%clk 0:02:44]} 47. Kc2 {[%clk 0:04:12.7]} 47... h2 {[%clk 0:02:42.3]} 48. Kxc1 {[%clk 0:04:11.3]} 48... h1=Q+ {[%clk 0:02:41.1]} 49. Kc2 {[%clk 0:04:10.3]} 49... a5 {[%clk 0:02:37.7]} 50. Kb2 {[%clk 0:04:08.1]} 50... a4 {[%clk 0:02:36]} 51. Ka3 {[%clk 0:04:07.6]} 51... Qb3# {[%clk 0:02:34.4]} 0-1""",
			'time_control': '600', 'end_time': 1532746664, 'rated': True, 'fen': '1k6/1p2p3/8/8/p7/KqP5/8/7q w - -', 
			'time_class': 'blitz', 'rules': 'chess', 
			'white': {
				'rating': 1432, 
				'result': 'checkmated',
				'@id':'https://api.chess.com/pub/player/username1',
				'username':'username1'
			}, 
			'black': {
				'rating': 1402, 
				'result': 'win', 
				'@id': 'https://api.chess.com/pub/player/username2',
				'username': 'username2'
			},
		}

	def test_pgn_to_dict(self):
		expected_keys = [
			'Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'ECO',
			'ECOUrl', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination',
			'StartTime', 'EndDate', 'EndTime', 'Link', 'Moves', 'Variation',]
		pgn_dict = process_data.pgn_to_dict(self.game_data['pgn'])
		self.assertIsInstance(pgn_dict, dict)
		for key in expected_keys:
			self.assertIn(key, pgn_dict.keys())

	def test_variatoin_from_url(self):
		example_var_url = 'https://www.chess.com/openings/C42-Petrovs-Defense-Three-Knights-Game'
		result = process_data.variation_from_url(example_var_url)
		self.assertEqual(result, 'Petrovs Defense Three Knights Game')

	def test_player_nationality(self):
		nationality = {'some_url/US':'United States'}
		player = {'@id':'some_url/US'}
		player = process_data.player_nationality(settings.COUNTRY_CODES, nationality, player)
		self.assertIn('nationality', player.keys())
		self.assertEqual(player['nationality'], 'United States')

	@unittest.skipIf(not settings.LIVE_TEST, 'Set LIVE_TEST to True in settings.py to run these test')
	def test_player_nationality_live(self):
		player_enpoint = f'https://api.chess.com/pub/player/{settings.USERNAME}' 
		#ENSURE THAT country IS THE SAME COUNTRY ASSOCIATED WITH THE USERNAME
		country = settings.COUNTRY_CODES[chess_com_data(player_enpoint)['country'].split('/')[-1]]
		nationality = {}
		player = {'@id':player_enpoint}
		player = process_data.player_nationality(settings.COUNTRY_CODES, nationality, player)
		self.assertIn('nationality', player.keys())
		self.assertEqual(player['nationality'], country)
		self.assertEqual(nationality[player_enpoint], country)



if __name__ == '__main__':
	unittest.main()