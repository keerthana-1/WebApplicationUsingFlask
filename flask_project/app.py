from flask import Flask,render_template,redirect,url_for,request,flash
from db_setup import Base,Owner,Post
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from flask import session as login_session
from functools import wraps
import os

app=Flask(__name__)
engine=create_engine('sqlite:///mydb.db')
Base.metadata.bind=engine
session=scoped_session(sessionmaker(bind=engine))

def login_required(f):
	@wraps(f)
	def x(*args,**kwargs):
		if 'email' not in login_session:
			return redirect(url_for('login'))
		return f(*args,**kwargs)
	return x

#def hello():
#	return "<h1>Welcome to python</h1>"
#@app.route('/hello/<name>/<rno>')
#def Hello_name(name,rno):
#	return "<h1><center>"+"My name is "+name+"<br>"+"My rollno is "+rno+"</center></h1>"

#@app.route('/add/<int:a>/<int:b>')
#def Hello_name(a,b):
#	return "sum is %d"%(a+b)

#@app.route('/html')
#def html():
#	return render_template('index.html')

#@app.route('/message/<name>')
#def message(name):
#	return render_template('message.html',name=name)

#@app.route('/surname/<sname>/<name>')
#def surname(sname,name):
#	return render_template('surname.html',sname=sname,name=name)

#@app.route('/numbers')
#def numbers():
#	l=range(1,101)
#	return render_template('numbers.html',numbers=l)

#@app.route('/admin/<name>')
#def hello_admin(name):
#	return 'hello %s'%name

#@app.route('/guest/<guest>')
#def guest_name(guest):
#	return "%s is a guest person"%guest

#@app.route('/user/<name>')
#def users(name):
#	if(name=="admin"):
#		return redirect(url_for("hello_admin"))
#	if(name=="guest"):
#		return redirect(url_for("guest_name"))

#@app.route('/table')
#def table():
#	return render_template('table.html')

#@app.route('/leap/<int:y1>/<int:y2>')
#def leap(y1,y2):
#	return render_template('leap.html',y1=y1,y2=y2)

#@app.route('/')
#@app.route('/atoi')
#def atoi():
#	return render_template('atoi.html')

@app.route('/')
@app.route('/home2')
def home():
	posts=session.query(Post).all()
	return render_template('home2.html',posts=posts)

@app.route('/register',methods=["POST","GET"])
def register():
	if request.method=="POST":
		name=request.form['name']
		email=request.form['email']
		password=request.form['password']
		owner=Owner(name=name,email=email,password=password)
		session.add(owner)
		session.commit()
		flash("owner is successfully created",'success')
	return render_template('register.html')

@app.route('/newpost',methods=["POST","GET"])
@login_required
def newpost():
	if request.method=="POST":
		title=request.form['title']
		image=request.form['image']
		owner_id=1
		post=Post(title=title,image=image,owner_id=owner_id)
		session.add(post)
		session.commit()
		flash("successfully posted",'success')
	return render_template('newpost.html')


@app.route('/login', methods=["POST","GET"])
def login():
	if request.method=="POST":
		email=request.form['email']
		password=request.form['password']
		owner=session.query(Owner).filter_by(email=email,password=password).one_or_none()
		if owner==None:
			flash("invalid credentials",'danger')
			return redirect(url_for('login'))
		
		login_session['email']=email
		login_session['name']=owner.name
		flash("welcome"+str(owner.name),'success')
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
	del login_session['email']
	del login_session['name']
	flash("logout success, visit again",'success')
	return redirect(url_for('home'))

@app.route('/post/<int:post_id>/edit',methods=["POST","GET"])
@login_required
def editpost(post_id):
	if request.method=='POST':
		title=request.form['title']
		image=request.form['image']
		post=session.query(Post).filter_by(id=post_id).one_or_none()
		post.title=title
		post.image=image
		session.add(post)
		session.commit()
		return redirect(url_for('home'))
	else:
		post=session.query(Post).filter_by(id=post_id).one_or_none()
		return render_template('update.html',post=post)

@app.route('/post/<int:post_id>/delete')
@login_required
def deletepost(post_id):
	post=session.query(Post).filter_by(id=post_id).one_or_none()
	session.delete(post)
	session.commit()
	flash("post is successfully deleted",'danger')
	return redirect('/')

@app.route('/upload')
@login_required
def fileupload():
	return render_template('fileupload.html')

@app.route('/store',methods=["POST","GET"])
@login_required
def store():
	if request.method=="POST":
		file=request.files['file']
		path=os.getcwd()+'/static/images/'
		file.save(path+file.filename)
		return render_template("success.html",name=file.filename)

#should be written last always 
if __name__ =='__main__':
	app.secret_key="!34835413hvk"
	app.run(debug=True,port=5000,host="localhost")