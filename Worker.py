from Models import *
from time import strptime,localtime
from datetime import datetime
import os,re

#Defining Functions
def return_deviceobj(devices_sonoff_ip):
    device = devices.query.filter_by(sonoff_ip=devices_sonoff_ip).all()[0]
    return device

def return_timearray(timestring):
    return (strptime(timestring, "%Y-%m-%dT%H:%M:%S")[0:6])

def update_sterday_kwh_dailysummary(kwh,devicename,timestring):
    time_array = return_timearray(timestring)
    daily_summary_record = daily_summary.query.filter(daily_summary.devices_name == devicename).filter(daily_summary.logtime_year == time_array[0]).filter(daily_summary.logtime_month == time_array[1]).filter(daily_summary.logtime_date == time_array[2]-1).all()

    if (len(daily_summary_record)):
        if (daily_summary_record[0].kwh_ontheday == kwh):
            pass
        else:
            daily_summary_record[0].kwh_ontheday = kwh
            db.session.commit()
    else:
        daily_summary_log = daily_summary(logtime_year=int(time_array[0]),logtime_month=int(time_array[1]),logtime_date=int(time_array[2]-1),devices_id=dsr_device.id,devices_name=dsr_device.name,devices_sonoff_ip=dsr_device.sonoff_ip,devices_sonoff_mac=dsr_device.sonoff_mac,kwh_ontheday=float(kwh))
        db.session.add(daily_summary_log)
        db.session.commit()

#Defining Log file paths
basedir = os.path.abspath(os.path.dirname(__file__))
input_logfile_path = os.path.join(basedir,'vjacsyslog.txt')
linestate_logfile_path = os.path.join(basedir,'linestate.txt')
worker_logfile_path = os.path.join(basedir,'worker_log.txt')
health_status_file_path = os.path.join(basedir,'healthstatus.txt')
DB_path = os.path.join(basedir,'powercharting.db')

#Opening files
linestate = open(linestate_logfile_path,'r+')
input_logfile = open(input_logfile_path,'r')
worker_logfile = open(worker_logfile_path,'a')
health_status = open(health_status_file_path,'w')

#initializing log file
worker_logfile.write('='*50+"\n")
worker_logfile.write(datetime.isoformat(datetime.now())+"\n")
worker_logfile.write('='*50+"\n")

health_status.write('-'*50+"\n")
health_status.write(datetime.isoformat(datetime.now())+"\n")
health_status.write('-'*50+"\n")
health_status.write('Worker Status: \n')


#Defining regular expressions to parse log files
device_state_parser = re.compile('[\w\s\:\,]+\|\/(\d+\.\d+\.\d+\.\d+)\|[\w\-\s]+\:\stele\/sonoffP2\/STATE\s\=\s\{\"Time\"\:\"([\w\-\:]+)\"\,\s\"Uptime\"\:([\d\.]+)\,\s\"Vcc\"\:([\d\.]+)\,\s"POWER\"\:\"(\w+)\"\,\s\"Wifi\"\:\{\"AP\"\:\d+\,\s\"SSID\"\:\"(\w+)\"\,\s\"RSSI\"\:([\d\.]+)\,\s\"APMac\"\:\"([\w\:]+)\"\}\}')
energy_state_parser = re.compile('[\w\s\:\,]+\|\/(\d+\.\d+\.\d+\.\d+)\|[\w\-\s]+\:\stele\/sonoffP2\/ENERGY\s\=\s\{\"Time\"\:\"([\w\-\:]+)\"\,\s\"Total\"\:[\d\.]+\,\s\"Yesterday\"\:([\d\.]+)\,\s\"Today\"\:([\d\.]+)\,\s\"Period\"\:(\d+)\,\s\"Power\"\:([\d\.]+)\,\s\"Factor\"\:([\d\.]+)\,\s\"Voltage\"\:([\d\.]+)\,\s\"Current\"\:([\d\.]+)\}')

#Reading the value of number of lines parsed last time & seeking to starting of file
linestate_value = int(linestate.readline())
linestate.seek(0)
worker_logfile.write("linestate read as "+ str(linestate_value)+"\n")

#Reading the actual Log update
input_buffer = input_logfile.readlines()

if linestate_value == len(input_buffer):
    print ("No new Log messages")
    worker_logfile.write("No new Log messages found in the latest worker process attempt\n")
    health_status.write("No new Log messages found in the latest worker process attempt\n")
elif linestate_value > len(input_buffer):
    print ("The Input Logfile seems to have changed/overwritten from first. Reset the statefile value to 0 manually")
    worker_logfile.write("The Input Logfile seems to have changed/overwritten from first. Reset the statefile value to 0 manually\n")
    health_status.write("The Input Logfile seems to have changed/overwritten from first. Reset the statefile value to 0 manually\n")
