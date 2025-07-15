from flask import Flask, render_template, request,redirect, url_for,jsonify,flash, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from contextlib import contextmanager
from db_config import get_connection


app=Flask(__name__)
app.config['SECRET_KEY'] ='mera_secret_key1234'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Sourabh123@localhost:3306/inventory_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db = SQLAlchemy(app)

# DATABASES 
class MaterialList(db.Model):
    __tablename__= 'material_list'
    material_id= db.Column(db.Integer,primary_key=True, nullable=False, unique=True)
    material_name=db.Column(db.String(100), nullable=False)
    unit_of_measure=db.Column(db.String(50), nullable=False)
    quantity=db.Column(db.Integer, nullable=False, default=0)
    price_per_unit=db.Column(db.Float, nullable=False, default=0.0)
    description=db.Column(db.Text, nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)
   
class User(db.Model):
    __tablename__= 'users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), nullable=False, unique=True)
    role = db.Column(db.String(50), nullable=False)
    password_hash=db.Column(db.String(256), nullable=False)
    email=db.Column(db.String(100), nullable=False, unique=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)

class VendorList(db.Model):
    __tablename__= 'vendor_list'
    vendor_id=db.Column(db.Integer,primary_key=True)
    vendor_name=db.Column(db.String(100), nullable=False)
    PAN_Number=db.Column(db.String(50), nullable=False, unique=True)
    mobile_number=db.Column(db.String(15), nullable=False, unique=True)
    email=db.Column(db.String(100), nullable=False, unique=True)
    address=db.Column(db.Text, nullable=True)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)

class PurchaseOrder(db.Model):
    __tablename__='purchase_orders' 
    order_id=db.Column(db.Integer, primary_key=True)
    material_id=db.Column(db.Integer, db.ForeignKey('material_list.material_id'), nullable=False)
    vendor_id=db.Column(db.Integer,db.ForeignKey('vendor_list.vendor_id'), nullable=False)
    order_date=db.Column(db.DateTime, default=datetime.utcnow)
    quantity=db.Column(db.Integer, nullable=False)
    total_price=db.Column(db.Float)

class Issue_Material(db.Model):
    __tablename__= 'issue_materials'
    issue_id=db.Column(db.Integer, primary_key=True)
    material_id=db.Column(db.Integer, db.ForeignKey('material_list.material_id'), nullable=False)
    issued_to=db.Column(db.String(100), nullable=False)
    issue_date=db.Column(db.DateTime, default=datetime.utcnow)
    quantity=db.Column(db.Integer, nullable=False)
    remarks=db.Column(db.Text, nullable=True)    

class MaterialMovement(db.Model):
    __tablename__= 'material_movements'
    tansaction_id=db.Column(db.Integer, primary_key=True)
    material_id=db.Column(db.Integer, db.ForeignKey('material_list.material_id'), nullable=False)
    movement_type=db.Column(db.String(50), nullable=False)  
    quantity=db.Column(db.Integer, nullable=False)
    store_id=db.Column(db.Integer, nullable=False)
    transaction_date=db.Column(db.DateTime, default=datetime.utcnow)
    remarks=db.Column(db.Text, nullable=True)

class StoreList(db.Model):
    __tablename__= 'stores'
    store_id=db.Column(db.Integer, primary_key=True)
    store_name=db.Column(db.String(100), nullable=False, unique=True)
    location=db.Column(db.String(200), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, onupdate=datetime.utcnow)    

