# 使用IDAPython模拟逆向程序执行过程，计算出Flag

def _next_inst(addr,step=1):
	for i in range(step):
		addr = NextHead(addr)
	return addr 

def _next_inst_opnd(addr,  pos, opnd):
	inst = NextHead(addr)
	while True:
		if GetOpnd(inst, pos) == opnd:
			return inst
		else:
			inst = NextHead(inst)
			

def handle_map(inst):
	global buf
	inst = _next_inst(inst,12)
	print hex(inst), GetDisasm(inst)
	chrs_addr = GetOperandValue(inst, 1) 
	#map
	chrs = GetManyBytes(chrs_addr, 0x100)
	#print hex(chrs_addr), chrs[:20].encode('hex')
	tmp = ''
	for i in buf:
		tmp += chr(chrs.index(i))
	buf = tmp

	return inst

def handle_xor(inst):
	global buf
	inst = _next_inst(inst,12)	
	print hex(inst), GetDisasm(inst)
	chrs_addr = GetOperandValue(inst, 1) 
	chrs = GetManyBytes(chrs_addr, 40)
	# Xor
	tmp = ''
	for i in xrange(0,40):
		tmp += chr(ord(buf[i]) ^ ord(chrs[i]))
	buf = tmp

	return inst

def handle_shift(inst):

	'''
	  for ( i = 0; ; ++i )
	  {
		result = i;
		if ( i >= a2 )
		  break;
		*(_BYTE *)(a1 + i) = 2 * *(_BYTE *)(i + a1) | (*(_BYTE *)(i + a1) >> 7);
	  }

	  we do reverse.
	'''
	global buf
	inst = _next_inst(inst,20)	
	print hex(inst), GetDisasm(inst)
	mov_off = GetOperandValue(inst, 1)
	#print mov_off
	tmp = ''
	for i in buf:
		tmp += chr(((ord(i) << mov_off ) | (ord(i) >> ( 8 - mov_off))) & 0xFF)
	buf = tmp

	return inst


'''
.text:080ACDA2                 mov     dword ptr [esp+14h], 0A25FEC83h
.text:080ACDAA                 mov     dword ptr [esp+18h], 0FBA3CE93h
.text:080ACDB2                 mov     dword ptr [esp+1Ch], 0FF06175Ah
.text:080ACDBA                 mov     dword ptr [esp+20h], 0C4D72D13h
.text:080ACDC2                 mov     dword ptr [esp+24h], 6A8DCEBEh
.text:080ACDCA                 mov     dword ptr [esp+28h], 0FC2615B8h
.text:080ACDD2                 mov     dword ptr [esp+2Ch], 44940184h
.text:080ACDDA                 mov     dword ptr [esp+30h], 1C23D7F8h
.text:080ACDE2                 mov     dword ptr [esp+34h], 431C24Bh
.text:080ACDEA                 mov     dword ptr [esp+38h], 570833A6h
'''
cmp_str = [0x0A25FEC83,0x0FBA3CE93,0xFF06175A,0x0C4D72D13,0x6A8DCEBE,0x0FC2615B8,0x44940184,0x1C23D7F8,0x431C24B,0x570833A6]
import struct 
cmp_str = ''.join( struct.pack('I', i) for i in cmp_str)

start_func = 0x0804851D
end_func = 0x080ACD80

buf = 'A'*40

def normal():
	inst = start_func
	while inst < end_func:
		inst = handle_map(inst)
		inst = NextFunction(inst)
		inst = handle_xor(inst)
		inst = NextFunction(inst)
		inst = handle_shift(inst)
		inst = NextFunction(inst)


inst = end_func # last last func

buf = cmp_str
while  inst >= start_func:	
	inst = PrevFunction(inst)
	inst = handle_shift(inst)
	print buf

	inst = PrevFunction(inst)
	inst = handle_xor(inst)
	print buf

	inst = PrevFunction(inst)
	inst = handle_map(inst)	
	print buf