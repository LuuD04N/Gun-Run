import pygame
import os
import random


pygame.init()


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gun&Run')
pygame.display.set_icon(pygame.image.load('assets\\icon.ico'))

clock = pygame.time.Clock()
FPS = 60

GRAVITY = 0.75
TILE_SIZE = 40

moving_left = False
moving_right = False
shoot = False

#Tải ảnh 
bullet_img_ori = pygame.image.load('assets\\Player\\Bullet\\0.png').convert_alpha()
bullet_img = pygame.transform.scale(bullet_img_ori, (bullet_img_ori.get_width() * 2, bullet_img_ori.get_height() * 2))

BG = (0, 0, 0)
RED = (255, 0, 0)

def draw_bg():
	screen.fill(BG)
	pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))



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

		#Kiểm tra va chạm với sàn <va chạm dọc>
		if self.rect.bottom + dy > 300:
			dy = 300 - self.rect.bottom
			self.in_air = False

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

#create sprite groups
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

player = Characters('player', 200, 200, 3, 5, 20)
enemy = Characters('enemy', 400, 200, 3, 2, 20)
# enemy1 = Characters('enemy', 500, 200, 3, 2, 20)
# enemy2 = Characters('enemy', 700, 200, 3, 2, 20)

enemy_group.add(enemy)
# enemy_group.add(enemy1)
# enemy_group.add(enemy2)



run = True
while run:

	clock.tick(FPS)

	draw_bg()

	player.update()
	player.draw()

	for enemy in enemy_group:
		enemy.ai()
		enemy.update()
		enemy.draw()

	#update and draw groups
	bullet_group.update()
	bullet_group.draw(screen)


	#Cập nhật hành động của nhân vật
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