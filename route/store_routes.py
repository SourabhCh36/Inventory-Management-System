#STORES

from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,StoreList
from flask import Flask, redirect,render_template,request,url_for,flash



@app.route('/stores')
@role_required(['admin','store_user'])
def stores():
    stores= StoreList.query.all()
    return render_template('stores/list.html', stores=stores)

@app.route('/stores/add',methods=['GET','POST'])
@role_required(['admin','store_user'])
def add_store():
    if request.method=='POST':
        stores=StoreList(
            store_id=request.form['store_id'],
            store_name=request.form['store_name'],
            location=request.form['location'],
            store_head=request.form['store_head'],
            
        )
        db.session.add(stores)
        db.session.commit()
        flash('Store added successfully','success')
        return redirect(url_for('stores'))
    return render_template('stores/add.html')

@app.route('/stores/edit/<int:store_id>', methods=['GET', 'POST'])
@role_required(['admin','store_user'])
def edit_store(store_id):
    store = StoreList.query.get_or_404(store_id)
    if request.method == 'POST':
        store.store_name = request.form['store_name']
        store.location=request.form['location'],
        store.store_head=request.form['store_head'],
        
        
        db.session.commit()
        flash('Store updated successfully!', 'success')
        return redirect(url_for('stores'))
    return render_template('stores/edit.html', store=store)

@app.route('/stores/delete/<int:store_id>')
@role_required(['admin','store_user'])
def delete_store(store_id):
    store = StoreList.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    flash('Store deleted successfully!', 'success')
    return redirect(url_for('stores'))