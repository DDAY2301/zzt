@echo off
cd /d "%~dp0"
echo ZZT - Lokalni predogled: http://127.0.0.1:8765/
echo Odprite navedeni naslov v brskalniku. Ctrl+C ustavi streznik.
start "" "http://127.0.0.1:8765/"
py -m http.server 8765 --directory site
if errorlevel 1 python -m http.server 8765 --directory site
