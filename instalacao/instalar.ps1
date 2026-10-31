<#
.SYNOPSIS
  Instalador idempotente da Oficina 3D v2 - Fase 1 (CUNHADO-PC).

.DESCRIPTION
  PADRAO = SO PLANEJA: imprime o plano e o estado de cada etapa, sem gravar nem baixar nada.
  Para executar de verdade: -Executar.

  Etapas (cada uma confere "ja feito?" e pula):
    a  espaco livre (>= MinLivreGB GiB depois do previsto) e guarda: nada em G:, Google Drive ou Desktop\RPG Assimilacao
    b  uv (nao baixa: usa BASE\ferramentas\uv\uv.exe, o uv do PATH, ou extrai o zip passado em -UvZip, com SHA256)
    c  uv python install 3.10 (em BASE\_cache\uv_python)
    d  venvs .venv_app (app + Hunyuan = o .venv_hunyuan do plano), .venv_triposr, .venv_mcp;
       torch 2.5.1+cu124 pelo indice do PyTorch; sem diso; TripoSR sem torchmcubes (compat + .pth);
       grava requirements_<venv>.lock com "uv pip freeze"
    e  clona Hunyuan3D-2GP @ f2456e0 e TripoSR @ 107cefd em BASE\motores e aplica os patches (git apply --check antes)
    f  baixa os modelos (baixar_modelos.py no .venv_app, pelo manifesto_modelos.json)
    g  teste rapido de import de cada venv

  Log (so no modo -Executar): BASE\_cache\logs\instalar_<data_hora>.log
  A politica do PowerShell 5.1 neste PC e Restricted fora do Claude: rode pelo instalar.cmd.

.EXAMPLE
  instalar.cmd
  instalar.cmd -Executar -UvZip "<pasta>\uv-0.13.6-x86_64-pc-windows-msvc.zip"
  instalar.cmd -Executar -Etapas d,g
#>
[CmdletBinding()]
param(
    [switch]$Executar,
    [switch]$SoPlanejar,
    [string]$UvZip = '',
    [string]$UvZipSha256 = 'A2A8820D5EEA32F08EF467EF3B7F66883A9B076D5737A2FC2FBB5F458D1BB50F',
    [string[]]$Etapas = @('a', 'b', 'c', 'd', 'e', 'f', 'g'),
    [double]$MinLivreGB = 20
)

Set-StrictMode -Version 2.0
$ErrorActionPreference = 'Stop'

if ($Executar -and $SoPlanejar) { throw 'Use -Executar OU -SoPlanejar, nao os dois.' }
$Planejar = -not $Executar
# Pelo "powershell -File", "-Etapas d,g" chega como um texto so: separar aqui.
$Etapas = @($Etapas | ForEach-Object { $_ -split '[,; ]+' } | Where-Object { $_ } | ForEach-Object { $_.ToLowerInvariant() })

$Instalacao = $PSScriptRoot
$Base = [System.IO.Path]::GetFullPath((Join-Path $Instalacao '..\..'))
. (Join-Path $Instalacao 'env.ps1') -SemCriar:$Planejar

