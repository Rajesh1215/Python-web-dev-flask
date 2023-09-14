from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import os
from werkzeug.utils import secure_filename

import datetime








app = Flask(__name__)
#key 
app.secret_key = 'qwertyuixcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:5000/topics'
app.config['UPLOAD_FOLDER']='C:\\Users\\kingr\\OneDrive\\Documents\\html\\blog\\new\\blog_post\\static'


db=SQLAlchemy(app)
key = Fernet.generate_key()
fernet = Fernet(key)

class Users(db.Model):
    email=db.Column(db.String(100),primary_key=True,nullable=False)
    fl=db.Column(db.String(30),nullable=False)
    ln=db.Column(db.String(30),nullable=False)
    ph=db.Column(db.Integer,nullable=False)
    adrs=db.Column(db.String(500),nullable=False)
    ps=db.Column(db.String(100),nullable=False)


class Blogs(db.Model):
    s_no = db.Column(db.Integer, nullable = False, primary_key = True,autoincrement=True)
    title = db.Column(db.String(20), nullable = False)
    img1 = db.Column(db.String(30), nullable = False)
    img2 = db.Column(db.String(30), nullable = False)
    img1sub =db.Column(db.String(50), nullable = False)
    img2sub=  db.Column(db.String(50), nullable = False)
    author_name = db.Column(db.String(30), nullable = False)
    content = db.Column(db.String(300), nullable = False)
    email=db.Column(db.String(100),nullable=False)
    genre=db.Column(db.String(30),nullable=False)
    dt = db.Column(db.DateTime, nullable = False)

with app.app_context():
    db.create_all()


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home/<email>')
def home(email):
  if session['username'] == email :
    blog=Blogs.query.filter_by(email=email)
    return render_template('home.html',email=email,blog=blog)
  else:
        return redirect(url_for('login'))

@app.route('/create/<email>')
def create(email):
    if session['username'] == email :
        return render_template('create.html',email=email)
    else:
        return redirect(url_for('login'))
@app.route('/about/<email>')
def about(email):
    if session['username'] == email :
        dtl=Users.query.filter_by(email = email).first()
        return render_template('about.html',dtl=dtl,email=email)
    else:
        return redirect(url_for('login'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/content/<v>')
def content(v):
    d=Blogs.query.filter_by(s_no = v).first()
    return render_template("content.html",d=d,email=session['username'])


@app.route('/logout')
def logout():
    session['username']=None
    return redirect(url_for('login'))

@app.route('/log',methods=['GET','POST'])
def log():
    if request.method=='POST' :
        usn=request.form.get('Username')
        ps=request.form.get("password")
        chk=Users.query.filter_by(email = usn).first()
        if (chk is None):
            return redirect(url_for('login'))
        else:
            if (chk.ps ==ps ):
                session['username']=chk.email
                return redirect(url_for('home',email=chk.email))
            else:
                return redirect(url_for('login'))
    return redirect(url_for('login'))


@app.route("/ac_cr",methods=['GET','POST'])
def ac_cr():
    if request.method=='POST' :
        em=request.form.get('em')
        fl=request.form.get('fl')
        ln=request.form.get('ln')
        ph=request.form.get('ph')
        adrs=request.form.get('adrs')
        ps=request.form.get('password')
        rps=request.form.get('repassword')

        if ps==rps :
            U=Users(email=em,fl=fl,ln=ln,ph=ph,adrs=adrs,ps=ps)
            db.session.add(U)
            db.session.commit()
            session['username'] = em
            return redirect(url_for('home',email=em))
        else:
            flash('Error: Please fill out all required fields with matching passwords')
            return redirect(url_for('signup'))
        

@app.route('/crecon', methods=['GET','POST'])
def crecon():
    if request.method=='POST' :
        auth_n=request.form.get('auth_name')
        title=request.form.get('title')
        cont=request.form.get('Content')
        genre=request.form.get('Genre')
        imgsub1=request.form.get('imgsub1')
        imgsub2=request.form.get('imgsub2')
        img1=request.files['img1']
        img2=request.files['img2']
        current_time = datetime.datetime.now()
        ft = current_time.strftime('%Y-%m-%d')
        B=Blogs(genre=genre,email=session['username'],content=cont,author_name=auth_n,dt=ft,img2sub=imgsub2,img1sub=imgsub1,img2=img2.filename,img1=img1.filename,title=title)
        db.session.add(B)
        db.session.commit()
        img1.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(img1.filename)))
        img2.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(img2.filename)))
        return redirect(url_for('create',email=session['username']))
        

@app.route('/change', methods=['GET','POST'])
def change():
    if request.method=='POST' :
        chn=Users.query.filter_by(email =session['username']).first()
        fl=request.form.get('fl')
        ln=request.form.get('ln')
        ph=request.form.get('ph')
        adrs=request.form.get('adrs')
        ps=request.form.get('password')
        rps=request.form.get('repassword')
        

        if ps==rps :
            chn.fl=fl
            chn.ln=ln
            chn.ph=ph
            chn.adrs=adrs
            chn.ps=ps
            db.session.commit()

            
            return redirect(url_for('about',email=session['username']))
        
        else:
            flash('Error: passwords not matched')
            return redirect(url_for('about',email=session['username']))



if __name__ == "__main__":
    app.run(debug=True)


