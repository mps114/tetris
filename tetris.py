import sys, pygame, random
from pygame.sprite import Sprite, Group
from time import sleep, time

		
# Screen Settings

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 300

#Block Settings

# Different Colors
WHITE  = (255,255,255) #background color
RED    = (155,0,0) #S
GREEN  = (0,155,0) #Z
BLUE   = (0,0,155) #I
YELLOW = (155,155,0) #O
PINK   = (255,192,203) #J
PURPLE = (128,0,128) #L
ORANGE = (255,128,0) #T

# Grouped Colors
COLORS = [RED, GREEN, BLUE, YELLOW, PINK, PURPLE, ORANGE]

# All the Shapes
S_SHAPE = ['-00_00','0_00_-0']
Z_SHAPE = ['00_-00','-0_00_0']
I_SHAPE = ['0_0_0_0','0000']
O_SHAPE = ['00_00']
J_SHAPE = ['0_000','00_0_0','000_--0','-0_-0_00']
L_SHAPE = ['--0_000','0_0_00','000_0','00_-0_-0']
T_SHAPE = ['-0_000','0_00_0','000_-0','-0_00_-0']

# Grouped Shapes
ALL_PIECES = [S_SHAPE, Z_SHAPE, I_SHAPE, O_SHAPE, J_SHAPE, L_SHAPE, T_SHAPE]

# Individual Blocks
BLOCK_SIZE = 30

# Fall Down Speed (needs to be factor of 30)
drop_speed = 30

# sleep time (will prob speed up as game goes on)
#sleep_time = 0.5

#MOVEDOWN = pygame.USEREVENT + 1

block_number = 0
rotation_number = 0





def main():
	#started = time()
	fall_speed = 0.4
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Tetris")
	screen.fill(WHITE)
	all_blocks = Group() 
	curr_blocks = Group()
	last_time = time()
	add_shape(screen, curr_blocks)


	while True:
		check_events(screen, curr_blocks)
		if at_bottom(screen, curr_blocks) == True or touching_blocks(screen, curr_blocks, all_blocks) == True:
			add_to_all_blocks(screen, curr_blocks, all_blocks)
			check_rows(screen, all_blocks)
			add_shape(screen, curr_blocks)
		elif time() - last_time > fall_speed:
			update_blocks(screen, curr_blocks)
			last_time = time()
			
		draw_screen(screen, all_blocks)	
		pygame.display.flip()

class Block(Sprite):
	"""A block with certain color, dimension, and location"""
	def __init__(self, screen, new_color):
		super().__init__()
		self.screen = screen
		
		# Create a block with default values
		self.rect = pygame.Rect(0,0,BLOCK_SIZE,BLOCK_SIZE)
		self.color = new_color

	def set_dimension(self, x_value, y_value):
		self.x = x_value
		self.y = y_value
		self.rect.x = self.x
		self.rect.y = self.y

	def draw_block(self):
		pygame.draw.rect(self.screen, self.color, self.rect)

	def check_right_edge(self):
		"""Return True if block is at the right edge of the screen"""
		is_there = False
		screen_rect  = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			is_there = True
		return is_there

	def check_left_edge(self):
		"""Return True if block is at the left edge of the screen"""
		is_there = False
		screen_rect  = self.screen.get_rect()
		if self.rect.left <= 0:
			is_there = True
		return is_there

	def move_right(self): 
		"""move the block to the right"""
		self.x += BLOCK_SIZE
		self.rect.x = self.x

	def move_left(self): 
		"""move the block to the left"""
		self.x -= BLOCK_SIZE
		self.rect.x = self.x


def check_shape_right_edge(screen,curr_blocks):
	is_there = False
	for a_block in curr_blocks.sprites():
		if a_block.check_right_edge():
			is_there = True
			break
	return is_there

def check_shape_left_edge(screen,curr_blocks):
	is_there = False
	for a_block in curr_blocks.sprites():
		if a_block.check_left_edge():
			is_there = True
			break
	return is_there

def move_all_right(screen, curr_blocks):
	for a_block in curr_blocks.sprites():
		a_block.move_right()
		a_block.draw_block()

def move_all_left(screen, curr_blocks):
	for a_block in curr_blocks.sprites():
		a_block.move_left()
		a_block.draw_block()

def check_keydown_events(screen, event, curr_blocks):
	#global drop_speed
	if event.key == pygame.K_RIGHT:
		if check_shape_right_edge(screen, curr_blocks) == False:
			screen.fill(WHITE)
			move_all_right(screen, curr_blocks)
	if event.key == pygame.K_LEFT:
		if check_shape_left_edge(screen, curr_blocks) == False:
			screen.fill(WHITE)
			move_all_left(screen, curr_blocks)
	if event.key == pygame.K_UP:
		screen.fill(WHITE)
		rotate(screen, curr_blocks)
	if event.key == pygame.K_SPACE:
		screen.fill(WHITE)
		add_shape(screen, curr_blocks)
	"""if event.key == pygame.K_DOWN:
		drop_speed = 6"""

