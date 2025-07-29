#MOVEMENTS
from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,MaterialMovement,StoreList
from flask import Flask, redirect,render_template,request,url_for,flash



@app.route('/movements')
@role_required(['admin','movement_user'])
def movements():
    movements=MaterialMovement.query.all()
    return render_template('movements/list.html',movements=movements)

@app.route('/movements/add',methods=['GET','POST'])
@role_required(['admin','movement_user'])
def add_movement():
    if request.method =='POST':
        movement=MaterialMovement(
            
            material_id=request.form['material_id'],
            movement_type=request.form['movement_type'],
            quantity=request.form['quantity'],
            store_id=request.form.get('store_id') if request.form.get('store_id') else None,
            remarks=request.form.get('remarks', '')
        )
        db.session.add(movement)
        db.session.commit()
        flash('Material movement added succcessfully', 'success')
        return redirect(url_for('movements'))
    
    materials = MaterialList.query.all()
    stores=StoreList.query.all()
    return render_template('movements/add.html',materials=materials,stores=stores)

@app.route('/movements/edit/<int:tansaction_id>', methods=['GET', 'POST'])
@role_required(['admin','movement_user'])
def edit_movement(tansaction_id):
    movement = MaterialMovement.query.filter_by(tansaction_id=tansaction_id).first_or_404()

    if request.method == 'POST':
        movement.material_id = request.form['material_id']
        movement.movement_type = request.form['movement_type']
        movement.quantity = request.form['quantity']
        movement.store_id = request.form['store_id']
        movement.remarks = request.form.get('remarks', '')

        db.session.commit()
        flash('Material movement updated successfully!', 'success')
        return redirect(url_for('movements'))
    
    materials = MaterialList.query.all()
    stores = StoreList.query.all()
    return render_template('movements/edit.html', movement=movement, materials=materials, stores=stores)

@app.route('/movements/delete/<int:tansaction_id>')
@role_required(['admin','movement_user'])
def delete_movement(tansaction_id):
    movement = MaterialMovement.query.filter_by(tansaction_id=tansaction_id).first_or_404()

    db.session.delete(movement)
    db.session.commit()
    flash('Material movement deleted successfully!', 'success')
    return redirect(url_for('movements'))