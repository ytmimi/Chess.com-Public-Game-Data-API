import os
import sys
import re
import random

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(path, 'chess_com'))

import settings

import unittest


class Test_Regex_Settings(unittest.TestCase):
	'''
	Tests that the Regex's defined in the settings module match
	their inteded pattern.
	'''
	#The board
	def test_file(self):
		for file in 'abcdefgh':
			self.assertTrue(re.match(settings.FILE, file))

	def test_rank(self):
		for rank in range(1, 9):
			self.assertTrue(re.match(settings.RANK, f'{rank}'))

	def test_square(self):
		for letter in 'abcdefgh':
			for i in range(1,9):
				square = f'{letter}{i}'
				self.assertTrue(re.match(settings.SQUARE, square))

	#basic moves
	def test_promote(self):
		for letter in 'abcdefgh':
			for piece in 'QRNB':
				for num in [1,8]:
					promote = f'{letter}{num}={piece}'
					self.assertTrue(re.match(settings.PROMOTE, promote))

	def test_piece_move(self):
		for letter in 'abcdefgh':
			for piece in 'KQRNB':
				for num in range(1, 9):
					move = f'{piece}{letter}{num}'
					self.assertTrue(re.match(settings.PIECE_MOVE, move ))

	def test_pawn_move(self):
		for letter in 'abcdefgh':
			for num in range(2,8):
				move = f'{letter}{num}'
				self.assertTrue(re.match(settings.PAWN_MOVE, move ))

	def test_king_side_castle(self):
		self.assertTrue(re.match(settings.KING_CASTLE, 'O-O'))

	def test_queen_side_castle(self):
		self.assertTrue(re.match(settings.QUEEN_CASTLE, 'O-O-O'))

	#Basic Captures
	def test_peice_capture(self):
		for file in 'abcdefgh':
			for piece in 'KQRNB':
				for num in range(1,9):
					cap = f'{piece}x{file}{num}'
					self.assertTrue(re.match(settings.PIECE_CAPTURE, cap))

	def test_pawn_capture(self):
		files = 'abcdefgh'
		for i, file in enumerate(files):
			for num in range(1,9):
				if file !='h':
					cap = f'{file}x{files[i+1]}{num}'
					self.assertTrue(re.match(settings.PAWN_CAPTURE, cap))
		for i, file in enumerate(file[::-1]):
			for num in range(1,9):
				if file !='a':
					cap = f'{file}x{files[i+1]}{num}'
					self.assertTrue(re.match(settings.PAWN_CAPTURE, cap))

	#Ambiguous moves and captures
	def test_piece_file_move(self):
		'''test ambiguous moves, where more clarification is needed by adding the file
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for piece in 'QRNB':
			for num in range(1,9):
				move = f'{piece}ab{num}'
				self.assertTrue(re.match(settings.PIECE_FILE_MOVE, move))

	def test_piece_rank_move(self):
		'''test ambiguous moves, where more clarification is needed by adding the rank
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}2f{num}'
				self.assertTrue(re.match(settings.PIECE_RANK_MOVE, move))

	def test_piece_file_rank_move(self):
		'''test ambiguous moves, where more clarification is needed by adding the file and rank
		not all moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}d2f{num}'
				self.assertTrue(re.match(settings.PIECE_FILE_RANK_MOVE, move))

	def test_piece_file_capture(self):
		'''test ambiguous moves, where more clarification is needed by adding the file
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for piece in 'QRNB':
			for num in range(1,9):
				move = f'{piece}axb{num}'
				self.assertTrue(re.match(settings.PIECE_FILE_CAPTURE, move))

	def test_piece_rank_capture(self):
		'''test ambiguous moves, where more clarification is needed by adding the rank
		not all  moves test may be legal, but its important to test for the general patter
		to make sure our regular expression can catch these moves
		'''
		for peice in 'QRNB':
			for num in range(1,9):
				move = f'{peice}2xf{num}'
				self.assertTrue(re.match(settings.PIECE_RANK_CAPTURE, move))

class Test_Other_Settings(unittest.TestCase):
	def test_Game_results(self):
		self.assertIsInstance(settings.GAME_RESULTS, dict)
		#some example codes
		self.assertEqual(settings.GAME_RESULTS['win'], 'Win')
		self.assertEqual(settings.GAME_RESULTS['repetition'],'Draw by repetition')
		self.assertEqual(settings.GAME_RESULTS['insufficient'],'Insufficient material')
		self.assertEqual(settings.GAME_RESULTS['50move'],'Draw by 50-move rule')
		self.assertEqual(settings.GAME_RESULTS['abandoned'],'Abandoned')
		self.assertEqual(settings.GAME_RESULTS['bughousepartnerlose'],'Bughouse partner lost')


	def test_Country_Codes(self):
		test_country_dict = {'XA':'Canary Islands', 'XB':'Basque Country',
				'XC':'Catalonia', 'XE':'England', 'XG':'Galicia',
				'XK':'Kosovo', 'XP':'Palestine', 'XS':'Scotland',
				'XW' : 'Wales', 'XX':'International',
			}
		self.assertIsInstance(settings.COUNTRY_CODES, dict)
		for key in test_country_dict.keys():
			self.assertEqual(test_country_dict[key], settings.COUNTRY_CODES[key])


if __name__ == '__main__':
	unittest.main()