# Guardião v1.1 — 09/11/2026

Correção registrada em arquivo novo, sem apagar o v1.

**O que aconteceu:** no PR #1, o Guardião barrou o próprio manual (`GUARDIAO.md`), porque ele cita `rm -rf` como exemplo. Foi um falso alarme.

**Correção:** a busca por comandos destrutivos agora ignora textos de documentação (`.md`, `.txt`, `.rst`). Os arquivos apagados continuam vigiados em qualquer tipo de arquivo.

**Testes (6 de 6 como esperado):**
- Manual citando comandos: liberado.
- Nota `.md` citando `rm -rf`: liberado.
- Script `.sh` com `rm -rf`: bloqueado.
- Python com `shutil.rmtree`: bloqueado.
- O mesmo, com a label `OK-Sounavy`: liberado.
- PR que apaga o `README.md`: bloqueado.