class StockList(db.Model):
    __tablename__= 'stock_list'
    stock_id=db.Column(db.Integer, primary_key=True)
    material_id=db.Column(db.Integer, db.ForeignKey('material_list.material_id'), nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    quantity=db.Column(db.Integer, nullable=False, default=0)
    last_updated=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Role-based access control
def role_required(roles):
    def decorator(f):
        @wraps(f)
        def decorated_fuction(*args,**kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if user.role not in roles and user.role !='admin':
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args,**kwargs)
        return decorated_fuction
    return decorator

#Routes
@app.route('/')
def index():
    return redirect(url_for('login'))

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

#MARETIAL
@app.route('/materials')
@role_required(['admin','material_user'])
def materials():
    materials=MaterialList.query.all()
    return render_template('materials.html',materials=materials)

@app.route('/materials/add',methods=['GET', 'POST'])
@role_required(['admin', 'material_user'])
def material_add():
    if request.method == 'POST':
        material_id = request.form['material_id']
        material_name = request.form['material_name']
        unit_of_measure = request.form['unit_of_measure']
        quantity = request.form['quantity']
        price_per_unit = request.form['price_per_unit']
        description = request.form.get('description', '')

        new_material = MaterialList(
            material_id=material_id,
            material_name=material_name,
            unit_of_measure=unit_of_measure,
            quantity=quantity,
            price_per_unit=price_per_unit,
            description=description
        )
        db.session.add(new_material)
        db.session.commit()
        flash('Material added successfully!', 'success')
        return redirect(url_for('materials'))
    
    return render_template('materials/add.html')

@app.route('/materials/edit/<int:material_id>', methods=['GET', 'POST'])
@role_required(['admin','material_user'])
def material_edit(material_id):
    material=MaterialList.query.get_or_404(material_id)
    if request.method == 'POST':
        material.material_name=request.form['material_name']
        material.unit_of_measure=request.form['unit_of_measure']
        material.quantiity=request.form['quantity']
        material.price_per_unit=request.form['price_per_unit']
        material.description=request.form.get('description', '')

        db.session.commit()
        flash('Material updated successfully!', 'success')
        return redirect(url_for('materials'))
    return render_template('materials/edit.html', material=material)

@app.route('/materials/delete/<int:material_id>')
@role_required(['admin','material_user'])
def delete_material(material_id):
    material=MaterialList.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Material deleted successfully!', 'success')
    return redirect(url_for('materials'))

#MOVEMENTS
@app.route('/movements')
@role_required(['admin','movement_user'])
def movements():
    movements=MaterialMovement.query.all()
    return render_template('movements/list.html',movements=movements)

@app.route('/movements/add',methods=['GET','POST'])
@role_required(['admin','movement_user'])
def movement_add():
    if request.method =='POST':
        movement=MaterialMovement(
            
            material_id=request.form['material_id'],
            movement_type=request.form['movement_type'],
            quantity=request.form['quantity'],
            store_id=request.form['store_id'] if request.form['form_store'] else None,
            remarks=request.form.get('remarks', '')
        )
        db.session.add(movement)
        db.session.commit()
        flash('Material movement added succcessfully', 'success')
        return redirect(url_for('movements'))
    
    materials = MaterialList.query.all()
    stores=StoreList.query.all()
    return render_template('movements/add.html',materials=materials,stores=stores)

@app.route('/movements/edit/<int:transaction_id>', methods=['GET', 'POST'])
@role_required(['admin','movement_user'])
def movement_edit(transaction_id):
    movement = MaterialMovement.query.get_or_404(transaction_id)
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

@app.route('/movements/delete/<int:transaction_id>')
@role_required(['admin','movement_user'])
def movement_delete(transaction_id):
    movement = MaterialMovement.query.get_or_404(transaction_id)
    db.session.delete(movement)
    db.session.commit()
    flash('Material movement deleted successfully!', 'success')
    return redirect(url_for('movements'))

#PURCSHASE
@app.route('/purchase_orders')
@role_required(['admin','purchase_user'])
def purchase_orders():
    orders=PurchaseOrder.query.all()
    return render_template('purchase_orders/list.html', orders=orders)

@app.route('/purchase_orders/add', methods=['GET', 'POST'])
@role_required(['admin', 'purchase_user'])
def purchase_order_add():
    if request.method == 'POST':
        material_id = request.form['material_id']
        vendor_id = request.form['vendor_id']
        order_date = request.form['order_date']
        quantity = int(request.form['quantity'])  # Convert to int

        # 🔍 Get material to fetch price
        material = MaterialList.query.get(material_id)
        if not material:
            flash('Invalid material selected.', 'danger')
            return redirect(url_for('purchase_order_add'))

        # 🧮 Calculate total price
        total_price = quantity * material.price_per_unit

        po = PurchaseOrder(
            material_id=material_id,
            vendor_id=vendor_id,
            order_date=order_date,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(po)
        db.session.commit()
        flash('Purchase order added successfully!', 'success')
        return redirect(url_for('purchase_orders'))

    materials = MaterialList.query.all()
    vendors = VendorList.query.all()
    return render_template('purchase_orders/add.html', materials=materials, vendors=vendors)

@app.route('/purchase_orders/edit/<int:order_id>', methods=['GET', 'POST'])
@role_required(['admin','purchase_user'])
def purchase_order_edit(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)
    if request.method == 'POST':
        order.material_id = request.form['material_id']
        order.vendor_id = request.form['vendor_id']
        order.order_date = request.form['order_date']
        order.quantity = request.form['quantity']
        order.total_price = request.form['total_price']

        db.session.commit()
        flash('Purchase order updated successfully!', 'success')
        return redirect(url_for('purchase_orders'))
    
    materials = MaterialList.query.all()
    vendors = VendorList.query.all()
    return render_template('purchase_orders/edit.html', order=order, materials=materials, vendors=vendors)

@app.route('/purchase_orders/delete/<int:order_id>')
@role_required(['admin', 'purchase_user'])
def purchase_order_delete(order_id):
    order = PurchaseOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Purchase order deleted successfully!', 'success')
    return redirect(url_for('purchase_orders'))     

#ISSUE INDENTS

@app.route('/Issue_Materials')
@role_required(['admin','indent_user'])
def issue_materials():
    issues = Issue_Material.query.all()
    return render_template('issue_materials/list.html', issues=issues)

@app.route('/issue_materials/add', methods=['GET', 'POST'])
@role_required(['admin','indent_user'])
def issues_add():
    if request.method== 'POST':
        issues= Issue_Material(
            issue_id=request.form['issue_id'],
            material_id=request.form['material_id'],
            issued_to=request.form['issued_to'],
            issue_date=request.form['issue_date'],
            quantity=request.form['quantity'],
            remarks=request.form.get('remarks', '')
        )
        db.session.add(issues)
        db.session.commit()
        flash('Material issued successfully!', 'success')
        return redirect(url_for('issue_materials'))
    materials=MaterialList.query.all()
    return render_template('issue_indent/add.html', materials=materials)

@app.route('/issue_materials/edit/<int:issue_id>', methods=['GET', 'POST'])
@role_required(['admin','indent_user'])
def issue_edit(issue_id):
    issue = Issue_Material.query.get_or_404(issue_id)
    if request.method == 'POST':
        issue.material_id = request.form['material_id']
        issue.issued_to = request.form['issued_to']
        issue.issue_date = request.form['issue_date']
        issue.quantity = request.form['quantity']
        issue.remarks = request.form.get('remarks', '')

        db.session.commit()
        flash('Material issued updated successfully!', 'success')
        return redirect(url_for('issue_materials'))
    
    materials = MaterialList.query.all()
    return render_template('issue_indent/edit.html', issue=issue, materials=materials)

@app.route('/issue_materials/delete/<int:issue_id>')
@role_required(['admin','indent_user'])
def issue_delete(issue_id):
    issue = Issue_Material.query.get_or_404(issue_id)
    db.session.delete(issue)
    db.session.commit()
    flash('Material issued deleted successfully!', 'success')
    return redirect(url_for('issue_materials'))

#VENDORS

@app.route('/vendors')
@role_required(['admin','vendor_user'])
def vendors():
    vendors=VendorList.query.all()
    return render_template('vendors/list.html', vendors=vendors)

@app.route('/vendors/add',methods=['GET','POST'])
@role_required(['admin','vendor_user'])
def vendor_add():
    if request.method=='POST':
        vendor=VendorList(
            vendor_id=request.form['vendor_id'],
            vendor_name=request.form['vendor_name'],
            PAN_Number=request.form['PAN_Number'],
            mobile_number=request.form['mobile_number'],
            email=request.form['email'],
            address=request.form.get('address', '')
        )
        db.session.add(vendor)
        db.session.commit()
        flash('Vendor added sussecfully!', 'success')
        return redirect(url_for('vendors'))
    return render_template('vendors/add.html')

@app.route('/vendors/edit/<int:vendor_id>', methods=['GET', 'POST'])
@role_required(['admin','vendor_user'])
def vendor_edit(vendor_id):
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
def vendor_delete(vendor_id):
    vendor = VendorList.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    flash('Vendor deleted successfully!', 'success')
    return redirect(url_for('vendors'))

#STORES

@app.route('/stores')
@role_required(['admin','store_user'])
def stores():
    stores= StoreList.query.all()
    return render_template('stores/list.html', stores=stores)

@app.route('/stores/add',methods=['GET','POST'])
@role_required(['admin','store_user'])
def store_add():
    if request.method=='POST':
        stores=StoreList(
            store_id=request.form['store_id'],
            store_name=request.form['store_name'],
            location=request.form['location'],
            
        )
        db.session.add(stores)
        db.session.commit()
        flash('Store added successfully','success')
        return redirect(url_for('stores'))
    return render_template('stores/add.html')

@app.route('/stores/edit/<int:store_id>', methods=['GET', 'POST'])
@role_required(['admin','store_user'])
def store_edit(store_id):
    store = StoreList.query.get_or_404(store_id)
    if request.method == 'POST':
        store.store_name = request.form['store_name']
        store.location=request.form['location'],
        store.created_at=request.form['created_at'],
        store.updated_at=request.form['updated_at']
        db.session.commit()
        flash('Store updated successfully!', 'success')
        return redirect(url_for('stores'))
    return render_template('stores/edit.html', store=store)

@app.route('/stores/delete/<int:store_id>')
@role_required(['admin','store_user'])
def store_delete(store_id):
    store = StoreList.query.get_or_404(store_id)
    db.session.delete(store)
    db.session.commit()
    flash('Store deleted successfully!', 'success')
    return redirect(url_for('stores'))

#STOCK 

@app.route('/stock')
@role_required(['admin', 'stock_user'])
def stock():
    stocks = StockList.query.all()
    return render_template('stock/list.html', stocks=stocks)


@app.route('/stock/add', methods=['GET', 'POST'])
@role_required(['admin', 'stock_user'])
def add_stock():
    if request.method == 'POST':
        stock = StockList(
            material_id=request.form['material_id'],
            store_id=request.form['store_id'],
            quantity=request.form['quantity'],
            
        )
        db.session.add(stock)
        db.session.commit()
        flash('Stock added successfully', 'success')
        return redirect(url_for('stock'))
    
    materials = MaterialList.query.all()
    stores = StoreList.query.all()
    return render_template('stock/add.html', materials=materials, stores=stores)

@app.route('/stock/edit/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'stock_user'])
def edit_stock(id):
    stock = StockList.query.get_or_404(id)

    if request.method == 'POST':
        stock.material_id = request.form['material_id']
        stock.store_id = request.form['store_id']
        stock.quantity = request.form['quantity']
        stock.last_updated = datetime.utcnow()  # optional, if not auto-set

        db.session.commit()
        flash('Stock updated successfully', 'success')
        return redirect(url_for('stock'))

    materials = MaterialList.query.all()
    stores = StoreList.query.all()
    return render_template('stock/edit.html', stock=stock, materials=materials, stores=stores)

@app.route('/stock/delete/<int:id>')
@role_required(['admin', 'stock_user'])
def delete_stock(id):
    stock = StockList.query.get_or_404(id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock deleted successfully', 'success')
    return redirect(url_for('stock'))

#USER

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
        user.username = request.form['username']
        role = request.form['role']
        password = request.form['password']

        user.role = role
        if password.strip():  # Only update password if provided
            user.password_hash = generate_password_hash(password)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)