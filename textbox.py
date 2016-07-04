#from __future__ import print_function
#import textwrap

class Textbox(object):
	def __init__(self, rows, columns):
		self.chars = [['' for x in range(columns)] for y in range(rows)] 
		self.rows = rows
		self.cols = columns
		self.text = ''
		self.pos = (0,0)

	def linelen(self, y):
		x = 0
		for c in self.chars[y]:
			if c == '\n' or c == '':
				break
			x += 1
		return x
			
	
	def setCursor(self, x, y):
		y = self.rows - 1 if y >= self.rows else y
		len = self.linelen(y)
		x = len if x > len else x
		self.pos = (x,y)
	
	def getText(self, a, b):
		minp = a if ((a[1] < b[1] or (a[1] == b[1] and a[0] < b[0]))) else b
		maxp = a if (minp == b) else b
		p = self.pos
		self.setCursor(minp[0],minp[1])
		i = self.pos
		self.setCursor(maxp[0],maxp[1])
		j = self.pos + 1 if self.pos < len(self.text) else self.pos
		#print('minp:',minp,'maxp:',maxp,'i:',i,'j:',j)
		t = self.text[i:j]
		self.pos = p
		return t
	
	def addText(self, t):		
		self.text = self.text[:self.pos] + t + self.text[self.pos:]
		self.pos += len(t)
		
	def deleteText(self, c):
		#print('before del:',self.text)
		c = min(c, self.pos)
		a = max(c,min(len(self.text)-1,self.pos))
		self.text = self.text[:self.pos-c] + self.text[self.pos:]
		self.pos -= c
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
		r[-1] = r[-1] + ' '
		return r
				
	
	def cursor(self):
		x = 0
		y = 0
		#print('cursor:',self.pos,len(self.text))
		pos = min(self.pos,len(self.text))
		for i in range(pos):
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
	
	tb5 = Textbox(10,10)
	tb5.addText('MOV R0 R1\n')
	tb5.addText('SUB R2 R3\n')
	t1 = tb5.getText((0,0),(2,0))
	tb5.addText('ADD R4 R5\n')
	tb5.printlines()
	print('copied text:',t1)

if __name__ == '__main__':
	unittest()