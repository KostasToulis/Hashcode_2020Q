import numpy as np 
import random
import time


class Book:
	def __init__(self,id,score):
		self.id = id
		self.score = score
		self.scanned = True

class Library:
	def __init__(self,id,sign_time,books_per_day,books_in_library,total_score):
		self.id = id
		self.sign_time = sign_time
		self.books_per_day = books_per_day
		self.books_in_library = books_in_library
		self.total_score = total_score
		self.signed = False
		kt=0.5
		kb=0.5
		self.value = (kt*self.total_score+kb*self.books_per_day)/self.sign_time
		self.signing = sign_time



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
		books_in_library.sort(key=lambda x: x.score)
		total_score = np.sum([b.score for b in books_in_library])
		libraries.append(Library(id=len(libraries),sign_time=sign_time,books_per_day=books_per_day,books_in_library=books_in_library,total_score=total_score))
		c += 2

	return B,L,D,books,libraries

B,L,D,books,libraries = read_input("b_read_on.txt")	

print(B,L,D)

k=0
print([b.id for b in books])

print(libraries[k].id,[b.id for b in libraries[k].books_in_library])
