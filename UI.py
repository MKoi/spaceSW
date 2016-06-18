import pygame 
from pygame.locals import *
from textbox import Textbox

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
targetfps = 60 
screen_width = 640 
screen_height = 480

class TextboxUI(Textbox):
	# r = pygame rect
	# fs = fontsize
	def __init__(self, rows, columns, r, fs):
		super(TextboxUI, self).__init__(rows, columns)
		self.font = pygame.font.Font(None, fs)
		cs = self.font.size('x')
		w = cs[0]*(columns+2)
		h = cs[1]*(rows+2) + self.font.get_linesize()*(rows-1) 
		self.textgfx = pygame.Surface((w,h))

	def renderText(self):
		self.textgfx.fill(BLACK)
		y = 0
		for l in self.lines():
			gfx = self.font.render(l, 0, WHITE)
			self.textgfx.blit(gfx,(0,y))
			y += self.font.size(l)[1] #+ self.font.get_linesize()
		
	def addText(self,t):
		super(TextboxUI, self).addText(t)
		self.renderText()


def unittest(): 
	pygame.init() 
	screen = pygame.display.set_mode((screen_width, screen_height)) 
	pygame.display.set_caption('UItest') 
	pygame.mouse.set_visible(1) 
	background = pygame.Surface(screen.get_size()) 
	background = background.convert() 
	background.fill(BLACK) 
 
	tb = TextboxUI(10,10,(0,0),12)
	tb.addText('MOV\nLDR R0 R1\nADD R0 R1\n')
 
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
		screen.blit(tb.textgfx,(0,0))
		pygame.display.flip()

		
if __name__ == '__main__':
	unittest()
