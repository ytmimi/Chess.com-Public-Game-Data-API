import os
import csv

#PATH TO THE PROJECT DIRECTORIES
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_PATH, 'CSVs')

#FILES OUTPUT BY RUNNING main.py. SAVED TO CSV_DIR
NATIONALLITY_FILE = 'nationality.csv'
GAME_DATA_FILE = 'chess_data.csv'

#USERNAME
USERNAME = os.environ['USERNAME']

#ARCHIVE ENDPOINT USED FOR API REQUESTS
#https://www.chess.com/news/view/published-data-api#pubapi-endpoint-games-archive-list
ARCHIVE_ENDPOINT=f'https://api.chess.com/pub/player/{USERNAME}/games/archives'

#DETERMIN IF LIVE TESTS ARE RUN
LIVE_TEST = False

#REGULAR EXPRESSIONS STRING THAT REPRESENT ALGEBRAIC CHESS NOTATION
FILE = '[a-h]' #f
RANK = '[1-8]' #8
SQUARE = f'{FILE}{RANK}' #a1

PAWN_MOVE = f'{SQUARE}' #e4 
PIECE_MOVE = f'[KQRNB]{SQUARE}'#Qb3

PIECE_FILE_MOVE = f'[QRNB]{FILE}{SQUARE}' #Ndf5 
PIECE_RANK_MOVE = f'[QRNB]{RANK}{SQUARE}' #N6f4 
PIECE_FILE_RANK_MOVE = f'[QRNB]{FILE}{RANK}{SQUARE}' #Nb3d4 

PAWN_CAPTURE = f'{FILE}x{SQUARE}' #exd4
PIECE_CAPTURE = f'[KQRNB]x{SQUARE}' #Bxf7
PIECE_FILE_CAPTURE = f'[QRNB]{FILE}x{SQUARE}' #Rfxd8
PIECE_RANK_CAPTURE = f'[QRNB]{RANK}x{SQUARE}' #N6xd5

KING_CASTLE = 'O-O' 
QUEEN_CASTLE = 'O-O-O' 
PROMOTE = f'{SQUARE}=[QRNB]'#h1=Q 

MOVE_RE_LIST = [
	PROMOTE, QUEEN_CASTLE, KING_CASTLE, PIECE_RANK_CAPTURE, 
	PIECE_FILE_CAPTURE, PIECE_CAPTURE, PAWN_CAPTURE, PIECE_FILE_RANK_MOVE, 
	PIECE_RANK_MOVE, PIECE_FILE_MOVE, PIECE_MOVE, PAWN_MOVE
]

#GAME RESULT CODES AS DEFINED BY CHESS.COM'S API
#https://www.chess.com/news/view/published-data-api#game-results
GAME_RESULTS = {
	'win':'Win', 'checkmated':'Checkmated', 'agreed':'Draw agreed',
	'repetition':'Draw by repetition', 'timeout':'Timeout', 'resigned':'Resigned',
	'stalemate':'Stalemate', 'lose':'Lose', 'insufficient':'Insufficient material',
	'50move':'Draw by 50-move rule', 'abandoned':'Abandoned', 'kingofthehill':'Opponent King reached the hill',
	'threecheck':'Checked for the 3rd time', 'timevsinsufficient':'Draw by timeout vs insufficient material',
	'bughousepartnerlose':'Bughouse partner lost'
}

#COUNTRY CODES : 2-CHARACTER ISO 3166 CODES 
#https://www.chess.com/news/view/published-data-api#pubapi-endpoint-country
def load_country_codes():
	"""Loads country_code.csv into a dictionary of 'code':'country name' pairs"""
	country_dict = {}
	with open(os.path.join(CSV_DIR,'country_code.csv'), 'r') as country:
		file_reader = csv.reader(country,)
		for i, row in enumerate(file_reader):
			if i != 0:
				country_dict[row[0]] = row[1]
	return country_dict

COUNTRY_CODES = load_country_codes()








