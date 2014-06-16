
## to solve the puzzle, the answer line is hash of above and below line

import hashlib, os

lines = tuple(open('puzzle.txt', 'r'))[1:]
length = len(lines)

# count = 0

# while count < 500:
# 	above = lines[count-1]
# 	below = lines[count+1]
# 	if hashlib.sha224(above + below).hexdigest() == lines[count]:
# 		print "ANSWER on line " + count


print hashlib.sha224('cdee50af39843863c151aa24d4e34df456d43a4a4c2a271e6b78ad66' + '5277f2360e1f63d93095e1364382630017aa76319d506d22b09b1ce4').hexdigest()