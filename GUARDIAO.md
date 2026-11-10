# Guardião dos Repositórios v1 — 09/11/2026

Conceito: Sounavy (Antônio Alberto Lopes Elias, ORCID 0000-0002-5602-9916). Engenharia: Claude (Anthropic).

O Guardião nunca apaga nada. Ele vigia, avisa, bloqueia e preserva.

| Quando | O que faz |
|---|---|
| Push que apaga arquivo | Cria o ramo `resgate-DATA-commit` com tudo de volta e abre issue ALERTA |
| PR com `rm -rf`, `--force`, `os.remove`, `shutil.rmtree`, arquivo apagado… | Bloqueia o merge até a label `OK-Sounavy` |
| Todo dia 00:17 (Brasília) | Diário novo em `diario/AAAA-MM-DD.md` no ramo `guardiao-diario`, com selo SHA-256 |
| Todo dia | Issue pedindo README, LICENSE, CITATION.cff e AUTORIA.md se faltarem |

Testado em 09/11/2026 em repositório simulado (modo DRY_RUN): 7 de 7 cenários com o resultado esperado.
Ainda não rodou no GitHub de verdade: isso acontece quando este ramo entrar no main.
