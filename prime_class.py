import time
import itertools as it
import math as m
import sqlite3 as sql
import queries as q
import numpy as np
#print(sql.sqlite_version)

class BasePrime():
    def __init__(self,db_name: str, prime_limit = 100, overwrite = False):
        self.db_conn = sql.connect(f'data/prime_{db_name}.db')
        self.prime_limit = prime_limit
        if overwrite:
            self.db_conn.execute(q.OVERWRITE_PRIME_TABLE)
            self.db_conn.commit()
        self.db_conn.execute(q.CREATE_PRIME_TABLE)
        self.db_conn.execute(q.CREATE_PRIME_TABLE_INITIAL)
        self.db_conn.commit()
    def __del__(self):
        #self.summary()
        self.db_conn.close()
    def upsert_db(self,p: int, t: int):
        self.db_conn.execute(q.INSERT_PRIME_TABLE.format(prime=p, count=1, time=t))
        self.db_conn.commit()
    def get_max_prime(self):
        x = self.db_conn.execute(q.GET_MAX_PRIME).fetchall()
        return x[0][0]
    def get_n_prime(self, n):
        cursor = self.db_conn.execute(q.GET_N_PRIME.format(n=n)).fetchall()
        return cursor
    def get_n_small_prime(self, n):
        cursor = self.db_conn.execute(q.GET_N_SMALL_PRIME.format(n=n)).fetchall()
        return cursor
    def get_all_prime(self):
        cursor = self.db_conn.execute(q.GET_ALL_PRIME).fetchall()
        return cursor
    def get_num_prime(self,n):
        cursor = self.db_conn.execute(q.GET_NUM_PRIME.format(n=n)).fetchall()
        return cursor[0][0]
    def get_sum_prime(self,n):
        cursor = self.db_conn.execute(q.GET_SUM_PRIME.format(n=n)).fetchall()
        return cursor[0]
    def get_sub_prime(self, n):
        cursor = self.db_conn.execute(q.GET_SUB_PRIME.format(n=n)).fetchall()
        return cursor
    def find_primes(self):
        # Override THIS
        return [self.prime_limit]
    def time_primes(self):
        t0 = time.time_ns()
        ps = self.find_primes()
        dt = time.time_ns() - t0
        # print(ps,dt)
        return (ps, dt)
    def run(self):
        while self.get_max_prime() < self.prime_limit:
            ps,ts = self.time_primes()
            num_p = len(ps)
            if num_p == 0:return False
            t = m.ceil(ts / num_p)
            for p in ps:
                #print(p,t)
                self.upsert_db(p,t)
        self.summary()
        return True
    def summary(self):

        print('Summary:')
        qty = self.get_num_prime(self.prime_limit)
        count, time = self.get_sum_prime(self.prime_limit)

        print('Primes Qty - {}'.format(qty))
        print('Primes Count - {}'.format(count))
        print('Primes Time - {}'.format(time))
        print('Per Count - {}'.format(round(time/count,1)))
        print('Per Qty - {}'.format(round(qty/count,1)))
        rmod=0
        plist = self.get_sub_prime(self.prime_limit)
        for i in range(0,len(plist),2):
            max_width = 50

            if i+1<len(plist):
                space = max_width - len(str(plist[i]))
                print("{}{}{}".format(plist[i],' '*space,plist[i+1]))
            else:
                print("{}".format(plist[i]))

class SimplePrime(BasePrime):
    def __init__(self, prime_limit = 100, overwrite = True):
        super().__init__('simple', prime_limit, overwrite)
    def find_primes(self):
        N = self.get_max_prime()
        while True:
          N+=2
          ps = [row[0] for row in self.get_sub_prime(m.ceil(m.sqrt(N)))]
          #print('maxstore-',max(ps))
          div = False
          for p in ps:
            if N % p == 0:
              div = True
              break
          if div == False:
            #print('found-',N)
            return [N,]

def log_b(b,arg):
    return m.log(arg)/m.log(b)

