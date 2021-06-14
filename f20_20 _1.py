import numpy as np
import random
from operator import itemgetter

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
    self.sent_books = list()
    self.total_score = total_score
    self.signed = False
    kt=0.8
    kb=0.2
    self.value = (kt*self.total_score/8093  +kb*self.books_per_day/99998)/(self.sign_time/1000 )
    self.signing = sign_time

#a_example
#b_read_on #20 #100000 #1
#c_incunabula #1000 #8093 #99998
#d_tough_choices #2 #910 #1
#e_so_many_books #10 #129651 #2
#f_libraries_of_the_world #300 #412714 #10

def read_input(filename):
  books = []
  libraries = []

  lines = open(filename,'r').readlines()
  B,L,D = [int(val) for val in lines[0].split()]
  book_scores = [int(val) for val in lines[1].split()]

  books = [Book(id=i,score=book_scores[i]) for i in range(len(book_scores))]

  c = 2
  max1 = 0
  max2 = 0
  max3 = 0
  for i in range(L):
    n_books,sign_time,books_per_day = [int(val) for val in lines[c].split()]
    books_in_library = [int(val) for val in lines[c+1].split()]
    books_in_library = [books[id] for id in books_in_library]
    books_in_library.sort(key=lambda x: x.score, reverse=True)
    total_score = np.sum([b.score for b in books_in_library])
    libraries.append(Library(id=len(libraries),sign_time=sign_time,books_per_day=books_per_day,books_in_library=books_in_library,total_score=total_score))
    if sign_time > max1:
      max1 = sign_time
    if total_score > max2:
      max2 = total_score
    if books_per_day > max3:
      max3 = books_per_day
    c += 2


  return B,L,D,books,libraries, max1, max2, max3



def create_output(signed_libraries, libraries):
  s = 0
  for i in signed_libraries:
    if len(libraries[i].sent_books) != 0:
      s = s + 1
  f = open("output.txt", "w")
  f.write(str(s)+ "\n")
  for i in signed_libraries:
    if len(libraries[i].sent_books) != 0:
      string = ""
      f.write((str(i).rstrip('\n')))
      f.write((str(" ").rstrip('\n')))
      f.write((str(len(libraries[i].sent_books)).rstrip('\n')))
      f.write('\n')
      for j in libraries[i].sent_books:
          f.write((str(j).rstrip('\n')))
          f.write((str(" ").rstrip('\n')))
      f.write('\n')
  f.close()



#a_example
#b_read_on #20 #100000 #1
#c_incunabula #1000 #8093 #99998
#d_tough_choices #2 #910 #1
#e_so_many_books #10 #129651 #2
#f_libraries_of_the_world #300 #412714 #10


B,L,D,books,libraries, max1, max2, max3 = read_input("c_incunabula.txt") 
print(max1, max2, max3)
print(B,L,D)

k=0
# print([b.id for b in books])

# print(libraries[k].id,[b.id for b in libraries[k].books_in_library])



tmp_libraries = libraries + []
tmp_libraries.sort(key=lambda x: x.value,reverse=True)
# print("hello", libraries[1].books_in_library[1].id)
pending_libraries = [x.id for x in tmp_libraries]
signed_libraries = list()
# print(libraries[0].id, [x.id for x in libraries[0].books_in_library])
ON_OFF = np.ones(B)

t = 0
while t<D:
  print(t,D)
  # if np.mod(t,20) == 0:
  #   for i in pending_libraries:
  #     libraries[i].total_score = np.sum([b.score for b in libraries[i].books_in_library])
  #     libraries[i].value = (0.8*libraries[i].total_score/8093  +0.2*libraries[i].books_per_day/99998)/(libraries[i].sign_time/1000)
  #   tmp_pending = pending_libraries[1:]
  #   tmp_pending.sort(key=lambda x: libraries[x].value,reverse=True)
  #   pending_libraries = [pending_libraries[0]] + tmp_pending

  if signed_libraries:
    for i in signed_libraries:
      sent = 0
      asd = libraries[i].books_per_day
      while (sent<libraries[i].books_per_day)and(libraries[i].books_in_library):
        if ON_OFF[libraries[i].books_in_library[0].id] == 1:
          sent = sent + 1
          ON_OFF[libraries[i].books_in_library[0].id] = 0
          libraries[i].sent_books.append(libraries[i].books_in_library[0].id)
        libraries[i].books_in_library.pop(0)
      # print(i, sent, asd)
  if pending_libraries:
    if len(libraries[pending_libraries[0]].books_in_library) == 0:
        pending_libraries.pop(0)
  if pending_libraries:
    libraries[pending_libraries[0]].sign_time = libraries[pending_libraries[0]].sign_time - 1
    if libraries[pending_libraries[0]].sign_time == 0: #maybe
      signed_libraries.append(pending_libraries[0])
      pending_libraries.pop(0)

  t = t+1

create_output(signed_libraries, libraries)


