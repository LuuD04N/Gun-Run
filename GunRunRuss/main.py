import pygame
import os
import random
import csv

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gun&Run')
pygame.display.set_icon(pygame.image.load('assets\\icon.ico'))

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 91
level = 0


moving_left = False
moving_right = False
shoot = False

#Tải ảnh 
bullet_img_ori = pygame.image.load('assets\\Player\\Bullet\\0.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img_ori, (bullet_img_ori.get_width() * 2, bullet_img_ori.get_height() * 2))

#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png')
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

BG = (0, 0, 0)
RED = (255, 0, 0)

def draw_bg():
	screen.fill(BG)


class Characters(pygame.sprite.Sprite):
	def __init__(self, char_type, x, y, scale, speed, ammo):
		pygame.sprite.Sprite.__init__(self)
		self.alive = True
		self.char_type = char_type
		self.speed = speed
		# #co the luoc bo
		# self.ammo = ammo
		# self.star_ammo = ammo

		self.health = 100
		self.max_health = self.health

		self.shoot_cooldown = 0
		self.direction = 1
		self.vel_y = 0
		self.jump = False
		self.in_air = True
		self.flip = False
		self.animation_list = []
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()
		#create ai specific var
		self.move_counter = 0
		self.vision = pygame.Rect(0, 0, 150, 20)
		self.idling = False
		self.idling_counter = 0



		#Tải tất cả ảnh của người chơi
		animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Shoot']
		for animation in animation_types:
			#Đặt lại danh sách tạm thời
			temp_list = []
			#Đếm số file trong 1 folder
			num_of_frames = len(os.listdir(f'assets\\{self.char_type}\\{animation}'))
			for i in range(num_of_frames):
				img = pygame.image.load(f'assets\\{self.char_type}\\{animation}\\{i}.png').convert_alpha()
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
		#Tạo lại trạng thái biến 
		dx = 0
		dy = 0

		#Tạo biến di chuyển và phương thức DI CHUYỂN <trái - phải>
		if moving_left:
			dx = -self.speed
			self.flip = True
			self.direction = -1
		if moving_right:
			dx = self.speed
			self.flip = False
			self.direction = 1

		#Phương thức NHẢY
		if self.jump == True and self.in_air == False:
			self.vel_y = -15
			self.jump = False
			self.in_air = True
			
		#Áp dụng lực hấp dẫn
		self.vel_y += GRAVITY
		if self.vel_y > 10:
			self.vel_y
		dy += self.vel_y

		#Check va cham
		for tile in world.obstacle_list:
			#check va cham theo x
			if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
				dx = 0
			#check va cham theo y	
			if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
				#check if below the ground, i.e jumping
				if self.vel_y < 0:
					self.vel_y = 0
					dy = tile[1].bottom - self.rect.top
				#check if above the ground, i.e falling
				elif self.vel_y >= 0:
					self.vel_y = 0
					self.in_air = False
					dy = tile[1].top - self.rect.bottom


		#Cập nhật vị trí khung
		self.rect.x += dx
		self.rect.y += dy

	def shoot(self):
		if self.shoot_cooldown == 0: #and self.ammo > 0:
			self.shoot_cooldown = 20
			player.update_action(4)

			#dat toa do cho hop voi duong dan ban nhan vat
			bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), (10 + self.rect.centery), self.direction)
			bullet_group.add(bullet)
			#reduce ammo
			# self.ammo -= 1
			# if self.ammo == 0:
			# 	print("Out of bullets")

	def ai(self):
		if self.alive and player.alive:
			if self.idling == False and random.randint(1, 200) == 1:
				self.update_action(0)
				self.idling = True
				self.idling_counter = 50
			#kiem tra khi enemy gan nguoi choi
			if self.vision.colliderect(player.rect):
				#dung chay va doi mat nguoi choi
				self.update_action(0)
				#shoot
				self.shoot()
				self.update_action(4)
			else:
				if self.idling == False:
					if self.direction == 1:
						ai_move_right = True 
					else:
						ai_move_right = False
					ai_move_left = not ai_move_right
					self.move(ai_move_left, ai_move_right)
					self.update_action(1)
					self.move_counter += 1
					#cap nhat tam nhin
					self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
					pygame.draw.rect(screen, RED, self.vision) 
	
		
					if self.move_counter > TILE_SIZE: #dao huong
						self.direction *= -1 
						self.move_counter *= -1 
	
				else:
					self.idling_counter -= 1
					if self.idling_counter <= 0:
						self.idling = False




	def update_animation(self):
		#update animation
		ANIMATION_COOLDOWN = 100
		#Cập nhật hình ảnh dựa trên số frame
		self.image = self.animation_list[self.action][self.frame_index]
		#Nếu thời gian các lần cập nhật quá thời gian chạy frame thì cập nhật lại <update_time>
		if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#Nếu lặp đến ảnh cuối thì lặp lại từ đầu
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) -1
			else:
				self.frame_index = 0



	def update_action(self, new_action):
		#Kiểm tra hành động có khác hành động trước hay không
		if new_action != self.action:
			self.action = new_action
			#Cập nhật cài đặt animation
			self.frame_index = 0
			self.update_time = pygame.time.get_ticks()



	def draw(self):
		screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

	def check_alive(self):
		if self.health <= 0:
			self.health = 0
			self.speed = 0
			self.alive = False
			self.update_action(3)

