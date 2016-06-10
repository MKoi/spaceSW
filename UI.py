import pygame 
from pygame.locals import *


WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
targetfps = 60 
screen_width = 640 
screen_height = 480

def unittest(): 
	pygame.init() 
	screen = pygame.display.set_mode((screen_width, screen_height)) 
	pygame.display.set_caption('UItest') 
	pygame.mouse.set_visible(1) 
	background = pygame.Surface(screen.get_size()) 
	background = background.convert() 
	background.fill(BLACK) 
 
	clock = pygame.time.Clock()
	exitgame = False
	while not exitgame: 
		dt = clock.tick(targetfps) 
		for event in pygame.event.get(): 
			if event.type == QUIT: 
				exitgame = True 
				break 
			elif event.type == KEYDOWN and event.key == K_ESCAPE: 
				exitgame = True 
				break 
		screen.blit(background, (0, 0))
		pygame.display.flip()

		
if __name__ == '__main__':
	unittest()
