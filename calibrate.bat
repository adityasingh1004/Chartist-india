@echo off
rem Re-run Chartist's verdict calibration on every NSE/BSE stock and global series.
rem Downloads 10 years of daily bars from Yahoo (unofficial), then reads every chart point-in-time.
rem A full run takes hours. It is safe to stop (Ctrl+C) and start again: downloads resume.
rem Quick test first:  calibrate.bat --sample 10
cd /d "%~dp0"
where py >nul 2>nul && (py -3 chartist\calibrate.py --fetch %*) || (python chartist\calibrate.py --fetch %*)
pause
