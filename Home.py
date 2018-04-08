import os
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'powercharting.db')
db = SQLAlchemy(app)

@app.route('/dashboard')
def dashboard():
    return ('dashboard.html')

if __name__ == '__main__':
    app.run()
