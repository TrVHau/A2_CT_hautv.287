@echo off
chcp 65001 > nul
echo ========================================================
echo   Khoi dong Assignment 1: He Chan Doan Benh Tieu Duong
echo   URL: http://localhost:5000
echo ========================================================
cd /d "%~dp0web_app"
python app.py 5000
pause
