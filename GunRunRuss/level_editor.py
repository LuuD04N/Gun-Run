import pygame
import button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

#define game variables
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 45
level = 1
current_tile = 0  
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
#define colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
BLACK = (0, 0, 0)

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('assets/Player/john_static.png').convert_alpha()
load_img = pygame.image.load('assets/Enemy/grunt.png').convert_alpha()

#define font
font = pygame.font.SysFont('Futura', 30)

#create buttons
save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)

#make a button list
button_list = []
button_col = 0
button_row = 0

#load images
bg6_img_orig = pygame.image.load('assets/Background/6.png').convert_alpha()
bg6_img = pygame.transform.scale(bg6_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg5_img_orig = pygame.image.load('assets/Background/5.png').convert_alpha()
bg5_img = pygame.transform.scale(bg5_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg4_img_orig = pygame.image.load('assets/Background/4.png').convert_alpha()
bg4_img = pygame.transform.scale(bg4_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg3_img_orig = pygame.image.load('assets/Background/3.png').convert_alpha()
bg3_img = pygame.transform.scale(bg3_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg2_img_orig = pygame.image.load('assets/Background/2.png').convert_alpha()
bg2_img = pygame.transform.scale(bg2_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

bg1_img_orig = pygame.image.load('assets/Background/1.png').convert_alpha()
bg1_img = pygame.transform.scale(bg1_img_orig, (SCREEN_WIDTH, SCREEN_HEIGHT))

#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * MAX_COLS
	world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
	world_data[ROWS - 1][tile] = 0

#function for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#create function for drawing background
def draw_bg():
	screen.fill((0,0,0))
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))
		screen.blit(bg4_img, ((x * width) - scroll * 0.45, SCREEN_HEIGHT - bg4_img.get_height() - 10))
		screen.blit(bg5_img, ((x * width) - scroll * 0.5, SCREEN_HEIGHT - bg5_img.get_height() - 10))

#draw grid
def draw_grid():
	#vertical lines
	for c in range(MAX_COLS + 1):
		pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
	#horizontal lines
	for c in range(ROWS + 1):
		pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

#function for drawing the world tiles
def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

for i in range(len(img_list)):
	tile_button = button.Button(SCREEN_WIDTH + (50 * button_col) + 50, 50 * button_row + 50, img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 5:
		button_row += 1
		button_col = 0

run = True
while run:

	clock.tick(FPS)

	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
	draw_text('RESTART GAME TO LOAD LEVEL !', font, RED, SCREEN_WIDTH - 100, SCREEN_HEIGHT + LOWER_MARGIN - 70)

	#save and load data
	if save_button.draw(screen):
		#save level data
		with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter = ',')
			for row in world_data:
				writer.writerow(row)
		#alternative pickle method
		#pickle_out = open(f'level{level}_data', 'wb')
		#pickle.dump(world_data, pickle_out)
		#pickle_out.close()
	if load_button.draw(screen):
		#load in level data
		#reset scroll back to the start of the level
		scroll = 0
		with open(f'level{level}_data.csv', newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter = ',')
			for x, row in enumerate(reader):
				for y, tile in enumerate(row):
					world_data[x][y] = int(tile)
		#alternative pickle method
		#world_data = []
		#pickle_in = open(f'level{level}_data', 'rb')
		#world_data = pickle.load(pickle_in)
				

	#draw tile panel and tiles
	pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	#choose a tile
	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	#highlight the selected tile
	pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

	#scroll the map
	if scroll_left == True and scroll > 0:
		scroll -= 5 * scroll_speed
	if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
		scroll += 5 * scroll_speed

	#add new tiles to the screen
	#get mouse position
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	#check that the coordinates are within the tile area
	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		#update tile value
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 1:
				level -= 1
			if event.key == pygame.K_LEFT:
				scroll_left = True
			if event.key == pygame.K_RIGHT:
				scroll_right = True
			if event.key == pygame.K_q:
				scroll_speed = 5
			if event.key == pygame.K_ESCAPE:
				run = False


		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				scroll_left = False
			if event.key == pygame.K_RIGHT:
				scroll_right = False
			if event.key == pygame.K_q:
				scroll_speed = 1


	pygame.display.update()

pygame.quit()
