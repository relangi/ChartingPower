# Charting Power
Small Historical charting application to show power usage of different devices over time. This project has a SonoffP2 home automation device that tracks the power usage of each device connected and polls that data to a Syslog server. Our project contains two individual processes
* ### Worker Process
That parses the log files and updates the Local SQLite DB and does Maintenance of DB
* ### Web Application
That displays interactive charts to end users. Different tabs include
 * Dashboard - Represents Daily Power units usage over last 100 days
 * Custom Reports - Can select reports of choice for a particular device. Time yet to be inlcuded
 * Add new Devices - Can add new Sonoff Devices as required
 * Health Status - Represents Health Status captured during the last worker process run.

## Procedure to run the application
* Browse to the directory required & build a seperate virtualenv, to avoid conflict with other applications. Python ver 2.7
* activate the Virtualenv and install the modules flask, flask_sqlalchemy, flask_wtf
    > virtualenv ChartingPower
    > cd ChartingPower/scripts/active.bat
    > pip install flask, flask_sqlalchemy, falsk_wtf
* execute the Home.py
  >_python Home.py_
* Ensure to append the new logs to the "vjacsyslog.txt" file
* Schedule Worker script using crontab at the required frequency.


