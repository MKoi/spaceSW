from __future__ import print_function

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
		

class Cpu:

	def __init__(self, labels, code, regc, ports):
		self.labels = labels
		self.code = code
		self.regs = [mem(0,False) for i in range(regc)]
		self.updateflags(0)
		self.ports = ports
		self.PC = 0
		self.jumped = False
		self.resetdelay = 0
		self.status = 'RUN'

	def reset(self, code, labels, delay):
		self.resetdelay = delay
		self.code = code
		self.labels = labels
		self.PC = 0
		self.jumped = False
		for r in self.regs:
			r.store(0)
		
		
	def resolveaddr(self, addr, indirect = False):
		r = None
		try:
			val = int(addr) if addr.isdigit() else int(addr[1:])
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
		self.LZ = (val < 0)
		
	def move(self, dst, src):
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()
		self.updateflags(val)
		self.resolveaddr(dst).store(val)
	
	def load(self, dst, src):
		srcmem = self.resolveaddr(src, True)		
		val = srcmem.load()
		self.status = 'LOAD'
		self.resolveaddr(dst).store(val)
		srcmem.val = None
		self.updateflags(val)
			
	def store(self, dst, src):
		val = int(src) if src.isdigit() else self.resolveaddr(src).load()
		self.resolveaddr(dst, True).store(val)
		self.status = 'STORE'
		
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
			
	def jump(self, dst):
		if dst[0] == 'R' and len(dst) > 1 and dst[1:].isdigit():
			self.PC += self.resolveaddr(dst).load()
			self.jumped = True
		elif dst[0] == '-' and dst[1:].isdigit():
			self.PC -= int(dst[1:])
			self.jumped = True
		elif dst.isdigit():
			self.PC += int(dst)
			self.jumped = True
		elif self.labels and dst in self.labels:
			self.PC = self.labels[dst]
			self.jumped = True
		else:
			raise CpuException(DATA_ABORT)
			
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
			self.jump(dst)
	
	def nop(self):
		pass
	
	def step(self):
		if self.resetdelay:
			self.resetdelay -= 1
			if not self.resetdelay:
				self.status = 'RESET'
			return
		try:
			inst = self.code[self.PC]
			opcode = inst[0]
			if opcode == 'LDR': self.load(inst[1],inst[2])
			elif opcode == 'STR': self.store(inst[1],inst[2])
			elif opcode == 'MOV': self.move(inst[1],inst[2])
			elif opcode == 'ADD': self.addop(inst[1],inst[2]) 
			elif opcode == 'SUB': self.subop(inst[1],inst[2])
			elif opcode == 'CMP': self.compare(inst[1],inst[2])
			elif opcode == 'JMP': self.jump(inst[1])
			elif opcode == 'JGZ': self.jumpGZ(inst[1])
			elif opcode == 'JLZ': self.jumpLZ(inst[1])
			elif opcode == 'JEQ': self.jumpEQ(inst[1])
			elif opcode == 'JNE': self.jumpNE(inst[1])
			elif opcode == 'NOP': self.nop()
			else: raise CpuException(UNDEFINED_INST)
			self.status = 'RUN'
			if not self.jumped:
				self.PC += 1
				if self.PC == len(self.code):
					self.PC = 0
			else:
				self.jumped = False
		except IndexError:
			print('PC invalid:',self.PC)
			self.status = 'EXCEPTION'
			self.reset(self.code, self.labels, 3)
		except CpuException as e:
			if e.value != BLOCKED_IO:
				self.status = 'EXCEPTION'
				self.reset(self.code, self.labels, 3)
			else:
				self.status = 'IDLE'

	def printstatus(self):
		print(self.code[self.PC])
		print('PC:',self.PC)
		for i in range(len(self.regs)-1):
			print('R',i,'=',self.regs[i].val,',',)
		i = len(self.regs)-1
		print('R',i,'=',self.regs[i].val)
		print(self.status)
					
def unittest():
	ports = [mem(None,True) for i in range(10)]
	code1 = [
		('LDR','R0','1'),
		('ADD','R0','1'),
		('MOV','R1','2'),
		('STR','R1','R0')
	]
	cpu1 = Cpu(None, code1, 2, ports)
	code2 = [
		('STR','1','1'),
		('LDR','R0','2'),
		('STR','1','R0'),
		('JMP','-2')
	]
	cpu2 = Cpu(None, code2, 2, ports)
	for i in range(10):
		cpu1.step()
		cpu2.step()
		print('CPU1:')
		cpu1.printstatus()
		print('CPU2:')
		cpu2.printstatus()
		print('P1:',ports[1].val)
		print('P2:',ports[2].val)
		
if __name__ == '__main__':
	unittest()