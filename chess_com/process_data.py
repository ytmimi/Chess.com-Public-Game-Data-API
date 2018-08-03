import re
from settings import MOVE_RE_LIST
from chess_api import player_info

def check_checkmate_move(re_str):
	'''
	re_str: string that denotes a regular expression for a chess move
	returns a regular expression string that accounts for the original re, as 
	well as, the move coming with check(+) or checkmate(#).
	'''
	return fr'{re_str}\+|{re_str}#|{re_str}'

def combine_move_re():
	''' 
	joins all the regular expression stored in MOVE_RE_LIST into one
	large regex. Returns the compiled regex.
	'''
	move_re = ''
	for re_str in MOVE_RE_LIST:
		if move_re != '':
			move_re = f'{move_re}|{check_checkmate_move(re_str)}'
		else:
			move_re=check_checkmate_move(re_str)
	return re.compile(move_re)

MOVE_RE = combine_move_re()

def move_index(x):
 	return (x/2)+1

def parse_chess_moves(move_str):
	""""
	move_str: a string containing chess moves
	returns a dict containing the moves played each game in the form
	{1:{W:_ , B:_}, 2:{W:_, B:_}, 3:{W:_, B:_} ...}
	"""
	move_lst = re.findall(MOVE_RE, move_str)
	move_dict = {}
	if len(move_lst) == 0:
		return {1:{'W':'-', 'B':'-'}}
	elif len(move_lst) % 2 == 0:
		for i in range(0,len(move_lst), 2):
			index = move_index(i)
			move_dict[index] = {'W':move_lst[i], 'B': move_lst[i+1]}
	else:
		for i in range(0,len(move_lst), 2):
			if i == len(move_lst)-1:
				index = move_index(i)
				move_dict[index] = {'W':move_lst[i], 'B':'-'}
			else:
				index = move_index(i)
				move_dict[index] = {'W':move_lst[i], 'B':move_lst[i+1]}
	return move_dict

def strip_brackets(string):
	return string.replace('[', '').replace(']','')

def variation_from_url(variation_url):
	variation_str = variation_url.split('/')[-1]
	variat_lst = variation_str.split('-')[1:]
	return ' '.join(variat_lst)

def pgn_to_dict(pgn_str):
	""""
	pgn_str: str from each game dictionaries pgn key
	returns a dictionary with the following keys: 
	'Event', 'Site', 'Date', 'Round', 'White', 'Black', 'Result', 'ECO',
	'ECOUrl', 'WhiteElo', 'BlackElo', 'TimeControl', 'Termination',
	'StartTime', 'EndDate', 'EndTime', 'Link', 'Moves' 'Variation',
	"""
	pgn_data = pgn_str.split('\n')
	pgn_dict = {}
	for item in pgn_data[:-2]:
		category, value, _ = strip_brackets(item).split('"')
		pgn_dict[category.strip()] = value
	pgn_dict['Moves'] = parse_chess_moves(pgn_data[-1])
	pgn_dict['Variation'] = variation_from_url(pgn_dict['ECOUrl'])
	return pgn_dict

def player_nationality(country_codes: dict,nationality: dict, player_dict: dict):
	''' 
	Either makes a request to get the players nationality, or loads the nationality 
	from the passed in nationality dictionary. Then updates the player_dict to include
	that nationality.
	'''
	player_enpoint = player_dict['@id']
	if nationality.get(player_enpoint) != None:
		player_dict['nationality'] = nationality[player_enpoint]
	else:
		try:
			country_url = player_info(player_enpoint)['country']
			code = country_url.split('/')[-1]
			country = country_codes[code]
		except Exception as e:
			country = 'Unknown'
		player_dict['nationality'] = country
		nationality[player_enpoint] = country
	return player_dict





