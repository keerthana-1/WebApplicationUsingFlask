import sqlite3
con=sqlite3.connect('vrsec.db')
cur=con.cursor()#query execution
query="select * from student"
try:
    cur.execute(query)
    con.commit()
    for i in cur:
        for j in i:
            print(j)
except Exception as e:
    print(e)

    
    
