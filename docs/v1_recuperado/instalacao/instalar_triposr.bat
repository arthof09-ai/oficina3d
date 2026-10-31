@echo off
rem Ambiente separado do TripoSR (transformers 4.35, diferente do Hunyuan).
rem Roda dentro do ambiente do MSVC para compilar o torchmcubes.
set "B=E:\RPG_Assimilacao\Oficina3D"
set "TEMP=%B%\_cache\tmp"
set "TMP=%B%\_cache\tmp"
set "PIP_CACHE_DIR=%B%\_cache\pip"
set "PATH=C:\Program Files (x86)\Microsoft Visual Studio\Installer;%PATH%"
call "%B%\Ferramentas\VSBuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul
if not exist "%B%\.venv_triposr\Scripts\python.exe" "%B%\Ferramentas\Python310\python.exe" -m venv "%B%\.venv_triposr"
set "PY=%B%\.venv_triposr\Scripts\python.exe"
"%PY%" -m pip install --upgrade pip setuptools wheel
"%PY%" -m pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu124
"%PY%" -m pip install scikit-build-core cmake ninja pybind11
"%PY%" -m pip install --no-build-isolation -r "%B%\motores\TripoSR\requirements.txt" "torch==2.5.1" "torchvision==0.20.1"
echo PIP_EXIT=%ERRORLEVEL%
cd /d "%B%\motores\TripoSR"
"%PY%" -c "import torch, torchmcubes, transformers, trimesh; from tsr.system import TSR; print('IMPORT OK', torch.__version__, torch.cuda.is_available(), transformers.__version__, 'mcubes_cuda' in dir(torchmcubes))"
echo FIM
