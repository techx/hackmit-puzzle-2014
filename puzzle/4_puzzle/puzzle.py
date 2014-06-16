#############################################
# HackMIT 2014 Registration Puzzle
# Unique to each user
# Uses salted SHA512 hash
# Made by Michael Holachek
#############################################

import hashlib, os, binascii, random

puzzle = []
puzzle_length = 500
secret = "CanadianNyanCat"
answer_line = random.randint(10,puzzle_length)

puzzle.append("Read between the lines to find the key. " + str(answer_line))

for i in range(1, puzzle_length):
	puzzle.append( hashlib.sha224(secret + str(i)).hexdigest() )

puzzle[answer_line] = hashlib.sha224( puzzle[answer_line-1] + puzzle[answer_line+1] ).hexdigest()

if hashlib.sha224( puzzle[answer_line-1]  + puzzle[answer_line+1] ).hexdigest() == puzzle[answer_line]:
	print "True"

# PUZZLE_ID = binascii.b2a_hex(os.urandom(3))
# PUZZLE_LINE = random.randint(10,501)
# PUZZLE_LINE_HEX = str(hex(PUZZLE_LINE))[2:]

# print "New puzzle with ID " + PUZZLE_ID + " and answer line #" + str(PUZZLE_LINE) + " // hex: " + PUZZLE_LINE_HEX


# LINE_LENGTH = 28
# INSTRUCTIONS_LINE = 0

# lines = []

# for i in range(0, 501):
# 	if i == INSTRUCTIONS_LINE:
# 		lines.append("Read between the lines to find the key. Your puzzle ID: " + PUZZLE_ID + PUZZLE_LINE_HEX)
# 	else:
# 		lines.append(binascii.b2a_hex(os.urandom(LINE_LENGTH)))

# print lines[PUZZLE_LINE - 1], lines[PUZZLE_LINE + 1]

# lines[PUZZLE_LINE] = hashlib.sha224(lines[PUZZLE_LINE - 1] + lines[PUZZLE_LINE - 1]).hexdigest()

# print lines[PUZZLE_LINE]


# f = open('puzzle.txt', 'w')

# for line in lines:
# 	f.write(line + '\n')

# f.close()

## check answer
# answer_to_check = "e9b81ab7"
# correct_answer = ANSWER

# if answer_to_check == correct_answer:
# 	print "SOLVED!"
