# -*- coding: utf-8 -*-
#get primes needs to be more efficient

import pandas
import math
import itertools

def get_primes(n):
    fh=open('primes.txt','r')
    primes=[int(a.strip()) for a in fh.read().split(',')]
    fh.close()
    botlimit=max(primes)
    toplimit = n

    sieve = [True for i in range(toplimit + 1)]
    for p in primes:
        for n in range(p**2, toplimit + 1, p):
            sieve[n] = False
    a = botlimit+1
    while a ** 2 <= toplimit:
        print (a, end="\r")
        if sieve[a] == True:
            for b in range(a ** 2, toplimit + 1, a):
                sieve[b] = False
        a += 1
    fh=open('primes.txt','a')
    for a in range(botlimit+1, toplimit + 1):
        if sieve[a] == True:
            primes.append(a)
            
            fh.write(','+str(a))
    fh.close()
    print('primes complete', end='\n')
    return primes

def factorize(x):
    o=x
    primes = PRIMES
    factor_save=FACTORS
    factors = []
    xt=0
    while x != 1:
        print (o,x, end="\r")
        if xt==x:raise ValueError('No prime factor found {}'.format(x))
        else:xt=x
        if x in factor_save: 
            factors.extend(factor_save[x])
            save_factors(o,factors)
            return factors
        for i in primes:
            if x % i == 0:
                factors.append(i)
                x = x / i
                break

    save_factors(o,factors) 
    
    return factors

def get_factors():
    fh=open('factors.txt','r')
    f1=fh.read().split('\n')
    f2=[f.split(':') for f in f1]
    factors={int(x[0]) : [int(x) for x in x[1].split(',')] for x in f2}
    return factors
def save_factors(x,f):
    fh=open('factors.txt','a')
    s='\n'+str(x)+':'
    for x in range(len(f)):
        s+=str(f[x])
        if x!=len(f)-1:s+=','
    fh.write(s)
    fh.close()
    
PRIMES=get_primes(100)
FACTORS=get_factors()
#################################################
print('retrieved saved factors')

A=[p for p in PRIMES[0:1]]
for a in range(len(A)): 
    A.append(-1*A[a])
B=[p for p in PRIMES[2:4]]
for a in range(len(B)): 
    B.append(-1*B[a])
    
x=[a for a in range(3,15)]
y=[a for a in range(3,15)]
print('x,y')

r=[]
for a1,b1,x1,y1 in itertools.product(A,B,x,y):
    if not (abs(a1)==abs(b1)) and not (a1<0 and x1%2==0) and not (b1<0 and y1%2==0) and math.gcd(a1,b1)==1:
        r.append((a1,x1,b1,y1))
print('r')

z=[abs(r1[0]**r1[1]+r1[2]**r1[3]) for r1 in r]
print('z')

print('primes')
PRIMES=get_primes(max(z))

print('factors')
p=[factorize(z1) for z1 in z]
print('factors complete')
for l in p:
    for x in l:
        if l.count(x) %3==0:
            print('HEY : ',l)
            break

df=pandas.DataFrame(data={'A':[r1[0] for r1 in r],'x':[r1[1] for r1 in r],'B':[r1[2] for r1 in r],'y':[r1[3] for r1 in r],'z':[z1 for z1 in z],'p':p})

print(df.to_string())

