#USER

from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,User
from flask import Flask, redirect,render_template,request,url_for,flash,session
from werkzeug.security import generate_password_hash

@app.route('/users')
@role_required(['admin'])
def users():
    users = User.query.all()
    return render_template('users/list.html', users=users)

@app.route('/users/add', methods=['GET', 'POST'])
@role_required(['admin'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Choose another.', 'danger')
            return redirect(url_for('add_user'))

        # Create new user
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash('User added successfully', 'success')
        return redirect(url_for('users'))
    
    return render_template('users/add.html')

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@role_required(['admin'])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
       
        role = request.form['role']
        

        user.role = role
        

        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('users'))

    return render_template('users/edit.html', user=user)

@app.route('/users/delete/<int:id>')
@role_required(['admin'])
def delete_user(id):
    user = User.query.get_or_404(id)

    # Optional: Prevent deleting own account
    if user.id == session.get('user_id'):
        flash("You can't delete your own account while logged in.", 'danger')
        return redirect(url_for('users'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('users'))