"""def check_keyup_events(screen, event):
	global drop_speed
	if event.key == pygame.K_DOWN:
		drop_speed = 3"""


def check_events(screen, curr_blocks):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(screen, event, curr_blocks)
			

		"""elif event.type == pygame.KEYUP:
			check_keyup_events(screen, event)"""


def add_shape(screen, curr_blocks):
	"""adds random shape and rotation"""
	# For now, just start at x = 90
	# find random block (colors length = all_pieces length)
	global block_number
	global rotation_number
	block_number = random.randint(0, len(COLORS) - 1)
	rotation_number = random.randint(0, len(ALL_PIECES[block_number]) - 1)

	avg_x_val = 90
	top_y_val = 0

	create_shape(screen, curr_blocks, block_number, rotation_number, avg_x_val, top_y_val)

def create_shape(screen, curr_blocks, block_number, rotation_number, avg_x_val, top_y_val):
	"""function that creates a shape with the shape key"""
	# clear curr_blocks first
	curr_blocks.empty()

	curr_color = COLORS[block_number] # will always be determined by block_number
	filler_x_val = avg_x_val # for bottom of for loop
	for i in ALL_PIECES[block_number][rotation_number]:
		if i == '0':
			new_block = Block(screen,curr_color)
			new_block.set_dimension(avg_x_val,top_y_val)
			curr_blocks.add(new_block)
			new_block.draw_block()
			avg_x_val += BLOCK_SIZE
		elif i == '-':
			avg_x_val += BLOCK_SIZE
		elif i == '_':
			top_y_val += BLOCK_SIZE
			avg_x_val = filler_x_val

def rotate(screen, curr_blocks):
	"""rotate the shape"""
	# move to the next rotation number
	global block_number
	global rotation_number
	if rotation_number == len(ALL_PIECES[block_number]) - 1:
		rotation_number = 0
	else:
		rotation_number += 1

	# find the middle x_value
	avg_x_val = 0
	for a_block in curr_blocks.copy():
		avg_x_val += a_block.x
	avg_x_val = avg_x_val/len(curr_blocks)
	x_multiplier = int(avg_x_val/30)
	avg_x_val = x_multiplier * 30

	top_y_val = 600
	for a_block in curr_blocks.copy():
		if a_block.rect.y < top_y_val:
			top_y_val = a_block.rect.y
	y_multiplier = int(top_y_val/30)
	top_y_val = y_multiplier * 30

	"""
	# find top_y_value
	top_y_val = 600
	for a_block in curr_blocks.copy():
		if a_block.y < top_y_val:
			top_y_val = a_block.y"""

	# rotate to new position, ignore the checking edges for now
	create_shape(screen, curr_blocks, block_number, rotation_number, avg_x_val, top_y_val)

def update_blocks(screen, curr_blocks):
	# could use the .move(x,y) method
	global drop_speed
	screen.fill(WHITE)
	for block in curr_blocks.sprites():
		block.rect.y += drop_speed
		block.draw_block()

def at_bottom(screen, curr_blocks):
	#check if moving block is at the bottom of the screen
	is_bottom = False
	for block in curr_blocks.copy():
		if block.rect.bottom == 600:
			is_bottom = True
			break
	return is_bottom

def add_to_all_blocks(screen, curr_blocks, all_blocks):
	# add all the current blocks to all blocks and empty current blocks
	for block in curr_blocks.copy():
		#print("y: ", block.rect.y)
		#print("x: ", block.rect.x)
		all_blocks.add(block)
	curr_blocks.empty()

def draw_screen(screen, all_blocks):
	#screen.fill(WHITE)
	for block in all_blocks.sprites():
		block.draw_block()

def touching_blocks(screen, curr_blocks, all_blocks):
	is_touching = False
	for block1 in curr_blocks.copy():
		if is_touching == True:
			break
		for block2 in all_blocks.copy():
			if block1.rect.bottom == block2.rect.y and block1.rect.x == block2.rect.x:
				is_touching = True
				break
	return is_touching


def check_rows(screen, all_blocks):
	y_search = 570 # screen height - 30
	count = 0
	row_num = 1
	still_block = True
	while still_block == True:
		for block in all_blocks.copy():
			if block.rect.y == y_search:
				count += 1
		if count >= 10:
			delete_row(screen, all_blocks, row_num)
			lower_blocks(screen, all_blocks, row_num)
			check_rows(screen, all_blocks)
		elif count == 0:
			still_block = False
		else:
			row_num += 1
			y_search -= BLOCK_SIZE
		count = 0
	

def delete_row(screen, all_blocks, row_number):
	for block in all_blocks.copy():
		if block.rect.y == 600 - (row_number * BLOCK_SIZE):
			all_blocks.remove(block)

def lower_blocks(screen, all_blocks, row_number):
	for block in all_blocks.copy():
		if block.rect.y < 600 - (row_number * BLOCK_SIZE):
			all_blocks.remove(block)
			block.rect.y += BLOCK_SIZE
			#block.rect.y = block.y
			all_blocks.add(block)

	draw_screen(screen, all_blocks)

main()






