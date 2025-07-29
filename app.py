from flask import Flask, render_template, request,redirect, url_for,jsonify,flash, session
from extension import db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mera_secret_key1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Sourabh123@localhost:3306/inventory_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
