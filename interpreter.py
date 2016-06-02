import parser
import cpu
from parser import Statement

def step(s, cpu):
	if s.opcode == 'MOV':
		dst = cpu.memory(s.op1)
		if s.op2.isdigit() and dst:
			return dst.store(int(s.op2))
		elif dst:
			return cpu.move(src, dst)
		else:
			return cpu.DATA_ABORT
	elif s.opcode == 'ADD':
		
			