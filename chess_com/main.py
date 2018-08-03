import os
import csv
from process_data import pgn_to_dict, player_nationality
from chess_api import archived_games, monthly_games 
from settings import (USERNAME, CSV_DIR, GAME_RESULTS, COUNTRY_CODES, 
						ARCHIVE_ENDPOINT, NATIONALLITY_FILE, GAME_DATA_FILE)

def load_player_nationality():
	if NATIONALLITY_FILE in os.listdir(CSV_DIR):
		player_nat_dict = {}
		with open(os.path.join(CSV_DIR, NATIONALLITY_FILE), 'r') as player_nat:
			file_reader = csv.reader(player_nat,)
			for row in file_reader:
				player_nat_dict[row[0]] = row[1]
		return player_nat_dict
	else: return {}

def store_player_nationality(player_nationality: dict):
	with open(os.path.join(CSV_DIR, NATIONALLITY_FILE), 'w') as player_nat:
		file_writer = csv.writer(player_nat)
		for key, value in player_nationality.items():
			file_writer.writerow([key, value])

def store_game_data(game_data: dict):
	with open(os.path.join(CSV_DIR, GAME_DATA_FILE), 'w') as games:
		file_writer = csv.writer(games)
		headers = list(game_data.keys())
		file_writer.writerow(headers)
		for i in range(len(game_data[headers[0]])):
			row = []
			for header in headers:
				row.append(game_data[header][i])
			file_writer.writerow(row)

def sort_player_and_opponent(white: dict, black: dict):
	''' 
	Adds a new key 'side', to each dictonary
	returns a tuple (player, opponent) based on which had white and black
	'''
	white['side'] = 'White'
	black['side'] = 'Black'
	if white['username'].lower() == USERNAME.lower():
		return white, black		
	return black, white


def set_data_values(data: dict, player: dict, opponent: dict, pgn_dict: dict):
	''' '''
	data['Player'].append(player['username'])
	data['Player Rating'].append(player['rating'])
	data['Player Nationality'].append(player['nationality'])
	data['Player Side'].append(player['side'])
	data['Player Result'].append(GAME_RESULTS[player['result']])
	data['Player First Move'].append(pgn_dict['Moves'][1][player['side'][0]])
	
	data['Opponent'].append(opponent['username'])
	data['Opponent Rating'].append(opponent['rating'])
	data['Opponent Nationality'].append(opponent['nationality'])
	data['Opponent Side'].append(opponent['side'])
	data['Opponent Result'].append(GAME_RESULTS[opponent['result']])
	data['Opponent First Move'].append(pgn_dict['Moves'][1][opponent['side'][0]])
	
	data['Variation'].append(pgn_dict['Variation'])
	data['Termination'].append(pgn_dict['Termination'])
	data['Moves'].append(max(pgn_dict['Moves'].keys()))
	data['Date'].append(pgn_dict['EndDate'])



if __name__ == '__main__':
	nationality_dict = load_player_nationality()
	all_data ={
		'Player':[],'Player Rating':[],'Player Nationality':[],
		'Player Side':[],'Player Result':[],'Player First Move':[],
		'Opponent':[],'Opponent Rating':[],'Opponent Nationality':[],
		'Opponent Side':[],'Opponent Result':[],'Opponent First Move':[],
		'Variation':[],'Termination':[],'Moves':[],'Date':[],
	}
	
	for url in archived_games(ARCHIVE_ENDPOINT):
		for games in monthly_games(url):
			player, opponent = sort_player_and_opponent(games['white'], games['black'])
			player = player_nationality(COUNTRY_CODES, nationality_dict, player)
			opponent = player_nationality(COUNTRY_CODES, nationality_dict, opponent)
			pgn = pgn_to_dict(games['pgn'])
			set_data_values(all_data, player, opponent, pgn)
	store_game_data(all_data)
	store_player_nationality(nationality_dict)

