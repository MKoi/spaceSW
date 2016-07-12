#from __future__ import print_function
#import textwrap
def biggerThan(a,b):
	return a[1] > b[1] or (a[1] == b[1] and a[0] > b[0]) 

class Textbox(object):
	def __init__(self, rows, columns):
		self.chars = [['' for x in range(columns)] for y in range(rows)]
		self.bak = [['' for x in range(columns)] for y in range(rows)]
		self.rows = rows
		self.cols = columns
		#self.text = ''
		self.pos = (0,0)
		self.lastchar = None
		self.debug = False
	
	def dprint(self,*args):
		if self.debug:
			print(args)
	
	def endofline(self, x, y):
		if x >= self.cols:
			return True
		return self.chars[y][x] == '\n' or self.chars[y][x] == ''
	
	def save(self):
		for i in range(self.cols):
			for j in range(self.rows):
				self.bak[j][i] = self.chars[j][i]
	
	def restore(self):
		for i in range(self.cols):
			for j in range(self.rows):
				self.chars[j][i] = self.bak[j][i]
				
	def linelen(self, y):
		x = 0
		while not self.endofline(x,y):
			x += 1
		return x
	
	def maxIndex(self, y):
		return min(self.linelen(y),self.cols-1)
		
	
	def prevPos(self, p):
		x,y = p
		if x == 0:
			if y == 0:
				return None
			else:
				y -= 1
				x = self.maxIndex(y)
		else:
			x -= 1
		return (x,y)
	
	def nextPos(self, p):
		if not p:
			return (0,0)
		x,y = p
		if self.chars[y][x] == '\n':
			return (0,y+1)
		x = (x+1) % self.cols
		if x == 0:
			return (x,y+1)
		return (x,y)
	
	def limits(self, x, y):
		if biggerThan((x,y),self.lastchar):
			return self.lastchar
		x = min(x,self.maxIndex(y))
		return (x,y)
	
	def setCursor(self, x, y):
		if not self.lastchar:
			self.pos = (0,0)
			return self.pos
		if y > self.lastchar[1]:
			self.pos = self.nextPos(self.lastchar)
			return self.pos
		maxi = self.maxIndex(y)
		if x > maxi:
			if y == self.lastchar[1]:
				x,y = self.nextPos(self.lastchar)
			else:
				x = maxi
		self.pos = (x,y)
		return self.pos
	
	def getText(self, a, b):
		self.dprint('getText',a,b)
		minp = a if ((a[1] < b[1] or (a[1] == b[1] and a[0] < b[0]))) else b
		maxp = a if (minp == b) else b
		#print('maxp,minp:',maxp,minp)
		savp = self.pos
		minp = self.limits(minp[0],minp[1])
		#print('maxp,minp:',maxp,minp)
		maxp = self.limits(maxp[0],maxp[1])
		t = ''
		p = minp
		#print('maxp,minp:',maxp,minp)
		while p != maxp:
			#print('t:',t,'p:',p)
			t += self.chars[p[1]][p[0]]
			p = self.nextPos(p)
		t += self.chars[p[1]][p[0]]
		self.pos = savp
		self.dprint('getText return:',t)
		return t
	
	def appendText(self, t, updatePos=True):
		self.dprint('appendText:',t,self.pos)
		if not t:
			return
		p = self.pos
		for c in t:
			prevp = p
			self.chars[p[1]][p[0]] = c
			p = self.nextPos(p)
		self.lastchar = prevp
		if updatePos:
			self.pos = p
	
	def getEnd(self):
		if self.nextPos(self.lastchar) == self.pos:
			return ''
		return self.getText(self.pos,self.lastchar)
	
	def insertText(self, t):
		self.dprint('insertText:',t,self.pos)
		if not t:
			return
		tmpt = self.getEnd()
		p = self.pos
		for c in t:
			prevp = p
			self.chars[p[1]][p[0]] = c
			p = self.nextPos(p)
		self.lastchar = prevp
		self.pos = p
		self.appendText(tmpt, False)	
	
	def addText(self, t):
		self.save()
		try:
			if self.nextPos(self.lastchar) == self.pos:
				self.appendText(t)
			else:
				self.insertText(t)
			return True
		except IndexError:
			self.restore()
			return False
		
	def deleteText(self, c):
		self.dprint('deleteText:',c,self.pos)
		if not c:
			return
		tmpt = self.getEnd()
		while self.pos and c:
			self.pos = self.prevPos(self.pos)
			c -= 1
		if not self.pos:
			self.pos = (0,0)
			self.lastchar = None
		else:
			self.lastchar = self.prevPos(self.pos)
		self.appendText(tmpt, False)
	
	def lines(self):
		r = []
		p = (0,0)
		last = self.nextPos(self.lastchar)
		while p != last:
			c = self.chars[p[1]][p[0]]
			if p[0] == 0:
				r.append('')
			if c == '\n':
				c = ' '
			r[-1] = r[-1] + c
			p = self.nextPos(p)
		if p[0] == 0:
			r.append('')
		r[-1] = r[-1] + ' '
		return r
				
	
	def cursor(self):
		return self.pos
					
	def printlines(self):
		print('PRINT LINES START')
		print('chars:',self.chars)
		print('lines:')
		for l in self.lines():
			print(l)
		print('cursor:',self.cursor())
		print('last char:',self.lastchar)
		print('PRINT LINES END')
	
				
		

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
	tb4.debug = True
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
	tb4.addText('foo')
	tb4.printlines()
	tb4.deleteText(1)
	tb4.printlines()
	tb4.deleteText(1)
	tb4.printlines()
	tb4.deleteText(1)
	tb4.printlines()
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