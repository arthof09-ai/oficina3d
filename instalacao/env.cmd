@echo off
rem Ambiente da Oficina 3D v2 para cmd.exe. Uso:  call "<BASE>\app\instalacao\env.cmd"
rem BASE = duas pastas acima desta. Tudo de cache fica em BASE\_cache. So ASCII de proposito.
for %%I in ("%~dp0..\..") do set "OFICINA3D_BASE=%%~fI"

rem Guarda: nunca G:, Google Drive ou o espelho antigo Desktop\RPG Assimilacao.
echo(%OFICINA3D_BASE%| findstr /b /i /c:"G:" >nul && goto :proibido
echo(%OFICINA3D_BASE%| findstr /i /c:"\Desktop\RPG Assimila" /c:"Google Drive" /c:"\Meu Drive" /c:"\My Drive" >nul && goto :proibido

set "OFICINA3D_JOBS=%OFICINA3D_BASE%\jobs"
set "HF_HOME=%OFICINA3D_BASE%\_cache\huggingface"
set "HY3DGEN_MODELS=%OFICINA3D_BASE%\_cache\hy3dgen"
set "U2NET_HOME=%OFICINA3D_BASE%\_cache\u2net"
set "TEMP=%OFICINA3D_BASE%\_cache\tmp"
set "TMP=%OFICINA3D_BASE%\_cache\tmp"
set "UV_CACHE_DIR=%OFICINA3D_BASE%\_cache\uv"
set "UV_PYTHON_INSTALL_DIR=%OFICINA3D_BASE%\_cache\uv_python"
set "UV_PYTHON_PREFERENCE=only-managed"
set "UV_LINK_MODE=hardlink"
set "UV_NO_PROGRESS=1"
set "PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True"
set "HF_HUB_DISABLE_SYMLINKS_WARNING=1"
set "HF_HUB_DISABLE_TELEMETRY=1"
rem Para rodar os motores sem rede depois dos downloads:  set "HF_HUB_OFFLINE=1"

rem Arquivo dos jobs concluidos (oficina3d/arquivar.py le OFICINA3D_ARQUIVO como a
rem raiz Oficina3D_v2 do Drive). Resolvido por curinga: este arquivo fica 100% ASCII
rem e o nome real da pasta tem til (P5, 31/10/2026).
for /d %%D in ("G:\Meu Drive\RPG*") do set "OFICINA3D_ARQUIVO=%%D\Oficina3D_v2"

for %%P in ("%OFICINA3D_JOBS%" "%HF_HOME%" "%HY3DGEN_MODELS%" "%U2NET_HOME%" "%TEMP%" "%UV_CACHE_DIR%" "%UV_PYTHON_INSTALL_DIR%" "%OFICINA3D_BASE%\_cache\logs" "%OFICINA3D_BASE%\locks" "%OFICINA3D_BASE%\motores") do (
    if not exist "%%~P\" mkdir "%%~P"
)
exit /b 0

:proibido
echo env.cmd: OFICINA3D_BASE em lugar proibido (G:/Drive/Desktop): %OFICINA3D_BASE%
set "OFICINA3D_BASE="
exit /b 4
