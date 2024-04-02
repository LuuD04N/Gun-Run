import pygame
from pygame import mixer
import os
import random
import csv
import button

mixer.init()
pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gun&Run')
pygame.display.set_icon(pygame.image.load('assets/icon.ico'))


#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 44
MAX_LEVELS = 3
scale_tamban = 1.5
screen_scroll = 0
bg_scroll = 0
level = 0
star_game = False
enemy_count = 0


#define player action variables
moving_left = False
moving_right = False
shoot = False

#load sounds
if level < MAX_LEVELS - 1:
	pygame.mixer.music.load('assets/audio/level_music.mp3')
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play(-1, 0.0, 5000)
else:
	pygame.mixer.music.load('assets/audio/boss_music.mp3')
	pygame.mixer.music.set_volume(0.1)
	pygame.mixer.music.play(-1, 0.0, 5000)


jump_fx = pygame.mixer.Sound('assets/audio/sfx/jump.wav')
jump_fx.set_volume(0.5)
shoot_fx = pygame.mixer.Sound('assets/audio/sfx/shot.wav')
shoot_fx.set_volume(0.5)
health_fx = pygame.mixer.Sound('assets/audio/sfx/health.wav')
health_fx.set_volume(0.3)
powerup_fx = pygame.mixer.Sound('assets/audio/sfx/powerup.wav')
powerup_fx.set_volume(3)
explode_fx = pygame.mixer.Sound('assets/audio/sfx/explode.wav')
explode_fx.set_volume(3)

#pick up boxes
health_box_img = pygame.image.load('assets/Tilemap/39.png').convert_alpha()
power_box_img = pygame.image.load('assets/Tilemap/41.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'PowerUp'	: power_box_img
}

#define font
font = pygame.font.SysFont('Futura', 30)

#buttons images
start_img_ori = pygame.image.load('assets/Buttons/Play.png').convert_alpha()
start_img = pygame.transform.scale(start_img_ori, (start_img_ori.get_width() * 5, start_img_ori.get_height() * 4))

exit_img_ori = pygame.image.load('assets/Buttons/Close.png').convert_alpha()
exit_img = pygame.transform.scale(exit_img_ori, (exit_img_ori.get_width() * 3, exit_img_ori.get_height() * 3))

restart_img_ori = pygame.image.load('assets/Buttons/Restart.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img_ori, (restart_img_ori.get_width() * 5, restart_img_ori.get_height() * 5))

bg_menu_ori = pygame.image.load('assets/Background/menu_bg.png').convert_alpha()
bg_menu = pygame.transform.scale(bg_menu_ori, (SCREEN_WIDTH, SCREEN_HEIGHT))

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

# load bullet images
bullet_img = pygame.image.load('assets/Player/Bullet/0.png').convert_alpha()

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


#define colours
BG = (144, 201, 120)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

#draw backgrounds 
def draw_bg_0_to_3():
	screen.fill(BG)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))
		screen.blit(bg4_img, ((x * width) - bg_scroll * 0.45, SCREEN_HEIGHT - bg4_img.get_height() - 10))
		screen.blit(bg5_img, ((x * width) - bg_scroll * 0.5, SCREEN_HEIGHT - bg5_img.get_height() + 10))

def draw_bg_4():
	screen.fill(BG)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))

def draw_bg_5():
	screen.fill(BG)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		


