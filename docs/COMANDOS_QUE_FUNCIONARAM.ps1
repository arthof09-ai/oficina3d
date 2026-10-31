# COMANDOS QUE FUNCIONARAM (na ordem), para reproduzir a Oficina 3D v2 do zero no CUNHADO-PC.
# Só entra aqui o que foi executado e deu certo. Vira a base do instalacao\instalar.ps1.

# 1. Pastas e repositório (31/10/2026)
$b = "C:\Users\txcga\RPG_Local\Oficina3D"
foreach ($d in 'motores','_cache','jobs','jobs_teste','locks') { New-Item -ItemType Directory -Force "$b\$d" | Out-Null }
# Primeira vez: gh repo create arthof09-ai/oficina3d --private --clone  (depois renomear a pasta para app)
# Reinstalação: git clone https://github.com/arthof09-ai/oficina3d.git "$b\app"
