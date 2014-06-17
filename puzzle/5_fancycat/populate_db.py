import csv
from catgif.models import *

## run from inside catgif directory
## on terminal: python manage.py shell < ../populate_db.py

Post.objects.delete()

with open('../posts.csv', 'rb') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=",", quotechar='"')
	for row in csvreader:
		post = Post(title=row[1], slug=row[0], body=row[2], image_url=row[3])
		post.save()

print "Done loading data."

post = Post.objects.get()
print post