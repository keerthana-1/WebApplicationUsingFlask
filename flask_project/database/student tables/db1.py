import sqlite3
con=sqlite3.connect('vrsec.db')
cur=con.cursor()#query execution
query='create table student(sno text,sname text,branch text,phno integer,email text)'
try:
    cur.execute(query)
except Exception as e:
    print(e)
finally:
    print("***successfully created***")
    
    
