
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
		return val
		

class cpu:
	def __init__(self, regc, ports):
		self.regs = [mem(0,False) for i in range(regc)]
		self.updateflags(0)
		self.ports = ports
		
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
		return self.resolveaddr(dst).store(val)
	
	def load(self, dst, src):
		srcmem = self.resolveaddr(src, True)
		val = srcmem.load()
		self.resolveaddr(dst).store(val)
		srcmem.store(None)
		self.updateflags(val)
		return val
			
	def store(self, dst, src):
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()
		return self.resolveaddr(dst, True).store(val)
		
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
		return val2
	
		def addop(self, dst, src):
			return self.addorsub(dst, src, '+')
		
		def subop(self, dst, src):
			return self.addorsub(dst, src, '-')
			