import os
import sys
import re
import random

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(path, 'chess_com'))

import process_data as gm

import unittest



class Test_base_re(unittest.TestCase):
	def test_file(self):
		for file in 'abcdefgh':
			self.assertTrue(re.match(gm.FILE, file))

	def test_rank(self):
		for rank in range(1, 9):
			self.assertTrue(re.match(gm.RANK, f'{rank}'))

	def test_square(self):
		for letter in 'abcdefgh':
			for i in range(1,9):
				square = f'{letter}{i}'
				self.assertTrue(re.match(gm.SQUARE, square))



class Test_basic_moves(unittest.TestCase):
	def test_promote(self):
		for letter in 'abcdefgh':
			for piece in 'QRNB':
				for num in [1,8]:
					promote = f'{letter}{num}={piece}'
					self.assertTrue(re.match(gm.PROMOTE, promote))

	def test_piece_move(self):
		for letter in 'abcdefgh':
			for piece in 'KQRNB':
				for num in range(1, 9):
					move = f'{piece}{letter}{num}'
					self.assertTrue(re.match(gm.PIECE_MOVE, move ))

	def test_pawn_move(self):
		for letter in 'abcdefgh':
			for num in range(2,8):
				move = f'{letter}{num}'
				self.assertTrue(re.match(gm.PAWN_MOVE, move ))

	def test_king_side_castle(self):
		self.assertTrue(re.match(gm.KING_CASTLE, 'O-O'))

	def test_queen_side_castle(self):
		self.assertTrue(re.match(gm.QUEEN_CASTLE, 'O-O-O'))



class Test_basic_captures(unittest.TestCase):
	def test_peice_capture(self):
		for file in 'abcdefgh':
			for piece in 'KQRNB':
				for num in range(1,9):
					cap = f'{piece}x{file}{num}'
					self.assertTrue(re.match(gm.PIECE_CAPTURE, cap))

	def test_pawn_capture(self):
		files = 'abcdefgh'
		for i, file in enumerate(files):
			for num in range(1,9):
				if file !='h':
					cap = f'{file}x{files[i+1]}{num}'
					self.assertTrue(re.match(gm.PAWN_CAPTURE, cap))
		for i, file in enumerate(file[::-1]):
			for num in range(1,9):
				if file !='a':
					cap = f'{file}x{files[i+1]}{num}'
					self.assertTrue(re.match(gm.PAWN_CAPTURE, cap))


class Test_Ambiguous_moves_and_captures(unittest.TestCase):
	def test_piece_file_move(self):
		'''test ambigous moves, where more clarification is needed by adding the file
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for piece in 'QRNB':
			for num in range(1,9):
				move = f'{piece}ab{num}'
				self.assertTrue(re.match(gm.PIECE_FILE_MOVE, move))

	def test_piece_rank_move(self):
		'''test ambigous moves, where more clarification is needed by adding the rank
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}2f{num}'
				self.assertTrue(re.match(gm.PIECE_RANK_MOVE, move))

	def test_piece_file_rank_move(self):
		'''test ambigous moves, where more clarification is needed by adding the file and rank
		not all moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}d2f{num}'
				self.assertTrue(re.match(gm.PIECE_FILE_RANK_MOVE, move))

	def test_piece_file_capture(self):
		'''test ambigous moves, where more clarification is needed by adding the file
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for piece in 'QRNB':
			for num in range(1,9):
				move = f'{piece}axb{num}'
				self.assertTrue(re.match(gm.PIECE_FILE_CAPTURE, move))

	def test_piece_rank_capture(self):
		'''test ambigous moves, where more clarification is needed by adding the rank
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}2xf{num}'
				self.assertTrue(re.match(gm.PIECE_RANK_CAPTURE, move))



class Test_Check_and_Checkmate(unittest.TestCase):
	'''
	class to test that if a move is made and it comes with check or checkmate
	that it is recognized by the appropriate regular expression
	'''
	@classmethod
	def setUpClass(cls):
		#examples of each kind of move/capture
		cls.promote = 'h1=Q'
		cls.piece_move = 'Qb3'
		cls.pawn_move = 'e4'
		cls.piece_file_move = 'Ndf5'
		cls.piece_rank_move = 'N6f4'
		cls.piece_file_rank_move = 'Nb3d4'
		cls.piece_capture = 'Bxf7'
		cls.pawn_capture = 'exd4'
		cls.piece_file_capture = 'Rfxd8'
		cls.piece_rank_capture = 'N6xd5'
		cls.king_castle = 'O-O'
		cls.queen_castle = 'O-O-O'
		cls.example_list = [
			cls.promote, cls.piece_move, cls.pawn_move, cls.piece_file_move,
			cls.piece_rank_move, cls.piece_file_rank_move, cls.piece_capture,
			cls.pawn_capture, cls.piece_file_capture, cls.piece_rank_capture,
			cls.king_castle, cls.queen_castle
		]
		cls.re_list = [
			gm.PROMOTE, gm.PIECE_MOVE, gm.PAWN_MOVE, gm.PIECE_FILE_MOVE,
			gm.PIECE_RANK_MOVE, gm.PIECE_FILE_RANK_MOVE, gm.PIECE_CAPTURE,
			gm.PAWN_CAPTURE, gm.PIECE_FILE_CAPTURE, gm.PIECE_RANK_CAPTURE,
			gm.KING_CASTLE, gm.QUEEN_CASTLE
		]

	def test_check_checkmate_move_function(self):
		for re_str in self.re_list:
			result = gm.check_checkmate_move(re_str)
			self.assertEqual(result, fr'{re_str}\+|{re_str}#|{re_str}')

	def test_check_checkmat_move(self):
		for re_str, move in zip(self.re_list, self.example_list):
			new_re = gm.check_checkmate_move(re_str)
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
		all_moves = re.findall(gm.MOVE_RE, self.no_timestamp)
		self.assertEqual(len(all_moves), 55)
		self.assertEqual(all_moves, self.no_timestamp_lst)

	def test_timestamp(self):
		all_moves = re.findall(gm.MOVE_RE, self.timestamp)
		self.assertEqual(len(all_moves), 102)
		self.assertEqual(all_moves, self.timestamp_lst)

	def test_move_index(self):
		self.assertEqual(gm.move_index(0), 1)
		self.assertEqual(gm.move_index(2), 2)
		self.assertEqual(gm.move_index(4), 3)
		self.assertEqual(gm.move_index(6), 4)

	def test_parse_chess_moves_no_timestamp(self):
		move_dict = gm.parse_chess_moves(self.no_timestamp)
		self.assertEqual(move_dict, self.no_timestamp_dict)
		self.assertEqual(len(move_dict.keys()), 28)

	def test_parse_chess_moves_timestamp(self):
		move_dict = gm.parse_chess_moves(self.timestamp)
		self.assertEqual(move_dict, self.timestamp_dict)
		self.assertEqual(len(move_dict.keys()), 51)




if __name__ == '__main__':
	unittest.main()