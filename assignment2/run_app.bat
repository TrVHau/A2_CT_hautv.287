@echo off
chcp 65001 > nul
echo ========================================================
echo   Khoi dong Assignment 2: He Du Doan Gia Nha (Web & Mobile)
echo   Desktop URL: http://localhost:5001
echo   Mobile URL:  http://localhost:5001/mobile
echo ========================================================
cd /d "%~dp0web_mobile_app"
python app.py 5001
pause
