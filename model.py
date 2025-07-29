from extension import db
from datetime import datetime

# DATABASES 
class MaterialList(db.Model):
    __tablename__= 'material_list'
    material_id= db.Column(db.Integer,primary_key=True, nullable=False, unique=True)
    material_name=db.Column(db.String(100), nullable=False)
    unit_of_measure=db.Column(db.String(50), nullable=False)
    quantity=db.Column(db.Integer, nullable=False, default=0)
    price_per_unit=db.Column(db.Float, nullable=False, default=0.0)
    description=db.Column(db.Text, nullable=True)
    category=db.Column(db.String(200),nullable=False)
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
    store_head=db.Column(db.String(200), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    

class StockList(db.Model):
    __tablename__= 'stock_list'
    stock_id=db.Column(db.Integer, primary_key=True)
    material_id=db.Column(db.Integer, db.ForeignKey('material_list.material_id'), nullable=False)
    store_id=db.Column(db.Integer, db.ForeignKey('stores.store_id'), nullable=False)
    quantity=db.Column(db.Integer, nullable=False, default=0)
    last_updated=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
