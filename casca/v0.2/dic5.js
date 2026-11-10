// Motor do dicionário em camadas — porte fiel do ENCLAVE_v5.py (06/11/2026) para JavaScript.
// Conceito: Sounavy. Engenharia: Claude. Formato CLXD2:<8 do SHA>|<corpo>, "~xy" = entrada xy, "~~" = um ~.
// Um texto comprimido aqui abre no ENCLAVE_v5 do iPhone quando o dicionário tem o mesmo SHA.
var DIC5 = (function () {
  var ALFA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  var TIL = "~", CAB2 = "CLXD2:", MAX_PESSOAL = 1200, JANELA_PESSOAL = 300;
  var W = "[\\p{L}\\p{N}_]";
  var RE_OK = new RegExp("^" + W + "([^\\n]*" + W + ")?$", "u");
  var RE_PAL = new RegExp(W + "+", "gu");
  var RE_TOK = new RegExp(W + "+|[^\\p{L}\\p{N}_\\s]", "gu");
  var RE_ALNUM = /^[\p{L}\p{N}]+$/u;
  var enc = new TextEncoder();
  function nbytes(s) { return enc.encode(s).length; }
  function ncp(s) { return Array.from(s).length; }
  function pyStrip(s) { return s.replace(/^\s+|\s+$/g, ""); }
  function pySplit(s) { return s.split(/\s+/).filter(function (x) { return x; }); }
  function cmpPy(a, b) { var A = Array.from(a), B = Array.from(b), n = Math.min(A.length, B.length);
    for (var i = 0; i < n; i++) { var x = A[i].codePointAt(0), y = B[i].codePointAt(0); if (x !== y) return x < y ? -1 : 1; }
    return A.length - B.length; }
  async function sha256(s) {
    var b = await crypto.subtle.digest("SHA-256", enc.encode(s));
    return Array.from(new Uint8Array(b)).map(function (x) { return x.toString(16).padStart(2, "0"); }).join("");
  }
  function listaOk(lista, ja) {
    var vistos = new Set(ja || []), out = [];
    lista.forEach(function (x) {
      x = pyStrip(x);
      if (nbytes(x) >= 4 && x.indexOf(TIL) < 0 && !vistos.has(x) && RE_OK.test(x)) { vistos.add(x); out.push(x); }
    });
    return out;
  }
  function odontoEntradas(d) { return listaOk(d.ODONTO_FRASES.concat(pySplit(d.ODONTO_TXT))); }
  function montar(cam) {
    var e = listaOk(cam.lingua);
    e = e.concat(listaOk(cam.especialidade.entradas, e));
    e = e.concat(listaOk(cam.pessoal, e));
    return e.slice(0, 62 * 62);
  }
  async function fazer(cam, extra) {
    var e = montar(cam);
    var d = { camadas: cam, entradas: e, sha: await sha256(e.join("\n")) };
    for (var k in (extra || {})) d[k] = extra[k];
    return d;
  }
  async function fabrica(dados) {
    return fazer({ lingua: pySplit(dados.LINGUA_TXT),
                   especialidade: { nome: "odontologia", entradas: odontoEntradas(dados) }, pessoal: [] },
                 { versao: 0, origem: "base de fabrica" });
  }
  var cache = {};
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }   // no modo "u", "-" e "/" não podem ser escapados
  function maquina(d) {
    if (!cache[d.sha]) {
      var e = d.entradas, ordem = e.map(function (_, i) { return i; });
      ordem.sort(function (a, b) { return ncp(e[b]) - ncp(e[a]); });   // estável, como o sorted() do Python
      var pos = {}; e.forEach(function (x, i) { pos[x] = i; });
      cache[d.sha] = { pad: new RegExp("(?<!" + W + ")(?:" + ordem.map(function (i) { return esc(e[i]); }).join("|") + ")(?!" + W + ")", "gu"), pos: pos };
    }
    return cache[d.sha];
  }
  function comprimir(texto, d, achar) {
    var m = maquina(d);
    var corpo = texto.split(TIL).join(TIL + TIL).replace(m.pad, function (x) {
      var p = m.pos[x]; return TIL + ALFA[Math.floor(p / 62)] + ALFA[p % 62]; });
    var saida = CAB2 + d.sha.slice(0, 8) + "|" + corpo;
    if (descomprimir(saida, achar || function () { return d; }) !== texto) throw new Error("compressao nao voltou igual; nada entregue");
    return saida;
  }
  function descomprimir(pacote, achar) {
    if (pacote.indexOf(CAB2) !== 0 || pacote.indexOf("|") < 0) throw new Error("isso nao e um texto CLXD2");
    var resto = pacote.slice(CAB2.length), cut = resto.indexOf("|");
    var sha8 = resto.slice(0, cut), corpo = resto.slice(cut + 1);
    var d = achar(sha8);
    if (!d) throw new Error("nao tenho o dicionario " + sha8 + " nesta Casa");
    var e = d.entradas, out = [], i = 0;
    while (i < corpo.length) {
      var c = corpo[i];
      if (c !== TIL) { out.push(c); i++; continue; }
      if (corpo[i + 1] === TIL) { out.push(TIL); i += 2; continue; }
      var a = corpo[i + 1], b = corpo[i + 2];
      if (!a || !b || ALFA.indexOf(a) < 0 || ALFA.indexOf(b) < 0 || ALFA.indexOf(a) * 62 + ALFA.indexOf(b) >= e.length)
        throw new Error("codigo quebrado na posicao " + i);
      out.push(e[ALFA.indexOf(a) * 62 + ALFA.indexOf(b)]); i += 3;
    }
    return out.join("");
  }
  function estimarTokens(t) {
    return (t.match(RE_TOK) || []).reduce(function (s, p) {
      return s + (RE_ALNUM.test(p) ? Math.max(1, Math.floor((ncp(p) + 3) / 4)) : 1); }, 0);
  }
  function medir(texto, d) {
    var c = comprimir(texto, d);
    return { orig: nbytes(texto), dic: nbytes(c), tok_o: estimarTokens(texto), tok_d: estimarTokens(c),
             igual: descomprimir(c, function () { return d; }) === texto, pacote: c };
  }
  // camada PESSOAL: entra o que se repete nas últimas 300 falas, sai o que parou de ser falado
  async function aprender(atual, textos) {
    textos = textos.slice(0, JANELA_PESSOAL);
    var fixas = new Set(listaOk(atual.camadas.lingua).concat(atual.camadas.especialidade.entradas));
    var conta = new Map();
    textos.forEach(function (t) {
      var pal = t.match(RE_PAL) || [];
      for (var n = 1; n <= 4; n++) for (var i = 0; i + n <= pal.length; i++) {
        var f = pal.slice(i, i + n).join(" ");
        if ((n > 1 && t.indexOf(f) < 0) || fixas.has(f)) continue;
        conta.set(f, (conta.get(f) || 0) + 1);
      }
    });
    var ganho = [];
    conta.forEach(function (c, f) { if (c >= 2) ganho.push([(nbytes(f) - 3) * c - ncp(f), f]); });
    ganho.sort(function (x, y) { return x[0] - y[0] || cmpPy(x[1], y[1]); });
    var pessoal = ganho.reverse().filter(function (g) { return g[0] > 0; }).map(function (g) { return g[1]; }).slice(0, MAX_PESSOAL);
    var saiu = atual.camadas.pessoal.filter(function (f) { return pessoal.indexOf(f) < 0; }).length;
    var cam = { lingua: atual.camadas.lingua, especialidade: atual.camadas.especialidade, pessoal: pessoal };
    var d = await fazer(cam, { aprendeu_de: textos.length, sairam: saiu });
    return { d: d, novo: d.sha !== atual.sha, saiu: saiu };
  }
  return { fabrica: fabrica, fazer: fazer, aprender: aprender, comprimir: comprimir, descomprimir: descomprimir,
           medir: medir, estimarTokens: estimarTokens, listaOk: listaOk, sha256: sha256, CAB2: CAB2 };
})();
if (typeof module !== "undefined") module.exports = DIC5;
