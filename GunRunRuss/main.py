import pygame
import os
import random
import csv

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 31
screen_scroll = 0
bg_scroll = 0
level = 0

#define player action variables
moving_left = False
moving_right = False
shoot = False
grenade = False
grenade_thrown = False


#load background images 
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

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)
#bullet
bullet_img = pygame.image.load('assets/Player/Bullet/0.png').convert_alpha()

#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#define font
font = pygame.font.SysFont('Futura', 30)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_bg():
	screen.fill(BG)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))
		screen.blit(bg4_img, ((x * width) - bg_scroll * 0.45, SCREEN_HEIGHT - bg4_img.get_height() - 10))
		screen.blit(bg5_img, ((x * width) - bg_scroll * 0.5, SCREEN_HEIGHT - bg5_img.get_height() - 10))



class Characters(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		self.shoot_cooldown = 0
		self.health = 100
		self.max_health = self.health
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#ai specific variables
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0
		
		#load all images for the players
		animation_types = ['Idle', 'Run', 'Jump', 'Death']
		for animation in animation_types:
			#reset temporary list of images
			temp_list = []
			#count number of files in the folder
			num_of_frames = len(os.listdir(f'assets/{self.char_type}/{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'assets/{self.char_type}/{animation}/{i}.png').convert_alpha()
				img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
				temp_list.append(img)
			self.animation_list.append(temp_list)

		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.width = self.image.get_width()
		self.height = self.image.get_height()


	def update(self):
		self.update_animation()
		self.check_alive()
		#update cooldown
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1


	def move(self, moving_left, moving_right):
		#reset movement variables
		screen_scroll = 0
		dx = 0
		dy = 0

		#assign movement variables if moving left or right
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#jump
		if self.jump == True and self.in_air == False:
			self.vel_y = -15
			self.jump = False
			self.in_air = True

		#apply gravity
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		#check for collision
		for tile in world.obstacle_list:
			#check collision in the x direction
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
				#if the ai has hit a wall then make it turn around
				if self.char_type == 'Enemy':
					self.direction *= -1
					self.move_counter = 0
			#check for collision in the y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e. jumping
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom


		#check if going off the edges of the screen
		if self.char_type == 'Player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll based on player position
		if self.char_type == 'Player':
			if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
				self.rect.x -= dx
				screen_scroll = -dx

		return screen_scroll



	def shoot(self):
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = 20
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)


	def ai(self):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)#0: idle
				self.idling = True
				self.idling_counter = 50
			#check if the ai in near the player
			if self.vision.colliderect(player.rect):
				#stop running and face the player
				self.update_action(0)#0: idle
				#shoot
				self.shoot()
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_moving_right = True
					else:
						ai_moving_right = False
					ai_moving_left = not ai_moving_right
					self.move(ai_moving_left, ai_moving_right)
					self.update_action(1)#1: run
					self.move_counter += 1
					#update ai vision as the enemy moves
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

					if self.move_counter > TILE_SIZE:
						self.direction *= -1
						self.move_counter *= -1
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False

		#scroll
		self.rect.x += screen_scroll


	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 100
		#update image depending on current frame
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out the reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.frame_index = 0



	def update_action(self, new_action):
		#check if the new action is different to the previous one
		if new_action != self.action:
			self.action = new_action
			#update the animation settings
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)


	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		self.level_length = len(data[0])
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile == 0:
						self.obstacle_list.append(tile_data)
					elif tile >= 1 and tile <= 10:
						water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)
					elif tile >= 11 and tile <= 22:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)
					elif tile == 23:#create player
						player = Characters('Player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5)
					elif tile == 24:#create enemies
						enemy = Characters('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2)
						enemy_group.add(enemy)

		return player


	def draw(self):
		for tile in self.obstacle_list:
			tile[1][0] += screen_scroll
			screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

	def update(self):
		self.rect.x += screen_scroll

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		pygame.sprite.Sprite.__init__(self)
		self.speed = 10
		self.image = bullet_img
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.direction = direction

	def update(self):
		#move bullet
		self.rect.x += (self.direction * self.speed) + screen_scroll
		#check if bullet has gone off screen
		if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
			self.kill()
		#check for collision with level
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect):
				self.kill()

		#check collision with characters
		if pygame.sprite.spritecollide(player, bullet_group, False):
			if player.alive:
				player.health -= 5
				self.kill()
		for enemy in enemy_group:
			if pygame.sprite.spritecollide(enemy, bullet_group, False):
				if enemy.alive:
					enemy.health -= 25
					self.kill()

#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()




#create empty tile list
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)
#load in level data and create world
with open(f'level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)



run = True
while run:

	clock.tick(FPS)

	#update background
	draw_bg()

	#draw world map
	world.draw()

	player.update()
	player.draw()

	for enemy in enemy_group:
		enemy.ai()
		enemy.update()
		enemy.draw()

	#update and draw groups
	bullet_group.update()
	decoration_group.update()
	water_group.update()
	
	bullet_group.draw(screen)
	decoration_group.draw(screen)
	water_group.draw(screen)

	#update player actions
	if player.alive:
		#shoot bullets
		if shoot:
			player.shoot()
		if player.in_air:
			player.update_action(2)#2: jump
		elif moving_left or moving_right:
			player.update_action(1)#1: run
		else:
			player.update_action(0)#0: idle
		screen_scroll = player.move(moving_left, moving_right)
		bg_scroll -= screen_scroll

	for event in pygame.event.get():
		#quit game
		if event.type == pygame.QUIT:
			run = False
		#keyboard presses
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_UP and player.alive:
				player.jump = True
			if event.key == pygame.K_ESCAPE:
				run = False


		#keyboard button released
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False


	pygame.display.update()

pygame.quit()