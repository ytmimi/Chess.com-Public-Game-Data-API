import re

FILE = '[a-h]'
RANK = '[1-8]'
SQUARE = f'{FILE}{RANK}'


PAWN_MOVE = f'{SQUARE}' #e4 #check
PIECE_MOVE = f'[KQRNB]{SQUARE}'#Qb3

PIECE_FILE_MOVE = f'[QRNB]{FILE}{SQUARE}' #Ndf5 #check
PIECE_RANK_MOVE = f'[QRNB]{RANK}{SQUARE}' #N6f4 #check
PIECE_FILE_RANK_MOVE = f'[QRNB]{FILE}{RANK}{SQUARE}' #Nb3d4 #check

PAWN_CAPTURE = f'{FILE}x{SQUARE}' #exd4
PIECE_CAPTURE = f'[KQRNB]x{SQUARE}' #Bxf7
PIECE_FILE_CAPTURE = f'[QRNB]{FILE}x{SQUARE}' #Rfxd8
PIECE_RANK_CAPTURE = f'[QRNB]{RANK}x{SQUARE}' #N6xd5

KING_CASTLE = 'O-O' #check
QUEEN_CASTLE = 'O-O-O' #check
PROMOTE = f'{SQUARE}=[QRNB]'#h1=Q #check

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

def parse_chess_moves(move_lst):
	moves = {}
	if len(move_lst) == 0:
		moves[1] = {'White':0, 'Black':0}
	elif len(move_lst) % 2 == 0:
		for i in range(0,len(move_lst), 2):
			index = move_index(i)
			white = move_lst[i]
			black = move_lst[i+1]
			moves[index] = {'White':white, 'Black':black}
	else:
		for i in range(0,len(move_lst), 2):
			if i == len(move_lst)-1:
				index = move_index(i)
				white = move_lst[i]
				black = None
				moves[index] = {'White':white, 'Black':black}
			else:
				index = move_index(i)
				white = move_lst[i]
				black = move_lst[i+1]
				moves[index] = {'White':white, 'Black':black}
	return moves

def move_dict(move_str):
	moves = re.findall(MOVE_RE, move_str)
	return parse_chess_moves(moves)
