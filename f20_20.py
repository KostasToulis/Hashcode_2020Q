import numpy as np
import random
from operator import itemgetter

class Building:
  def __init__(self,id,type,plan, r, c, value):
    self.id = id
    self.type = type
    self.plan = plan
    self.value = value
    self.r = r
    self.c = c

class Block:
  def __init__(self, Block_residential, Block_utility, score):
    self.residential = Block_residential
    self.utility = Block_utility
    self.score = score


def read_input(file):
  res = []
  util = []
  max_h = 0
  max_w = 0

  lines = open(file,'r').readlines()
  H,W,D,B = [int(val) for val in lines[0].split()]
  c = 1
  for i in range(B):
    tp,hp,wp,v = [val for val in lines[c].split()]
    hp,wp,v  = int(hp),int(wp),int(v)
    if hp>max_h: max_h = hp
    if wp>max_w: max_w = wp
    plan = []
    for r in range(hp):
      row = [1*(val=='#') for val in lines[c+r+1].rstrip('\n')]
      plan.append(row)
    plan = np.array(plan)
    c = c+hp+1
    if tp=='R': res.append(Building(id=len(res),type='R',plan=plan, r = hp, c = wp,value=v)) 
    if tp=='U': util.append(Building(id=len(util),type='U',plan=plan, r = hp, c = wp,value=v))
  return H,W,D,B,res,util,max_h,max_w




def create_output(results):
  f = open("output.txt", "w")
  f.write(str(len(results))+ "\n")
  for i in range(0,len(results)):
      string = ""
      for j in range(0, len(results[i])):
          f.write((str(results[i][j]).rstrip('\n')))
          f.write((str(" ").rstrip('\n')))
      f.write('\n')
  f.close()

def check_no_overlap(Plan, Project, point_x, point_y):
  sum1 = 0
  sum2 = 0
  for i in range(point_x, point_x+Project.r):
    for j in range(point_y, point_y+Project.c):
      sum1 = sum1 + Project.plan[i-point_x][j-point_y]
      sum2 = sum2 + Plan[i][j] + Project.plan[i-point_x][j-point_y]
      # print(sum1, sum2)
  if sum1==sum2:
    return True
  else:
    return False

def find_block(H, W, max_h, max_w):
  max_h = max_h*2
  while(np.mod(H, max_h) != 0):
    max_h = max_h + 1

  max_w = max_w*2
  while(np.mod(W, max_w) != 0):
    max_w = max_w + 1
  return max_h, max_w, (H/max_h)*(W/max_w)

def scoring(Block_residential, Block_utility, D, f):
  score = 0
  s = 0
  for res in Block_residential:
    if f == 1:
      print(s, len(Block_residential))
      s = s + 1
    uti_flag = np.zeros(1000)
    for uti in Block_utility:
      if uti_flag[uti.value] == 0:
        min_dist = 0
        for i in range(0, res.r):
          for j in range(0, res.c):
            for i_u in range(0, uti.r):
              for j_u in range(0, uti.c):
                dist = abs(i-i_u)+ abs(j-j_u)
                if dist < min_dist:
                  min_dist = dist
                  uti_flag[uti.value] = 1
      if min_dist <= D:
        score = score + res.value
  return score

H,W,D,B,Residential,Utilities,max_h,max_w = read_input('c_going_green.in')

Buildings = Residential + Utilities
print(len(Residential))
print(len(Utilities))
print(np.random.randint(len(Buildings)+1))
Blocks = list()
max_score = 0
max_h, max_w, all_blocks = find_block(H, W, max_h, max_w)
new_flag = 0
init_flag = 0
while (new_flag <= 10):
  print(new_flag)
  Block_residential = list()
  Block_utility = list()
  if len(Blocks) == 11:
    del Blocks[0]
    for i in range(len(Blocks)):
      print("BL ", Blocks[i][2])
  # print(len(Blocks))
  overlap_flag = 0
  Block = np.zeros((max_h, max_w))
  while (overlap_flag <= 1000):
    # print(overlap_flag)
    rnd_building = Buildings[np.random.randint(len(Buildings))]
    rnd_pos_r = np.random.randint(max_h)
    rnd_pos_c = np.random.randint(max_w)
    if ((rnd_pos_r + rnd_building.r) < max_h) and ((rnd_pos_c + rnd_building.c) < max_w):
      if check_no_overlap(Block, rnd_building, rnd_pos_r, rnd_pos_c):
        overlap_flag = 0
        for i in range(rnd_building.r):
          for j in range(rnd_building.c):
            Block[i+rnd_pos_r][j+rnd_pos_c] = rnd_building.plan[i][j]
        if rnd_building.type == 'R':
          Block_residential.append(rnd_building)
        else:
          Block_utility.append(rnd_building)
      else:
        overlap_flag = overlap_flag + 1
  score = scoring(Block_residential, Block_utility, D, 0)
  # print(11111, score, len(Block_residential), len(Block_utility))
  if init_flag == 0:
    Blocks.append([Block_residential, Block_utility, score]) 
    init_flag = 1
  else:
    if score > Blocks[-1][2]:
      new_flag = 0
      print("best", score)
      # Blocks.append([Block_residential, Block_utility, score])
    else: 
      new_flag = new_flag + 1
    Blocks.append([Block_residential, Block_utility, score])
    Blocks.sort(key=lambda x: x[2])
    
print(len(Blocks))
for i in range(len(Blocks)):
  print(Blocks[i][2])



All_Plant = np.zeros((H, W))
All_residential = list()
All_utility = list()
for i in range(0, H, max_h):
  for j in range(0, W, max_w):
    print(i,j,H,W)
    for res in Blocks[-1][0]:
      All_residential.append(res)
      for i2 in range(res.r):
          for j2 in range(res.c):
            All_Plant[i+res.r+i2][j+res.c+j2] = res.plan[i2][j2]
    for uti in Blocks[-1][1]:
      All_utility.append(uti)
      for i2 in range(uti.r):
          for j2 in range(uti.c):
            All_Plant[i+uti.r+i2][j+uti.c+j2] = uti.plan[i2][j2]

# print(scoring(All_residential, All_utility, D, 1))

