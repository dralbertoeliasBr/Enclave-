#!/usr/bin/env python3
"""
GUARDIÃO DOS REPOSITÓRIOS v1 — 09/11/2026
Conceito: Sounavy (Antônio Alberto Lopes Elias, ORCID 0000-0002-5602-9916)
Engenharia: Claude (Anthropic)

Arquivo único, sem dependências (só biblioteca padrão do Python).
O Guardião NUNCA apaga nada. Ele vigia, avisa, bloqueia e preserva.

Modos (detectados pelo evento do GitHub Actions):
  push          -> se algum arquivo foi apagado: cria ramo de resgate apontando
                   para o commit anterior (tudo preservado) e abre issue ALERTA.
  pull_request  -> procura comandos destrutivos nas linhas novas; se achar e o
                   PR não tiver a label OK-Sounavy, falha (bloqueia merge).
  schedule /
  workflow_dispatch -> diário de bordo (arquivo novo por dia, no ramo
                   guardiao-diario, com hash SHA-256) + checklist de documentos.

DRY_RUN=1 -> não chama a API do GitHub; só imprime o que faria (para teste).
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

LABEL_OK = "OK-Sounavy"
DOCS_OBRIGATORIOS = ["README.md", "LICENSE", "CITATION.cff", "AUTORIA.md"]
RAMO_DIARIO = "guardiao-diario"
EXTENSOES_TEXTO = (".md", ".txt", ".rst")  # v1.1: documentação não é comando
PADROES_DESTRUTIVOS = [
    r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f",     # rm -rf / rm -fr
    r"\brm\s+-[a-zA-Z]*f[a-zA-Z]*r",
    r"git\s+push\s+.*(--force|-f\b)",
    r"git\s+(branch|tag)\s+-[dD]\b",
    r"git\s+push\s+\S+\s+:\S+",          # git push origin :ramo (apaga ramo)
    r"git\s+reset\s+--hard",
    r"\bos\.remove\(",
    r"\bos\.unlink\(",
    r"\bos\.rmdir\(",
    r"shutil\.rmtree\(",
    r"\.unlink\(",
    r"DROP\s+(TABLE|DATABASE)",
    r"TRUNCATE\s+TABLE",
]

DRY = os.environ.get("DRY_RUN") == "1"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = os.environ.get("GITHUB_REPOSITORY", "local/teste")
API = os.environ.get("GITHUB_API_URL", "https://api.github.com")
HOJE = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
DATA = HOJE.strftime("%Y-%m-%d")


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def api(method, path, body=None):
    if DRY:
        print(f"[DRY_RUN] {method} {path} {json.dumps(body, ensure_ascii=False)[:400] if body else ''}")
        return {}
    req = urllib.request.Request(
        f"{API}/repos/{REPO}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            txt = r.read().decode()
            return json.loads(txt) if txt else {}
    except urllib.error.HTTPError as e:
        print(f"Aviso API {method} {path}: {e.code} {e.read().decode()[:300]}")
        return {}


def issue_aberta_com_titulo(titulo):
    if DRY:
        return False
    itens = api("GET", "/issues?state=open&per_page=100") or []
    return any(i.get("title") == titulo for i in itens if isinstance(i, dict))


def abrir_issue(titulo, corpo, labels=None):
    if issue_aberta_com_titulo(titulo):
        print(f"Issue já aberta: {titulo}")
        return
    api("POST", "/issues", {"title": titulo, "body": corpo, "labels": labels or ["guardiao"]})


# ---------------------------------------------------------------- push
def modo_push(evento):
    antes, depois = evento.get("before", ""), evento.get("after", "")
    if not antes or set(antes) == {"0"}:
        print("Push inicial ou ramo novo: nada a comparar.")
        return 0
    apagados = git("diff", "--name-only", "--diff-filter=D", antes, depois).splitlines()
    apagados = [a for a in apagados if a]
    if not apagados:
        print("Nenhum arquivo apagado neste push. Tudo preservado.")
        return 0
    autor = evento.get("pusher", {}).get("name", "desconhecido")
    ramo = evento.get("ref", "").replace("refs/heads/", "")
    resgate = f"resgate-{DATA}-{antes[:7]}"
    api("POST", "/git/refs", {"ref": f"refs/heads/{resgate}", "sha": antes})
    lista = "\n".join(f"- `{a}`" for a in apagados)
    corpo = (
        f"**O Guardião detectou {len(apagados)} arquivo(s) apagado(s).**\n\n"
        f"- Ramo: `{ramo}`\n- Quem enviou: `{autor}`\n- Commit: `{depois[:7]}`\n\n"
        f"{lista}\n\n"
        f"**Nada se perdeu.** O ramo `{resgate}` guarda o estado anterior, com todos os arquivos.\n"
        f"Se a deleção foi intencional, feche esta issue. Se não foi, restaure a partir do ramo de resgate "
        f"num arquivo/ramo novo (regra: correção em arquivo novo)."
    )
    abrir_issue(f"ALERTA Guardião: {len(apagados)} arquivo(s) apagado(s) em {depois[:7]}", corpo,
                ["guardiao", "alerta"])
    print(f"Resgate criado: {resgate} | apagados: {apagados}")
    return 0  # não falha o push: o push já aconteceu; o papel aqui é preservar e avisar


# ---------------------------------------------------------- pull_request
def achar_destrutivos(diff_texto):
    achados = []
    arquivo = "?"
    for linha in diff_texto.splitlines():
        if linha.startswith("+++ "):
            arquivo = linha[6:] if linha.startswith("+++ b/") else linha[4:]
            continue
        if linha.startswith("+") and not linha.startswith("+++"):
            # v1.1: texto de documentação só descreve comandos, não executa
            if arquivo.lower().endswith(EXTENSOES_TEXTO):
                continue
            for p in PADROES_DESTRUTIVOS:
                if re.search(p, linha, re.IGNORECASE):
                    achados.append((arquivo, linha[1:].strip()[:160], p))
                    break
    return achados


def modo_pull_request(evento):
    pr = evento.get("pull_request", {})
    base = pr.get("base", {}).get("sha", "")
    cabeca = pr.get("head", {}).get("sha", "")
    labels = [l.get("name") for l in pr.get("labels", [])]
    diff = git("diff", f"{base}...{cabeca}")
    achados = [a for a in achar_destrutivos(diff) if not a[0].startswith(".github/guardiao/")]
    apagados = [a for a in git("diff", "--name-only", "--diff-filter=D", f"{base}...{cabeca}").splitlines() if a]
    if not achados and not apagados:
        print("PR limpo: nenhum comando destrutivo, nenhum arquivo apagado.")
        return 0
    linhas = [f"- `{a}` → `{l}`" for a, l, _ in achados] + [f"- arquivo apagado: `{a}`" for a in apagados]
    msg = "**Guardião:** este PR tem ações destrutivas:\n\n" + "\n".join(linhas)
    if LABEL_OK in labels:
        print(msg + f"\n\nLabel {LABEL_OK} presente: liberado pelo dono.")
        return 0
    num = pr.get("number")
    if num:
        api("POST", f"/issues/{num}/comments",
            {"body": msg + f"\n\nO merge fica bloqueado até o dono pôr a label `{LABEL_OK}`."})
    print(msg)
    return 1


# --------------------------------------------------------------- diário
def hash_da_arvore(ref="HEAD"):
    listagem = git("ls-tree", "-r", ref)
    return hashlib.sha256(listagem.encode()).hexdigest()


def modo_diario():
    padrao = git("rev-parse", "--abbrev-ref", "HEAD")
    commits = git("log", "--since=24 hours ago", "--pretty=format:- `%h` %an — %s (%ad)", "--date=iso")
    selo = hash_da_arvore()
    texto = (
        f"# Diário de bordo — {DATA}\n\n"
        f"Repositório: `{REPO}` | ramo vigiado: `{padrao}`\n\n"
        f"## Mudanças nas últimas 24 horas\n\n{commits or '- Nenhuma mudança.'}\n\n"
        f"## Selo do dia (SHA-256 da árvore de arquivos)\n\n`{selo}`\n\n"
        f"Gerado pelo Guardião v1. Este arquivo nunca é editado; amanhã nasce outro.\n"
    )
    caminho = f"diario/{DATA}.md"
    if DRY:
        print(f"[DRY_RUN] escreveria {caminho} no ramo {RAMO_DIARIO}:\n{texto}")
    else:
        existe = api("GET", f"/contents/{caminho}?ref={RAMO_DIARIO}")
        if existe.get("sha"):
            print(f"{caminho} já existe: não reescrevo (regra: nunca editar o passado).")
        else:
            ramo_ok = api("GET", f"/branches/{RAMO_DIARIO}")
            if not ramo_ok.get("name"):
                api("POST", "/git/refs", {"ref": f"refs/heads/{RAMO_DIARIO}", "sha": git("rev-parse", "HEAD")})
            import base64
            api("PUT", f"/contents/{caminho}", {
                "message": f"Guardião: diário {DATA}",
                "content": base64.b64encode(texto.encode()).decode(),
                "branch": RAMO_DIARIO,
            })
    # checklist de documentos
    faltando = [d for d in DOCS_OBRIGATORIOS if not os.path.exists(d)]
    if faltando:
        corpo = "O Guardião encontrou documentos faltando:\n\n" + "\n".join(f"- [ ] `{d}`" for d in faltando)
        corpo += "\n\nCada um ajuda na autoria e na anterioridade. Crie em arquivo novo."
        abrir_issue("Guardião: documentos faltando", corpo, ["guardiao", "documentos"])
    print(f"Diário {DATA} | selo {selo[:16]}… | faltando: {faltando or 'nada'}")
    return 0


def main():
    nome = os.environ.get("GITHUB_EVENT_NAME", "workflow_dispatch")
    caminho = os.environ.get("GITHUB_EVENT_PATH")
    evento = json.load(open(caminho)) if caminho and os.path.exists(caminho) else {}
    if nome == "push":
        return modo_push(evento)
    if nome in ("pull_request", "pull_request_target"):
        return modo_pull_request(evento)
    return modo_diario()


if __name__ == "__main__":
    sys.exit(main())
