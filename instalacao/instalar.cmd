@echo off
rem Oficina 3D v2 - Fase 1. Sem argumentos: SO MOSTRA O PLANO (nada e gravado).
rem Executar:  instalar.cmd -Executar -UvZip "<caminho>\uv-0.13.6-x86_64-pc-windows-msvc.zip"
rem A politica do PowerShell 5.1 neste PC e Restricted fora do Claude; o Bypass vale so para este processo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0instalar.ps1" %*
exit /b %ERRORLEVEL%
