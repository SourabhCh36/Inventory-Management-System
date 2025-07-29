from flask import redirect,url_for,render_template,request,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from app import app
from auth_routes import role_required
from extension import db
from model import User


    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password= request.form['password']
        user=User.query.filter_by(username=username).first()
        if user and check_password_hash (user.password_hash, password):
            session['user_id'] = user.id
            session['username']=user.username
            session['role']= user.role
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid usesrname or password.', 'error')
    return render_template('login.html')

@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method =='POST':
        username= request.form['username']
        password =request.form['password']
        role=request.form['role']
        email=request.form['email']

        if User.query.filter_by(username=username).first():
            flash('Username already exists.','danger')
            return redirect(url_for('register'))
        else:
            new_user=User(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
                email=email
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@role_required(['admin','material_user','movement_user','purchase_user','indent_user','store_user','stock_user'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
