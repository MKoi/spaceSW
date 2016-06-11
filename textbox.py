import textwrap

class Textbox:
	def __init__(self, rows, columns):
		self.rows = rows
		self.cols = columns
		self.lines = ['']
		self.pos = (0,0)
		#self.lineWrap = False
	
	def setCursor(self, x, y):
		y = max(0,min(len(self.lines)-1,y))
		x = max(0,min(len(self.lines[y]),x))
		self.pos = (x,y)
	
	def addText(self, text):
		x,y = self.pos
		l1 = text.splitlines()
		l = []
		for s in l1:
			l2 = textwrap.wrap(s,self.cols)
			for ss in l2:
				l.append(ss)
		y2 = y + len(l) - 1
		x2 = len(l[-1]) if len(l) > 1 else x + len(l[0])
		s1 = self.lines[y][:x] + l[0] + self.lines[y][x:]
		l2 = textwrap.wrap(s1,self.cols)
		y2 = y2 + len(l2) - 1
		x2 = len(l2[-1]) if len(l2) > 1 and len(l) == 1 else x2
		l[0] = l2[0]
		for i in range(1,len(l2)):
			l.insert(i,l2[i])
		if len(l) < self.rows:
			self.lines[y] = l[0]
			for i in range(1,len(l)):
				self.lines.insert(y+i,l[i])
			self.pos = (x2,y2)
					
	def printlines(self):
		print('lines:')
		for l in self.lines:
			print(l)
	
	def deleteText(self, pos, count):
		pass

def unittest():
	tb = Textbox(10,5)
	tb.printlines()
	tb.addText('foo')
	tb.printlines()
	tb.setCursor(1,0)
	tb.addText('bar')
	tb.printlines()
	tb.setCursor(10,10)
	tb.addText(' MOV')
	tb.printlines()
	tb.addText(' MOV\nHUUHAAA\n end')
	tb.printlines()

if __name__ == '__main__':
	unittest()