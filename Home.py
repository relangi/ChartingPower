import os,Models
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'powercharting.db')
db = SQLAlchemy(app)

@app.route('/dashboard')
def dashboard():
    labels_data = [str(val.logtime_year)+'/'+str(val.logtime_month)+'/'+str(val.logtime_date) for val in Models.daily_summary.query.limit(100).all()]
    values_data = [float(val.kwh_ontheday) for val in Models.daily_summary.query.limit(100).all()]
    return render_template('linechart.html',title='Last 100 days of Power usage',labels=labels_data, values=values_data,max=10)

if __name__ == '__main__':
    app.run()
