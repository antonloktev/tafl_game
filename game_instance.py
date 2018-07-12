import pygame as pg, numpy as np, random as rnd

class GameInstance:
	
	# "Статические" поля
	board_init = [[ 0,  0, -1, -1, -1,  0,  0], \
	              [ 0,  0,  0, -1,  0,  0,  0], \
		      [-1,  0, +1, +1, +1,  0, -1], \
	              [-1, -1, +1, +2, +1, -1, -1], \
		      [-1,  0, +1, +1, +1,  0, -1], \
	              [ 0,  0,  0, -1,  0,  0,  0], \
	  	      [ 0,  0, -1, -1, -1,  0,  0]]
	turn_init = 1	# Первыми ходят защитники
	victory_reason_init = None	# Причина победы
	
	def __init__(self):
		self.board = [[ 0,  0, -1, -1, -1,  0,  0], \
	              	      [ 0,  0,  0, -1,  0,  0,  0], \
			      [-1,  0, +1, +1, +1,  0, -1], \
		              [-1, -1, +1, +2, +1, -1, -1], \
			      [-1,  0, +1, +1, +1,  0, -1], \
			      [ 0,  0,  0, -1,  0,  0,  0], \
			      [ 0,  0, -1, -1, -1,  0,  0]]
		self.turn = GameInstance.turn_init
		self.victory_reason = GameInstance.victory_reason_init
	
	def new_game(self):
		self.board = [[ 0,  0, -1, -1, -1,  0,  0], \
	                  [ 0,  0,  0, -1,  0,  0,  0], \
				      [-1,  0, +1, +1, +1,  0, -1], \
				      [-1, -1, +1, +2, +1, -1, -1], \
				      [-1,  0, +1, +1, +1,  0, -1], \
				      [ 0,  0,  0, -1,  0,  0,  0], \
				      [ 0,  0, -1, -1, -1,  0,  0]]
		self.turn = GameInstance.turn_init
		self.victory_reason = GameInstance.victory_reason_init
	
	def get_current_setup(self):
		attackers_squares = []
		defenders_squares = []
		kings_squares = []
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] == -1:
					attackers_squares.append((i+1,j+1))
				elif self.board[i][j] == 1:
					defenders_squares.append((i+1,j+1))
				elif self.board[i][j] == 2:
					kings_squares.append((i+1,j+1))
		return (attackers_squares, defenders_squares, kings_squares)		
	def get_current_turn(self):
		return self.turn
	def get_victory_reason(self):
		return self.victory_reason
	
	def move(self, begin_square, end_square):
		
		if self.victory_reason is not None:
			raise Exception('this game is over')	
		
		occupation = self.board[end_square[0]-1][end_square[1]-1]
		if occupation != 0:
			raise Exception('square (%d, %d) is already occupied by %s' % (end_square[0], end_square[1], "Defender" if occupation == 1 else ("King" if occupation == 2 else "Attacker")))
		
		self.board[end_square[0]-1][end_square[1]-1] = self.board[begin_square[0]-1][begin_square[1]-1]
		self.board[begin_square[0]-1][begin_square[1]-1] = 0
		
		self.turn *= -1
		removed_pieces = []
		
		victory = rnd.randint(-10, 10)
		if victory == -10:
			self.victory_reason = "Attackers won!"
		elif victory == 10:
			self.victory_reason = "Defenders won!"
		
		return (removed_pieces, self.turn, self.victory_reason)
