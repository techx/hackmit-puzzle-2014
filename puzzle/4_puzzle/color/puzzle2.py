import random, os, binascii

r = lambda: random.randint(0,255)

c2 = ('%02X%02X%02X' % (r(),r(),r()))


for i in range(0, 60):
	for j in range(0, 60):
		c1 = ('%02X%02X%02X' % (r(),r(),r()))
		link = binascii.b2a_hex(os.urandom(6))
		print "<a href='" + link + "'><div style='background:#" + c1 + "'></div></a>"
	print "<div id='break'></div>"