class PrimePair():
    def __init__(self,pair,db_conn = None):
        self.db_conn = db_conn
        pair = [ list(l) for l in pair]
        [ list(l).sort() for l in pair]

        if pair[0][0]==2:
            self.pair = pair
        else:
            self.pair = pair[::-1]

        self.big_prime = max(max(self.pair[0]),max(self.pair[1]))
        self.constraint = (self.big_prime+2)**2

        self.a = self.pair[0]
        self.b = self.pair[1]
        self.p = self.pair[0] + self.pair[1]
        self.breaker = len(self.pair[0])
        self.plen = len(self.p)
        self.e = [1 for x in self.p]
        self.ps = []
        self.emax = [1 for x in self.p]
        self.tol = 10**-1

        aprod = np.product(self.pair[0])
        bprod = np.product(self.pair[1])
        element_cap = 10**20

        for x in range(self.plen):
            if x < self.breaker:
                self.emax[x] = m.ceil(log_b(self.p[x],element_cap/aprod))

            else:
                self.emax[x] = m.ceil(log_b(self.p[x],element_cap/bprod))

    def __str__(self):
        return self.pair
    def carry(self,tolflag):
        self.e[1]+=1
        for x in range(1,self.plen):
            if self.e[x] > self.emax[x] or (tolflag and self.e[x]>1):
                if x+1>=self.plen:return True
                self.e[x] = 1
                self.e[x+1] += 1
                tolflag=False

        return False


    def calculate(self, e = False):
        if not e: e = [x for x in self.e]
        outa = 1
        outb =1
        for x in range(self.plen):
            if x < self.breaker:
                outa*=self.p[x]**e[x]
            else:
                outb*=self.p[x]**e[x]
        return outa-outb
    def get_bounds(self, e = False):
        outa = 1
        outb =1
        if not e: e = [x for x in self.e]
        for x in range(1,self.plen):
            if x < self.breaker:
                outa*=self.p[x]**e[x]
            else:
                outb*=self.p[x]**e[x]
        if (outb-self.constraint)/outa <=0:
            xmin = 1
        else: xmin = log_b(self.p[0],(outb-self.constraint)/outa)
        if (outb+self.constraint)/outa <=0:
            xmax = 0
        else: xmax = log_b(self.p[0],(outb+self.constraint)/outa)
        #print('Bounds ',xmax,xmin)

        return max(1,m.ceil(xmin)), max(0,m.floor(xmax)), xmax-xmin < self.tol
    def check_out(self, out):
        out = abs(out)
        if  out > 1 and out < self.constraint:
            self.ps.append(out)
            return True
        return False
    def run(self):
        print('Running for ',self.pair)
        end_flag = False
        while not end_flag:
            xmin,xmax, tolflag = self.get_bounds()
            #print(xmin,xmax)
            #print(self.p,self.e,self.emax)
            if xmin <= xmax:

                for x in range(xmin,xmax+1):
                    self.e[0] = x
                    out = self.calculate()
                    #print(self.p,self.e,out)
                    self.check_out(out)

            end_flag=self.carry(tolflag)


        print('Found' ,self.ps)
        return self.ps

class LucasPrime(BasePrime):
    def __init__(self, prime_limit = 100, overwrite = True):
        super().__init__('lucas', prime_limit, overwrite)
        self.comb_counter = 1
        # if overwrite:
        #     self.db_conn.execute(q.OVERWRITE_LUCAS_TABLE)
        #     self.db_conn.commit()
        # self.db_conn.execute(q.CREATE_LUCAS_TABLE)
        # self.db_conn.execute(q.CREATE_LUCAS_TABLE_INITIAL)
        # self.db_conn.commit()
    def comb_list(self):
      #print("Finding Combinations")
      self.comb_counter+=1
      primes=[row[0] for row in self.get_n_small_prime(self.comb_counter)]

      comblist =[ v for l in [list(it.combinations(primes,r))
                for r in range(1,self.comb_counter)]
                for v in l]

      calclist = [PrimePair((comblist[r],comblist[::-1][r]),self.db_conn) for r in range(0,int(len(comblist)/2))]
      #print('calclist')
      #[print(x.pair) for x in calclist]
      return calclist

    def find_primes(self):
      #print("Finding Primes")
      pair_list = self.comb_list()
      ps = []
      for pair in pair_list:
          ps+=pair.run()
      return ps
