#STOCK
from app import app
from auth_routes import role_required
from extension import db
from model import MaterialList,StockList,StoreList
from flask import Flask, redirect,render_template,request,url_for,flash


@app.route('/stock')
@role_required(['admin', 'stock_user'])
def stocks():
    stocks = StockList.query.all()
    return render_template('stock/list.html', stocks=stocks)


@app.route('/stock/add', methods=['GET', 'POST'])
@role_required(['admin', 'stock_user'])
def add_stock():
    if request.method == 'POST':
        stocks = StockList(
            material_id=request.form['material_id'],
            store_id=request.form['store_id'],
            quantity=request.form['quantity'],
            
        )
        db.session.add(stocks)
        db.session.commit()
        flash('Stock added successfully', 'success')
        return redirect(url_for('stocks'))
    
    materials = MaterialList.query.all()
    stores = StoreList.query.all()
    return render_template('stock/add.html', materials=materials, stores=stores)

@app.route('/stock/edit/<int:stock_id>', methods=['GET', 'POST'])
@role_required(['admin', 'stock_user'])
def edit_stock(stock_id):
    stock = StockList.query.get_or_404(stock_id)

    if request.method == 'POST':
        stock.material_id = request.form['material_id']
        stock.store_id = request.form['store_id']
        stock.quantity = request.form['quantity']

        db.session.commit()
        flash('Stock updated successfully', 'success')
        return redirect(url_for('stocks'))

    materials = MaterialList.query.all()
    stores = StoreList.query.all()
    return render_template('stock/edit.html', stock=stock, materials=materials, stores=stores)

@app.route('/stock/delete/<int:stock_id>')
@role_required(['admin', 'stock_user'])
def delete_stock(stock_id):
    stock = StockList.query.get_or_404(stock_id)
    db.session.delete(stock)
    db.session.commit()
    flash('Stock deleted successfully', 'success')
    return redirect(url_for('stocks'))