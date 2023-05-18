import sqlite3
con=sqlite3.connect('vrsec.db')
cur=con.cursor()#query execution
query='insert into student values("178w1a1201","keerthana","it",7780464328,"keerthi@gmail.com")'
try:
    cur.execute(query)
    con.commit()
except Exception as e:
    print(e)
finally:
    print("***successfully inserted***")
    
    
