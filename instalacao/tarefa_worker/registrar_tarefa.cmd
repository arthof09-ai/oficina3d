@echo off
rem Registra (ou remove) a Tarefa Agendada do worker da Oficina 3D.
rem Usuario atual, sem admin. Uso:
rem   registrar_tarefa.cmd            registra (ou atualiza) a tarefa
rem   registrar_tarefa.cmd /remover   remove a tarefa
rem   registrar_tarefa.cmd /gerar     so gera o XML final (nao registra)
setlocal EnableExtensions
set "NOME=Oficina3D_Worker"
set "AQUI=%~dp0"
for %%I in ("%AQUI%..\..") do set "APP=%%~fI"
for %%I in ("%APP%\..") do set "BASE=%%~fI"
set "MODELO=%AQUI%tarefa_worker.xml"
set "XML_GERADO=%BASE%\_cache\tmp\tarefa_worker_gerada.xml"
set "USUARIO=%USERDOMAIN%\%USERNAME%"

if /i "%~1"=="/remover" goto remover

if not exist "%MODELO%" (
  echo ERRO: modelo nao encontrado: "%MODELO%"
  exit /b 1
)
if /i not "%~1"=="/gerar" if not exist "%BASE%\.venv_app\Scripts\pythonw.exe" (
  echo ERRO: "%BASE%\.venv_app\Scripts\pythonw.exe" nao existe. Instale a Oficina antes.
  exit /b 1
)
if not exist "%BASE%\_cache\tmp" mkdir "%BASE%\_cache\tmp"

rem Troca os marcadores e grava em UTF-16 (o schtasks prefere assim).
powershell -NoProfile -ExecutionPolicy Bypass -Command "$x=[IO.File]::ReadAllText($env:MODELO); $x=$x.Replace('UTF-8'+[char]34+'?','UTF-16'+[char]34+'?').Replace('__USUARIO__',$env:USUARIO).Replace('__APP__',$env:APP).Replace('__BASE__',$env:BASE); [IO.File]::WriteAllText($env:XML_GERADO,$x,[Text.Encoding]::Unicode)"
if errorlevel 1 (
  echo ERRO ao gerar o XML.
  exit /b 1
)
echo XML gerado: "%XML_GERADO%"
if /i "%~1"=="/gerar" exit /b 0

schtasks /Create /TN "%NOME%" /XML "%XML_GERADO%" /F
if errorlevel 1 (
  echo ERRO: o schtasks recusou. Veja o README.md desta pasta ^(alternativa sem tarefa: atalho na pasta Inicializar^).
  exit /b 1
)
schtasks /Query /TN "%NOME%" /V /FO LIST
exit /b 0

:remover
schtasks /Delete /TN "%NOME%" /F
exit /b %errorlevel%
