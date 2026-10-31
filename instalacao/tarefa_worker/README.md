# Tarefa Agendada do worker

Faz o worker da Oficina 3D subir sozinho no logon do usuário (plano v2, Fase 1 item 4).

- Usuário atual, **sem admin**, só quando ele está logado (`InteractiveToken`).
- Começa **2 minutos** depois do logon, com **prioridade baixa**, sem janela.
- Sem limite de tempo; uma instância só; o Agendador tenta de novo em falha (3x a cada 5 min).
- A ação roda `<BASE>\.venv_app\Scripts\pythonw.exe instalacao\tarefa_worker\iniciar_worker.py`
  com cwd = `app\`. O `iniciar_worker.py` carrega o `instalacao\env.cmd`, confere o
  `worker.lock` (não abre um segundo worker), roda `pythonw -m oficina3d.worker` e o
  reinicia se cair (desiste depois de 5 quedas em 1 hora).
- Log: `<BASE>\_cache\logs\tarefa_worker.log`.
- O próprio worker pausa quando outro programa usa a GPU (`oficina3d.travas.gpu_ocupada_por_outros`)
  e quando o C: fica abaixo de 20 GB (`oficina3d.saude.disco_ok`).

## Registrar
Num prompt comum (não precisa de admin), na pasta `app`:
```
instalacao\tarefa_worker\registrar_tarefa.cmd
```
Para só ver o XML final sem registrar: `registrar_tarefa.cmd /gerar` (grava em `<BASE>\_cache\tmp\`).

Conferir: `schtasks /Query /TN Oficina3D_Worker /V /FO LIST`. Rodar agora: `schtasks /Run /TN Oficina3D_Worker`.

## Remover
```
instalacao\tarefa_worker\registrar_tarefa.cmd /remover
```
(ou `schtasks /Delete /TN Oficina3D_Worker /F`). Para parar só agora: `schtasks /End /TN Oficina3D_Worker`.

## Se o schtasks recusar (acesso negado)
Alternativa sem tarefa: criar na pasta Inicializar (`shell:startup`) um atalho para
`<BASE>\.venv_app\Scripts\pythonw.exe` com o argumento
`"<APP>\instalacao\tarefa_worker\iniciar_worker.py"` e "Iniciar em" = `<APP>`
(sem o atraso de 2 min e sem a prioridade baixa da tarefa; o lançador já baixa a prioridade do worker).
