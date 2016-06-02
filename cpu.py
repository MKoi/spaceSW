
ports = []

UNDEFINED_INST = 0xF001
BLOCKED_IO = 0xF002
DATA_ABORT = 0xF003



class mem:
	def __init__(self,val=None, blk=False):
		self.val = val
		self.isblocking = blk
	
	def load(self):
		if self.isblocking:
			if self.val:
				return self.val
			else:
				return BLOCKED_IO
		else: 
			return self.val
	
	def store(self, val):
		if self.isblocking and self.val:
			return BLOCKED_IO
		else:
			self.val = val
		return val
		

class cpu:
	def __init__(self, regc, ports):
		self.regs = [mem(0,False) for i in range(regc)]
		self.updateflags(0)
		self.ports = ports
		
	def resolveaddr(self, addr, indirect = False):
		r = None
		val = int(addr) if addr.isdigit() else int(addr[1:-1])
		if addr.isdigit() and 0 <= val < len(self.ports):
			r = self.ports[val]
		elif val < len(self.regs)
			if indirect:
				val2 = self.regs[val].load()
				if 0 <= val2 < len(self.ports):
					r = self.ports[val2]
			else:
				r = self.regs[val]
		return r
		
	def updateflags(self, val):
		self.Z = (val == 0)
		self.GZ = (val > 0)
		selg.LZ = (val < 0)
		
	def move(self, dst, src):
		dstmem = self.resolveaddr(dst)
		if dstmem:
			if src.isdigit():
				dstmem.store(int(src))
				self.updateflags(int(src))
				return int(src)
			else:
				srcmem = self.resolveaddr(src)
				if srcmem:
					val = srcmem.load()
					self.updateflags(val)	
					return val
		return DATA_ABORT
	
	def load(self, dst, src):
		dstmem = self.resolveaddr(dst)
		srcmem = self.resolveaddr(src, True)
		if dstmem and srcmem:
			val = srcmem.load()
			if val == BLOCKED_IO:
				return BLOCKED_IO
			dstmem.store(val)
			srcmem.store(None)
			
	def store(self, dst, src):
		dstmem = self.resolveaddr(dst, True)
		srcmem = self.resolveaddr(src)
		
			