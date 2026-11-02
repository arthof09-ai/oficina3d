"""Gate 0 reproduzivel: builds CPU em copia/venv separados, sem baixar pesos."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--tentativa', type=int, default=1)
attempt = parser.parse_args().tentativa
if attempt < 1:
    parser.error('tentativa deve ser positiva')
OUT = BASE / 'evidencias' / ('gate0' if attempt == 1 else f'gate0_tentativa{attempt}')
if (OUT / 'resultado.json').exists():
    raise RuntimeError('Tentativa ja registrada; use outro numero para preservar a prova')
ENGINE = BASE / 'motores' / 'Hunyuan3D-2GP'
PYTHON = BASE / '.venv_paint' / 'Scripts' / 'python.exe'
OUT.mkdir(parents=True, exist_ok=True)
if Path(sys.prefix).resolve() != PYTHON.parents[1].resolve():
    raise RuntimeError('Execute no venv proprio .venv_paint')
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1',
           TEMP=str(BASE / '_cache' / 'tmp'), TMP=str(BASE / '_cache' / 'tmp'),
           TORCH_EXTENSIONS_DIR=str(BASE / '_cache' / 'torch_extensions'),
           TORCH_CUDA_ARCH_LIST='8.9', MAX_JOBS='2')
report = {'tentativa': attempt, 'python': sys.version, 'prefix': sys.prefix,
          'ferramentas': {x: shutil.which(x) for x in ['nvcc', 'cl', 'g++']},
          'versoes': {x: importlib.metadata.version(x) for x in
                     ['torch', 'setuptools', 'wheel', 'pybind11', 'ninja']},
          'tentativas': [], 'gpu_inferencia': False}

def save():
    (OUT / 'resultado.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

def run(name, args, cwd, timeout=300):
    start = time.perf_counter()
    try:
        result = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        result = subprocess.CompletedProcess(args, 124, (exc.stdout or b'') + b'\nTIMEOUT')
    except OSError as exc:
        result = subprocess.CompletedProcess(args, 127, str(exc).encode('utf-8'))
    log = OUT / (name + '.log')
    log.write_bytes(result.stdout)
    row = {'nome': name, 'comando': args, 'cwd': str(cwd), 'exit_code': result.returncode,
           'tempo_s': round(time.perf_counter() - start, 4), 'log_bytes': log.stat().st_size,
           'sha256_log': hashlib.sha256(result.stdout).hexdigest()}
    report['tentativas'].append(row)
    save()
    print(json.dumps(row), flush=True)
    return result.returncode

run('nvcc_version', ['nvcc', '--version'], BASE)
run('cl_version', ['cl'], BASE)
# cl sem argumentos retorna 0 nesta toolchain; diagnostico nao substitui build.
for name, folder, module in [
    ('rasterizer', 'custom_rasterizer', 'custom_rasterizer'),
    ('painter', 'differentiable_renderer', 'mesh_processor')]:
    cwd = ENGINE / 'hy3dgen' / 'texgen' / folder
    setup = cwd / 'setup.py'
    report[name + '_setup_sha256'] = hashlib.sha256(setup.read_bytes()).hexdigest()
    run(name + '_build', [str(PYTHON), '-B', 'setup.py', 'build_ext', '--inplace'], cwd)
    run(name + '_import', [str(PYTHON), '-B', '-c', f'import torch; import {module}; print({module}.__file__)'], cwd)
for name, folder, module in [
    ('rasterizer', 'custom_rasterizer', 'custom_rasterizer_kernel'),
    ('painter', 'differentiable_renderer', 'mesh_processor')]:
    code = (f'import torch; import {module} as m; from importlib.machinery import EXTENSION_SUFFIXES; '
            'print(m.__file__); assert any(m.__file__.endswith(s) for s in EXTENSION_SUFFIXES), '
            '"import Python nao comprova extensao nativa"')
    run(name + '_native', [str(PYTHON), '-B', '-c', code],
        ENGINE / 'hy3dgen' / 'texgen' / folder)
report['gate0_aprovado'] = all(x['exit_code'] == 0 for x in report['tentativas'])
report['decisao'] = 'prosseguir spike' if report['gate0_aprovado'] else 'Gate 0 reprovado nesta tentativa; registrar erro e seguir outra frente'
save()
print(report['decisao'])

sys.exit(0 if report["gate0_aprovado"] else 1)
