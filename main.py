import pygame as pg, sys, math, random as rnd
from pygame.locals import *
from game_instance import GameInstance


class Piece(pg.sprite.Sprite):
	def __init__(self, width, grid, square, image_path):
		self.grid = grid
		self.square = square
		self.zoomed = False
		
		self.width_zin  = round(width * 1.1)
		self.width_zout = round(width * 0.75)
		
		self.image_path = "sprites\\attacker%d.png" % rnd.randint(1,3)
		self.image_zin  = pg.transform.smoothscale(pg.image.load(image_path), (self.width_zin, self.width_zin))
		self.image_zout = pg.transform.smoothscale(pg.image.load(image_path), (self.width_zout, self.width_zout))
		
		pg.sprite.Sprite.__init__(self)
		
		self.image = self.image_zout
		transColor = self.image.get_at((1,1))
		self.image.set_colorkey(transColor)
		
		self.rect = self.image.get_rect()
	def move_to_square(self, square):
		if square is None:
			raise Exception("could not move to None square")
		else:
			self.square = square
	def zoom_in(self):
		self.zoomed = True
	def zoom_out(self):
		self.zoomed = False
	def update(self):
		if self.zoomed:
			self.image = self.image_zin
		else:
			self.image = self.image_zout
		self.rect = self.image.get_rect()
		pos = get_square_coordinates(self.square)
		self.rect.center = (pos[0] + round(self.grid['square_width']/2), pos[1] + round(self.grid['square_width']/2))

class AttackerPiece(Piece):
	def __init__(self, width, grid, square):
		Piece.__init__(self, width, grid, square, ("sprites\\attacker%d.png" % rnd.randint(1,3)) )
		self.type = -1

class DefenderPiece(Piece):
	def __init__(self, width, grid, square):
		Piece.__init__(self, width, grid, square, ("sprites\\defender%d.png" % rnd.randint(1,3)) )
		self.type = 1

class KingPiece(Piece):
	def __init__(self, width, grid, square):
		Piece.__init__(self, width, grid, square, "sprites\\king.png")
		self.type = 2



pg.init()

# === Информация о размерах === #

screen_width  = 1200
screen_height = 800
board_to_screen_ratio = 0.85
'''
board_path = "board.png"
grid_inner_margin = 30.5	# пикселей до верхнего левого угла верхней левой клетки
grid_square_width = 21.75	# ширина клетки в пикселях
grid_squares_num  = 11 		# ширина доски в клетках
'''
board_path = "board_2.png"
grid_inner_margin = 14#150		# пикселей до верхнего левого угла верхней левой клетки
grid_square_width = 138#99		# ширина клетки в пикселях
grid_squares_num  = 7 		# ширина доски в клетках

# ============================= #

# Инифицализируем экран
screen = pg.display.set_mode((screen_width, screen_height), 0, 32)
pg.display.set_caption("Hnefatafl")

# Изображение фона
background_img = pg.image.load("background.jpg")
background_img = pg.transform.smoothscale(background_img, (screen_width, screen_height))

# Изображение доски
board_width = round(min(screen_width, screen_height) * board_to_screen_ratio)	# Новая ширина и высота доски в пискелях (после растягивания по окну)
outer_margin = round((min(screen_width, screen_height) - board_width) / 2)		# Отступ от верхнего левого края окна до верхнего левого угла доски
board_img = pg.image.load(board_path)
board_scale_ratio = board_img.get_width()
board_img = pg.transform.smoothscale(board_img, (board_width, board_width))
board_scale_ratio = board_img.get_width() / board_scale_ratio
init_board_img = board_img

# Словарь с информацией о размерах клеток
grid = {'inner_margin': grid_inner_margin, 'square_width': grid_square_width, 'squares_num': grid_squares_num}
# Масштабируем в соответствии с размерами окна
grid['inner_margin'] = round(grid['inner_margin'] * board_scale_ratio) #+ outer_margin
grid['square_width'] = round(grid['square_width'] * board_scale_ratio)

# Шрифт
fontSize = 32
fontColor = (255,255,255)
myFont = pg.font.Font("freesansbold.ttf", fontSize)


