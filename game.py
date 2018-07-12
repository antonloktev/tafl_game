import pygame as pg, sys, math, random as rnd
from pygame.locals import *


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

class DefenderPiece(Piece):
	def __init__(self, width, grid, square):
		Piece.__init__(self, width, grid, square, ("sprites\\defender%d.png" % rnd.randint(1,2)) )

class KingPiece(Piece):
	def __init__(self, width, grid, square):
		Piece.__init__(self, width, grid, square, "sprites\\king.png")



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


# Шрифт
fontSize = 32
fontColor = (255,255,255)
myFont = pg.font.Font("freesansbold.ttf", fontSize)

# Инициализация спрайтов
pieces = pg.sprite.Group()
attackers_squares = [(1,3), (1,4), (1,5), (2,4), (3,1), (3,7), (4,1), (4,2), (4,6), (4,7), (5,1), (5,7), (6,4), (7,3), (7,4), (7,5)]
for s in attackers_squares:
	p = AttackerPiece(grid['square_width'], grid, s)
	pieces.add(p)
defenders_squares = [(3,3), (3,4), (3,5), (4,3), (4,5), (5,3), (5,4), (5,5)]
for s in defenders_squares:
	p = DefenderPiece(grid['square_width'], grid, s)
	pieces.add(p)
kings_squares = [(4,4)]
p = KingPiece(grid['square_width'], grid, (4,4))
pieces.add(p)

mainLoop = True

moving_piece = None

while mainLoop:
	
	# События
	for event in pg.event.get():
		
		if event.type == QUIT:
			mainLoop = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				mainLoop = False
		
		if event.type == MOUSEBUTTONDOWN:
			try:
				if moving_piece is not None:
					moving_piece.move_to_square(current_square)
					moving_piece.zoom_out()
					moving_piece = None
				else:
					for s in pieces.sprites():
						if s.square == current_square:
							moving_piece = s
							moving_piece.zoom_in()
							break
						else:
							moving_piece = None
			except Exception as e:
				print(e)
		
	# Обновление информации о координатах квадрата под курсором
	current_square = get_board_square(pg.mouse.get_pos())
	if current_square is not None:
		text_mouse = "Mouse over (%d, %d)" % (current_square[1], current_square[0])
	else:
		text_mouse = "Mouse not over board"
	
	pieces.update()
	
	#board_img.blit(init_board_img, (0,0))
	screen.blit(background_img, (0,0))
	screen.blit(board_img, (outer_margin, outer_margin))
	pieces.draw(screen)
	
	font_img = myFont.render(text_mouse, True, (fontColor))
	screen.blit(font_img, (board_width + 2*outer_margin, outer_margin))
	
	pg.display.update()
	
pg.quit()
