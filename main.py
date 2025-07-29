from flask import redirect,url_for
from app import app,db
import dashboard
from route.__init__ import *

@app.route('/')
def index():
    return redirect(url_for('login'))
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)