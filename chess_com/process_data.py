import re

FILE = '[a-h]'
RANK = '[1-8]'
SQUARE = f'{FILE}{RANK}'

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

def check_checkmate_move(re_str):
	'''
	re_str: string that denotes a regular expression for a chess move
	returns a regular expression string that accounts for the original re, as 
	well as, the move coming with check(+) or checkmate(#).
	'''
	return fr'{re_str}\+|{re_str}#|{re_str}'

def combine_move_re():
	mv_list = [
		PROMOTE, QUEEN_CASTLE, KING_CASTLE, PIECE_RANK_CAPTURE, PIECE_FILE_CAPTURE,
		PIECE_CAPTURE, PAWN_CAPTURE, PIECE_FILE_RANK_MOVE, PIECE_RANK_MOVE, PIECE_FILE_MOVE, 
		PIECE_MOVE, PAWN_MOVE]
	move_re = ''
	for re_str in mv_list:
		checks_re = check_checkmate_move(re_str)
		if move_re != '':
			move_re = f'{move_re}|{checks_re}'
		else:
			move_re=checks_re
	return re.compile(move_re)

MOVE_RE = combine_move_re()

def move_index(x):
 	return (x/2)+1

def parse_chess_moves(move_str):
	""""
	move_str: a string containing chess moves
	returns a dict containing the moves played each game in the form
	{1:{W:_ , B:_}, 2:{W:_, B:_}, ...}
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

