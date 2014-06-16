from Crypto.Cipher import AES
import base64
import hashlib
import random
from flask import Flask
from flask import render_template
from flask_limiter import Limiter
from flask import request
import bleach
import os

app = Flask(__name__)
limiter = Limiter(app, global_limits=["1 per second"])

### 4841434b.com app

secret = "CanadianNyanCat"

BLOCK_SIZE = 16
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
secret_key = base64.b64decode('Ioa5fUurvqyOQsCAn53RLg==')


@app.route("/")
def index():
	return render_template('index.html')

@app.route("/generate")
@limiter.limit("15 per minute")
def generate():
	puzzle = []
	puzzle_length = 500
	answer_line = random.randint(10,puzzle_length)
	cipher = AES.new(secret_key)
	answer_link_encrypted = EncodeAES(cipher, str(answer_line)).encode('hex')

	# puzzle.append("Read between the lines. Puzzle code: " + )

	for i in range(0, puzzle_length):
		puzzle.append( hashlib.sha224(secret + str(i) + str(answer_line)).hexdigest() )

	puzzle[answer_line] = hashlib.sha224( puzzle[answer_line-1] + puzzle[answer_line+1] ).hexdigest()

	puzzle_text = ""

	for line in puzzle:
		printed_line = line + "<br>"
		puzzle_text += printed_line

	return render_template('puzzle.html', puzzle_id=answer_link_encrypted, puzzle=puzzle_text)


@app.route("/check", methods=['GET'])
@limiter.limit("20 per minute")
def check():
	if request.method == "GET":
		guess_line = bleach.clean(request.args.get('guess_line'))
		puzzle_id = bleach.clean(request.args.get('puzzle_id')).decode('hex')
		
		cipher = AES.new(secret_key)
		decrypted_answer = DecodeAES(cipher, puzzle_id)
		
		if guess_line == decrypted_answer:
			return render_template('answer.html')
		else:
			return "Looks like you have some solving to do!"
	else:
		return "Looks like you have some solving to do!"


@app.errorhandler(404)
def page_not_found(e):
	return "Page not found."

# def encrypt(key, plaintext):
#   cipher = ARC4.new(key)
#   print cipher.encrypt(plaintext)
#   return base64.b64encode(cipher.encrypt(plaintext))

# def decrypt(key, ciphertext):
#   cipher = ARC4.new(key)
#   return cipher.decrypt(base64.b64decode(ciphertext))




if __name__ == "__main__":
	app.run(debug=True)