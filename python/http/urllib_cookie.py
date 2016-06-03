import urllib2 
import cookielib

cj = cookielib.CookieJar();
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj));
urllib2.install_opener(opener);

URL = "http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php"
buf = urllib2.urlopen(URL).read().decode("utf-8")
result = eval(buf[buf.rindex("<br/>")+6:buf.index("=<input")])
print buf
print result

req = urllib2.Request(URL, "v=%s" % result)
buf = urllib2.urlopen(req).read().decode("utf-8")
print buf