import numpy as np
import pygame
import sys
import math

class Connect4(object):
	def __init__(self):
		pygame.init()
		self.BLUE = (0,0,255)
		self.BLACK = (0,0,0)
		self.RED = (255,0,0)
		self.YELLOW = (255,255,0)
		self.ROW_COUNT = 6
		self.COLUMN_COUNT = 7
		self.board = self.create_board()
		self.game_over = False
		self.SQUARESIZE = 100
		self.width = self.COLUMN_COUNT * self.SQUARESIZE
		self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
		self.size = (self.width, self.height)
		self.RADIUS = int(self.SQUARESIZE / 2 - 5)
		self.myfont = pygame.font.SysFont("monospace", 75)
		self.screen = pygame.display.set_mode(self.size)
		self.draw_board()
		self.colors = {0 : self.RED, 1 : self.YELLOW}
		self.time_of_last_move = pygame.time.get_ticks()
		pygame.display.update()


	def create_board(self):
		return np.zeros((self.ROW_COUNT,self.COLUMN_COUNT))

	def drop_piece(self, row, col, piece):
		self.board[row][col] = piece
		self.draw_board()

	def is_valid_location(self, board, col):
		return board[self.ROW_COUNT-1][col] == 0

	def get_next_open_row(self, col):
		for r in range(self.ROW_COUNT):
			if self.board[r][col] == 0:
				return r

	def print_board(self):
		print(np.flip(self.board, 0))

	def winning_move(self, piece):
		# Check horizontal locations for win
		for c in range(self.COLUMN_COUNT-3):
			for r in range(self.ROW_COUNT):
				if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
					return True

		# Check vertical locations for win
		for c in range(self.COLUMN_COUNT):
			for r in range(self.ROW_COUNT-3):
				if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
					return True

		# Check positively sloped diaganols
		for c in range(self.COLUMN_COUNT-3):
			for r in range(self.ROW_COUNT-3):
				if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
					return True

		# Check negatively sloped diaganols
		for c in range(self.COLUMN_COUNT-3):
			for r in range(3, self.ROW_COUNT):
				if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
					return True

	def draw_board(self):
		for c in range(self.COLUMN_COUNT):
			for r in range(self.ROW_COUNT):
				pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
				pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)

		for c in range(self.COLUMN_COUNT):
			for r in range(self.ROW_COUNT):
				if self.board[r][c] == 1:
					pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
				elif self.board[r][c] == 2:
					pygame.draw.circle(self.screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
		pygame.display.update()

	def mouse_motion(self, posx, turn):
		pygame.draw.circle(self.screen, self.colors[turn], (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
		pygame.display.update()

	def move(self, col, turn):
		row = self.get_next_open_row(col)
		self.drop_piece(row, col, turn+1)
		self.time_of_last_move = pygame.time.get_ticks()

		if self.winning_move(turn+1):
			label = self.myfont.render(f"Player {turn+1} wins!!", 1, self.colors[turn])
			self.screen.blit(label, (40, 10))
			self.game_over = True

		self.print_board()
		self.draw_board()

	def ready(self):
		return pygame.time.get_ticks() - self.time_of_last_move > 500

	def main_loop(self):
		turn = 0
		while not self.game_over:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
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
					self.mouse_motion(posx, turn)
		pygame.time.wait(3000)

if __name__ == "__main__":
	client = Connect4()
	client.main_loop()




