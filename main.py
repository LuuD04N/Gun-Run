import pygame, os, random, csv, button, asyncio
from pygame import mixer

mixer.init()
pygame.init()
#--------------------VARIABLES---------------------#
#set framerate
clock = pygame.time.Clock()
FPS = 60

#define game variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.72)
GRAVITY = 0.75
SCROLL_THRESH = 200
ROWS = 16
COLS = 150 
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 45
MAX_LEVELS = 7
ENDING_TEXT_SPEED = 1
ENDING_CRE_TEXT_SPEED = 1

#define colours
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

scale_tamban = 1.5
screen_scroll = 0
bg_scroll = 0
level = 1
start_game = False
enemy_count = 0
ending_text_y = SCREEN_HEIGHT + 120
ending_cre_text_y = SCREEN_HEIGHT
setting = True
exit_menu = True
exit_ingame = False
hint_check = False
hint_count = 0
play_count = 0
is_level_editor = False

#define player action variables
moving_left = False
moving_right = False
shoot = False

#--------------------SCREEN---------------------#

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gun&Run')
pygame.display.set_icon(pygame.image.load('assets/icon.ico'))

#--------------------IMAGES, FONTS AND SOUNDS---------------------#
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
death_fx = pygame.mixer.Sound('assets/audio/sfx/death_sound.WAV')
death_fx.set_volume(3)

#pick up boxes
health_box_img = pygame.image.load('assets/Tilemap/39.png').convert_alpha()
power_box_img = pygame.image.load('assets/Tilemap/41.png').convert_alpha()
item_boxes = {
	'Health'	: health_box_img,
	'PowerUp'	: power_box_img
}

#define font
font = pygame.font.SysFont('Futura', 30)
font_ending = pygame.font.SysFont('Futura', 70)

#buttons images
start_img_ori = pygame.image.load('assets/Buttons/Play.png').convert_alpha()
start_img = pygame.transform.scale(start_img_ori, (start_img_ori.get_width() * 5, start_img_ori.get_height() * 4))

exit_img_ori = pygame.image.load('assets/Buttons/Close.png').convert_alpha()
exit_img = pygame.transform.scale(exit_img_ori, (exit_img_ori.get_width() * 3, exit_img_ori.get_height() * 3))

restart_img_ori = pygame.image.load('assets/Buttons/Restart.png').convert_alpha()
restart_img = pygame.transform.scale(restart_img_ori, (restart_img_ori.get_width() * 5, restart_img_ori.get_height() * 5))

setting_img_ori = pygame.image.load('assets/Buttons/Settings.png').convert_alpha()
setting_img = pygame.transform.scale(setting_img_ori, (setting_img_ori.get_width() * 2, setting_img_ori.get_height() * 2))

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

bg_menu_ori = pygame.image.load('assets/Background/menu_bg.png').convert_alpha()
bg_menu = pygame.transform.scale(bg_menu_ori, (SCREEN_WIDTH, SCREEN_HEIGHT))

# load bullet images
bullet_img = pygame.image.load('assets/Player/Bullet/0.png').convert_alpha()
boss_bullet_img = pygame.transform.scale2x(pygame.image.load('assets/Boss/Bullet/2.png')).convert_alpha()
enemy_bullet_img = pygame.transform.scale2x(pygame.image.load('assets/Enemy/Bullet/0.png')).convert_alpha()

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


def level_music():
	pygame.mixer.music.load('assets/audio/level_music.ogg')
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play(-1, 0.0, 5000)

def boss_music():
	pygame.mixer.music.load('assets/audio/boss_music.ogg')
	pygame.mixer.music.set_volume(0.1)
	pygame.mixer.music.play(-1, 0.0, 5000)

def ending_music():
	pygame.mixer.music.load('assets/audio/ending_music.ogg')
	pygame.mixer.music.set_volume(0.3)
	pygame.mixer.music.play(-1, 10.0, 5000)

if level < MAX_LEVELS - 1:
	level_music()
elif level == MAX_LEVELS - 1:
	boss_music()
else:
	ending_music()

def draw_text(screen, text, font, text_col, x, y):
    lines = text.split("\n")  #split text if " endl "
    for i, line in enumerate(lines):
        img = font.render(line, True, text_col)
        screen.blit(img, (x, y + i * font.get_linesize()))