# ------------------------------------------------------------------ dados
$IndiceTorch = 'https://download.pytorch.org/whl/cu124'
$PacotesTorch = @('torch==2.5.1+cu124', 'torchvision==0.20.1+cu124')
$UvLocal = Join-Path $Base 'ferramentas\uv\uv.exe'
$Venvs = @(
    @{ Nome = '.venv_app';     Req = 'requisitos\app.txt';     Torch = $true;  Pth = $false; EstimativaGB = 5.5 },
    @{ Nome = '.venv_triposr'; Req = 'requisitos\triposr.txt'; Torch = $true;  Pth = $true;  EstimativaGB = 1.5 },
    @{ Nome = '.venv_mcp';     Req = 'requisitos\mcp.txt';     Torch = $false; Pth = $false; EstimativaGB = 0.1 }
)
$Motores = @(
    @{ Nome = 'Hunyuan3D-2GP'; Url = 'https://github.com/deepbeepmeep/Hunyuan3D-2GP.git'; Commit = 'f2456e0'; Patches = @(); EstimativaGB = 0.25 },
    @{ Nome = 'TripoSR'; Url = 'https://github.com/VAST-AI-Research/TripoSR.git'; Commit = '107cefd'; Patches = @('patches\triposr_bake_texture.patch'); EstimativaGB = 0.05 }
)
# GiB. transitorio = wheel do torch (~2,5 GB) no cache do uv durante a instalacao.
$Estimativas = @{ uv = 0.05; python310 = 0.1; transitorio = 2.5 }
$Testes = @(
    @{ Venv = '.venv_app'; Pasta = 'motores\Hunyuan3D-2GP'; Exige = @('IMPORT OK', '+cu124 True');
       Codigo = "import torch, mmgp, pymeshlab, trimesh, transformers, diffusers, fastapi, rembg, huggingface_hub; from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline; from hy3dgen.rembg import BackgroundRemover; print('IMPORT OK', torch.__version__, torch.cuda.is_available(), transformers.__version__, diffusers.__version__)" },
    @{ Venv = '.venv_triposr'; Pasta = 'motores\TripoSR'; Exige = @('IMPORT OK', '+cu124 True', '\compat\torchmcubes\__init__.py');
       Codigo = "import torch, torchmcubes, transformers, trimesh, onnxruntime, moderngl, xatlas; from tsr.system import TSR; from tsr.bake_texture import bake_texture; print('IMPORT OK', torch.__version__, torch.cuda.is_available(), transformers.__version__, torchmcubes.__file__)" },
    @{ Venv = '.venv_mcp'; Pasta = ''; Exige = @('IMPORT OK');
       Codigo = "import psutil, importlib.metadata as m; from mcp.server.mcpserver import MCPServer; print('IMPORT OK mcp', m.version('mcp'))" }
)

$script:LogArq = $null
$script:Pararia = $false
$script:Pendencias = @()
if (-not $Planejar) {
    $script:LogArq = Join-Path $Base ('_cache\logs\instalar_{0}.log' -f (Get-Date -Format 'yyyyMMdd_HHmmss'))
}

# ------------------------------------------------------------------ utilidades
function Escrever([string]$Msg) {
    $linha = '{0} {1}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Msg
    Write-Host $linha
    if ($script:LogArq) { Add-Content -LiteralPath $script:LogArq -Value $linha -Encoding UTF8 }
}

function Formatar-Args([string[]]$A) {
    return (($A | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }) -join ' ')
}

# Executa (ou, no plano, so mostra) um comando externo; falha se o codigo de saida nao for 0.
function Rodar([string]$Exe, [string[]]$A, [string]$Pasta = '') {
    $onde = ''
    if ($Pasta) { $onde = " (em $Pasta)" }
    Escrever ('  > {0} {1}{2}' -f $Exe, (Formatar-Args $A), $onde)
    if ($Planejar) { return }
    $eap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    if ($Pasta) { Push-Location -LiteralPath $Pasta }
    try {
        & $Exe @A 2>&1 | ForEach-Object { Escrever ('    ' + $_.ToString()) }
        $codigo = $LASTEXITCODE
    } finally {
        if ($Pasta) { Pop-Location }
        $ErrorActionPreference = $eap
    }
    if ($codigo -ne 0) { throw ('Falhou (codigo {0}): {1} {2}' -f $codigo, $Exe, (Formatar-Args $A)) }
}

# Consulta somente leitura (roda tambem no modo plano). Devolve Codigo, Saida e Linhas.
function Consultar([string]$Exe, [string[]]$A, [string]$Pasta = '', [switch]$SoStdout) {
    $eap = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    if ($Pasta) { Push-Location -LiteralPath $Pasta }
    $linhas = @()
    $codigo = -1
    try {
        if ($SoStdout) { $linhas = @(& $Exe @A 2>$null | ForEach-Object { $_.ToString() }) }
        else { $linhas = @(& $Exe @A 2>&1 | ForEach-Object { $_.ToString() }) }
        $codigo = $LASTEXITCODE
    } catch {
        $linhas = @($_.Exception.Message)
    } finally {
        if ($Pasta) { Pop-Location }
        $ErrorActionPreference = $eap
    }
    return @{ Codigo = $codigo; Linhas = $linhas; Saida = (($linhas -join "`n").Trim()) }
}