class World():
	def __init__(self):
		self.obstacle_list = []

	def process_data(self, data):
		#iterate through each value in level data file
		for y, row in enumerate(data):
			for x, tile in enumerate(row):
				if tile >= 0:
					img = img_list[tile]
					img_rect = img.get_rect()
					img_rect.x = x * TILE_SIZE
					img_rect.y = y * TILE_SIZE
					tile_data = (img, img_rect)
					if tile >= 52 and tile <= 90:
						self.obstacle_list.append(tile_data)

					elif tile >= 0 and tile <= 22: #trap
						water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
						water_group.add(water)

					elif tile >= 25 and tile <= 51:
						decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
						decoration_group.add(decoration)

					elif tile == 23: #create player
						player = Characters('player', x * TILE_SIZE, y * TILE_SIZE, 3, 5, 20)
						#create health bar <if want>

					elif tile == 24: #create enemy
						enemy = Characters('enemy', x * TILE_SIZE, y * TILE_SIZE, 3, 2, 20)
						enemy_group.add(enemy)
		return player

	def draw(self): 
		for tile in self.obstacle_list:
			screen.blit(tile[0], tile[1])


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
		self.rect.x += (self.direction * self.speed)
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
				print('player: '+ str(player.health))
				self.kill()
		if pygame.sprite.spritecollide(enemy, bullet_group, False):
			if enemy.alive:
				enemy.health -= 25
				print('enemy: ' + str(enemy.health))
				self.kill()

class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_TYPES - self.image.get_height()))

class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_TYPES - self.image.get_height()))

#create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()



#create empty tile list 
world_data = []
for row in range(ROWS):
	r = [-1] * COLS
	world_data.append(r)

#load in level data and create world
with open(f'level{level}_data.csv', newline = '') as csvfile:
	reader = csv.reader(csvfile, delimiter= ',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World()
player = world.process_data(world_data)

#loop game
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

	#Cập nhật hành động của nhân vật
	if player.alive:
		#shoot bullets 
		if shoot:
			player.shoot()
		if player.in_air:
			player.update_action(2)#2: jump+
		elif moving_left or moving_right:
			player.update_action(1)#1: run
		else:
			player.update_action(0)#0: idle
		player.move(moving_left, moving_right)


	for event in pygame.event.get():
		#Tắt game
		if event.type == pygame.QUIT:
			run = False
		#Nút bấm
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				moving_left = True
			if event.key == pygame.K_RIGHT:
				moving_right = True
			if event.key == pygame.K_UP and player.alive:
				player.jump = True
			if event.key == pygame.K_SPACE:
				shoot = True
			if event.key == pygame.K_ESCAPE:
				run = False


		#Nút thả
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				moving_left = False
			if event.key == pygame.K_RIGHT:
				moving_right = False
			if event.key == pygame.K_SPACE:
				shoot = False




	pygame.display.update()

pygame.quit()