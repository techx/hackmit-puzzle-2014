
## to solve the puzzle, the answer line is hash of above and below line

import hashlib

puzzle_text = tuple(open('puzzle.txt', 'r'))
puzzle_line_count = len(puzzle_text)
current_line = 0

while current_line < puzzle_line_count:
	above = puzzle_text[current_line-1][:-1]
	below = puzzle_text[current_line+1][:-1]
	hash1 = hashlib.sha224(above + below).hexdigest()
	if hash1 + "\n" == puzzle_text[current_line]:
		print "Found on ", current_line
		break
	current_line += 1
	if current_line > 499:
		break
