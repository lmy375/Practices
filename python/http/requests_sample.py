import requests
import re

s = requests.session()
resp = s.get('http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php')
cal_str = re.findall('([0-9*+()]+)=', resp.content)[0]
print "[*]cal:", cal_str
result = eval(cal_str)
print "[*]result:", result
resp2 = s.post('http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php',data = {'v':str(result)})

print resp2.content