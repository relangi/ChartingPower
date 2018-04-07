# Charting Power
Small Historical charting application to show power usage of different devices over time. This project has a SonoffP2 home automation device that tracks the power usage of each device connected and polls that data to a Syslog server. Our project contains two individual processes
* ### Worker Process
That parses the log files and updates the Local SQLite DB and does Maintenance of DB
* ### Web Application
That displays interactive charts to end users.

