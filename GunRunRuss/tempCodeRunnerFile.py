#store tiles in a list
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'assets/Tilemap/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)

save_img = pygame.image.load('assets/Player/john_static.png').convert_alpha()
load_img = pygame.image.load('assets/Enemy/grunt.png').convert_alpha()
