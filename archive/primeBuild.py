import pandas
import math
import itertools
import sqlite3
import gc

def get_primes(n,talk=False,commit_on=500):
    n=math.floor(n)
    if talk:print('primes - {}'.format(n))
    con = sqlite3.connect('data/primeplay.db')
    t=int(con.execute('select max(number) from intfactors').fetchall()[0][0])
    if t>=n:
        primes=[x[0] for x in con.execute('select number from intfactors where remainder=1 and number <=?',[n]).fetchall()]
        con.close()
        return primes
    while t<=n:
        t+=1
        
        primeflag=True
        for p in [x[0] for x in con.execute('select number from intfactors where remainder=1 and number <? order by number asc',[int(t**(1/2))+1]).fetchall()]:
            if t%p==0:
                primeflag=False
                con.execute('INSERT or ignore INTO intfactors VALUES (?,?,?)',(t,p,t/p))
                break
        if primeflag:con.execute('INSERT or ignore INTO intfactors VALUES (?,?,?)',(t,t,1))      
        if t%commit_on==0:
            con.commit()
            if talk:print ('num: {}                                  '.format(t), end="\r")
            gc.collect()
    
    primes=[x[0] for x in con.execute('select number from intfactors where remainder=1').fetchall()]
    con.commit() 
    con.close()
    if talk:print('primes - {} - complete'.format(n))
    return primes

def factorize(x,talk=False):
    t=int(x)
    get_primes(x/2)
    factors=[]
    con = sqlite3.connect('data/primeplay.db')
    while t != 1:
        num,pf,rem= con.execute('select * from intfactors where number = ?',[t]).fetchall()[0]
        factors.append(pf)
        t=rem
    con.close()
    if talk:print ('num: {} factors: {}                                   '.format(t,factors), end="\r")
    return factors

for x in range(99000000,100000001,10000):
    get_primes(x,talk=True)
    gc.collect()