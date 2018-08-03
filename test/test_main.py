import os
import sys
import re

PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(PATH, 'chess_com'))

import main
from settings import NATIONALLITY_FILE, GAME_DATA_FILE, USERNAME

import unittest
from unittest import mock
from shutil import rmtree


TEST_PATH = os.path.join(PATH, 'test_files')


#patches the DIR_PATH variable so that Test can use a temporary directory
@mock.patch('main.CSV_DIR', new=TEST_PATH,)
class Test_File_Read_and_Write(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		os.makedirs(TEST_PATH, exist_ok=True)

	@classmethod
	def tearDownClass(cls):
		rmtree(TEST_PATH)

	def tearDown(cls):
		files = os.listdir(TEST_PATH)
		if len(files) > 0:
			for file in files:
				os.remove(os.path.join(TEST_PATH, file))

	def test_load_player_nationality_No_File(self):
		nationality = main.load_player_nationality()
		self.assertEqual(nationality, {})

	def test_load_player_nationality_File_Found(self):
		nationality = {'username1':'United States', 'username2': 'Germany'}
		main.store_player_nationality(nationality)
		self.assertIn(NATIONALLITY_FILE, os.listdir(TEST_PATH))
		loaded_nationality = main.load_player_nationality()
		self.assertEqual(loaded_nationality, nationality)


	def test_store_player_nationality(self):
		nationality = {'username1':'France', 'username2': 'Italy'}
		main.store_player_nationality(nationality)
		self.assertIn(NATIONALLITY_FILE, os.listdir(TEST_PATH))

	def test_store_game_data(self):
		#just a test. the actual game_data dictionary includes more fields
		game_data ={
			'Player':['username1', 'username1', 'username1'],
			'Player Rating':[900, 980, 1200],
			'Player Nationality':['US', 'US', 'US'],
		}
		main.store_game_data(game_data)
		self.assertIn(GAME_DATA_FILE, os.listdir(TEST_PATH))



#pathches the USERNAME variable to use a generic username: 'Player'
@mock.patch('main.USERNAME', new='Player',)
class Test_Sort_and_Store_Values(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.white1 = {'username':'Player'}
		cls.black1 = {'username':'Opponent'}
		cls.white2 = {'username':'Opponent'}
		cls.black2 = {'username':'Player'}

	def test_sort_player_and_opponent_white_black(self):
		player, opponent = main.sort_player_and_opponent(self.white1, self.black1)
		self.assertEqual(player['username'], 'Player')
		self.assertEqual(player['side'], 'White')
		self.assertEqual(opponent['username'], 'Opponent')
		self.assertEqual(opponent['side'], 'Black')

	def test_sort_player_and_opponent_black_white(self):
		player, opponent = main.sort_player_and_opponent(self.white2, self.black2)
		self.assertEqual(player['username'], 'Player')
		self.assertEqual(player['side'], 'Black')
		self.assertEqual(opponent['username'], 'Opponent')
		self.assertEqual(opponent['side'], 'White')

	@unittest.skip('Need to finish test')
	def test_set_data_values(self):
		pass



if __name__ == '__main__':
	unittest.main()