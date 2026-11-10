# REGISTRO — Casca do Enclave v0.2 (09/11/2026, 22:35)
Conceito: Sounavy. Engenharia e testes: Claude. Acordo ético v1 (selo 70706526). Arquivo novo; nada anterior foi alterado.

## O que é
A casca web (Safari do iPhone) com o cérebro do ENCLAVE_v5:
- **10 boxes** na numeração do v5: 00 Inox · 01 Vermelho · 02 Laranja · 03 Amarelo · 04 Verde · 05 Azul · 06 Anil · 07 Violeta · 08 Black · 09 Doca.
- **Arquivista** lê por dentro (nunca pelo nome): privado → Black; código → Violeta (código com segredo → Black); projeto → Vermelho; resto → Amarelo. Stop/Go: o mesmo conteúdo na mesma caixa não entra duas vezes.
- **Nome inteligente**: 7 + caixa + AAAAMMDD-HHMMSS + 8 do SHA-256 (o texto nunca entra no nome). Ex.: 703-20261109-223338-c4139856.
- **Dicionário em 3 camadas** portado do v5: língua 1.800 + odontologia 176 + pessoal (aprende das últimas 300 falas). Formato CLXD2 idêntico. Cada versão nova é guardada; texto antigo continua abrindo.
- **Black**: AES-GCM + 3 pedaços (A, B, A⊕B); quaisquer 2 reabrem. Senha de teste ("trava falsa", decisão de 06/11).
- **Doca**: diário que só cresce.

## Provas (rodadas, não suposições)
- Motor JS × código do v5 em Python, mesmos textos: SHA de fábrica **27f35b93** igual; 10 textos comprimidos idênticos; tokens estimados iguais; camada pessoal aprendida idêntica (mesmo SHA).
- Frase de consultório: **106 → 60 bytes**, igual ao FIO do v5.
- Texto comprimido na casca foi aberto pelo método do v5 em Python: voltou igual.
- Casa em node: 13 de 13. Página no Chrome (390 px, tela de iPhone): autoteste **18 de 18**, nenhum erro de JavaScript, sem rolagem lateral, dados persistem ao recarregar.
- NÃO testado ainda no iPhone real.

## Limites honestos
- A casca guarda só neste aparelho (navegador). Para levar: "Copiar a Casa" → Drive.
- Selo da casca é SHA-256 (sem senha); no v5 é HMAC com a senha. Os nomes ficam no mesmo formato, mas o selo de um não confere o outro.
- O texto de exemplo com a palavra "paciente" vai para a Black: regra do v5 (LGPD), de propósito.

## SHA-256 dos arquivos
- 2f80b3d1b0e6dcf86f60b046050d18c2de5ead1b041274d1a9b3b3cdfae0edde  enclave-casa-v0.2.html
- 75cbe0661263908355d81df9534dc5a6f7cb517a4e973d4f86ac139a3c29850e  dic5.js
- 9528e78c12e17cbdfccb787bd21686c701b5acc48899289fab82519585fdeb7a  casa.js
- 23d147446a7c78cd042cad003b64c169876a8ca1212f06c5bbd60b6a2826859e  dados_v5.js
