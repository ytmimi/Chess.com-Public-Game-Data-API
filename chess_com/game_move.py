import re

no_timestamp = '1. d4 d5 2. Nc3 c6 3. e4 Nf6 4. Bd3 Bg4 5. Nf3 e6 6. e5 Nfd7 7. Bg5 f6 8. h3 Bf5 9. Bxf5 exf5 10. e6 fxg5 11. exd7+ Nxd7 12. Qe2+ Be7 13. O-O-O O-O 14. Rhe1 Bd6 15. Nxg5 Qxg5+ 16. Kb1 Qg6 17. f3 Nf6 18. Qe6+ Kh8 19. Qxd6 Rae8 20. b3 Qxg2 21. Ne2 Qxf3 22. Nf4 Ne4 23. Rxe4 Qxd1+ 24. Kb2 Rg8 25. Rxe8 Rxe8 26. Qd7 Rg8 27. Qf7 Qxd4+ 28. Ka3 Qxf4 0-1'
timestamp = '1. e4 {[%clk 0:09:56.9]} 1... e5 {[%clk 0:09:58.5]} 2. f4 {[%clk 0:09:40.1]} 2... exf4 {[%clk 0:09:56.1]} 3. Nf3 {[%clk 0:09:39.1]} 3... d6 {[%clk 0:09:53.6]} 4. d4 {[%clk 0:09:29.6]} 4... Bg4 {[%clk 0:09:44.5]} 5. Bxf4 {[%clk 0:09:23.9]} 5... Nf6 {[%clk 0:09:41.1]} 6. Nc3 {[%clk 0:09:14.4]} 6... Nc6 {[%clk 0:09:34.5]} 7. h3 {[%clk 0:09:10.3]} 7... Bh5 {[%clk 0:09:20.6]} 8. Be2 {[%clk 0:08:58.4]} 8... Be7 {[%clk 0:09:15.6]} 9. Qd3 {[%clk 0:08:53.1]} 9... Qd7 {[%clk 0:09:12.2]} 10. a3 {[%clk 0:08:48.9]} 10... O-O-O {[%clk 0:08:52.2]} 11. g4 {[%clk 0:08:34.7]} 11... Nxg4 {[%clk 0:08:45.6]} 12. hxg4 {[%clk 0:08:31.3]} 12... Bxg4 {[%clk 0:08:44.3]} 13. O-O-O {[%clk 0:08:27.9]} 13... Bf6 {[%clk 0:08:39.9]} 14. Nb5 {[%clk 0:08:11.8]} 14... a6 {[%clk 0:08:36]} 15. d5 {[%clk 0:07:52.1]} 15... Bxf3 {[%clk 0:08:11.4]} 16. Bxf3 {[%clk 0:07:32.7]} 16... Ne5 {[%clk 0:07:55.5]} 17. Bxe5 {[%clk 0:07:27.9]} 17... Bxe5 {[%clk 0:07:52.4]} 18. Nd4 {[%clk 0:07:11.5]} 18... Kb8 {[%clk 0:07:32.4]} 19. Be2 {[%clk 0:06:18.5]} 19... Qa4 {[%clk 0:07:21.3]} 20. Rh3 {[%clk 0:06:01.7]} 20... g6 {[%clk 0:06:53.8]} 21. Qb3 {[%clk 0:05:53.9]} 21... Qxb3 {[%clk 0:06:48]} 22. Rxb3 {[%clk 0:05:51.9]} 22... Ka7 {[%clk 0:06:34.6]} 23. Rf1 {[%clk 0:05:18.6]} 23... Rhf8 {[%clk 0:06:28.2]} 24. Nf3 {[%clk 0:05:08.1]} 24... Bf4+ {[%clk 0:06:21.2]} 25. Kb1 {[%clk 0:05:05.5]} 25... g5 {[%clk 0:06:19.6]} 26. Nd4 {[%clk 0:04:57.7]} 26... h6 {[%clk 0:05:51.9]} 27. Nf5 {[%clk 0:04:54.9]} 27... Rh8 {[%clk 0:05:36.5]} 28. Rh1 {[%clk 0:04:39]} 1-0'
#							checkmate			checkm 			   normal move      castles
move_re = re.compile(r'[A-Za-z]{1,4}[1-8]#|[A-Za-z]{1,4}[1-8]\+|[A-Za-z]{1,4}[1-8]|O-O|O-O-O')

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
	moves = re.findall(move_re, move_str)
	return parse_chess_moves(moves)
