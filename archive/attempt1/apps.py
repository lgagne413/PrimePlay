import time
import itertools as it
from math import *

#Notes
#probability of prime = 1/log n
#prime factors log log n
#log n average gap size
#gap between primes at least m! to m!+m - reduce m! to lcm
#primorials conjecture - most frequent gaps

#naieve approach.  check each number for divisibility of each known prime
class findprime0(object):
  def __init__(self):
    print("Reading Saved Data")
    self.primes = []
    fh = open("primes.txt","r")
    for line in fh:
      if "x" in line:
        line=line.replace("x","")
        self.primes.append(int(line))
      elif line == "" or line == "\n":
        continue
      elif int(line.strip()):
        self.primes.append(int(line))
    fh.close()

  def __del__(self):
    print("Writing Data")
    self.primes.sort()
    fh = open("primes.txt","w")
    for num in self.primes:
      fh.write("\n"+str(num))
    fh.close()
    return

  def run(self):
    t0=time.process_time()
    self.calcPrime()
    time.process_time()
    return


  def calcPrime(self):
    foundPrime = False
    N = max(self.primes)
    while not foundPrime:
      N+=2
      ps = [p for p in self.primes if p<math.sqrt(N)]
      div = False
      for p in ps:
        if N % p == 0:
          div = True
      if div == False:
        foundPrime = True
        print(N)
        self.primes.append(N)
    return 


