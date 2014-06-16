
## to solve the puzzle, the answer line is hash of above and below line

import hashlib, os, sys

lines = tuple(open('puzzle.txt', 'r'))
line_number = lines[0][-4:]
length = len(lines)


count = 0

while count < length:
	above = lines[count-1][:-1]
	below = lines[count+1][:-1]
	hash1 = hashlib.sha224(above + below).hexdigest()
	if hash1 + "\n" == lines[count]:
		print "Found on ", count
		sys.exit(1)
	count += 1
	if count > 499:
		sys.exit(1)
