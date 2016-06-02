import re
from recordtype import recordtype

Statement = recordtype('Statement', 'label opcode op1 op2 error', default=None)
statement_err = 'invalid statement: '
op_err = 'invalid operand: '
op_miss_err = 'missing operand!'
opcode_err = 'invalid opcode: '
unk_err = 'unspecified error'

# s = statement record
# op = operand text
# ilist = instruction dict
# i = operand num
def handleoperand(s,op,ilist,i):
	m = ilist[s.opcode]
	if m[i] == None and op == None:
		return
	elif m[i] == None and op:
		s.error = op_err + op
	elif m[i] and not op:
		s.error = op_miss_err
	else:
		if m[i].match(op):
			s.op1 = op
		else:
			s.error = op_err + op


def printstatement(s):
	if not s.error:
		if s.label:
			print s.label
		elif s.opcode:
			print s.opcode, s.op1, s.op2
		else:
			print 'comment'
	else:
		print s.error
		

def parse(t):
	print 'parse:',t
	
	
	m = re.compile('\s*((?!R[0-9]{1,3}:)[A-Z0-9]{1,8}:)?(([A-Z]{3})(\s+[A-Z0-9]+)?(\s+[A-Z0-9]+)?)?\s*$')
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
	s = Statement()
	r = m.match(t)
	if r:
		if r.group(1):
			s.label = r.group(1)
		if r.group(2):		
			if r.group(3):
				if r.group(3) in ilist:
					s.opcode = r.group(3)
					handleoperand(s,r.group(4),ilist,0)
					handleoperand(s,r.group(5),ilist,1)
				else:
					s.error = opcode_err + r.group(3)
			else:
				s_error = opcode_err + t
		if not s.label and not s.opcode:
			s.error = statement_err + t
	else:
		r2 = mc.match(t)
		if not r2:
			s.error =  statement_err + t
	printstatement(s)
			
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
		'SOV R0 R1',
		'  # foo',
		'#'
	]
	for t in tst:
		parse(t)

#unittest()