@echo off
rem Start Chartist on Windows. Needs Python 3.10 or newer (https://www.python.org/downloads/).
cd /d "%~dp0"
where py >nul 2>nul && (py -3 chartist\app.py %*) || (python chartist\app.py %*)
