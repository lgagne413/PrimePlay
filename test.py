import sqlite3
con = sqlite3.connect('data/primeplay.db')
m=con.execute('select max(number) from intfactors').fetchall()[0][0]
for x in con.execute('select * from intfactors where  number >?-100 order by number asc',[m]).fetchall():
    print(x)
con.close()