#draw backgrounds 
def draw_bg_1_to_3():
	screen.fill(GREEN)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))
		screen.blit(bg4_img, ((x * width) - bg_scroll * 0.45, SCREEN_HEIGHT - bg4_img.get_height() - 10))
		screen.blit(bg5_img, ((x * width) - bg_scroll * 0.5, SCREEN_HEIGHT - bg5_img.get_height() + 10))

def draw_bg_4_to_5():
	screen.fill(GREEN)
	width = bg1_img.get_width()
	for x in range(5):
		screen.blit(bg1_img, ((x * width) - bg_scroll * 0.3, 0))
		screen.blit(bg2_img, ((x * width) - bg_scroll * 0.35, SCREEN_HEIGHT - bg2_img.get_height() - 10))
		screen.blit(bg3_img, ((x * width) - bg_scroll * 0.4, SCREEN_HEIGHT - bg3_img.get_height() - 10))

def draw_bg_6_to_7():
	screen.fill(GREEN)
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
	hint_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data

#--------------------CLASSES---------------------#
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
				if boss.alive == True:
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

			if self.char_type == 'Player' and not self.check_death:
				death_fx.play()
				self.check_death = True

			if self.char_type == 'Player':
				self.rect.y -= 1

			if self.char_type == 'Enemy' and not self.check_death:
				pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/audio/sfx/explode.wav'))
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
						boss = Boss(x * TILE_SIZE, y * TILE_SIZE, 2, 3)
						enemy_group.add(boss)
						enemy_count += 1
					
					elif tile == 42:
						exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
						exit_group.add(exit)

					elif tile == 44:
						hint = Hint(img, x * TILE_SIZE, y * TILE_SIZE)
						hint_group.add(hint)

		return player, health_bar


	def draw(self):
		for tile in self.obstacle_list:
			if tile[0] != img_list[43] or enemy_count > 0 :
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

