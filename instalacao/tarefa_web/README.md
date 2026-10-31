# Tarefa Agendada da pagina web

Faz a pagina da Oficina 3D (http://127.0.0.1:8765) subir sozinha no logon do
usuario (plano v2, Fase 1 item 5). Espelho da tarefa do worker.

- Usuario atual, **sem admin**, so quando ele esta logado (`InteractiveToken`).
- Comeca **2 minutos** depois do logon, com **prioridade baixa**, sem janela.
- Sem limite de tempo; uma instancia so; o Agendador tenta de novo em falha.
- A acao roda `<BASE>\.venv_app\Scripts\pythonw.exe instalacao\tarefa_web\iniciar_web.py`
  com cwd = `app\`. O lancador carrega o `instalacao\env.cmd`, confere se a
  porta 8765 ja responde (nao sobe uma segunda web) e reinicia a web se ela
  cair (desiste depois de 5 quedas em 1 hora).
- Log: `<BASE>\_cache\logs\tarefa_web.log`.

## Registrar
Num prompt comum (nao precisa de admin), na pasta `app`:
```
instalacao\tarefa_web\registrar_tarefa.cmd
```
Conferir: `schtasks /Query /TN Oficina3D_Web /V /FO LIST`. Rodar agora:
`schtasks /Run /TN Oficina3D_Web`.

## Remover
```
instalacao\tarefa_web\registrar_tarefa.cmd /remover
```
