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
		self.borderw = 1
		self.font = pygame.font.Font(None, fs)
		self.charsize = self.font.size('X')
		self.w = self.charsize[0]*(columns+2) + 2*self.borderw
		self.h = self.charsize[1]*(rows+2) + self.font.get_linesize()*(rows-1) +  2*self.borderw
		self.textgfx = pygame.Surface((self.w,self.h))
		self.cursorgfx = pygame.Surface(self.charsize)
		pygame.draw.rect(self.cursorgfx, WHITE, pygame.Rect(0, 0, self.charsize[0], self.charsize[1]), 0)
		self.cpos = (0,0)
		self.mousebdown = None
		self.clipBoard = None

	def getKeyPress(self):
		for event in pygame.event.get():
			if event.type == KEYDOWN:    
				return event.key
			else:
				return False
	
	def getPointerInput(self):
		for e in pygame.event.get((MOUSEBUTTONDOWN,MOUSEBUTTONUP,MOUSEMOTION)):
			if e.type == MOUSEBUTTONDOWN:
				self.mousebdown = e
			elif e.type == MOUSEBUTTONUP and self.mousebdown:
				p1 = self.pos2cursorPos(self.mousebdown.pos[0],self.mousebdown.pos[1])
				p2 = self.pos2cursorPos(e.pos[0],e.pos[1])
				if p1 == p2:
					self.setCursor(p2[0],p2[1])
					self.updateCursor(p2)
				else:
					#print('copy:',p1,p2)
					self.clipBoard = super(TextboxUI, self).getText(p1,p2)
					#print('copied:',self.clipBoard,self.pos)
	
	def getInput(self):  
		keyPress = 0
		for event in pygame.event.get(KEYDOWN):
			keyPress = event.key

		if keyPress == K_RETURN:
			self.addText('\n')
		elif keyPress == K_SPACE:
			self.addText(' ')
		elif keyPress == K_BACKSPACE:
			self.deleteText(1)
			self.renderText()
			self.updateCursor()
		elif keyPress >= 32 and keyPress <= 126:
			#capitalise it
			if 96 < keyPress < 123:
				keyPress -= 32
			c = chr(keyPress)
			self.addText(c)

	
	def renderText(self):
		self.textgfx.fill(BLACK)
		pygame.draw.rect(self.textgfx, WHITE, Rect(0,0,self.w, self.h), self.borderw)
		y = self.borderw
		for l in self.lines():
			gfx = self.font.render(l, 0, WHITE)
			self.textgfx.blit(gfx,(self.borderw,y))
			y += self.charsize[1] #+ self.font.get_linesize()
	
	def setCursorScreen(self,x,y):
		cpos = self.pos2cursorPos(x,y)
		self.setCursor(cpos[0],cpos[1])
		self.updateCursor(cpos)
	
	def pos2cursorPos(self,x,y):
		ly = 0
		while y-self.charsize[1] > 0:
			ly += 1
			y -= self.charsize[1]
		ll = self.lines()
		ly = min(len(ll)-1,ly)
		l = ll[ly]
		m = self.font.metrics(l)
		xx = 0
		i = 0
		for i in range(len(m)):
			xx += m[i][4]
			if xx >= x:
				break
		return (i,ly)
	
	def updateCursor(self, pos=None):
		cpos = pos if pos else self.cursor()
		cx,cy = cpos
		print('cpos:',cpos)
		print(self.lines())
		cursorY = self.charsize[1] * cy
		ll = self.lines()
		cursorX = self.font.size(ll[cy][:cx])[0] if cy < len(ll) else 0
		self.cpos = (cursorX,cursorY)
	
	def render(self, s):
		s.blit(self.textgfx,(0,0))
		cpos = (self.cpos[0] + self.borderw, self.cpos[1] + self.borderw)
		s.blit(self.cursorgfx, cpos)
	
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
	tb.addText('MOV\nLDR R0 R1\nADD R2 R3\nSUB')
 
	pygame.key.set_repeat(500,250)
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
		tb.getPointerInput()
		tb.getInput()
		pygame.event.clear()
		tb.render(screen)
		pygame.display.flip()

		
if __name__ == '__main__':
	unittest()