else:
    update_buffer = input_buffer[linestate_value::]
    print("There are "+ str(len(update_buffer))+" lines of new log updates to parse")
    worker_logfile.write("There are "+ str(len(update_buffer))+" lines of new log updates to parse\n")
    health_status.write("There are "+ str(len(update_buffer))+" lines of log updates parsed in last Worker process attempt\n")

    for eachline in update_buffer:
        dsr = device_state_parser.findall(eachline)
        esr = energy_state_parser.findall(eachline)
        if (len(dsr)):
            worker_logfile.write(str(dsr[0])+"\n")
            if (return_deviceobj(dsr[0][0])):
                dsr_device = return_deviceobj(dsr[0][0])
                dsr_year = int(return_timearray(dsr[0][1])[0])
                dsr_month = int(return_timearray(dsr[0][1])[1])
                dsr_date = int(return_timearray(dsr[0][1])[2])
                dsr_hour = int(return_timearray(dsr[0][1])[3])
                dsr_minute = int(return_timearray(dsr[0][1])[4])
                dsr_second = int(return_timearray(dsr[0][1])[5])
                dsr_vcc = float(dsr[0][3])
                dsr_power_status = bool(1 if dsr[0][4]=='ON' else 0)
                dsr_signal_strength = float(dsr[0][6])

                new_device_state_log = device_state(logtime_year=dsr_year,logtime_month=dsr_month,logtime_date=dsr_date,logtime_hour=dsr_hour,logtime_minute=dsr_minute,logtime_second=dsr_second,devices_id=dsr_device.id,devices_name=dsr_device.name,devices_sonoff_ip=dsr_device.sonoff_ip,devices_sonoff_mac=dsr_device.sonoff_mac,power_status=dsr_power_status,wifi_strength=dsr_signal_strength,vcc=dsr_vcc)
                db.session.add(new_device_state_log)
            else:
                worker_logfile.write(str(dsr[0][0])+" device with that IP dont exist in db")

        elif (len(esr)):
            worker_logfile.write(str(esr[0])+"\n")
            if (return_deviceobj(esr[0][0])):

                esr_device = return_deviceobj(esr[0][0])
                esr_year = int(return_timearray(esr[0][1])[0])
                esr_month = int(return_timearray(esr[0][1])[1])
                esr_date = int(return_timearray(esr[0][1])[2])
                esr_hour = int(return_timearray(esr[0][1])[3])
                esr_minute = int(return_timearray(esr[0][1])[4])
                esr_second = int(return_timearray(esr[0][1])[5])
                esr_kwh_yesterday = float(esr[0][2])
                esr_kwh_sofar_today = float(esr[0][3])
                esr_period = int(esr[0][4])
                esr_power = float(esr[0][5])
                esr_factor = float(esr[0][6])
                esr_voltage = float(esr[0][7])
                esr_current = float(esr[0][8])

                update_sterday_kwh_dailysummary(esr_kwh_yesterday,esr_device.name,esr[0][1])

                new_energy_state_log = energy_state(logtime_year=esr_year,logtime_month=esr_month,logtime_date=esr_date,logtime_hour=esr_hour,logtime_minute=esr_minute,logtime_second=esr_second,devices_id=esr_device.id,devices_name=esr_device.name,devices_sonoff_ip=esr_device.sonoff_ip,devices_sonoff_mac=esr_device.sonoff_mac,period=esr_period,power=esr_power,factor=esr_factor,voltage=esr_voltage,current=esr_current,kwh_sofar_today=esr_kwh_sofar_today,kwh_yesterday=esr_kwh_yesterday)
                db.session.add(new_energy_state_log)

            else:
                worker_logfile.write(str(esr[0][0])+" device with that IP dont exist in db")

        else:
            worker_logfile.write('The logline below dont match either of ds/es \n')
            worker_logfile.write(str(eachline)+"\n")

    linestate.write(str(len(input_buffer)))
    db.session.commit()
    worker_logfile.write("\nDB Commit completed")
    health_status.write("\n Worker succesfully ran last time on the above time stamp.")


#Updating DB Status
health_status.write("\nDB Status:\n")
health_status.write("Records in \"devices\" table :"+ str(len(devices.query.all())) +"\n")
health_status.write("Records in \"device_state\" table :"+ str(len(device_state.query.all())) +"\n")
health_status.write("Records in \"energy_state\" table :"+ str(len(energy_state.query.all())) +"\n")
health_status.write("Records in \"daily_summary\" table :"+ str(len(daily_summary.query.all())) +"\n")

health_status.write("\n DB Size is "+ str(round(float(os.stat(DB_path).st_size)/1024/1024,5)) +" MB\n")

#Closing Files
worker_logfile.write("***End of Script***\n")

linestate.close()
input_logfile.close()
worker_logfile.close()
health_status.close()