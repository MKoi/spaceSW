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
		self.charsize = self.font.size('X')
		w = self.charsize[0]*(columns+2)
		h = self.charsize[1]*(rows+2) + self.font.get_linesize()*(rows-1) 
		self.textgfx = pygame.Surface((w,h))
		self.cursorgfx = pygame.Surface(self.charsize)
		pygame.draw.rect(self.cursorgfx, WHITE, pygame.Rect(0, 0, self.charsize[0], self.charsize[1]), 0)
		self.cpos = (0,0) 	

	def getKeyPress(self):
		for event in pygame.event.get():
			if event.type == KEYDOWN:    
				return event.key
			else:
				return False
	
	def getInput(self):  
		keyPress = 0
		for event in pygame.event.get(KEYDOWN):
			keyPress = event.key

		if keyPress == K_RETURN:
			self.addText('\n')
		elif keyPress == K_SPACE:
			self.addText(' ')
		elif keyPress >= 32 and keyPress <= 126:
			#capitalise it 
			keyPress -= 32
			c = chr(keyPress)
			self.addText(c)

	
	def renderText(self):
		self.textgfx.fill(BLACK)
		y = 0
		for l in self.lines():
			gfx = self.font.render(l, 0, WHITE)
			self.textgfx.blit(gfx,(0,y))
			y += self.charsize[1] #+ self.font.get_linesize()
		
	
	def updateCursor(self):
		cpos = self.cursor()
		cursorY = self.charsize[1] * cpos[1]
		cursorX = self.font.size(self.lines()[cpos[1]][:cpos[0]])[0]
		self.cpos = (cursorX,cursorY)
	
	def render(self, s):
		s.blit(self.textgfx,(0,0))
		s.blit(self.cursorgfx, self.cpos)
	
	def addText(self,t):
		super(TextboxUI, self).addText(t)
		self.renderText()
		self.updateCursor()


def unittest(): 
	pygame.init() 
	screen = pygame.display.set_mode((screen_width, screen_height)) 
	pygame.display.set_caption('UItest') 
	pygame.mouse.set_visible(1) 
	background = pygame.Surface(screen.get_size()) 
	background = background.convert() 
	background.fill(BLACK) 
 
	tb = TextboxUI(10,10,(0,0),12)
	tb.addText('MOV\nLDR R0 R1\nADD R0 R1\nSUB')
 
	clock = pygame.time.Clock()
	exitgame = False
	while not exitgame: 
		dt = clock.tick(targetfps) 
		elist = pygame.event.get()
		for event in elist: 
			if event.type == QUIT: 
				exitgame = True 
				break 
			elif event.type == KEYDOWN and event.key == K_ESCAPE: 
				exitgame = True 
				break
			else:
				pygame.event.post(event)
		screen.blit(background, (0, 0))
		tb.getInput()
		pygame.event.clear()
		tb.render(screen)
		pygame.display.flip()

		
if __name__ == '__main__':
	unittest()
