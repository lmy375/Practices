import requests
import time

from pwn import *
#p = process("./regex")

def pwn_it(ip, idx):
	#
	# here is exp to get flag.
	# ...
	
	flag = buf.strip()

	assert len(flag) == 32

	print '[*]flag:', flag
	return flag

# get flag one by one.
def loop():

	for i in range(120,134):
		# skip myself.
		if i== 131:
			continue

		ip = '192.168.168.' + str(i)
		try:
			pwn_it(ip)
		except:
			print 'error'
		raw_input()

# get flag and auto submit.
def auto():
	count = 0
	for i in range(120,134):
		idx = i - 119
		if i== 131 or i==133:
			continue
		ip = '192.168.168.' + str(i)
		try:
			flag = pwn_it(ip, idx)		
			cookie =  "PHPSESSID=r1ok5mqncr2dgem41mibqg05l3"
			r = requests.post('http://192.168.168.102/judgead.php', data={"flag":flag, "number":2}, headers={"Cookie":cookie})
			print r.content
			if 'ok' in r.content:
				count += 1
			time.sleep(3)

		except Exception, e:
			print '[!]error', e
		#raw_input()
	print '*' * 50
	print '[*] total:' ,count
	print '*' * 50

if __name__ == '__main__':
	while True:
		
		auto()
		time.sleep(60*2)