function Testar-Proibido([string]$Caminho) {
    if (-not $Caminho) { return $false }
    $s = $Caminho.Replace('/', '\').ToLowerInvariant()
    if ($s.StartsWith('g:') -or $s.StartsWith('\\?\g:')) { return $true }
    foreach ($x in @('\desktop\rpg assimila', 'google drive', 'googledrive', '\meu drive', '\my drive')) {
        if ($s.Contains($x)) { return $true }
    }
    return $false
}

# Juncoes/links simbolicos no caminho da BASE (um deles poderia levar ao G:).
function Alvos-Reparse([string]$Caminho) {
    $alvos = @()
    $p = $Caminho
    while ($p) {
        if (Test-Path -LiteralPath $p) {
            $it = Get-Item -LiteralPath $p -Force
            if ($it.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
                $t = ''
                try { $t = (@($it.Target) -join ';') } catch { $t = '?' }
                $alvos += ('{0} -> {1}' -f $p, $t)
            }
        }
        $pai = Split-Path -Parent $p
        if (-not $pai -or $pai -eq $p) { break }
        $p = $pai
    }
    return , $alvos
}

function Prop($Obj, [string]$Nome) {
    $p = $Obj.PSObject.Properties[$Nome]
    if ($p) { return $p.Value }
    return $null
}

function Achar-Uv {
    if (Test-Path -LiteralPath $UvLocal) { return $UvLocal }
    $c = Get-Command uv -ErrorAction SilentlyContinue
    if ($c) { return $c.Source }
    return $null
}

function Exigir-Uv {
    $u = Achar-Uv
    if ($u) { return $u }
    if ($Planejar) { return '<uv>' }
    throw 'uv ausente: rode a etapa b antes (veja as opcoes no plano).'
}

function Achar-Python310 {
    $d = $env:UV_PYTHON_INSTALL_DIR
    if ($d -and (Test-Path -LiteralPath $d)) {
        $c = Get-ChildItem -LiteralPath $d -Directory -Filter 'cpython-3.10*' -ErrorAction SilentlyContinue |
             Sort-Object Name -Descending | Select-Object -First 1
        if ($c -and (Test-Path -LiteralPath (Join-Path $c.FullName 'python.exe'))) { return (Join-Path $c.FullName 'python.exe') }
    }
    $u = Achar-Uv
    if ($u) {
        $r = Consultar $u @('python', 'find', '3.10') -SoStdout
        if ($r.Codigo -eq 0 -and $r.Saida -and $d -and $r.Saida.StartsWith($d, [System.StringComparison]::OrdinalIgnoreCase)) { return $r.Saida }
    }
    return $null
}

function Caminho-Lock($V) { return (Join-Path $Instalacao ('requirements_{0}.lock' -f $V.Nome.TrimStart('.'))) }

function Fonte-Venv($V) {
    $lock = Caminho-Lock $V
    if (Test-Path -LiteralPath $lock) { return $lock }
    return (Join-Path $Instalacao $V.Req)
}

function Venv-Feito($V) {
    $marca = Join-Path (Join-Path $Base $V.Nome) '.oficina3d_instalado'
    if (-not (Test-Path -LiteralPath $marca)) { return $false }
    $hash = (Get-FileHash -LiteralPath (Fonte-Venv $V) -Algorithm SHA256).Hash
    return ((Get-Content -LiteralPath $marca -Raw).Trim() -eq $hash)
}

function Bytes-Modelos-Pendentes {
    $man = Get-Content -LiteralPath (Join-Path $Instalacao 'manifesto_modelos.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $total = [int64]0
    foreach ($i in $man.itens) {
        $prev = [int64]0
        if (Prop $i 'bytes') { $prev = [int64](Prop $i 'bytes') } elseif (Prop $i 'bytes_estimado') { $prev = [int64](Prop $i 'bytes_estimado') }
        $rel = [string](Prop $i 'arquivo')
        if (Prop $i 'subpasta') { $rel = (Prop $i 'subpasta') + '\' + $rel }
        $presente = $false
        $parcial = [int64]0
        if ($i.modo -eq 'hf_cache') {
            $snaps = Join-Path $Base (($i.destino -replace '/', '\') + '\hub\models--' + ($i.repo -replace '/', '--') + '\snapshots')
            if (Test-Path -LiteralPath $snaps) {
                foreach ($s in (Get-ChildItem -LiteralPath $snaps -Directory)) {
                    if (Test-Path -LiteralPath (Join-Path $s.FullName $rel)) { $presente = $true }
                }
            }
        } else {
            $dest = Join-Path $Base ($i.destino -replace '/', '\')
            if (Test-Path -LiteralPath $dest) { $presente = $true }
            elseif (Test-Path -LiteralPath ($dest + '.part')) { $parcial = (Get-Item -LiteralPath ($dest + '.part')).Length }
        }
        if (-not $presente) { $total += [Math]::Max([int64]0, $prev - $parcial) }
    }
    return $total
}

function Calcular-Previsto {
    $p = [ordered]@{}
    $p['modelos'] = [int64](Bytes-Modelos-Pendentes)
    $p['uv'] = [int64]0
    if (-not (Achar-Uv)) { $p['uv'] = [int64]($Estimativas.uv * 1GB) }
    $p['python310'] = [int64]0
    if (-not (Achar-Python310)) { $p['python310'] = [int64]($Estimativas.python310 * 1GB) }
    $p['venvs'] = [int64]0
    $torchPendente = $false
    foreach ($v in $Venvs) {
        if (-not (Venv-Feito $v)) {
            $p['venvs'] += [int64]($v.EstimativaGB * 1GB)
            if ($v.Torch) { $torchPendente = $true }
        }
    }
    $p['motores'] = [int64]0
    foreach ($m in $Motores) {
        if (-not (Test-Path -LiteralPath (Join-Path $Base ('motores\' + $m.Nome)))) { $p['motores'] += [int64]($m.EstimativaGB * 1GB) }
    }
    $p['transitorio'] = [int64]0
    if ($torchPendente) { $p['transitorio'] = [int64]($Estimativas.transitorio * 1GB) }
    $soma = [int64]0
    foreach ($k in @($p.Keys)) { $soma += $p[$k] }
    $p['total'] = $soma
    return $p
}

function GiB([double]$Bytes) { return ('{0:N2} GiB' -f ($Bytes / 1GB)) }

# ------------------------------------------------------------------ etapas
function Etapa-A {
    Escrever '== (a) Espaco livre e guarda contra G:/Google Drive/Desktop'
    $erros = @()
    $vars = @('OFICINA3D_BASE', 'OFICINA3D_JOBS', 'HF_HOME', 'HY3DGEN_MODELS', 'U2NET_HOME', 'TEMP', 'TMP', 'UV_CACHE_DIR', 'UV_PYTHON_INSTALL_DIR')
    foreach ($n in $vars) {
        $val = [Environment]::GetEnvironmentVariable($n, 'Process')
        if (Testar-Proibido $val) { $erros += ('{0}={1}' -f $n, $val) }
        elseif (-not $val -or -not $val.StartsWith($Base, [System.StringComparison]::OrdinalIgnoreCase)) { $erros += ('{0} fora da BASE: {1}' -f $n, $val) }
    }
    if (Testar-Proibido $Base) { $erros += "BASE: $Base" }
    foreach ($r in (Alvos-Reparse $Base)) {
        if (Testar-Proibido $r) { $erros += "juncao/link para lugar proibido: $r" }
        else { Escrever "  aviso: ponto de reparse no caminho da BASE: $r" }
    }
    $raiz = [System.IO.Path]::GetPathRoot($Base)
    $di = New-Object System.IO.DriveInfo $raiz
    if ($di.DriveType -ne [System.IO.DriveType]::Fixed) { $erros += ('disco da BASE nao e local/fixo: {0} ({1})' -f $raiz, $di.DriveType) }
    $rotulo = ''
    try { $rotulo = $di.VolumeLabel } catch { $rotulo = '' }
    if ($rotulo -match 'Google') { $erros += "o disco da BASE parece o Google Drive: $raiz ($rotulo)" }
    if ($erros.Count -gt 0) {
        foreach ($e in $erros) { Escrever "  PROIBIDO: $e" }
        throw 'Guarda G:/Drive falhou: nada foi feito.'
    }
    Escrever '  guarda OK: BASE e caches no disco local, nada em G:, Google Drive ou Desktop\RPG Assimilacao.'

    $p = Calcular-Previsto
    foreach ($k in @($p.Keys)) { if ($k -ne 'total') { Escrever ('  previsto {0,-12} {1}' -f $k, (GiB $p[$k])) } }
    $livre = $di.AvailableFreeSpace
    $depois = $livre - $p['total']
    Escrever ('  livre agora em {0}: {1}; previsto: {2}; depois: {3} (minimo {4} GiB)' -f $raiz, (GiB $livre), (GiB $p['total']), (GiB $depois), $MinLivreGB)
    if (($depois / 1GB) -lt $MinLivreGB) {
        if ($Planejar) { Escrever '  PARARIA AQUI: espaco insuficiente.'; $script:Pararia = $true }
        else { throw ('Espaco insuficiente: ficariam {0} livres (< {1} GiB).' -f (GiB $depois), $MinLivreGB) }
    } else { Escrever '  espaco OK.' }
}

function Etapa-B {
    Escrever '== (b) uv'
    $uv = Achar-Uv
    if ($uv) {
        Escrever ('  ja feito: {0} ({1}) - pula' -f $uv, (Consultar $uv @('--version')).Saida)
        return
    }
    if (-not $UvZip) {
        Escrever '  uv NAO encontrado. Este instalador nao baixa o uv. Opcoes (escolha uma e rode de novo):'
        Escrever '   1) Biblioteca do Drive (preferida): 07 - Aplicativos e instaladores\Oficina3D_Biblioteca_Claude\uv_0.13.6\uv-0.13.6-x86_64-pc-windows-msvc.zip'
        Escrever '      instalar.cmd -Executar -UvZip "<caminho do zip>"   (SHA256 esperado A2A8820D...8D1BB50F; o zip e so lido, nada e gravado no Drive)'
        Escrever '   2) winget install --id=astral-sh.uv -e   (instala no perfil do usuario, fora da BASE; reabrir o terminal)'
        Escrever '   3) Release oficial https://github.com/astral-sh/uv/releases/download/0.13.6/uv-x86_64-pc-windows-msvc.zip + o .sha256 do release; depois a opcao 1'
        Escrever '   Nao recomendado: irm https://astral.sh/uv/install.ps1 | iex (executa script remoto).'
        if ($Planejar) { $script:Pendencias += 'uv (etapa b)'; return }
        throw 'uv ausente.'
    }
    if (-not (Test-Path -LiteralPath $UvZip)) { throw "UvZip nao existe: $UvZip" }
    $sha = (Get-FileHash -LiteralPath $UvZip -Algorithm SHA256).Hash
    if ($sha -ne $UvZipSha256.ToUpperInvariant()) { throw ('SHA256 do zip do uv nao confere: {0} (esperado {1})' -f $sha, $UvZipSha256) }
    Escrever "  zip do uv conferido: SHA256 $sha"
    $destino = Split-Path -Parent $UvLocal
    if ($Planejar) { Escrever "  > extrairia o zip em $destino"; return }
    New-Item -ItemType Directory -Force -Path $destino | Out-Null
    Expand-Archive -LiteralPath $UvZip -DestinationPath $destino -Force
    if (-not (Test-Path -LiteralPath $UvLocal)) {
        $achado = Get-ChildItem -LiteralPath $destino -Recurse -Filter 'uv.exe' | Select-Object -First 1
        if (-not $achado) { throw "uv.exe nao veio no zip: $UvZip" }
        Get-ChildItem -LiteralPath $achado.DirectoryName -File | Move-Item -Destination $destino -Force
    }
    Escrever ('  uv pronto: {0} ({1})' -f $UvLocal, (Consultar $UvLocal @('--version')).Saida)
}

function Etapa-C {
    Escrever '== (c) Python 3.10 gerenciado pelo uv'
    $py = Achar-Python310
    if ($py) { Escrever "  ja feito: $py - pula"; return }
    $uv = Exigir-Uv
    Rodar $uv @('python', 'install', '3.10')
    if (-not $Planejar) {
        $py = Achar-Python310
        if (-not $py) { throw "Python 3.10 nao apareceu em $($env:UV_PYTHON_INSTALL_DIR)" }
        Escrever "  ok: $py"
    }
}

function Garantir-Pth([string]$Py) {
    $compat = Join-Path $Instalacao 'compat'
    if ($compat -match '[^\x20-\x7E]') { throw "O caminho do compat precisa ser ASCII (para o .pth): $compat" }
    if (-not (Test-Path -LiteralPath $Py)) {
        Escrever "  > gravaria oficina3d_compat.pth (1 linha, ASCII sem BOM: $compat) no site-packages do venv"
        return
    }
    $sp = (Consultar $Py @('-c', "import sysconfig; print(sysconfig.get_paths()['purelib'])") -SoStdout).Saida
    if (-not $sp -or -not (Test-Path -LiteralPath $sp)) { throw "Nao achei o site-packages de $Py" }
    $pth = Join-Path $sp 'oficina3d_compat.pth'
    if ((Test-Path -LiteralPath $pth) -and ((Get-Content -LiteralPath $pth -Raw).Trim() -eq $compat)) {
        Escrever "  .pth ja certo: $pth - pula"
        return
    }
    if ($Planejar) { Escrever "  > gravaria $pth com: $compat"; return }
    [System.IO.File]::WriteAllText($pth, $compat + "`r`n", [System.Text.Encoding]::ASCII)
    Escrever "  .pth gravado: $pth"
}

function Etapa-D {
    Escrever '== (d) venvs (Python 3.10 pelo uv; cache em UV_CACHE_DIR, hardlink)'
    $uv = Exigir-Uv
    foreach ($v in $Venvs) {
        $dir = Join-Path $Base $v.Nome
        $py = Join-Path $dir 'Scripts\python.exe'
        $lock = Caminho-Lock $v
        $fonte = Fonte-Venv $v
        $marca = Join-Path $dir '.oficina3d_instalado'
        if (Venv-Feito $v) {
            Escrever ('  {0}: ja feito (marca bate com {1}) - pula' -f $v.Nome, (Split-Path -Leaf $fonte))
            if ($v.Pth) { Garantir-Pth $py }
            continue
        }
        Escrever ('  {0}: instalar por {1}' -f $v.Nome, (Split-Path -Leaf $fonte))
        if (-not (Test-Path -LiteralPath $py)) { Rodar $uv @('venv', '--python', '3.10', $dir) }
        if ($v.Torch) { Rodar $uv (@('pip', 'install', '--python', $py) + $PacotesTorch + @('--index-url', $IndiceTorch)) }
        $a = @('pip', 'install', '--python', $py, '-r', $fonte)
        if ($v.Torch) { $a += @('--extra-index-url', $IndiceTorch, '--index-strategy', 'unsafe-best-match') }
        Rodar $uv $a
        if ($v.Pth) { Garantir-Pth $py }
        if ($Planejar) {
            Escrever ('  > {0} pip freeze --python {1}  ->  {2} (se ainda nao existir)' -f $uv, $py, $lock)
            continue
        }
        $f = Consultar $uv @('pip', 'freeze', '--python', $py) -SoStdout
        if ($f.Codigo -ne 0 -or $f.Linhas.Count -eq 0) { throw "uv pip freeze falhou em $($v.Nome)" }
        $texto = (($f.Linhas | Where-Object { $_.Trim() }) -join "`r`n") + "`r`n"
        if (Test-Path -LiteralPath $lock) {
            if ((Get-Content -LiteralPath $lock -Raw).Trim() -ne $texto.Trim()) {
                [System.IO.File]::WriteAllText($lock + '.novo', $texto, [System.Text.Encoding]::ASCII)
                Escrever "  AVISO: o freeze difere do lock; gravei $lock.novo para comparar (o lock nao foi trocado)."
            }
        } else {
            [System.IO.File]::WriteAllText($lock, $texto, [System.Text.Encoding]::ASCII)
            Escrever "  lock gravado: $lock"
        }
        $hash = (Get-FileHash -LiteralPath (Fonte-Venv $v) -Algorithm SHA256).Hash
        [System.IO.File]::WriteAllText($marca, $hash, [System.Text.Encoding]::ASCII)
        Escrever "  $($v.Nome): ok"
    }
}

function Etapa-E {
    Escrever '== (e) motores: clone no commit fixo + patches'
    $g = Get-Command git -ErrorAction SilentlyContinue
    $git = 'git'
    if ($g) { $git = $g.Source }
    elseif ($Planejar) { Escrever '  git NAO encontrado no PATH'; $script:Pendencias += 'git (etapa e)' }
    else { throw 'git ausente.' }
    foreach ($m in $Motores) {
        $dir = Join-Path $Base ('motores\' + $m.Nome)
        if (Test-Path -LiteralPath $dir) {
            if (-not (Test-Path -LiteralPath (Join-Path $dir '.git'))) { throw "$dir existe sem .git: confira a mao (nao mexo)." }
            $head = (Consultar $git @('-C', $dir, 'rev-parse', 'HEAD') -SoStdout).Saida
            if (-not $head.StartsWith($m.Commit)) { throw ('{0}: HEAD {1} diferente de {2}: confira a mao (nao mexo).' -f $m.Nome, $head, $m.Commit) }
            Escrever ('  {0}: clone ja no commit {1} - pula' -f $m.Nome, $m.Commit)
        } else {
            # autocrlf=false: os arquivos ficam com LF, igual ao repositorio, e o git apply bate byte a byte.
            Rodar $git @('-c', 'core.autocrlf=false', 'clone', '--filter=blob:none', '--no-checkout', $m.Url, $dir)
            Rodar $git @('-C', $dir, 'config', 'core.autocrlf', 'false')
            Rodar $git @('-C', $dir, 'checkout', '--detach', $m.Commit)
        }
        foreach ($pt in $m.Patches) {
            $arq = Join-Path $Instalacao $pt
            if (-not (Test-Path -LiteralPath $arq)) { throw "patch ausente: $arq" }
            if (-not (Test-Path -LiteralPath $dir)) {
                Escrever "  > $git -C $dir apply --check $arq"
                Escrever "  > $git -C $dir apply $arq"
                continue
            }
            if ((Consultar $git @('-C', $dir, 'apply', '--reverse', '--check', $arq)).Codigo -eq 0) {
                Escrever "  patch ja aplicado: $pt - pula"
                continue
            }
            $chk = Consultar $git @('-C', $dir, 'apply', '--check', $arq)
            if ($chk.Codigo -ne 0) { throw ('git apply --check falhou para {0}: {1}' -f $pt, $chk.Saida) }
            Escrever "  git apply --check OK: $pt"
            Rodar $git @('-C', $dir, 'apply', $arq)
        }
    }
}

function Etapa-F {
    Escrever '== (f) modelos: baixar_modelos.py (no .venv_app) pelo manifesto_modelos.json'
    $pyApp = Join-Path $Base '.venv_app\Scripts\python.exe'
    $script = Join-Path $Instalacao 'baixar_modelos.py'
    if ($Planejar) {
        Escrever ('  > {0} {1} --min-livre-gb {2}' -f $pyApp, $script, $MinLivreGB)
        $pyPlano = $null
        $pyArgs = @()
        if (Test-Path -LiteralPath $pyApp) { $pyPlano = $pyApp }
        else {
            $c = Get-Command py -ErrorAction SilentlyContinue
            if ($c) { $pyPlano = $c.Source; $pyArgs = @('-3') }
        }
        if ($pyPlano) {
            Escrever '  plano do baixar_modelos.py --so-planejar:'
            $r = Consultar $pyPlano ($pyArgs + @($script, '--so-planejar', '--min-livre-gb', [string]$MinLivreGB))
            foreach ($l in $r.Linhas) { Escrever ('    ' + $l) }
            if ($r.Codigo -eq 2) { $script:Pararia = $true }
        }
        return
    }
    if (-not (Test-Path -LiteralPath $pyApp)) { throw '.venv_app ausente: rode a etapa d antes.' }
    Rodar $pyApp @($script, '--min-livre-gb', [string]$MinLivreGB)
}

function Etapa-G {
    Escrever '== (g) teste rapido de import de cada venv'
    $falhas = 0
    foreach ($t in $Testes) {
        $py = Join-Path (Join-Path $Base $t.Venv) 'Scripts\python.exe'
        $pasta = ''
        if ($t.Pasta) { $pasta = Join-Path $Base $t.Pasta }
        if ($Planejar) {
            $onde = ''
            if ($pasta) { $onde = " (em $pasta)" }
            Escrever ('  > {0} -W ignore -c "{1}"{2}' -f $py, $t.Codigo, $onde)
            continue
        }
        if (-not (Test-Path -LiteralPath $py)) { Escrever "  FALHA $($t.Venv): venv ausente"; $falhas++; continue }
        $r = Consultar $py @('-W', 'ignore', '-c', $t.Codigo) $pasta -SoStdout
        $ok = ($r.Codigo -eq 0)
        foreach ($x in $t.Exige) { if (-not $r.Saida.Contains($x)) { $ok = $false } }
        if ($ok) { Escrever ('  OK {0}: {1}' -f $t.Venv, $r.Saida) }
        else {
            $falhas++
            Escrever ('  FALHA {0} (codigo {1}): {2}' -f $t.Venv, $r.Codigo, $r.Saida)
            $e = Consultar $py @('-W', 'ignore', '-c', $t.Codigo) $pasta
            foreach ($l in ($e.Linhas | Select-Object -Last 8)) { Escrever ('    ' + $l) }
        }
    }
    if ($falhas -gt 0) { throw "$falhas venv(s) falharam no teste de import." }
}

# ------------------------------------------------------------------ principal
$codigoSaida = 0
try {
    $modo = 'PLANO (nada e gravado nem baixado; para executar: instalar.cmd -Executar)'
    if (-not $Planejar) { $modo = 'EXECUTAR' }
    Escrever ('Oficina 3D v2 - instalador da Fase 1 - modo {0}' -f $modo)
    Escrever ('BASE = {0}' -f $Base)
    if ($script:LogArq) { Escrever ('log  = {0}' -f $script:LogArq) }
    foreach ($e in @('a', 'b', 'c', 'd', 'e', 'f', 'g')) {
        if ($Etapas -notcontains $e) { Escrever "== ($e) fora de -Etapas: pula"; continue }
        switch ($e) {
            'a' { Etapa-A }
            'b' { Etapa-B }
            'c' { Etapa-C }
            'd' { Etapa-D }
            'e' { Etapa-E }
            'f' { Etapa-F }
            'g' { Etapa-G }
        }
    }
    if ($Planejar) {
        if ($script:Pendencias.Count -gt 0) { Escrever ('PENDENTE antes de executar: ' + ($script:Pendencias -join '; ')) }
        if ($script:Pararia) { Escrever 'O plano PARARIA por falta de espaco.'; $codigoSaida = 2 }
        Escrever 'Fim do plano: nada foi gravado.'
    } else {
        Escrever 'Fim: todas as etapas pedidas terminaram.'
    }
} catch {
    Escrever ('ERRO: ' + $_.Exception.Message)
    $codigoSaida = 1
}
exit $codigoSaida
