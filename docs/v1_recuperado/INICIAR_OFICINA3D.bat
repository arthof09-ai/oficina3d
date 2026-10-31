@echo off
rem Liga a Oficina 3D: worker (processa a fila na GPU) + página web, e abre o navegador.
rem Tudo roda no disco E:. Para desligar: feche as duas janelas "Oficina3D".
setlocal
set "B=E:\RPG_Assimilacao\Oficina3D"
set "TEMP=%B%\_cache\tmp"
set "TMP=%B%\_cache\tmp"
set "PYTHONUTF8=1"
cd /d "%B%\app"
start "Oficina3D - worker" /min "%B%\.venv\Scripts\python.exe" -m oficina3d.worker
start "Oficina3D - web" /min "%B%\.venv\Scripts\python.exe" -m oficina3d.web
timeout /t 4 /nobreak >nul
start "" http://127.0.0.1:8765
endlocal
