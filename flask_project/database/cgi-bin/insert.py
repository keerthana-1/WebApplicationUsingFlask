import sqlite3,cgi

print("Content-Type:text/html \r\n\r\n")
form=cgi.FieldStorage()
a=form.getvalue('rollno')
b=form.getvalue('name')
c=form.getvalue('branch')
d=form.getvalue('phno')
f=form.getvalue('mail')
con=sqlite3.connect('mydb.db')
cur=con.cursor()
query='insert into student values("'+str(a)+'","'+str(b)+'","'+str(c)+'","'+str(d)+'","'+str(f)+'")'
try:
	cur.execute(query)
	con.commit()
except Exception as e:
	print(e)
finally:
	print("**successfully inserted**")
