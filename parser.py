from __future__ import print_function
import re
from recordtype import recordtype

Statement = recordtype('Statement', [('opcode', None), ('ops', [])])
Error = recordtype('Error', 'text span', default=None)
statement_err = 'invalid statement: '
op_err = 'invalid operand '
op_miss_err = 'missing operand '
opcode_err = 'invalid opcode: '
unk_err = 'unspecified error'

# s = statement record
# op = operand text
# ilist = instruction dict
# i = operand num
def handleoperand(s,op,ilist,i):
	#print('handle op:',op)
	m = ilist[s.opcode]
	e = Error()
	if m[i] == None and op == None:
		return
	elif m[i] == None and op:
		e.text = op_err + str(i+1) + ':' + op
	elif m[i] and not op:
		e.text = op_miss_err + str(i+1)
	else:
		opstr = op.lstrip()
		if m[i].match(opstr):
			s.ops.append(opstr)
			return
		else:
			e.text = op_err + op
	return e

def printstatement(s):
	print(s.opcode,)
	for op in s.ops:
		print(op)
		

def parse(t):	
	m = re.compile('\s*((?!R[0-9]{1,3}:)[A-Z0-9]{1,8}:)?(([A-Z]+)(\s+[A-Z0-9]+)?(\s+[A-Z0-9]+)?)?\s*$')
	mc = re.compile('\s*#(.*)')
	mem = re.compile('R[0-9]{1,3}')
	lbl = re.compile('(?!R[0-9]{1,3}:)[A-Z0-9]{1,8}')
	lit = re.compile('-?[0-9]{1,3}')
	mem_or_lit = re.compile('(R[0-9]{1,3})|(-?[0-9]{1,3})')
	lbl_mem_or_lit = re.compile('([A-Z0-9]{1,8})|(-?[0-9]{1,3})')
	ilist = {
		'LDR': (mem,mem_or_lit),
		'STR': (mem_or_lit,mem_or_lit),
		'MOV': (mem,mem_or_lit),
		'ADD': (mem,mem_or_lit), 
		'SUB': (mem,mem_or_lit),
		'CMP': (mem,mem_or_lit),
		'JMP': (lbl_mem_or_lit,None),
		'JGZ': (lbl_mem_or_lit,None),
		'JLZ': (lbl_mem_or_lit,None),
		'JEQ': (lbl_mem_or_lit,None),
		'JNE': (lbl_mem_or_lit,None),
		'NOP': (None,None)
	}
	s = None
	r = m.match(t)
	errs = []
	label = None
	if r:	
		if r.group(1):
			label = r.group(1)
		if r.group(2):
			s = Statement()
			s.ops = []
			if r.group(3):
				if r.group(3) in ilist:
					s.opcode = r.group(3)
					e = handleoperand(s,r.group(4),ilist,0)
					if e:
						e.span = r.span(4)
						errs.append(e)
					e = handleoperand(s,r.group(5),ilist,1)
					if e:
						e.span = r.span(5)
						errs.append(e)
				else:
					errs.append(Error(opcode_err + r.group(3),r.span(3)))
			else:
				errs.append(Error(opcode_err + t,r.span(2)))
		if not label and not s:
			errs.append(Error(statement_err + t,r.span(2)))
	else:
		r2 = mc.match(t)
		if not r2:
			errs.append(Error(statement_err + t))

	return label,s,errs
			
def unittest():
	tst = [
		'FOO:',
		'FOO:JFWOFJWOFJWOFJWOFJOWJFOWFJ',
		'M3:',
		'M3M3:',
		'FOO:MOV',
		'MOV R0',
		' MOVR',
		'MOV R0 R1 R2',
		'MOV R0 R1',
		'MOV R0 FOO',
		'SOV R0 R1',
		'  # foo',
		'#'
	]
	for t in tst:
		print('parse',t)
		label,s,errs = parse(t)
		if label:
			print(label)
		if errs:
			for e in errs:
				print(e,)
		elif s:
			printstatement(s)

if __name__ == '__main__':
	unittest()