import textwrap
import pygame 
from pygame.locals import *


WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
targetfps = 60 
screen_width = 640 
screen_height = 480

class Textbox:
	def __init__(self, rows, columns):
		self.rows = rows
		self.cols = columns
		self.lines = ['']
		self.pos = (0,0)
		self.lineWrap = False
	
	def addText(self, text):
		x,y = self.pos
		l = text.splitlines()
		y2 = y + len(l) - 1
		x2 = len(l[-1]) if len(l) > 1 else x + len(l[0])
		s1 = self.lines[y][:x] + l[0] + self.lines[y][x:]
		l2 = textwrap.wrap(s1,self.cols)
		y2 = y2 + len(l2) - 1
		x2 = len(l2[-1]) if len(l2) > 1 and len(l) == 1 else x2
		l[0] = l2[0]
		for i in range(1,len(l2))
			l.insert(i,l2[i])
		if len(l) < self.rows:
			self.lines[y] = l[0]
			for i in range(1,len(l)):
				self.lines.insert(y+i,l[i])
			self.pos = (x2,y2)
					
	
	def deleteText(self, pos, count):
		pass
		

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
