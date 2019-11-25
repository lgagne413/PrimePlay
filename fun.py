import itertools as it
from math import *


def calcPrimes2(allp,pmax,calclist):
  possibles=[]
  
  for pair in calclist:
    for comb in pair:
      for num in comb:
        pass
      
    poss = abs(prod[0]-prod[1])
    if poss < (pmax+2)**2 and poss not in allp and poss not in possibles and poss >1:
      possibles.append(poss)
    poss = abs(prod[0]+prod[1])
    if poss < (pmax+2)**2 and poss not in allp and poss not in possibles and poss >1:
      possibles.append(poss)
  return possibles