class Hint(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
	
	def update(self):
		global hint_count
		self.rect.x += screen_scroll
		if pygame.sprite.collide_rect(self, player):
			hint_check = True
			hint_count += 1
			if hint_count > 0:
				if level == 1:
					if hint_check and hint_count >= 1 and hint_count <= 100:
						draw_text(screen, 'Press < > to move left and right, press ^ to jump', font, WHITE, 300, 300)	
				
					if hint_check and hint_count >= 101 and hint_count <= 200:
						draw_text(screen, 'Try to shoot by press SPACE', font, WHITE, 500, 300)	

					if hint_check and hint_count >= 201 and hint_count <= 400:
						draw_text(screen, 'Pass through those HEARTS to heal \n\n    Those POWER BOX to power up', font, WHITE, 350, 400)
				elif level == 2:
					if hint_check and hint_count >= 1 and hint_count <= 200:
						draw_text(screen, 'See that SPIKE? touch it if you want to see GODS', font ,WHITE, 300, 300)
				elif level == 4:
					if hint_check and hint_count >= 1 and hint_count <= 200:
						draw_text(screen, 'Keep going, the GREATEST mystery await you at the end', font, WHITE, 400, 150)
				elif level == 6:
					if hint_check and hint_count >=1 and hint_count <= 200:
						draw_text(screen, 'OMG, a big SKULL! Can you defeat it?', font, WHITE, 500, 300)	

			if hint_count >= 401:
				hint_count = 0

			
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
		self.health = 2000
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
			shoot_fx.play()


	def ai(self):
		global enemy_count
		#when boss alive
		if player.alive and self.alive:
			if self.health > 1500:
				self.move()
				self.update_action(1)  # 1: run
				self.rect.x += screen_scroll
				self.shoot()
			elif self.health >=1 and self.health <= 1500:
				self.bullet_cooldown = 6
				self.speed = 6
				self.move()
				self.update_action(4)
				self.rect.x += screen_scroll
				self.shoot()
			else:
				self.alive = False
				enemy_count -= 1
		
		#when boss die
		if player.alive and not self.alive:
			self.update_action(3)

			self.rect.x += screen_scroll
			self.health = 0
			
			if not self.sound_death:
				pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/audio/sfx/explode.wav'))
				pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/audio/sfx/boss_death.ogg'))

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
        self.image = pygame.transform.scale2x(bullet_img).convert_alpha()

class EnemyBullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.speed = 8  # Tốc độ đạn của enemy
        self.image = enemy_bullet_img

class BossBullet(Bullet):
    def __init__(self, x, y, direction):
        super().__init__(x, y, direction)
        self.speed = 8  # Tốc độ đạn của boss
        image = boss_bullet_img
        self.image = pygame.transform.scale(image, (image.get_width() * 0.55, image.get_height() * 0.55))


#--------------------BUTTONS---------------------#
start_button = button.Button(SCREEN_WIDTH // 2 - 52, SCREEN_HEIGHT // 2 - 100, start_img, 1)
exit_menu_button = button.Button(SCREEN_WIDTH // 2 - 48, SCREEN_HEIGHT // 2 + 30, exit_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 24, SCREEN_HEIGHT // 2 + 30, exit_img, 1)

setting_button = button.Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 30, setting_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 52, SCREEN_HEIGHT // 2 - 100, restart_img, 1)


#--------------------GROUPS---------------------#
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
spike_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
hint_group = pygame.sprite.Group()


#--------------------CREATE WORLD, LOAD FROM FILE---------------------#
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

def open_file():
	#game window
	SCREEN_WIDTH = 500
	SCREEN_HEIGHT = 446
	LOWER_MARGIN = 130
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
	
	save_img = pygame.image.load('assets/Buttons/Restart.png').convert_alpha()
	load_img = pygame.image.load('assets/Buttons/Levels.png').convert_alpha()
	next_img = pygame.image.load('assets/Buttons/Close.png').convert_alpha()
	
	#define font
	font = pygame.font.SysFont('Futura', 30)
	
	#create buttons
	save_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 100, save_img, 2)
	next_button = button.Button(SCREEN_WIDTH // 2 + 105, SCREEN_HEIGHT + LOWER_MARGIN - 100, next_img, 3)
	load_button = button.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 100, load_img, 2)
	
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
	
		draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 100)
		draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
		draw_text('RESTART GAME TO LOAD LEVEL !', font, RED, SCREEN_WIDTH - 100, SCREEN_HEIGHT + LOWER_MARGIN - 40)
	
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
		if next_button.draw(screen):
			is_level_editor = False
			return
					
	
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
	
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					scroll_left = False
				if event.key == pygame.K_RIGHT:
					scroll_right = False
				if event.key == pygame.K_q:
					scroll_speed = 1
	
	
		pygame.display.update()
	
	pygame.quit()

#--------------------LOOP GAME---------------------#
async def main():
	global scale_tamban
	global screen_scroll 
	global bg_scroll 
	global level
	global start_game 
	global enemy_count 
	global ending_text_y 
	global ending_cre_text_y 
	global setting 
	global exit_menu 
	global exit_ingame 
	global hint_check 
	global hint_count
	global play_count
	global is_level_editor 
	global world, player, health_bar

	#define player action variables
	global moving_left 
	global moving_right 
	global shoot 

	run = True
	while run:

		clock.tick(FPS)

		#--------------------START GAME---------------------#
		if is_level_editor:
			open_file()
		else:
			if start_game == False:
				#draw menu
				screen.blit(bg_menu, (0,0))
				#add buttons
				if start_button.draw(screen):
					start_game = True
					pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/audio/start_game.wav'))

				if exit_menu == True and exit_ingame == False:
					if exit_menu_button.draw(screen):
						run = False
				elif exit_menu == False and exit_ingame == True:
					if exit_button.draw(screen):
						run = False

				if setting == True:
					if setting_button.draw(screen):
						open_file()

			#--------------------IN GAME---------------------#
			else:
				#update background
				if level >= 1 and level <= 3:
					draw_bg_1_to_3()

				elif level >= 4 and level <= 5:
					draw_bg_4_to_5()
				else:
					draw_bg_6_to_7()

				if level == MAX_LEVELS:
					ending_text_y -= ENDING_TEXT_SPEED
					ending_cre_text_y -= ENDING_CRE_TEXT_SPEED
					if ending_text_y == SCREEN_HEIGHT // 2- 200:
						ENDING_TEXT_SPEED = 0	
					if ending_cre_text_y == SCREEN_HEIGHT // 2 - 100:
						ENDING_CRE_TEXT_SPEED = 0	

					text1 = 'Thanks for playing'
					text2 = 'CRE by: \n 1. Dang Khoa \n 2. Phong Luu'

					draw_text(screen, text1, font_ending, YELLOW, SCREEN_WIDTH // 2 - 300, ending_text_y)
					draw_text(screen, text2, font, WHITE, SCREEN_WIDTH // 2 - 300, ending_cre_text_y)
					if play_count == 0:
						draw_text(screen, f'\n\n\n\nCongratulations! {play_count} death, ON POINT!', font,  WHITE, SCREEN_WIDTH // 2 - 300, ending_cre_text_y)	
					elif play_count == 1:
						draw_text(screen, f'\n\n\n\nCongratulations! {play_count} death, very good!', font,  WHITE, SCREEN_WIDTH // 2 - 300, ending_cre_text_y)	
					else:
						draw_text(screen, f'\n\n\n\nCongratulations! {play_count} deaths, not bad!.', font, WHITE, SCREEN_WIDTH // 2 - 300, ending_cre_text_y)	


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
							draw_text(screen, f'Level: {level}', font, WHITE, 200, 12)	
							draw_text(screen, f'|   Enemy: {enemy_count}', font, WHITE, 300, 12)
							draw_text(screen, f'|   Boss\'s Health: {entity.health}', font, YELLOW, 750, 12)
							draw_text(screen, f'|  Skill\'s time: {player.power_up_timer}', font, WHITE, 440, 12)
							draw_text(screen, f'|  Deaths: {play_count}', font, WHITE, 620, 12)	

					else:
						entity.ai()
						entity.update()
						entity.draw()

						if level < MAX_LEVELS - 1:
							draw_text(screen, f'Level: {level}', font, WHITE, 200, 12)	
							draw_text(screen, f'|   Enemy: {enemy_count}', font, WHITE, 300, 12)
							draw_text(screen, f'|  Skill\'s time: {player.power_up_timer}', font, WHITE, 440, 12)
							draw_text(screen, f'|  Deaths: {play_count}', font, WHITE, 620, 12)	


				#update and draw groups
				bullet_group.update()
				decoration_group.update()
				spike_group.update()
				item_box_group.update()	
				exit_group.update()
				hint_group.update()

				bullet_group.draw(screen)
				decoration_group.draw(screen)
				spike_group.draw(screen)
				item_box_group.draw(screen)
				exit_group.draw(screen)
				hint_group.draw(screen)

				#--------------------IF PLAYER ALIVE---------------------#
				#update player actions
				if player.alive:
					#shoot bullets   
					if shoot and moving_left or shoot and moving_right:
						player.shoot()
						player.update_action(5)#5: run shoot
					elif shoot:
						player.shoot()
						player.update_action(4)#4: idle shoot
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

						if level <= MAX_LEVELS - 1:
							level += 1
							bg_scroll = 0
							world_data = reset_level()
							#load in level data and create world
							with open(f'level{level}_data.csv', newline='') as csvfile:
								reader = csv.reader(csvfile, delimiter=',')
								for x, row in enumerate(reader):
									for y, tile in enumerate(row):
										world_data[x][y] = int(tile)
							world = World()
							player, health_bar = world.process_data(world_data)

							#stop music and play new music in new levels
							if level == MAX_LEVELS - 1:
								boss_music()

							if level == MAX_LEVELS:
								ending_music()
						else:
							draw_text(screen, 'Kill yourself!', font, RED, SCREEN_WIDTH // 2 + 200, ending_cre_text_y)




				#--------------------IF PLAYER DIE---------------------#
				else:
					screen_scroll = 0
					if restart_button.draw(screen):
						bg_scroll = 0
						enemy_count = 0
						play_count += 1
						if level == MAX_LEVELS:
							level = 1
							start_game = False
							play_count = 0
							level_music()

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

			#--------------------KEY ACTIONS---------------------#
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
						if start_game == True:
							start_game = False
							setting = False
							exit_menu = False 
							exit_ingame = True
						else:
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
		await asyncio.sleep(0)
	pygame.quit()
asyncio.run(main())