#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	spike_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data



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
		self.vision = pygame.Rect(0, 0, 150 * scale_tamban, 20)
		self.idling = False
		self.idling_counter = 0
		self.check_death = False
		#update power
		self.power_up_timer = 0
		
		#load all images for the players
		animation_types = ['Idle', 'Run', 'Jump', 'Death', 'ShootIdle', 'ShootRun']
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
		
		if self.power_up_timer > 0:
			self.power_up_timer -= 1
		else:
			self.power_up_timer = 0


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
					self.move_counter += 1 #move_counter = 0
			#check for collision in the y direction
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height + 2):
				#check if below the ground, i.e. jumping
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e. falling
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom

		#check for collision with spike
		if pygame.sprite.spritecollide(self, spike_group, False):
			self.health = 0
		
		#check for collision with exit
		level_complete = False
		if pygame.sprite.spritecollide(self, exit_group, False):
			level_complete = True

		#check if fallen off the map
		if self.rect.bottom > SCREEN_HEIGHT:
			self.health = 0

		#check if going off the edges of the screen
		if self.char_type == 'Player':
			if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
				dx = 0

		#check for collision with spike
		if pygame.sprite.spritecollide(self, spike_group, False):
			self.health = 0

		#update rectangle position
		self.rect.x += dx
		self.rect.y += dy

		#update scroll based on player position
		if self.char_type == 'Player':
			if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH)\
				or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
				self.rect.x -= dx
				screen_scroll = -dx
		#check collision with boss
		for boss in enemy_group:
			if boss.char_type == 'Boss' and self.char_type == 'Player':
				if self.rect.colliderect(boss.rect):
					self.health -= 0.5  # trừ nửa máu

		return screen_scroll, level_complete



	def shoot(self):
		if self.shoot_cooldown == 0:
			if self.power_up_timer > 0:
				self.shoot_cooldown = 15
			else:
				self.shoot_cooldown = 30
			if self.char_type == "Player":
				bullet = PlayerBullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery + 5, self.direction)
			else:
				bullet = EnemyBullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery + 5, self.direction)
			
			bullet_group.add(bullet)
			shoot_fx.play()

	def ai(self):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)#0: idle
				self.idling = True
				self.idling_counter = 50
				
			#check if the ai in near the player
			if self.vision.colliderect(player.rect):
				#stop running and face the player
				self.shoot()
				self.update_action(4)
				
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
					self.vision.center = (self.rect.centerx + 75 * scale_tamban * self.direction, self.rect.centery)
					# pygame.draw.rect(screen, RED, self.vision)
					
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
		global enemy_count

		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)
			if self.char_type == 'Player':
				self.rect.y -= 1
			if self.char_type == 'Enemy' and not self.check_death:
				explode_fx.play()
				self.check_death = True
				enemy_count -= 1



	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		global enemy_count

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


					if tile >= 0 and tile <= 20 or tile == 43:
						self.obstacle_list.append(tile_data)

					elif tile >= 24 and tile <= 38:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)

					elif tile == 40: #trap
						spike = Spike(img, x * TILE_SIZE, y * TILE_SIZE)
						spike_group.add(spike)

					elif tile == 41:
						item_box = ItemBox('PowerUp', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)

					elif tile == 39:#create health box
						item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
						item_box_group.add(item_box)

					elif tile == 23:#create player
						player = Characters('Player', x * TILE_SIZE, y * TILE_SIZE, 1.65, 5)
						health_bar = HealthBar(10, 10, player.health, player.health)

					elif tile == 22:#create enemies
						enemy = Characters('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.65, 2)
						enemy_group.add(enemy)
						enemy_count += 1
					
					elif tile == 21:
						boss = Boss(x * TILE_SIZE, y * TILE_SIZE, 2, 2)
						enemy_group.add(boss)
						enemy_count += 1
					
					elif tile == 42:
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)


		return player, health_bar


	def draw(self):
		for tile in self.obstacle_list:
			if tile[0] != img_list[43] or enemy_count > 0:
				tile[1][0] += screen_scroll
				screen.blit(tile[0], tile[1])

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self):
		self.rect.x += screen_scroll


class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
  
	def update(self):
		#scroll
		self.rect.x += screen_scroll
		#check if the player has picked up the box
		if pygame.sprite.collide_rect(self, player):
			#check what kind of box it was
			if self.item_type == 'Health':
				player.health += 25
				health_fx.play()
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'PowerUp':
				powerup_fx.play()
				player.power_up_timer = 300 #300 khung hinh = 5 giay
			
			#delete the item box
			self.kill()

class HealthBar():
	def __init__(self, x, y, health, max_health):
		self.x = x
		self.y = y
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		#update with new health
		self.health = health
		#calculate health ratio
		ratio = self.health / self.max_health
		pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))
  
class Spike(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()) + 1)

	def update(self):
		self.rect.x += screen_scroll

class Boss(Characters):
	def __init__(self, x, y, scale, speed):
		super().__init__('Boss', x, y, scale, speed)
		self.health = 1000
		self.move_direction = 1  # 1 xuống, -1 lên
		self.shoot_cooldown = 0
		self.bullet_cooldown = 60
		self.sound_death = False
		self.alive = True
		

	def move(self):
		dx = 0
		dy = self.speed * self.move_direction

		# Kiểm tra va chạm với các vật cản
		for tile in world.obstacle_list:
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
			# Nếu va chạm, đổi chiều di chuyển
				self.move_direction *= -1
				dy = 0
				break

        # Cập nhật vị trí mới
		self.rect.y += dy
	
	def shoot(self):
		if self.shoot_cooldown == 0:
			self.shoot_cooldown = self.bullet_cooldown  # cooldown thấp, bắn nhanh
			if random.randint(1,2) == 1: 
				self.direction *= -1
			bullet = BossBullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
			bullet_group.add(bullet)
			# shoot_fx.play()


	def ai(self):
		global enemy_count
		if player.alive and self.alive:
			if self.health > 700:
				self.move()
				self.update_action(1)  # 1: run
				self.rect.x += screen_scroll
				self.shoot()
			elif self.health >=1 and self.health <= 700:
				self.bullet_cooldown = 10
				self.speed = 5
				self.move()
				self.update_action(4)
				self.rect.x += screen_scroll
				self.shoot()
			else:
				self.alive = False
				enemy_count -= 1

		if player.alive and not self.alive:
			self.update_action(3)
			self.rect.x += screen_scroll
			self.health = 0
			
			if not self.sound_death:
				explode_fx.play()
				self.sound_death = True
				
		if self.shoot_cooldown > 0:
			self.shoot_cooldown -= 1  # Giảm shoot_cooldown xuống sau mỗi khung hình

		

