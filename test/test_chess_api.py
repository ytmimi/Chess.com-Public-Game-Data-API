import os
import sys
import re
import random

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(path, 'chess_com'))

from chess_api import archived_games, monthly_games, player_info, chess_com_data
from settings import LIVE_TEST, USERNAME

import unittest

@unittest.skipIf(not LIVE_TEST, 'Set LIVE_TEST to True in settings.py to run these test')
class Test_Live_API(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.archive_endpoint=f'https://api.chess.com/pub/player/{USERNAME}/games/archives'
		cls.monthly_endpoint= chess_com_data(cls.archive_endpoint)['archives'][-1]
		cls.player_endpoint=f'https://api.chess.com/pub/player/{USERNAME}'

	def test_archived_games(self):
		api_data = archived_games(self.archive_endpoint)
		self.assertIsInstance(api_data, list)
		for item in api_data:
			self.assertIsInstance(item, str)
		self.assertIn(self.monthly_endpoint, api_data)

	def test_monthly_games(self):
		api_data = monthly_games(self.monthly_endpoint)
		self.assertIsInstance(api_data, list)
		for item in api_data:
			self.assertIsInstance(api_data[0], dict)
		
	def test_player_info(self):
		api_data = player_info(self.player_endpoint)
		self.assertIsInstance(api_data, dict)
		
		
if __name__ == '__main__':
	unittest.main()