#VENDORS

from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,VendorList
from flask import Flask, redirect,render_template,request,url_for,flash


@app.route('/vendors')
@role_required(['admin','vendor_user'])
def vendors():
    vendors=VendorList.query.all()
    return render_template('vendors/list.html', vendors=vendors)

@app.route('/vendors/add',methods=['GET','POST'])
@role_required(['admin', 'vendor_user'])
def add_vendor():
    if request.method == 'POST':
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        pan_number = request.form['PAN_Number']
        mobile_number = request.form['mobile_number']
        email = request.form['email']
        address = request.form.get('address', '')

        
        existing_pan = VendorList.query.filter_by(PAN_Number=pan_number).first()
        if existing_pan:
            flash("PAN number already exists. Please use a different number.", "danger")
            return redirect(url_for('add_vendor'))

        
        existing_email = VendorList.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for('add_vendor'))

       
        vendor = VendorList(
            vendor_id=vendor_id,
            vendor_name=vendor_name,
            PAN_Number=pan_number,
            mobile_number=mobile_number,
            email=email,
            address=address
        )

        try:
            db.session.add(vendor)
            db.session.commit()
            flash('Vendor added successfully!', 'success')
            return redirect(url_for('vendors'))
        except Exception as e:
            db.session.rollback()
            flash('Error while adding vendor: ' + str(e), 'danger')
            return redirect(url_for('add_vendor'))

    return render_template('vendors/add.html')


@app.route('/vendors/edit/<int:vendor_id>', methods=['GET', 'POST'])
@role_required(['admin','vendor_user'])
def edit_vendor(vendor_id):
    vendor = VendorList.query.get_or_404(vendor_id)
    if request.method == 'POST':
        vendor.vendor_name = request.form['vendor_name']
        vendor.PAN_Number = request.form['PAN_Number']
        vendor.mobile_number = request.form['mobile_number']
        vendor.email = request.form['email']
        vendor.address = request.form.get('address', '')

        db.session.commit()
        flash('Vendor updated successfully!', 'success')
        return redirect(url_for('vendors'))
    
    
    return render_template('vendors/edit.html', vendor=vendor)

@app.route('/vendors/delete/<int:vendor_id>')
@role_required(['admin','vendor_user'])
def delete_vendor(vendor_id):
    vendor = VendorList.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    flash('Vendor deleted successfully!', 'success')
    return redirect(url_for('vendors'))