class Decoration(pygame.sprite.Sprite):
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
					enemy.health -= 55
					self.kill()

class PlayerBullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.speed = 10  # Tốc độ đạn của player
        self.image = pygame.transform.scale2x(pygame.image.load('assets/Player/Bullet/0.png')).convert_alpha()

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.speed = 8  # Tốc độ đạn của enemy
        self.image = pygame.transform.scale2x(pygame.image.load('assets/Enemy/Bullet/0.png')).convert_alpha()

class BossBullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.speed = 8  # Tốc độ đạn của boss
        image = pygame.transform.scale2x(pygame.image.load('assets/Boss/Bullet/3.png')).convert_alpha()
        self.image = pygame.transform.scale(image, (image.get_width() * 0.55, image.get_height() * 0.55))

#create buttons
star_button = button.Button(SCREEN_WIDTH // 2 - 52, SCREEN_HEIGHT // 2 - 100, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 24, SCREEN_HEIGHT // 2 + 30, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 52, SCREEN_HEIGHT // 2 - 100, restart_img, 1)
		
#create sprite groups
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()




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
player, health_bar = world.process_data(world_data)



run = True
while run:

	clock.tick(FPS)
	if star_game == False:
		#draw menu
		screen.blit(bg_menu, (0,0))
		#add buttons
		if star_button.draw(screen):
			star_game = True
		if exit_button.draw(screen):
			run = False
		
	else:
		#update background
		if level == 0:
			draw_bg_0_to_3()
			
		elif level == 1:
			draw_bg_4()
		else:
			draw_bg_5()


		draw_text(f'Level: {level}', font, WHITE, 200, 15)	
		if level < MAX_LEVELS - 1:
			draw_text(f'|   Enemy: {enemy_count}', font, WHITE, 300, 15)
		
			

		#draw world map
		world.draw()
		
		#draw health bar player
		health_bar.draw(player.health)

		player.update()
		player.draw()
		for entity in enemy_group:
			if entity.char_type == 'Boss':
				entity.ai()
				entity.update()
				entity.draw()
				if level == MAX_LEVELS - 1:
					draw_text(f'|   Boss\'s Health: {entity.health}', font, WHITE, 300, 15)
			else:
				entity.ai()
				entity.update()
				entity.draw()

		#update and draw groups
		bullet_group.update()
		decoration_group.update()
		spike_group.update()
		item_box_group.update()	
		exit_group.update()
	
		bullet_group.draw(screen)
		decoration_group.draw(screen)
		spike_group.draw(screen)
		item_box_group.draw(screen)
		exit_group.draw(screen)

		#update player actions
		#player alive
		if player.alive:
			#shoot bullets
			if shoot and moving_left or shoot and moving_right:
				player.shoot()
				player.update_action(5)#run shoot
			elif shoot:
				player.shoot()
				player.update_action(4)#idle shoot
			elif player.in_air:
				player.update_action(2)#2: jump
			elif moving_left or moving_right:
				player.update_action(1)#1: run
			else:
				player.update_action(0)#0: idle

			screen_scroll, level_complete = player.move(moving_left, moving_right)
			bg_scroll -= screen_scroll

			#check if player has completed the level
			if level_complete:
				level += 1
				bg_scroll = 0
				world_data = reset_level()
				if level <= MAX_LEVELS:
					#load in level data and create world
					with open(f'level{level}_data.csv', newline='') as csvfile:
						reader = csv.reader(csvfile, delimiter=',')
						for x, row in enumerate(reader):
							for y, tile in enumerate(row):
								world_data[x][y] = int(tile)
					world = World()
					player, health_bar = world.process_data(world_data)

					#stop music and play new music when meet boss
					if level == MAX_LEVELS - 1:
						pygame.mixer.music.load('assets/audio/boss_music.mp3')
						pygame.mixer.music.set_volume(0.1)
						pygame.mixer.music.play(-1, 0.0, 5000)


					
		#player death
		else:
			screen_scroll = 0
			if restart_button.draw(screen):
				bg_scroll = 0
				enemy_count = 0
				world_data = reset_level()
				#load in level data and create world
				with open(f'level{level}_data.csv', newline='') as csvfile:
					reader = csv.reader(csvfile, delimiter=',')
					for x, row in enumerate(reader):
						for y, tile in enumerate(row):
							world_data[x][y] = int(tile)
				world = World()
				player, health_bar = world.process_data(world_data)
			elif exit_button.draw(screen):
				run = False


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
				jump_fx.play()
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