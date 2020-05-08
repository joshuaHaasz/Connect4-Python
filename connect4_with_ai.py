import numpy as np
import random
import pygame
import sys
import math
from connect4 import Connect4

class Connect4AI(Connect4):
	def __init__(self):
		super().__init__()
		self.PLAYER = 0
		self.AI = 1
		self.EMPTY = 0
		self.PLAYER_PIECE = 1
		self.AI_PIECE = 2
		self.WINDOW_LENGTH = 4

	def evaluate_window(self, window, piece):
		score = 0
		opp_piece = self.PLAYER_PIECE
		if piece == self.PLAYER_PIECE:
			opp_piece = self.AI_PIECE

		if window.count(piece) == 4:
			score += 100
		elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
			score += 5
		elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
			score += 2

		if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
			score -= 4

		return score

	def score_position(self, board, piece):
		score = 0

		## Score center column
		center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
		center_count = center_array.count(piece)
		score += center_count * 3

		## Score Horizontal
		for r in range(self.ROW_COUNT):
			row_array = [int(i) for i in list(board[r,:])]
			for c in range(self.COLUMN_COUNT-3):
				window = row_array[c:c+self.WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score Vertical
		for c in range(self.COLUMN_COUNT):
			col_array = [int(i) for i in list(board[:,c])]
			for r in range(self.ROW_COUNT-3):
				window = col_array[r:r+self.WINDOW_LENGTH]
				score += self.evaluate_window(window, piece)

		## Score posiive sloped diagonal
		for r in range(self.ROW_COUNT-3):
			for c in range(self.COLUMN_COUNT-3):
				window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		for r in range(self.ROW_COUNT-3):
			for c in range(self.COLUMN_COUNT-3):
				window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
				score += self.evaluate_window(window, piece)

		return score

	def is_terminal_node(self, board):
		return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

	def minimax(self, board, depth, alpha, beta, maximizingPlayer):
		valid_locations = self.get_valid_locations(board)
		is_terminal = self.is_terminal_node(board)
		if depth == 0 or is_terminal:
			if is_terminal:
				if self.winning_move(board, self.AI_PIECE):
					return (None, 100000000000000)
				elif self.winning_move(board, self.PLAYER_PIECE):
					return (None, -10000000000000)
				else: # Game is over, no more valid moves
					return (None, 0)
			else: # Depth is zero
				return (None, self.score_position(board, self.AI_PIECE))
		value = -math.inf if maximizingPlayer else math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = self.get_next_open_row(board, col)
			b_copy = board.copy()
			self.drop_piece(b_copy, row, col, self.AI_PIECE)
			new_score = self.minimax(b_copy, depth-1, alpha, beta, not maximizingPlayer)[1]
			if maximizingPlayer:
				if new_score > value:
					value = new_score
					column = col
				alpha = max(alpha, value)
			else:
				if new_score < value:
					value = new_score
					column = col
				beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

		# else: # Minimizing player
		# 	value = math.inf
		# 	column = random.choice(valid_locations)
		# 	for col in valid_locations:
		# 		row = self.get_next_open_row(board, col)
		# 		b_copy = board.copy()
		# 		self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
		# 		new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
		# 		if new_score < value:
		# 			value = new_score
		# 			column = col
		# 		beta = min(beta, value)
		# 		if alpha >= beta:
		# 			break
		# 	return column, value

	def get_valid_locations(self, board):
		valid_locations = []
		for col in range(self.COLUMN_COUNT):
			if self.is_valid_location(board, col):
				valid_locations.append(col)
		return valid_locations

	def main_loop(self):
			turn = random.randint(self.PLAYER, self.AI)
			while not self.game_over:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						sys.exit()
					if turn == self.PLAYER:
						if event.type == pygame.MOUSEMOTION:
							pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
							posx = event.pos[0]
							self.mouse_motion(posx, turn)
						if event.type == pygame.MOUSEBUTTONDOWN and self.ready():
							posx = event.pos[0]
							col = int(math.floor(posx / self.SQUARESIZE))
							if self.is_valid_location(self.board, col):
								self.move(col, turn)
								turn += 1
								turn = turn % 2
					else:
						col, minimax_score = self.minimax(self.board, 5, -math.inf, math.inf, True)

						if self.is_valid_location(self.board, col):
							self.move(col, turn)
							turn += 1
							turn = turn % 2
			pygame.time.wait(3000)

if __name__ == "__main__":
	client = Connect4AI()
	client.main_loop()