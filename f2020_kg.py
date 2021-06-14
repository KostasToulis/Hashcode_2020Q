import numpy as np 
import random
import time


class Book:
	def __init__(self,id,score):
		self.id = id
		self.score = score
		self.scanned = False

class Library:
	def __init__(self,id,sign_time,books_per_day,books_in_library,total_score):
		self.id = id
		self.sign_time = sign_time
		self.books_per_day = books_per_day
		self.books_in_library = books_in_library
		self.sent_books = []
		self.total_score = total_score
		self.signed = False
		kt=0.5
		kb=0.5
		self.value = (kt*self.total_score+kb*self.books_per_day)/self.sign_time
		#self.value = self.books_per_day
		self.signing = sign_time

	def send_books(self,books):
		for i in range(min(self.books_per_day,len(self.books_in_library))):
			if not self.books_in_library[i].scanned:
				self.sent_books.append(books[self.books_in_library[i].id])
				books[self.books_in_library[i].id].scanned = True
		self.books_in_library = self.books_in_library[self.books_per_day:]

	def signup(self,signed,pending):
		self.signing -= 1
		if self.signing == 0:
			signed.append(self)
			del pending[0]
		return signed,pending




def read_input(filename):
	books = []
	libraries = []

	lines = open(filename,'r').readlines()
	B,L,D = [int(val) for val in lines[0].split()]
	book_scores = [int(val) for val in lines[1].split()]

	books = [Book(id=i,score=book_scores[i]) for i in range(len(book_scores))]

	c = 2
	for i in range(L):
		n_books,sign_time,books_per_day = [int(val) for val in lines[c].split()]
		books_in_library = [int(val) for val in lines[c+1].split()]
		books_in_library = [books[id] for id in books_in_library]
		books_in_library.sort(key=lambda x: x.score,reverse=True)
		total_score = np.sum([b.score for b in books_in_library])
		libraries.append(Library(id=len(libraries),sign_time=sign_time,books_per_day=books_per_day,books_in_library=books_in_library,total_score=total_score))
		c += 2



	return B,L,D,books,libraries

in_name = "e_so_many_books.txt"
B,L,D,books,libraries = read_input(in_name)	


pending = libraries
pending.sort(key=lambda x: x.value,reverse=True)
signed = []
for d in range(D):
	for l in signed:
		l.send_books(books)
	if (len(pending)>0):
		signed,pending = pending[0].signup(signed,pending)

def create_output(fname,signed):
	f = open(fname,'w')
	A = len(signed)
	f.write(str(A)+'\n')
	for i in range(A):
		line1 = str(signed[i].id)+' '+str(len(signed[i].sent_books))
		
		line2 = ''
		for j in range(len(signed[i].sent_books)):
			line2 = line2 + str(signed[i].sent_books[j].id) + ' ' 

		f.write(line1+'\n')
		f.write(line2+'\n')

fname = 'output_'+in_name
create_output(fname,signed)