# Charting Power  
Small Historical charting application to show power usage of different devices over time. This project has a SonoffP2 home automation device that tracks the power usage of each device connected and polls that data to a Syslog server. Our project contains two individual processes  
* ### Worker Process  
That parses the log files and updates the Local SQLite DB and does Maintenance of DB  
* ### Web Application  
That displays interactive charts to end users. Different tabs include  
 * __Dashboard__ - Represents Daily Power units usage over last 100 days  
 * __Custom Reports__ - Can select reports of choice for a particular device. Time yet to be inlcuded  
 * __Add new Devices__ - Can add new Sonoff Devices as required  
 * __Health Status__ - Represents Health Status captured during the last worker process run.  
  
## Procedure to run the application  
* Browse to the directory required & build a seperate virtualenv, to avoid conflict with other applications. Python ver 2.7  
* activate the Virtualenv and install the modules flask, flask_sqlalchemy, flask_wtf  
  > _virtualenv __ChartingPower___  
  > _cd __ChartingPower/scripts/activate.bat___  
    _pip install __flask__, __flask_sqlalchemy__, __falsk_wtf___  
* Clone the Git Repository to a folder inside __ChartingPower__ Home Folder & Start the application from that path.
  >_python __Home.py___
* Ensure to append the new logs to the ___vjacsyslog.txt___ file  
* Schedule Worker script using crontab at the required frequency.