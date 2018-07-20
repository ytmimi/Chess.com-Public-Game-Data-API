import os
import csv
from requests_html import HTMLSession
import pandas as pd
import numpy as np
import json
import game_move as gm


'''
HTTP Responses from Chess.com
200 = "enjoy your JSON"
301 = if the URL you requested is bad, but we know where it should be; your client should remember and correct this to use the new URL in future requests
304 = if your client supports "ETag/If-None-Match" or "Last-Modified/If-Modified-Since" caching headers and the data have not changed since the last request
404 = we try to tell you if the URL is malformed or the data requested is just not available (e.g., a username for a user that does not exist)
410 = we know for certain that no data will ever be available at the URL you requested; your client should not request this URL again
429 = we are refusing to interpret your request due to rate limits; see "Rate Limiting" above
'''

session = HTMLSession()
USERNAME = os.environ['USERNAME']

game_results_codes = {
	'win':'Win', 'checkmated':'Checkmated', 'agreed':'Draw agreed',
	'repetition':'Draw by repetition', 'timeout':'Timeout', 'resigned':'Resigned',
	'stalemate':'Stalemate', 'lose':'Lose', 'insufficient':'Insufficient material',
	'50move':'Draw by 50-move rule', 'abandoned':'Abandoned', 'kingofthehill':'Opponent King reached the hill',
	'threecheck':'Checked for the 3rd time', 'timevsinsufficient':'Draw by timeout vs insufficient material',
	'bughousepartnerlose':'Bughouse partner lost'
}

def country_code_dict():
	country_dict = {}
	with open('country_code.csv', 'r') as country:
		file_reader = csv.reader(country,)
		for i, row in enumerate(file_reader):
			if i != 0:
				country_dict[row[0]] = row[1]
	return country_dict

coutry_codes = country_code_dict()

def convert_result_code(code):
	return game_results_codes[code]

def get_chess_com_data(url):
	response = session.get(url)
	return json.loads(response.html.html)

def get_archived_game_enpoints(username):
	''' 
	returns a list of api endpoints for the users game history
	''' 
	url = f'https://api.chess.com/pub/player/{username}/games/archives'
	return get_chess_com_data(url)['archives']

def profile_info_from_username(username):
	'''
	returns a dicionary with the following keys:
	['player_id', '@id', 'url', 'name', 'username', 'followers', 
	'country', 'location', 'last_online', 'joined', 'status', 'is_streamer']
	'''
	url = f'https://api.chess.com/pub/player/{username}'
	return get_chess_com_data(url)

def profile_info_from_endpoint(url):
	'''
	url: https://api.chess.com/pub/player/{username}

	returns a dicionary with the following keys:
	['player_id', '@id', 'url', 'name', 'username', 'followers', 
	'country', 'location', 'last_online', 'joined', 'status', 'is_streamer']
	'''
	return get_chess_com_data(url)

def historical_game_list(archived_endpoint):
	'''
	returns a list of game information.
	each list item is a dict with the following keys:
	['url', 'pgn', 'time_control', 'end_time', 'rated', 'fen', 
	'start_time', 'time_class', 'rules', 'white', 'black']
	most useful keys are 'black', 'white', 'pgn'
	'''
	return get_chess_com_data(archived_endpoint)['games']

def strip_brackets(string):
	return string.replace('[', '').replace(']','')

def strip_quotes(string):
	return string.replace('"', '')

def process_pgn(pgn_data):
	''' 
	returns a dict where the keys are:
	['Event', 'Site', 'Date', 'Round', 'White', 'Black', 
	'Result', 'ECO', 'ECOUrl', 'WhiteElo', 'BlackElo', 
	'TimeControl', 'Termination', 'StartTime', 
	'EndDate', 'EndTime', 'Link', 'Moves']
	'''
	pgn_data = pgn_data.split('\n')
	pgn_info = {}
	for item in pgn_data[:-2]:
		data = strip_brackets(item).split('"')
		key = data[0].strip()
		value = strip_quotes(data[1])
		pgn_info[key] = value
	all_moves = gm.move_dict(pgn_data[-1])
	print(all_moves)
	pgn_info['Moves'] = max(all_moves.keys())
	pgn_info['Opening Moves'] = all_moves[1]
	return pgn_info


def sort_player_and_opponent(white, black):
	''' 
	figures out which player is associated with which piece color.
	white: should be the white dict from historical game data
	black: should be the black dict from historical game data
	'''
	if white['username'].lower() == USERNAME:
		player = white
		player['side'] = 'White'
		opponent = black
		opponent['side'] = 'Black'
	else:
		player = black
		player['side'] = 'Black'
		opponent = white
		opponent['side'] = 'White'
	return player, opponent

