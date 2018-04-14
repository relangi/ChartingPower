import os,Models
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'powercharting.db')
db = SQLAlchemy(app)

@app.route('/dashboard')
def dashboard():
    #complete_lab_data = []
    #complete_val_data = []
    complete_data = []
    diff_devices = Models.devices.query.limit(10).all()
    for eachdevice in diff_devices:
        lab_val_data = [[str(val.logtime_year)+'/'+str(val.logtime_month)+'/'+str(val.logtime_date),float(val.kwh_ontheday)] for val in Models.daily_summary.query.filter(Models.daily_summary.devices_name == eachdevice.name ).limit(100).all()]
        max_val_set = max([val[1] for val in lab_val_data])
        lab_val_max = [lab_val_data,[max_val_set],[eachdevice.name],[eachdevice.id]]
        #label_data = [lab[0] for lab in lab_val_data]
        #value_data = [val[1] for val in lab_val_data]

        #complete_lab_data = complete_lab_data.append(label_data)
        #complete_val_data = complete_val_data.append(value_data)
        complete_data.append(lab_val_max)

    return render_template('linechart.html',charts = complete_data)

if __name__ == '__main__':
    app.run(debug="True")
