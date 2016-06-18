#from __future__ import print_function
#import textwrap

class Textbox(object):
	def __init__(self, rows, columns):
		self.rows = rows
		self.cols = columns
		self.text = ''
		self.pos = 0
		#self.wrapper = textwrap.TextWrapper(replace_whitespace=False,drop_whitespace=False,width=columns)
		#self.lineWrap = False
	
	def setCursor(self, x, y):
		#print('set cursor to ',(x,y))
		x = min(self.cols-1,x)
		xx = 0
		yy = 0
		for i in range(len(self.text)):
			if yy == y and xx == x:
				break
			if xx >= self.cols - 1 or self.text[i] == '\n':
				yy += 1
				xx = 0 
			else:
				xx += 1
		#print('cursor set to ',i,(xx,yy))
		self.pos = i
	
	def addText(self, t):		
		self.text = self.text[:self.pos] + t + self.text[self.pos:]
		self.pos += len(t)
		
	def deleteText(self, c):
		#print('before del:',self.text)
		a = max(c,min(len(self.text)-1,self.pos))
		self.text = self.text[:a-c] + self.text[a:]
		self.pos = a-c
		#print('after del:',self.text)
	
	def lines(self):
		r = ['']
		x = 0
		for i in range(len(self.text)):
			if x >= self.cols:
				r.append('')
				x = 0
			c = self.text[i]
			if c == '\n':
				#print('line:',r[-1])
				r[-1] = r[-1] + ' '
				r.append('')
				x = 0
			else:
				r[-1] = r[-1] + c
				x += 1
		return r
				
	
	def cursor(self):
		x = 0
		y = 0
		for i in range(self.pos):
			if x >= self.cols:
				y += 1
				x = 0
			if self.text[i] == '\n':
				y += 1
				x = 0
			else:
				x += 1
		return (x,y)
					
	def printlines(self):
		print('text:',self.text)
		print('lines:')
		for l in self.lines():
			print(l)
		print('cursor:',self.cursor())
	
				
		

def unittest():
	tb = Textbox(10,5)
	tb.printlines()
	tb.addText('foo')
	tb.printlines()
	tb.setCursor(1,0)
	tb.addText('bar')
	tb.printlines()
	tb.addText(' fii')
	tb.printlines()
	tb.setCursor(10,10)
	tb.addText(' MOV')
	tb.printlines()
	tb.addText(' MOV\nHUUHAAA\n end')
	tb.printlines()
	
	tb2 = Textbox(10,1)
	tb2.addText('foo\n')
	tb2.printlines()
	tb2.addText('bar\n')
	tb2.printlines()
	tb2.setCursor(2,0)
	tb2.addText('i\n')
	tb2.printlines()
	
	tb3 = Textbox(10,3)
	tb3.addText('foo\n')
	tb3.addText('foo\n')
	tb3.printlines()
	
	tb4 = Textbox(10,3)
	tb4.addText('foo\n')
	tb4.printlines()
	tb4.deleteText(4)
	tb4.printlines()
	tb4.addText('foo\n')
	tb4.addText('bar\n')
	tb4.setCursor(0,1)
	tb4.printlines()
	tb4.deleteText(3)
	tb4.printlines()

if __name__ == '__main__':
	unittest()