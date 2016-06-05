
ports = []

UNDEFINED_INST = 0xF001
BLOCKED_IO = 0xF002
DATA_ABORT = 0xF003

class CpuException(Exception):
	def __init__(self,val):
		self.value = val
	def __str__(self):
		return 'CPU Exception:' + self.val
		

class mem:
	def __init__(self,val=None, blk=False):
		self.val = val
		self.isblocking = blk
	
	def load(self):
		if self.isblocking:
			if self.val:
				return self.val
			else:
				raise CpuException(BLOCKED_IO)
		else: 
			return self.val
	
	def store(self, val):
		if self.isblocking and self.val:
			raise CpuException(BLOCKED_IO)
		else:
			self.val = val
		

class cpu:
	def __init__(self, labels, code, regc, ports):
		self.labels = labels
		self.code = code
		self.regs = [mem(0,False) for i in range(regc)]
		self.updateflags(0)
		self.ports = ports
		self.PC = 0
		
	def resolveaddr(self, addr, indirect = False):
		r = None
		try:
			val = int(addr) if addr.isdigit() else int(addr[1:-1])
			if addr.isdigit():
				r = self.ports[val]
			elif indirect:
				val2 = self.regs[val].load()
				r = self.ports[val2]
			else:
				r = self.regs[val]
		except IndexError:
			raise CpuException(DATA_ABORT)		
		return r
	
	def updateflags(self, val):
		self.Z = (val == 0)
		self.GZ = (val > 0)
		selg.LZ = (val < 0)
		
	def move(self, dst, src):
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()
		self.updateflags(val)
		self.resolveaddr(dst).store(val)
	
	def load(self, dst, src):
		srcmem = self.resolveaddr(src, True)
		val = srcmem.load()
		self.resolveaddr(dst).store(val)
		srcmem.store(None)
		self.updateflags(val)
			
	def store(self, dst, src):
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()
		self.resolveaddr(dst, True).store(val)
		
	def addorsub(self, dst, src, op):
		dstmem = self.resolveaddr(dst)
		val2 = dstmem.load()
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()			
		if op == '-':
			val2 -= val
		elif op == '+':
			val2 += val
		else:
			raise CpuException(UNDEFINED_INST)
		dstmem.store(val2)
		self.updateflags(val2)
	
		def addop(self, dst, src):
			self.addorsub(dst, src, '+')
		
		def subop(self, dst, src):
			self.addorsub(dst, src, '-')
		
		def compare(self, dst, src):
			dstmem = self.resolveaddr(dst)
			val2 = dstmem.load()
			val = int(src) if src.isdigit() else self.resolveaddr(src).load()
			val2 -= val
			self.updateflags(val2)
			
		def jump(self, dst)
			if dst[0] == 'R' and len(dst) > 1 and dst[1:-1].isdigit():
				self.PC += self.resolveaddr(dst).load()
			elif dst in self.labels:
				self.PC = self.labels[dst]
				
		def jumpGZ(self, dst):
			if self.GZ:
				self.jump(dst)
				
		def jumpLZ(self, dst):
			if self.LZ:
				self.jump(dst)
				
		def jumpEQ(self, dst):
			if self.EQ:
				self.jump(dst)
				
		def jumpNE(self, dst):
			if not self.EQ:
				self.jump(dst):
				