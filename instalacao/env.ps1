# Ambiente da Oficina 3D v2. Uso (dot-source):  . "<BASE>\app\instalacao\env.ps1"
# BASE = duas pastas acima desta (app\instalacao -> BASE). Tudo de cache fica em BASE\_cache.
# -SemCriar: so define as variaveis, nao cria pastas (usado pelo instalar.ps1 no modo plano).
# Arquivo so com ASCII de proposito (PowerShell 5.1 le .ps1 sem BOM como ANSI).
param([switch]$SemCriar)

$__o3dBase = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$__o3dBase = [System.IO.Path]::GetFullPath($__o3dBase)

# Guarda: nunca G:, Google Drive ou o espelho antigo Desktop\RPG Assimilacao.
$__o3dTeste = $__o3dBase.ToLowerInvariant()
if ($__o3dTeste.StartsWith('g:') -or $__o3dTeste.Contains('\desktop\rpg assimila') -or
    $__o3dTeste.Contains('google drive') -or $__o3dTeste.Contains('\meu drive') -or $__o3dTeste.Contains('\my drive')) {
    throw "env.ps1: OFICINA3D_BASE em lugar proibido (G:/Drive/Desktop): $__o3dBase"
}

$__o3dCache = Join-Path $__o3dBase '_cache'
$env:OFICINA3D_BASE        = $__o3dBase
$env:OFICINA3D_JOBS        = Join-Path $__o3dBase 'jobs'
$env:HF_HOME               = Join-Path $__o3dCache 'huggingface'
$env:HY3DGEN_MODELS        = Join-Path $__o3dCache 'hy3dgen'
$env:U2NET_HOME            = Join-Path $__o3dCache 'u2net'
$env:TEMP                  = Join-Path $__o3dCache 'tmp'
$env:TMP                   = $env:TEMP
$env:UV_CACHE_DIR          = Join-Path $__o3dCache 'uv'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $__o3dCache 'uv_python'
# uv: so Python gerenciado pelo uv (ignora o 3.12/3.13 do sistema); hardlink do cache para os venvs
# (mesmo disco: o torch ocupa espaco uma vez so nos dois venvs com torch).
$env:UV_PYTHON_PREFERENCE  = 'only-managed'
$env:UV_LINK_MODE          = 'hardlink'
$env:UV_NO_PROGRESS        = '1'
# PyTorch: pedido no plano 6.5. No Windows o PyTorch 2.5 pode avisar que nao suporta e ignorar (inofensivo).
$env:PYTORCH_CUDA_ALLOC_CONF = 'expandable_segments:True'
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = '1'
$env:HF_HUB_DISABLE_TELEMETRY = '1'
# Para rodar os motores sem rede depois que os modelos estiverem baixados:  $env:HF_HUB_OFFLINE = '1'

if (-not $SemCriar) {
    foreach ($__o3dP in @($env:OFICINA3D_JOBS, $env:HF_HOME, $env:HY3DGEN_MODELS, $env:U2NET_HOME, $env:TEMP,
                          $env:UV_CACHE_DIR, $env:UV_PYTHON_INSTALL_DIR, (Join-Path $__o3dCache 'logs'),
                          (Join-Path $__o3dBase 'locks'), (Join-Path $__o3dBase 'motores'))) {
        if (-not (Test-Path -LiteralPath $__o3dP)) { New-Item -ItemType Directory -Path $__o3dP -Force | Out-Null }
    }
}
Remove-Variable -Name __o3dTeste, __o3dP -ErrorAction SilentlyContinue
