@echo off
set "PATH=C:\Program Files (x86)\Microsoft Visual Studio\Installer;%PATH%"
call "E:\RPG_Assimilacao\Oficina3D\Ferramentas\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 echo VCVARS FALHOU
where cl
cl 2>&1 | findstr /i "Compiler Compilador"
where cmake
echo WindowsSdkVersion=%WindowsSdkVersion%