def get_board_square(mouse_pos):
	square = (math.ceil((mouse_pos[0] - grid['inner_margin'] - outer_margin) / grid['square_width']), math.ceil((mouse_pos[1] - grid['inner_margin'] - outer_margin) / grid['square_width']))
	if square[0] < 1 or square[0] > grid_squares_num or square[1] < 1 or square[1] > grid_squares_num:
		return None
	else:
		return (square[0], square[1])

def get_square_coordinates(square):
	if square[0] < 1 or square[0] > grid['squares_num'] or square[1] < 1 or square[1] > grid['squares_num']:
		raise Exception("not a valid square: (%d, %d), must be from 1 to %d." % (square[0], square[1], grid['squares_num']))
	else:
		return (round(grid['square_width']*(square[0]-1) + grid['inner_margin'] + outer_margin), round(grid['square_width']*(square[1]-1) + grid['inner_margin'] + outer_margin))

def set_up_board(pieces, squares):
	pieces.empty()
	for s in squares[0]:
		p = AttackerPiece(grid['square_width'], grid, s)
		pieces.add(p)
	for s in squares[1]:
		p = DefenderPiece(grid['square_width'], grid, s)
		pieces.add(p)
	for s in squares[2]:
		p = KingPiece(grid['square_width'], grid, s)
		pieces.add(p)

def get_sprite_by_square(square):
	sprite = None
	for s in pieces.sprites():
		if s.square == square:
			sprite = s
			break
	if sprite is None:
		raise Exception('could not find piece in (%d, %d)' % square)
	else:
		return sprite

# Инициализация объекта игровой партии
game_instance = GameInstance()

# Инициализация спрайтов
pieces = pg.sprite.Group()
set_up_board(pieces, game_instance.get_current_setup())

selected_piece = None

mainLoop = True
while mainLoop:
	
	# Обновление информации о координатах квадрата под курсором
	current_square = get_board_square(pg.mouse.get_pos())
	# Обновление информации о состоянии партии
	current_turn = game_instance.get_current_turn()
	victory_reason = game_instance.get_victory_reason()
	
	if victory_reason is None:
		text = "%s's turn" % ("Defender" if current_turn > 0 else "Attacker")
	else:
		fontColor = (255,0,0)
		text = victory_reason
	
	# События
	for event in pg.event.get():
		
		if event.type == QUIT:
			mainLoop = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				mainLoop = False
			if event.key == pg.K_r:
				game_instance.new_game()
				fontColor = (255,255,255)
				set_up_board(pieces, game_instance.get_current_setup())
		
		if event.type == MOUSEBUTTONDOWN:
			try:
				if selected_piece is None:
					selected_piece = get_sprite_by_square(current_square)
					print("Cur:", current_square)
					if victory_reason is not None:
						raise Exception('game is over: %s' % victory_reason)
					if selected_piece.type * current_turn < 0:
						raise Exception('could not select piece at (%d, %d): other player''s move' % current_square)
					
					selected_piece.zoom_in()
				else:
					if victory_reason is not None:
						raise Exception('game is over: %s' % victory_reason)
					if selected_piece.type * current_turn < 0:
						raise Exception('could not select piece at (%d, %d): other player''s move' % current_square)
					
					(removed_pieces, new_current_turn, new_victory_reason) = game_instance.move(selected_piece.square, current_square)
					
					for square in removed_pieces:
						print("Rem:", square)
						get_sprite_by_square(square).kill()
					
					selected_piece.move_to_square(current_square)
					selected_piece.zoom_out()
					selected_piece = None
					
					print(game_instance.board[0])
					print(game_instance.board[1])
					print(game_instance.board[2])
					print(game_instance.board[3])
					print(game_instance.board[4])
					print(game_instance.board[5])
					print(game_instance.board[6])
					
					current_turn = new_current_turn
					victory_reason = new_victory_reason
					
			except Exception as e:
				if selected_piece is not None:
					selected_piece.zoom_out()
					selected_piece = None
				print(e)
	
	pieces.update()
	
	screen.blit(background_img, (0,0))
	screen.blit(board_img, (outer_margin, outer_margin))
	pieces.draw(screen)
	
	font_img = myFont.render(text, True, (fontColor))
	screen.blit(font_img, (board_width + 2*outer_margin, outer_margin))
	
	pg.display.update()
	
pg.quit()
