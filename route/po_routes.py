from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList, PurchaseOrder, VendorList
from flask import redirect, render_template, request, url_for, flash


# 🧾 View all purchase orders
@app.route('/purchase_orders')
@role_required(['admin', 'purchase_user'])
def purchase_orders():
    orders = PurchaseOrder.query.all()
    return render_template('purchase_orders/list.html', orders=orders)


# ➕ Add a new purchase order
@app.route('/purchase_orders/add', methods=['GET', 'POST'])
@role_required(['admin', 'purchase_user'])
def add_purchase_order():
    if request.method == 'POST':
        try:
            material_id = int(request.form['material_id'])
            vendor_id = int(request.form['vendor_id'])
            order_date = request.form.get('order_date')
            quantity = int(request.form['quantity'])

            if quantity <= 0:
                flash("Quantity must be greater than zero.", "danger")
                return redirect(url_for('add_purchase_order'))

            material = MaterialList.query.get(material_id)
            if not material:
                flash("Material not found.", "danger")
                return redirect(url_for('add_purchase_order'))
            
            if quantity > material.quantity:
                flash("Insufficient material quantity available.", "danger")
                return redirect(url_for('add_purchase_order'))

            total_price = quantity * material.price_per_unit

            po = PurchaseOrder(
                material_id=material_id,
                vendor_id=vendor_id,
                quantity=quantity,
                total_price=total_price
            )
            db.session.add(po)
            db.session.commit()
            flash('Purchase order added successfully!', 'success')
            return redirect(url_for('purchase_orders'))

        except ValueError:
            flash("Invalid input. Please check your form fields.", "danger")
            return redirect(url_for('add_purchase_order'))

    materials = MaterialList.query.all()
    vendors = VendorList.query.all()
    return render_template('purchase_orders/add.html', materials=materials, vendors=vendors)


# ✏️ Edit a purchase order
@app.route('/purchase_orders/edit/<int:order_id>', methods=['GET', 'POST'])
@role_required(['admin', 'purchase_user'])
def edit_purchase_order(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)

    if request.method == 'POST':
        try:
            order.material_id = int(request.form['material_id'])
            order.vendor_id = int(request.form['vendor_id'])
            order.quantity = int(request.form['quantity'])

            if order.quantity <= 0:
                flash("Quantity must be greater than zero.", "danger")
                return redirect(url_for('edit_purchase_order', order_id=order_id))
            
            

            material = MaterialList.query.get(order.material_id)
            if not material:
                flash("Material not found.", "danger")
                return redirect(url_for('edit_purchase_order', order_id=order_id))
 
            if order.quantity > material.quantity:
                flash("Insufficient material quantity available.", "danger")
                return redirect(url_for('edit_purchase_order', order_id=order_id))
            
            order.total_price = order.quantity * material.price_per_unit
            db.session.commit()
            flash('Purchase order updated successfully!', 'success')
            return redirect(url_for('purchase_orders'))

        except ValueError:
            flash("Invalid input. Please check your form fields.", "danger")
            return redirect(url_for('edit_purchase_order', order_id=order_id))

    materials = MaterialList.query.all()
    vendors = VendorList.query.all()
    return render_template('purchase_orders/edit.html', order=order, materials=materials, vendors=vendors)


@app.route('/purchase_orders/delete/<int:order_id>')
@role_required(['admin', 'purchase_user'])
def delete_purchase_order(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Purchase order deleted successfully!', 'success')
    return redirect(url_for('purchase_orders'))
