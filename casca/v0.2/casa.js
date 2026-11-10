// A Casa do Enclave na casca (v0.2, 09/11/2026) — porte do ENCLAVE_v5: 10 boxes, Arquivista que lê por dentro,
// Black cifrada em 3 pedaços (2 de 3 reabrem), Doca que só cresce. Conceito: Sounavy. Engenharia: Claude.
var CASA = (function () {
  var PAPEL = {
    "00": { cor: "Inox", guarda: "quarentena: a porta de entrada" },
    "01": { cor: "Vermelho", guarda: "projetos, autobiografia, direitos autorais" },
    "02": { cor: "Laranja", guarda: "dados licenciáveis, só com o seu OK" },
    "03": { cor: "Amarelo", guarda: "trabalho, PDFs, textos, sessões" },
    "04": { cor: "Verde", guarda: "rotinas, hábitos, o que foi aprendido" },
    "05": { cor: "Azul", guarda: "fotos, áudio, memórias afetivas" },
    "06": { cor: "Anil", guarda: "reservada: o papel você define" },
    "07": { cor: "Violeta", guarda: "códigos e memória da GaIA" },
    "08": { cor: "Black", guarda: "privado: nunca sai, 3 pedaços" },
    "09": { cor: "Doca", guarda: "diário do Arquivista, só cresce" }
  };
  var PADROES_PRIVADOS = [["CPF", /\b\d{3}\.?\d{3}\.?\d{3}-\d{2}\b/], ["cartão", /\b(?:\d{4}[ -]){3}\d{4}\b/],
    ["e-mail", /[\w.+-]+@[\w-]+\.[\w.]+/], ["telefone", /\(?\b\d{2}\)?\s?9\d{4}-\d{4}\b/], ["CEP", /\b\d{5}-\d{3}\b/]];
  var PALAVRAS_PRIVADAS = ["senha", "password", "api_key", "apikey", "token", "segredo", "prontuario", "laudo", "paciente",
    "contrato", "rg ", "conta bancaria", "pix", "cofre", "privado"];
  var PALAVRAS_PROJETO = ["projeto", "gaia", "enclave", "livro", "tese", "capitulo", "clinica", "ideia", "arquitetura", "manifesto", "zenodo"];
  var enc = new TextEncoder(), dec = new TextDecoder();
  function semAcento(t) { return t.toLowerCase().normalize("NFD").replace(/\p{Mn}/gu, ""); }
  function privados(texto) {
    var achou = PADROES_PRIVADOS.filter(function (p) { return p[1].test(texto); }).map(function (p) { return p[0]; });
    var t = semAcento(texto);
    PALAVRAS_PRIVADAS.forEach(function (w) { if (t.indexOf(w) >= 0) achou.push("palavra “" + w.trim() + "”"); });
    if (/sk-[A-Za-z0-9_-]{16,}/.test(texto)) achou.push("chave de API");
    return achou;
  }
  function classificar(texto) {   // lê por dentro, nunca pelo nome
    if (/^\s*(def |class |import |from \w+ import |function |const |#!|<!doctype|<html)/im.test(texto)) {
      var reais = PADROES_PRIVADOS.filter(function (p) { return p[1].test(texto); }).map(function (p) { return p[0]; });
      if (/sk-[A-Za-z0-9_-]{16,}/.test(texto)) reais.push("chave de API");
      return reais.length ? ["08", "código com segredo: " + reais.slice(0, 3).join(", ")] : ["07", "código"];
    }
    var pv = privados(texto);
    if (pv.length) return ["08", "privado: " + pv.slice(0, 3).join(", ")];
    var t = semAcento(texto);
    var achou = PALAVRAS_PROJETO.filter(function (w) { return new RegExp("\\b" + w + "\\b").test(t); });
    if (achou.length) return ["01", "projeto: " + achou.slice(0, 3).join(", ")];
    return ["03", "texto geral"];
  }
  function dois(n) { return String(n).padStart(2, "0"); }
  function carimbo(d) { return d.getFullYear() + dois(d.getMonth() + 1) + dois(d.getDate()) + "-" + dois(d.getHours()) + dois(d.getMinutes()) + dois(d.getSeconds()); }
  function nomeInfo(cx, quando, selo) { return "7" + cx + "-" + carimbo(quando) + "-" + selo.slice(0, 8); }
  async function sha(bytes) { var b = await crypto.subtle.digest("SHA-256", bytes);
    return Array.from(new Uint8Array(b)).map(function (x) { return x.toString(16).padStart(2, "0"); }).join(""); }
  function b64(u) { var s = ""; u.forEach(function (x) { s += String.fromCharCode(x); }); return btoa(s); }
  function deb(s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); }
  function xor(a, b) { var o = new Uint8Array(a.length); for (var i = 0; i < a.length; i++) o[i] = a[i] ^ b[i]; return o; }
  async function chaveDe(senha, sal) {
    var base = await crypto.subtle.importKey("raw", enc.encode(senha), "PBKDF2", false, ["deriveKey"]);
    return crypto.subtle.deriveKey({ name: "PBKDF2", salt: sal, iterations: 200000, hash: "SHA-256" }, base,
      { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
  }
  async function trancar(senha, dados) {     // pacote = sal(16) + iv(12) + cifra AES-GCM
    var sal = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12));
    var ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv: iv }, await chaveDe(senha, sal), dados));
    var p = new Uint8Array(28 + ct.length); p.set(sal); p.set(iv, 16); p.set(ct, 28); return p;
  }
  async function destrancar(senha, p) {
    return new Uint8Array(await crypto.subtle.decrypt({ name: "AES-GCM", iv: p.slice(16, 28) }, await chaveDe(senha, p.slice(0, 16)), p.slice(28)));
  }
  function dividirEm3(p) {                   // igual ao v5: A, B e A^B — quaisquer 2 reconstroem
    var m = Math.ceil(p.length / 2), A = p.slice(0, m), B = new Uint8Array(m); B.set(p.slice(m));
    return [A, B, xor(A, B)];
  }
  function juntar2(ped, tam) {
    var A = ped[1] || xor(ped[2], ped[3]), B = ped[2] || xor(ped[1], ped[3]);
    var o = new Uint8Array(A.length + B.length); o.set(A); o.set(B, A.length); return o.slice(0, tam);
  }
  function nova() { return { itens: [], doca: [], dics: [] }; }
  async function arquivar(casa, texto, senha, quando) {
    quando = quando || new Date();
    var cl = classificar(texto), cx = cl[0], dados = enc.encode(texto), h = await sha(dados);
    var dup = casa.itens.find(function (i) { return i.sha === h && i.cx === cx; });
    if (dup) return { status: "STOP", item: dup, motivo: cl[1] };
    var it = { cx: cx, nome: nomeInfo(cx, quando, h), quando: quando.toISOString(), sha: h, tamanho: dados.length, motivo: cl[1] };
    if (cx === "08") {
      var pac = await trancar(senha, dados), ped = dividirEm3(pac);
      it.black = { p: ped.map(b64), tam: pac.length, selo_pacote: await sha(pac) };
    } else { it.texto = texto; }
    casa.itens.push(it);
    return { status: "GO", item: it, motivo: cl[1] };
  }
  async function reabrirBlack(it, senha, sem) {
    var ped = {};
    [1, 2, 3].forEach(function (i) { if (i !== sem) ped[i] = deb(it.black.p[i - 1]); });
    var pac = juntar2(ped, it.black.tam);
    if ((await sha(pac)) !== it.black.selo_pacote) throw new Error("pedaço adulterado");
    var dados = await destrancar(senha, pac);
    if ((await sha(dados)) !== it.sha) throw new Error("selo não confere");
    return dec.decode(dados);
  }
  async function confere(it) { return it.cx === "08" ? true : (await sha(enc.encode(it.texto))) === it.sha; }
  function doca(casa, linhas) { casa.doca.push({ ts: new Date().toISOString(), linhas: linhas }); }
  function falasRecentes(casa) {
    return casa.itens.filter(function (i) { return i.cx !== "08" && i.texto && !privados(i.texto).length; })
      .sort(function (a, b) { return a.quando < b.quando ? 1 : -1; }).map(function (i) { return i.texto; });
  }
  return { PAPEL: PAPEL, classificar: classificar, privados: privados, arquivar: arquivar, reabrirBlack: reabrirBlack,
           confere: confere, doca: doca, nova: nova, falasRecentes: falasRecentes, semAcento: semAcento };
})();
if (typeof module !== "undefined") module.exports = CASA;
