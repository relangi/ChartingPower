import os,Models
from flask import Flask, render_template, url_for, flash,request,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import *

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'powercharting.db')
app.config ['SECRET_KEY'] = 'M\x95KT\x98\x0cz\r\xd9\x03O\xafp \x9e\xb7\xceE\xee\x06\x9b@/e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/dashboard')
def dashboard():

    complete_data = []
    diff_devices = Models.devices.query.limit(10).all()
    for eachdevice in diff_devices:
        lab_val_data = [[str(val.logtime_year)+'/'+str(val.logtime_month)+'/'+str(val.logtime_date),float(val.kwh_ontheday)] for val in Models.daily_summary.query.filter(Models.daily_summary.devices_name == eachdevice.name ).limit(100).all()]
        max_set_len = len([val[1] for val in lab_val_data])
        if max_set_len:
            max_val_set = max([val[1] for val in lab_val_data])
        else:
            max_val_set = 0

        lab_val_max = [lab_val_data,[max_val_set],[eachdevice.name],[eachdevice.id]]

        complete_data.append(lab_val_max)

    return render_template('linechart.html',charts = complete_data)


@app.route('/customreports', methods = ['GET','POST'])
def customreports():
    complete_data = []
    dev_dd_list = [[val.name,val.id] for val in Models.devices.query.all()]
    x_axis = ['Time','PowerWatts','Voltage','Current']
    y_axis = ['SignalStrength','VCC','PowerStatus','PowerWatts','Voltage','Current','Factor','GradualKWH']
    attr_mapping = {'PowerWatts' : 'power', 'GradualKWH' : 'kwh_sofar_today','Voltage' : 'voltage', 'Current' : 'current', 'Factor' : 'factor','PowerStatus':'power_status', 'SignalStrength':'wifi_strength'}
    if request.method == 'POST':
        x = request.form['x_value']
        y = request.form['y_value']
        dev = request.form['device_value']

        if (validate_combination(x,y)[0]):
            table_val = validate_combination(x,y)[1]
            if (table_val == 'dsr'):
                lab_val_data = [[str(val.logtime_month)+'/'+str(val.logtime_date)+' '+str(val.logtime_hour)+':'+str(val.logtime_minute)+':'+str(val.logtime_second), float(getattr(val,str(attr_mapping[y]))) ] for val in Models.device_state.query.filter(Models.device_state.devices_id == dev ).limit(100).all()]
            else:
                if (x == 'Time'):
                    lab_val_data = [[str(val.logtime_month)+'/'+str(val.logtime_date)+' '+str(val.logtime_hour)+':'+str(val.logtime_minute)+':'+str(val.logtime_second), getattr(val,str(attr_mapping[y])) ] for val in Models.energy_state.query.filter(Models.energy_state.devices_id == dev ).limit(100).all()]
                else:
                    lab_val_data = [[ getattr(val,str(attr_mapping[x])) , getattr(val,str(attr_mapping[y])) ] for val in Models.energy_state.query.filter(Models.energy_state.devices_id == dev ).limit(100).all()]

            max_set_len = len([val[1] for val in lab_val_data])
            if max_set_len:
                max_val_set = max([val[1] for val in lab_val_data])
            else:
                max_val_set = 0
            devobj = Models.devices.query.filter(Models.devices.id == str(dev)).first()
            #app.logger.debug (dev)
            #app.logger.debug (type(devobj))
            lab_val_max = [lab_val_data,[max_val_set],[devobj.name],[devobj.id]]

            complete_data.append(lab_val_max)

            return render_template('customreports.html',charts = complete_data,x=x,y=y,x_axis=x_axis,y_axis=y_axis,dev_dd_list=dev_dd_list)
        else:
            flash('This is not a valid combination to generate Report')

    return render_template('customreports.html',x_axis=x_axis,y_axis=y_axis,dev_dd_list=dev_dd_list)

@app.route('/addnewdevices', methods =['GET','POST'])
def addnewdevices():
    nd_form = NewDevice()
    if nd_form.validate_on_submit():
        newdevice = Models.devices(name=nd_form.name.data,sonoff_ip=nd_form.sonoff_ip.data,sonoff_mac=nd_form.sonoff_mac.data)
        db.session.add(newdevice)
        db.session.commit()
        flash('New Device with name {} added'.format(newdevice.name))
        return redirect(url_for('dashboard'))

    return render_template('addnewdevices.html',form=nd_form)


@app.route('/healthstatus')
def healthstatus():
    hs_obj = open(os.path.join(basedir,'healthstatus.txt'),'r')
    hs_obj.seek(0)
    msg_data = hs_obj.readlines()
    hs_obj.close()
    return render_template('healthstatus.html',msg = msg_data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'),404


def validate_combination(x,y):
    vc0 = ['PowerWatts',['Factor','Voltage','Current'],'esr']
    vc1 = ['Voltage',['Current','PowerWatts'],'esr']
    vc2 = ['Current',['Voltage','PowerWatts'],'esr']
    vc3 = ['Time',['SignalStrength','VCC','PowerStatus'],'dsr']
    vc4 = ['Time',['PowerWatts', 'Factor','Voltage','Current','GradualKWH'],'esr']
    vc = [vc0,vc1,vc2,vc3,vc4]

    for eachcombi in vc:
        if eachcombi[0] == str(x):
            for eachy in eachcombi[1]:
                if eachy == str(y):
                    return [True,eachcombi[2]]
    return [False,'']

if __name__ == '__main__':
    app.run(debug="False")
