#############################################
# HackMIT 2014 Registration Puzzle
# Unique to each user
# Uses salted SHA512 hash
# Made by Michael Holachek
#############################################

import hashlib, os, binascii, random

EMAIL_ADDRESS = "holachek@mit.edu"
KEY = "CanadianNyanCat"

# helper functions
def split_by_n( seq, n ):
    """A generator to divide a sequence into chunks of n units."""
    while seq:
        yield seq[:n]
        seq = seq[n:]


## generate puzzle answer using email address
GEN_KEY = hashlib.sha224(KEY + EMAIL_ADDRESS).hexdigest()
SPLIT_KEY = list(split_by_n(GEN_KEY, 8))
ANSWER = SPLIT_KEY[0]

ANSWER_LINE = random.randint(1000, 9999)
INSTRUCTIONS_LINE = random.randint(10, 999)

f = open('puzzle.txt', 'w')

for i in range(0, 10000):
	if i == ANSWER_LINE:
		LINE = binascii.b2a_hex(os.urandom(30)) + '[' + ANSWER + ']' + binascii.b2a_hex(os.urandom(25 - len('[' + ANSWER + ']')))
	elif i == INSTRUCTIONS_LINE:
		LINE = "HAHAHA you'll never figure this out. Find the secret code."
	else:
		LINE = binascii.b2a_hex(os.urandom(50))
	f.write(LINE + '\n')

f.close()

## check answer
answer_to_check = "e9b81ab7"
correct_answer = ANSWER

if answer_to_check == correct_answer:
	print "SOLVED!"
