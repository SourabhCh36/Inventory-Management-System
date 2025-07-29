from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList
from flask import Flask, redirect,render_template,request,url_for,flash



@app.route('/materials')
@role_required(['admin','material_user'])
def materials():
    materials=MaterialList.query.filter_by(is_active=True).all()
    return render_template('materials/list.html',materials=materials)

@app.route('/materials/add',methods=['GET', 'POST'])
@role_required(['admin', 'material_user'])
def add_material():
    if request.method == 'POST':
        material_id = request.form['material_id']
        material_name = request.form['material_name']
        unit_of_measure = request.form['unit_of_measure']
        quantity = request.form['quantity']
        price_per_unit = request.form['price_per_unit']
        category=request.form['category']
        description = request.form.get('description', '')
        
        new_material = MaterialList(
            material_id=material_id,
            material_name=material_name,
            unit_of_measure=unit_of_measure,
            quantity=quantity,
            price_per_unit=price_per_unit,
            category=category,
            description=description
        )

        if not material_id:
            flash("Material ID is required.", "danger")
            return redirect(url_for('add_material'))
        
        try:
            material_id = int(material_id)
        except ValueError:
            flash("Material ID must be an integer.", "danger")
            return redirect(url_for('add_material'))

        try:
            price_per_unit = float(price_per_unit)
        except ValueError:
            flash("Price per unit should be a decimal number.", "danger")
            return redirect(url_for('add_material'))
        
        existing = MaterialList.query.get(material_id)
        if existing:
            flash("Material ID already exists. Please use a different ID.", "danger")
            return redirect(url_for('add_material'))

        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully!', 'success')
        return redirect(url_for('materials'))
    
    return render_template('materials/add.html')

@app.route('/materials/edit/<int:material_id>', methods=['GET', 'POST'])
@role_required(['admin','material_user'])
def edit_material(material_id):
    material=MaterialList.query.get_or_404(material_id)
    if request.method == 'POST':
        material.material_name=request.form['material_name']
        material.unit_of_measure=request.form['unit_of_measure']
        material.quantiity=request.form['quantity']
        material.price_per_unit=request.form['price_per_unit']
        material.category=request.form['category']
        material.description=request.form.get('description', '')

        db.session.commit()
        flash('Material updated successfully!', 'success')
        return redirect(url_for('materials'))
    return render_template('materials/edit.html', material=material)

@app.route('/materials/delete/<int:material_id>')
@role_required(['admin','material_user'])
def delete_material(material_id):
    material=MaterialList.query.get_or_404(material_id)
    material.is_active = False  # Soft delete
    db.session.commit()
    flash('Material deleted successfully!', 'success')
    return redirect(url_for('materials'))