#sum and difference of products of mutually exclusive primes
class findprime1(object):
  def __init__(self):
    print("Reading Saved Data")
    self.histogram = dict()
    self.primes = []
    self.primesx = []
    self.primal = 2
    self.calclist = []
    fh = open("primes.txt","r")
    flag=False
    for line in fh:
      if "x" in line:
        line=line.replace("x","")
        self.primes.append(int(line))
        self.primesx.append(int(line))
        self.primal = int(line)
        flag=True
      elif line == "" or line == "\n":
        continue
      elif int(line.strip()):
        self.primes.append(int(line))
        if flag == False:
          self.primesx.append(int(line))
    fh.close()
    self.pmax = max(self.primesx)

  def __del__(self):
    print("Writing Data")
    self.primes.extend(self.possibles)
    self.primes.sort()
    print(self.possibles)
    nxt = min([x for x in self.primes if x>self.primal])
    fh = open("primes.txt","w")
    for num in self.primes:
      if num == nxt:
        fh.write("\n"+str(num)+"x")
      else:
        fh.write("\n"+str(num))
    fh.close()
    for key,value in self.histogram.items():
      if key in self.primes:
        print(str(key) + "\t\t|||\t\t\t" + str(value))
      else:
        print(str(key) + "\t\t:::\t\t" + str(value))
    return

  def run(self):
    self.combList()
    self.calcPrime()
    return

  def combList(self):
    print("Finding Combinations")
    comblist = list()
    revcomblist = list()
    for r in range(1,len(self.primesx)):
      a = list(it.combinations(self.primesx,r))
      b = list(it.combinations(self.primesx,r))
      comblist.append(a)
      b.reverse()
      revcomblist.append(b)
    revcomblist.reverse()
    

    #length of comb
    for rnum in range(0,len(comblist)):
    #combination
      for combnum in range(0,len(comblist[rnum])):
        n1=comblist[rnum][combnum]
        n2=revcomblist[rnum][combnum]
      #print(n1,n2)
        self.calclist.append([n1,n2])
    if len(self.calclist)%2!=0:print("CALCLIST length not divisible by 2")
    self.calclist = self.calclist[0:len(self.calclist)//2] 
    return 

  def calcPrime(self):
    self.possibles=[]
    for pair in self.calclist:
      prod = []
      for comb in pair:
        hold=1
        for num in comb:
          hold*=num
        prod.append(hold)
      print(pair)
      poss = abs(prod[0]-prod[1])
      print(poss)
      self.histogram[poss] = self.histogram.get(poss,0)+1
      if poss < (self.pmax+2)**2 and poss not in self.primes and poss not in self.possibles and poss >1:
        self.possibles.append(poss)
      poss = abs(prod[0]+prod[1])
      self.histogram[poss] = self.histogram.get(poss,0)+1
      print(poss)
      if poss < (self.pmax+2)**2 and poss not in self.primes and poss not in self.possibles and poss >1:
        self.possibles.append(poss)
    return 


#only consider variable powers of 2 and 3
class findprime2(object):
  def __init__(self):
    print("Reading Saved Data")
    self.histogram = dict()
    self.primes = []
    self.primesx = []
    self.primal = 2
    self.calclist = []
    fh = open("primes.txt","r")
    flag=False
    for line in fh:
      if "x" in line:
        line=line.replace("x","")
        self.primes.append(int(line))
        self.primesx.append(int(line))
        self.primal = int(line)
        flag=True
      elif line == "" or line == "\n":
        continue
      elif int(line.strip()):
        self.primes.append(int(line))
        if flag == False:
          self.primesx.append(int(line))
    fh.close()
    self.pmax = max(self.primesx)

  def __del__(self):
    print("Writing Data")
    self.primes.extend(self.possibles)
    self.primes.sort()
    print(self.possibles)
    nxt = min([x for x in self.primes if x>self.primal])
    fh = open("primes.txt","w")
    for num in self.primes:
      if num == nxt:
        fh.write("\n"+str(num)+"x")
      else:
        fh.write("\n"+str(num))
    fh.close()
    for key,value in self.histogram.items():
      if key in self.primes:
        print(str(key) + "\t\t|||\t\t\t" + str(value))
      else:
        print(str(key) + "\t\t:::\t\t" + str(value))
    return

  def run(self):
    self.combList()
    self.calcPrime()
    return

  def combList(self):
    print("Finding Combinations")
    comblist = list()
    revcomblist = list()
    for r in range(1,len(self.primesx)):
      a = list(it.combinations(self.primesx,r))
      b = list(it.combinations(self.primesx,r))
      comblist.append(a)
      b.reverse()
      revcomblist.append(b)
    revcomblist.reverse()
    

    #length of comb
    for rnum in range(0,len(comblist)):
    #combination
      for combnum in range(0,len(comblist[rnum])):
        n1=comblist[rnum][combnum]
        n2=revcomblist[rnum][combnum]
      #print(n1,n2)
        self.calclist.append([n1,n2])
    if len(self.calclist)%2!=0:print("CALCLIST length not divisible by 2")
    self.calclist = self.calclist[0:len(self.calclist)//2] 
    return 

  def calcPrime(self):
    print("Calculating Primes")
    self.possibles=[]
    for pair in self.calclist:
      if pair[1][0]==2:
        temp = pair[0]
        pair[0]=pair[1]
        pair[1]=temp
      if pair[1][0]==3:
        case = "A"
        
      else:
        case = "B"
        
      Pl = [p for p in pair[0] if p!=2 and p!=3]
      P = 1
      for p in Pl:
        P*=p
      Ql = [p for p in pair[1] if p!=2 and p!=3]
      Q=1
      for q in Ql:
        Q*=q
      x=1
      ymin,ymax = self.yminmax(x,P,Q,case)
      
      tol = ymax - ymin
      while tol>=0:
        
        for y in range(ymin,ymax+1):
          if case == "A":
            poss = abs(2**x*P-3**y*Q)
            print(poss,pair,x,y)
            self.checkPrime(poss)
          elif case == "B":
            poss = abs(2**x*3**y*P-Q)
            print(poss,pair,x,y)
            self.checkPrime(poss)
        x+=1
        #log(-1)
        ymin,ymax = self.yminmax(x,P,Q,case)
        tol = ymax - ymin
        
      print(pair)
      
    return

  def yminmax(self,x,P,Q,case):
    if case == "A":
      if (-(self.pmax+2)**2+2**x*P)/Q<=0 or ceil(log((-(self.pmax+1.999)**2+2**x*P)/Q)/log(3)) <1:
        
        ymin = 1
      else:
        ymin = ceil(log((-(self.pmax+1.999)**2+2**x*P)/Q)/log(3))
        
      ymax = floor(log(((self.pmax+1.999)**2+2**x*P)/Q)/log(3))
      
    elif case == "B":
      if (-(self.pmax+1.999)**2+Q)/P <=0 or ceil((log(((-(self.pmax+1.999)**2+Q)/P))-x*log(2))/log(3))<1:
        ymin = 1
      else:
        ymin = ceil((log(((-(self.pmax+1.999)**2+Q)/P))-x*log(2))/log(3))
      ymax = floor((log(((self.pmax+1.999)**2+Q)/P)-x*log(2))/log(3))

    return ymin, ymax

  def checkPrime(self,poss):
    if poss not in self.primes and poss not in self.possibles and poss >1 and poss < (self.pmax+2)**2:
      print("New Prime!",poss)
      self.possibles.append(poss)
    return


#consider all variable powers?
class findprime3(object):
  def __init__(self):
    print("Reading Saved Data")
    self.histogram = dict()
    self.primes = []
    self.primesx = []
    self.primal = 2
    self.calclist = []
    fh = open("primes.txt","r")
    flag=False
    for line in fh:
      if "x" in line:
        line=line.replace("x","")
        self.primes.append(int(line))
        self.primesx.append(int(line))
        self.primal = int(line)
        flag=True
      elif line == "" or line == "\n":
        continue
      elif int(line.strip()):
        self.primes.append(int(line))
        if flag == False:
          self.primesx.append(int(line))
    fh.close()
    self.pmax = max(self.primesx)

  def __del__(self):
    print("Writing Data")
    self.primes.extend(self.possibles)
    self.primes.sort()
    print(self.possibles)
    nxt = min([x for x in self.primes if x>self.primal])
    fh = open("primes.txt","w")
    for num in self.primes:
      if num == nxt:
        fh.write("\n"+str(num)+"x")
      else:
        fh.write("\n"+str(num))
    fh.close()
    for key,value in self.histogram.items():
      if key in self.primes:
        print(str(key) + "\t\t|||\t\t\t" + str(value))
      else:
        print(str(key) + "\t\t:::\t\t" + str(value))
    return

  def run(self):
    self.combList()
    self.calcPrime()
    return

  def combList(self):
    print("Finding Combinations")
    comblist = list()
    revcomblist = list()
    for r in range(1,len(self.primesx)):
      a = list(it.combinations(self.primesx,r))
      b = list(it.combinations(self.primesx,r))
      comblist.append(a)
      b.reverse()
      revcomblist.append(b)
    revcomblist.reverse()
    

    #length of comb
    for rnum in range(0,len(comblist)):
    #combination
      for combnum in range(0,len(comblist[rnum])):
        n1=comblist[rnum][combnum]
        n2=revcomblist[rnum][combnum]
      #print(n1,n2)
        self.calclist.append([n1,n2])
    if len(self.calclist)%2!=0:print("CALCLIST length not divisible by 2")
    self.calclist = self.calclist[0:len(self.calclist)//2] 
    return 

  def calcPrime(self):
    print("Calculating Primes")
    self.possibles=[]
    for pair in self.calclist:
      pairflag = True
      Pl = [p for p in pair[0] if p!=2]
      exP=[1 for x in Pl]
      
      Ql = [p for p in pair[1]]
      exQ = [1 for x in Ql]
      ex=[]
      ex.extend(exP)
      ex.extend(exQ)
      while pairflag: #inside here change exponents
        bound=False
        count=0
        #recalculate P and Q
        P = 1
        for n in range(len(Pl)):
          P*=Pl[n]**ex[n]
        Q=1
        for n in range(len(Ql)):
          Q*=Ql[n]**ex[n+len(Pl)]
        
        ## find poss powers of 2
        y,ymax = self.yminmax(P,Q)
        if ymax - y < 0:
          bound=True
        else:
          while y<=ymax:
            self.checkPrime(abs(2**y*P-Q))  
            y+=1
          

        #update exponents / check flag
        print(ex)
        ex, pairflag = self.exponentUp(ex)
        print(pair)     
    return

  def exponentUp(ex):
    ex[0]+=1
    flag=True
    for n in range(len(ex)):
      if ex[n]==10:
        ex[n]=0
        try:
          ex[n+1]+=1
        except:
          flag=False
      pass
    return ex,flag

  def yminmax(self,P,Q):
    M = (self.pmax+2)**2
    if (-M+Q)/P<=0 or ceil(log((-M+Q)/P)/log(2)) <1:
        
      ymin = 1
    else:
      ymin = ceil(log((-M+Q)/Q)/log(2))
        
    ymax = floor(log((M+Q)/P)/log(2))
    return ymin, ymax

  def checkPrime(self,poss):
    if poss not in self.primes and poss not in self.possibles and poss >1:
      print(poss)
      self.possibles.append(poss)
    return
