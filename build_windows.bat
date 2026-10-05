@echo off
setlocal
cd /d "%~dp0"
python -m PyInstaller --noconfirm --onefile --windowed --name CyberDefense main.py
if errorlevel 1 exit /b 1
powershell -NoProfile -Command "Compress-Archive -LiteralPath 'dist\CyberDefense.exe' -DestinationPath 'dist\CyberDefense-Windows.zip' -Force"
if errorlevel 1 exit /b 1
echo Build criada em dist\CyberDefense-Windows.zip