def set_player_nationality_dict():
	path = os.path.abspath(__file__)
	if 'nationality.csv' in os.listdir(os.path.dirname(path)):
		player_nat_dict = {}
		with open('nationality.csv', 'r') as player_nat:
			file_reader = csv.reader(player_nat,)
			for i, row in enumerate(file_reader):
					player_nat_dict[row[0]] = row[1]
		return player_nat_dict
	else: return {}

player_nationality = set_player_nationality_dict()

def country_from_url(country_url):
	return country_url.split('/')[-1]

def set_player_nationality(player_dict):
	player_enpoint = player_dict['@id']
	if player_enpoint in player_nationality.keys():
		player_dict['nationality'] = player_nationality[player_enpoint]
	else:
		try:
			country = profile_info_from_endpoint(player_dict['@id'])['country']
			country = coutry_codes[country_from_url(country)]
		except Exception as e:
			country = country_from_url(country)
		player_dict['nationality'] = country
		player_nationality[player_enpoint] = country
	return player_dict

def variation_from_url(variation_url):
	variation_str = variation_url.split('/')[-1]
	variat_lst = variation_str.split('-')[1:]
	return ' '.join(variat_lst)

def set_data_values(player, opponent, pgn_dict):
	# player, opponent, and pgn_dict are all dicts
	player_data_dict['Player'].append(player['username'])
	player_data_dict['Player Rating'].append(player['rating'])
	player_data_dict['Player Nationality'].append(player['nationality'])
	player_data_dict['Player Side'].append(player['side'])
	player_data_dict['Player Result'].append(convert_result_code(player['result']))
	player_data_dict['Player First Move'].append(
				pgn_dict['Opening Moves'][player['side']])
	
	player_data_dict['Opponent'].append(opponent['username'])
	player_data_dict['Opponent Rating'].append(opponent['rating'])
	player_data_dict['Opponent Nationality'].append(opponent['nationality'])
	player_data_dict['Opponent Side'].append(opponent['side'])
	player_data_dict['Opponent Result'].append(convert_result_code(opponent['result']))
	player_data_dict['Opponent First Move'].append(
				pgn_dict['Opening Moves'][opponent['side']])
	
	player_data_dict['Variation'].append(variation_from_url(pgn_dict['ECOUrl']))
	player_data_dict['Termination'].append(pgn_dict['Termination'])
	player_data_dict['Moves'].append(pgn_dict['Moves'])
	player_data_dict['Date'].append(pgn_dict['EndDate'])


player_data_dict ={
	'Player':[],
	'Player Rating':[],
	'Player Nationality':[],
	'Player Side':[],
	'Player Result':[],
	'Player First Move':[],
	
	'Opponent':[],
	'Opponent Rating':[],
	'Opponent Nationality':[],
	'Opponent Side':[],
	'Opponent Result':[],
	'Opponent First Move':[],
	
	'Variation':[],
	'Termination':[],
	'Moves':[],
	'Date':[],
}

def get_data_set():
	for i, url in enumerate(get_archived_game_enpoints(USERNAME)):
		for data in historical_game_list(url):
			#player, opponent, and pgn_dict are all dicts
			player, opponent = sort_player_and_opponent(data['white'], data['black'])
			player = set_player_nationality(player)
			opponent = set_player_nationality(opponent)
			pgn_dict = process_pgn(data['pgn'])
			set_data_values(player, opponent, pgn_dict)
			
			
	
def data_set_to_excel():
	file_name = f'{USERNAME}.xlsx'
	writer = pd.ExcelWriter(file_name)
	df = pd.DataFrame(player_data_dict)
	df.to_excel(writer,'Game Data')
	writer.save()
	return df

def write_player_nationality_csv():
	with open('nationality.csv', 'w') as player_nat:
		file_writer = csv.writer(player_nat)
		for key, value in player_nationality.items():
			file_writer.writerow([key, value])

if __name__ == '__main__':
	get_data_set()
	data_set_to_excel()
	write_player_nationality_csv()
	# archived_endpoint = get_archived_game_enpoints(USERNAME)[0]
	# game_data = historical_game_list(archived_endpoint)[0]
	# process_pgn(game_data['pgn'])	
	# df = pd.DataFrame(player_data_dict)
	# print(player_nationality)
	# print(df[['Player First Move', 'Opponent First Move']].head())



