#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLXD2_PONTE.py  (09/11/2026)  -  bloco unico. Cole no Pythonista e aperte Play.
Conceito: Sounavy. Engenharia e testes: Claude. Acordo etico v1 (selo 70706526).
Nao mexe em nada do ENCLAVE_v5 (nem na Casa): so le a area de transferencia e mostra.

O que faz:
  1) Se voce copiou um texto CLXD2:... (da casca ou do v5), ABRE e mostra a frase original.
  2) Se copiou um texto comum, COMPRIME de dois jeitos e mede:
       - GUARDAR: troca tudo o que esta no dicionario (menos bytes; e o formato do v5).
       - IA     : so troca quando economiza token (palavra longa e expressao); se nem assim
                  compensar (o cabecalho tambem custa), manda o TEXTO PURO. Para mandar a uma IA.
     Os dois abrem com o MESMO decodificador (o do v5): so muda o que foi trocado.
  3) Roda um autoteste curto.
Dicionario: o de fabrica do ENCLAVE_v5 (lingua 1800 + odontologia 176), SHA 27f35b93.
As camadas NAO viajam: o dicionario fica nos dois lados; so os codigos ~xy viajam.
Tokens = ESTIMATIVA (so o contador do Claude da o numero real).
"""
import re, hashlib

LINGUA_TXT = "não você para está isso como aqui mais muito estou vamos tudo minha então pode agora quando fazer eles nós tenho estava certo quer sabe quem nada disse onde quero são dizer posso acho sobre porque mesmo coisa todos estão algo até tempo assim nunca vocês esse casa quê essa também ainda tão cara favor melhor noite temos obrigado talvez estamos esta deus alguém mãe vida senhor este isto sempre anos verdade seus dele ficar parece claro depois tinha falar coisas antes pessoas pouco pelo preciso apenas homem deve dois fazendo todo lugar acha fora estar qual disso trabalho precisa hoje ninguém novo queria comigo mundo saber alguma podemos grande sinto seja nossa poderia dinheiro suas será nome quanto qualquer pela outro dela nosso meus desculpe filho certeza vão hora outra sair toda volta problema obrigada olá tipo realmente sabia aconteceu menos mulher algum diga falando espere ótimo carro vezes amigo primeiro deveria seria venha três entre daqui sério voltar parte amor feliz embora família olhe deixar atrás tenha faça pensei ajudar todas olha aquele duas querida frente indo alguns dias lado podem merda pare tarde gosto precisamos caso fique dentro cidade momento pegar foram nenhum gente somos amanhã fosse cabeça gostaria amigos enquanto homens logo deles desde tanto garota pessoa legal rápido algumas cada jeito tentando meio outros têm medo minhas importa irmão errado história primeira quase horas encontrar nova essas pessoal difícil forma contra matar semana dizendo perto demais entrar esses achei deixe vejo polícia espero sido juntos ajuda caminho nisso elas quiser crianças manhã aquela sorte morte pensar papai veja fica teve quarto levar filha feito minutos morto porta tive entendo cima acabou chegar veio água mesma significa teria pronto esposa acredito ouvir gosta morrer nossos olhos garoto última coração contar importante jogo acontecendo razão mãos devo ideia consigo idiota passar havia problemas parar senhora corpo chefe poder mamãe cuidado começar espera ficou conta exatamente arma longe escola tentar pois terra droga ontem pensando única devia sendo causa guerra chance usar marido mão numa trabalhar sangue música esperar querem nenhuma tivesse digo estranho maior velho faço boca houve festa estavam fala mulheres conhece ouvi tirar esperando podia licença capitão preocupe comer fácil deixa novamente além irmã meses eram suficiente pais segundo sabemos muitas cinco bebê matou querido muita idéia saia muitos número deixou conseguir lembra dessa morreu tomar bastante neste maneira quatro filhos acontecer criança dormir durante possa desse vindo certa café possível casamento irá acordo quis equipe conheço ruim culpa jantar provavelmente consegue telefone esteja forte sentir viver chegou diferente sozinho prazer pergunta procurando iria terá conseguiu outras final minuto sala chega único nossas falta desta aquilo incrível devemos direito nessa vivo mudar faria porra perder falou segurança pagar plano descobrir conversar achar próxima sabem comida pegue diabos trás jovem trouxe acreditar olhar cama ponto passado pena colocar tchau nesse fale ouça nele calma filme pedir sente louco palavra pequeno john caras ouviu próximo médico pensa ligar pior força mostrar país acontece fogo entende baixo acabar continuar estiver lembro dizem srta vendo jogar livro adeus perguntar existe manter fazem cedo querer desculpa jack semanas estes começou hospital atenção seis linda último chamar escritório falei estávamos especial comprar após resto fiquei alô saiu ganhar controle fico brincando volte nesta garotas queremos presidente pegou real devem aonde precisar negócio doutor esteve encontro pelos escute finalmente estado cuidar armas aqueles umas dólares fato sentido pequena prisão casar trabalhando escolha puta amiga sozinha próprio cabelo deste estivesse engraçado policial perfeito passou alto palavras livre mente seguro menina própria bonito futuro entendi esqueça respeito entender estará visto estas agente sinal grupo andar presente milhões rosto mesa foto preso leve partir consegui sexo assassino pense chamado daí pediu jesus situação olhando perdeu voltou grandes modo viagem sistema rapazes simples linha achou entendeu estive salvar boas conhecer estaria emprego chama bonita conosco melhores mensagem michael contou idade crime questão trazer usando local simplesmente lindo tente encontrei ficará acredita levou precisam farei doente natal professor odeio rapaz motivo disseram fizeram seguir ótima programa campo normal continue vontade graças menino chão soube acabei perguntas surpresa lista sonho olho terminar irei resposta beber ordem encontrou senhores peguei hotel caixa quente povo acidente erro precisava diria advogado mortos aniversário inferno ataque david charlie vale frank fotos show abrir parabéns fome voce tiver ficando totalmente morta loja naquela energia conversa pelas espaço serviço monte assassinato negócios banco reunião estarei completamente george divertido ligou segunda perdi fundo lutar pudesse explicar fomos tome notícias céu trabalha exército mês mike parecia passa fará continua tire olhada tivemos carta lembrar roupas contato detetive passada fizemos papel área governo abra interessante horrível luta dando beleza certamente apartamento banheiro mudou capaz metade penso funciona tentei procurar tradução velha triste prometo prova barco bons tentou hein quantos senti decisão tenente bebida teremos através conselho avião juro saindo nela tocar breve pronta ligue frio anda missão chave lamento tinham impossível peça igreja namorado terrível maravilhoso namorada haver maioria tendo segredo leva verdadeiro viva naquele saiba roupa sete vítima drogas nave assunto mandou imediatamente diferentes ajude cair fazemos ouro loucura time vidas pobre ouvindo faremos puder vista começa alma aposto desses fazia paul general mestre adoro senhorita celular oficial cavalo companhia somente esquecer james peter parecer serão padre começo louca buscar esperava dito centro época estrada carne vestido posição cheio fugir meninas teste entrou maldito chamada ligação saúde diferença junto planeta duro passo bela proteger longo cachorro chegando embaixo coloque delas guarda escrever conheci cliente igual mandar bater falo pensou basta gostei encontramos porquê costas provar segundos lugares esquerda ambos coronel chame pés direita acredite aprender correr empresa dessas últimos cérebro informação perigo bola acham relação doce desculpas garotos destino sentindo deixei branco quais gostar cerca cerveja resolver serei regras cena creio norte público caiu sentar tiro oportunidade cozinha ficaria inteligente poderíamos toque propósito chá várias base york faculdade humano graça ordens lidar direto comandante cantar henry honra trem ação importo senhoras prontos depressa direção perigoso confiar sargento existem oito animais cheiro experiência clube mary queira volto sonhos esqueci estúpido justo janela corte saco sucesso quantas lixo desejo aceitar pedi deveríamos quão escuta vinho necessário terei preocupado saída dançar poderá rainha comum liberdade pega entendido disto tempos tanta dormindo tribunal chamou verão repente steve parecem vender belo máquina silêncio tínhamos informações receber meia passei mentira paris exemplo contrário raiva aula conseguimos socorro lhes liga escolher tornar cadê humanos ligo preocupar venham atirar azul pressão série perdido jamais vermelho exceto colocou legenda inteiro comando harry cartão paciente diretor esperança ilha câmera notícia errada sarah danny revisão devagar parem achamos banho américa traga conte bolsa excelente andando alta jimmy aquelas bomba adam preço iremos alex vive esconder arte começando jovens passando ocupado bill jane pedido cão sequer parceiro suspeito pele nível opinião pista emergência computador seguinte planos policiais irmãos daquele ônibus batalha nick rádio acaba prefiro tony fiquem perdão haverá livros apesar justiça dança braço costumava will líder cale pego vergonha criar almoço coragem risco pude roubar vários roubou negro espírito cansado defesa gostou principal novos bunda especialmente peço cartas enorme funcionar imaginar inimigo ganhou brilhante entra londres julgamento cheia pernas aparecer longa trata tirou juiz estrela ficam segura piada mora felizes inteira realidade procura relatório dizia saiam sapatos irão estação falamos restaurante responsável merece diante flores carros billy novas viram percebi dúvida conhecemos provas sejam evitar alvo tenham nomes pedaço destruir gato classe apareceu cheguei subir brincar buraco meninos infelizmente soldados gentil herói usou cadeia filmes morrendo acima gelo corrida xerife caramba busca suponho visão estás richard investigação yeah pedindo limpar árvore mentindo soubesse inglês estranha vídeo início fizer correndo endereço prédio tommy tamanho praia vieram nervoso havendo laboratório parede brincadeira amar cortar entrada super johnny descobriu vemos matei natureza metros idiotas testemunha projeto carreira deixando navio limpo comecei código responder gostava movimento ridículo estilo bravo jornal terminou bêbado pedra animal inocente toma mudança escreveu dados poderiam peixe jake americano velhos memória departamento pergunte contigo confiança estrelas absolutamente afinal contas adoraria floresta total dirigir obviamente episódio vimos major pescoço mark olhem preparar mantenha grávida vejam processo clientes entregar temporada diabo cadeira maria soldado esperem pôr tira assistir agradeço coma agradecer eddie chris férias desafio monstro histórias redor sentimentos menor virar perna operação esqueceu chegamos visita caro imagem escapar bala cristo apresentar conhecia distância chorar faca vencer definitivamente particular amava nariz fantástico milhares pontos braços branca dado nove perfeita perguntou beijo quieto prestes decidir troca ficarei verde seguida universo virá abaixo antigo madame passe apoio robert moça mercado imagino escuro bolo conhecido banda detalhes valor recebi doença relógio caminhão médicos rico espécie sabendo culpado presa perdendo dentes barulho tornou ryan cavalos agradável arrumar poucos baby parou máximo política majestade gostam parque kevin ponha leite quebrar concordo discutir desistir comprou levantar perdemos salvou daquela velocidade éramos bobby comece avó cirurgia milhão acesso chaves machucar marca dever cinema vêm relaxe livrar mesmos vento chamam preocupada encontrado ajudou depende ficamos verdadeira acabado recebeu portanto sobreviver fechar ganha permissão jogando noites levando princesa maldição disser vadia ruas possamos briga manda pensava desapareceu vítimas bateu anel pago maldita normalmente parado dono descansar palco maravilhosa come tiveram ponte noiva termos casado língua ouvido peso trocar debaixo fugiu unidos estaremos tomou comprei correto relacionamento obter controlar daniel humana calças martin matt orgulho acordar daria interesse garrafa mostre estados façam mentir dedos eric contrato salvo charles sentado aberta ameaça deveriam esperto corpos americanos conheceu descer vovó perguntando deram casos decidiu futebol camisa odeia forças aparentemente avô descobri querendo brian maiores central nacional sociedade táxi voar luzes agir enviar teoria veremos oferta cansada frança inglaterra preto ligado resultado profissional direi antiga rachel responda traz perda fantasma altura calor devíamos maluco assistente contei vitória perguntei números feita adorável chapéu divertir kelly morar jardim colega verá senão verificar príncipe scott porco mostra pessoalmente natural decidi terão serem enfim fonte motorista confie escolheu visitar diversão universidade terceiro juntar unidade responsabilidade firme artista deixado liguei pesquisa pressa rapidamente momentos consertar legendas anna próximos servir okay usado cala quebrou voltei escrito ficaram casal simon casas oeste tantas larry interessado casaco aberto encontre lisa canção chuva quisesse espada pequenos bordo voltando demorar ensinar achava mata acabamos mentiu jeff acaso portas valeu pensam modelo dedo sábado pertence baile pegamos geral atrasado parada viemos torna ajudando chegaram entanto dão seguindo proteção fita armário chamando thomas washington kate santo crédito segure jogos dói imprensa jason honesto aviso acampamento atirou serve coloquei vovô queriam interessa objetivo grana construir inimigos sensação mande competição militar paga funcionando corra morre orgulhoso tenta besteira nasceu propriedade darei partido enfermeira enviou encontraram roubo apaixonado membro chocolate internet domingo segredos mandei deseja corredor sinais material sexual devido smith acorde lance ovos lago atacar primo toca felicidade saí levante partes membros presos pão carona montanha passagem prefeito confusão peito rock venho inútil vingança topo contente invés ferido humor curso lição aeroporto original sentiu caralho prêmio"
ODONTO_TXT = "odontologia dentista paciente consulta consultório anamnese radiografia panorâmica tomografia periapical interproximal bruxismo apertamento articulação temporomandibular disfunção temporomandibular côndilo disco articular masseter temporal pterigóideo músculo mastigação oclusão maloclusão placa miorrelaxante placa oclusal desgaste dentário abfração erosão retração gengival gengiva gengivite periodontite periodonto bolsa periodontal sondagem sangramento raspagem alisamento radicular implante implantes osseointegração enxerto ósseo levantamento de seio pilar protético coroa prótese prótese total prótese parcial removível ponte fixa faceta lente de contato restauração resina composta amálgama ionômero canal tratamento endodôntico endodontia pulpite necrose pulpar abscesso fístula extração exodontia terceiro molar siso incisivo canino pré-molar molar maxila mandíbula palato língua mucosa saliva cárie biofilme flúor profilaxia clareamento ortodontia aparelho alinhador harmonização orofacial toxina botulínica preenchimento ácido hialurônico dor orofacial cefaleia isquemia inflamação crônica plexo venoso pterigoideo anestesia anestésico lidocaína articaína antibiótico amoxicilina analgésico anti-inflamatório ibuprofeno dipirona prescrição orçamento retorno agendamento prontuário odontograma plano de tratamento sensibilidade dentinária hipersensibilidade fratura dentária trinca oclusão cêntrica relação cêntrica guia canina lateralidade protrusão"
ODONTO_FRASES = ["articulação temporomandibular", "disfunção temporomandibular", "disco articular", "placa miorrelaxante", "placa oclusal", "desgaste dentário", "retração gengival", "bolsa periodontal", "alisamento radicular", "enxerto ósseo", "levantamento de seio", "pilar protético", "prótese total", "prótese parcial removível", "ponte fixa", "lente de contato", "resina composta", "tratamento endodôntico", "necrose pulpar", "terceiro molar", "harmonização orofacial", "toxina botulínica", "ácido hialurônico", "dor orofacial", "inflamação crônica", "plexo venoso", "plano de tratamento", "sensibilidade dentinária", "fratura dentária", "oclusão cêntrica", "relação cêntrica", "guia canina"]

ALFA = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
TIL, CAB2 = "~", "CLXD2:"


def _lista_ok(lista, ja=()):
    vistos, out = set(ja), []
    for x in lista:
        x = x.strip()
        if len(x.encode("utf-8")) >= 4 and TIL not in x and x not in vistos and re.match(r"^\w(.*\w)?$", x):
            vistos.add(x); out.append(x)
    return out


def fabrica():
    e = _lista_ok(LINGUA_TXT.split())
    e += _lista_ok(_lista_ok(ODONTO_FRASES + ODONTO_TXT.split()), e)
    e = e[:62 * 62]
    return {"entradas": e, "sha": hashlib.sha256("\n".join(e).encode("utf-8")).hexdigest()}


D = fabrica()


def estimar_tokens(t):
    return sum(max(1, (len(p) + 3) // 4) if p.isalnum() else 1 for p in re.findall(r"\w+|[^\w\s]", t))


def comprimir(texto, modo="guardar", d=D):
    e = d["entradas"]
    usar = range(len(e))
    if modo == "ia":                       # so troca quando a entrada custa mais token que o codigo (~xy = 2)
        usar = [i for i in usar if estimar_tokens(e[i]) > 2]
    ordem = sorted(usar, key=lambda i: -len(e[i]))
    pad = re.compile(r"(?<!\w)(?:" + "|".join(re.escape(e[i]) for i in ordem) + r")(?!\w)")
    pos = {x: i for i, x in enumerate(e)}
    corpo = pad.sub(lambda m: TIL + ALFA[pos[m.group(0)] // 62] + ALFA[pos[m.group(0)] % 62],
                    texto.replace(TIL, TIL + TIL))
    saida = CAB2 + d["sha"][:8] + "|" + corpo
    if abrir(saida) != texto:
        raise ValueError("nao voltou igual; nada entregue")
    return saida


def abrir(pacote, d=D):
    pacote = pacote[pacote.index(CAB2):] if CAB2 in pacote else pacote
    if not pacote.startswith(CAB2) or "|" not in pacote:
        raise ValueError("isso nao e um texto CLXD2")
    sha8, corpo = pacote[len(CAB2):].split("|", 1)
    if not d["sha"].startswith(sha8):
        raise ValueError("dicionario {} nao e o de fabrica (27f35b93). Abra no ENCLAVE_v5.".format(sha8))
    e, out, i = d["entradas"], [], 0
    while i < len(corpo):
        c = corpo[i]
        if c != TIL:
            out.append(c); i += 1; continue
        if corpo[i + 1:i + 2] == TIL:
            out.append(TIL); i += 2; continue
        a, b = corpo[i + 1:i + 2], corpo[i + 2:i + 3]
        if not a or not b or a not in ALFA or b not in ALFA or ALFA.index(a) * 62 + ALFA.index(b) >= len(e):
            raise ValueError("codigo quebrado na posicao {}".format(i))
        out.append(e[ALFA.index(a) * 62 + ALFA.index(b)]); i += 3
    return "".join(out)


def para_ia(texto):
    """Modo IA: comprime so se economizar token de verdade (o cabecalho CLXD2:xxxxxxxx| tambem custa).
    Se nao economizar, manda o texto puro. Devolve (saida, comprimiu)."""
    c = comprimir(texto, "ia")
    if estimar_tokens(c) < estimar_tokens(texto):
        return c, True
    return texto, False


def medida(texto, pacote):
    b = lambda s: len(s.encode("utf-8"))
    pc = lambda a, x: "{:+.0f}%".format(100.0 * (x - a) / a) if a else "-"
    return "bytes {} -> {} ({}) | tokens (estimativa) {} -> {} ({})".format(
        b(texto), b(pacote), pc(b(texto), b(pacote)), estimar_tokens(texto), estimar_tokens(pacote),
        pc(estimar_tokens(texto), estimar_tokens(pacote)))


def autoteste():
    ok, linhas = 0, []
    def t(c, m):
        nonlocal ok
        ok += bool(c); linhas.append(("OK  " if c else "XX  ") + m)
    t(D["sha"].startswith("27f35b93"), "dicionario igual ao ENCLAVE_v5 (27f35b93)")
    f = "a paciente voltou com bruxismo e dor na articulação temporomandibular, vamos fazer a placa miorrelaxante"
    g = comprimir(f)
    t(len(f.encode()) == 106 and len(g.encode()) == 60, "consultorio 106 -> 60 bytes (igual ao v5)")
    s = ("CLXD2:27f35b93|Meu ~3y, é ~01 ter ~nz a ~gC ~f4 e dezenas ~07 do ~0A mas ~3w caminhos e ~01 ~4f "
         "~he com ~3m ~0d ~0a avançar ~1f unimos ,?~4e ~15  ~1E")
    t(abrir(s).startswith("Meu medo, é você ter acesso"), "abre o CLXD2 feito na casca do Sounavy")
    for x in ["~ ~~ ~0a til", "", "linha\n\ttab", "emoji 😀 é ã", f]:
        t(abrir(comprimir(x, "ia")) == x and abrir(comprimir(x)) == x, "sem perda nos 2 modos: " + repr(x[:20]))
    for x in [abrir(s), f, "ok", "articulação temporomandibular e disfunção temporomandibular"]:
        saida, _ = para_ia(x)
        t(estimar_tokens(saida) <= estimar_tokens(x) and (abrir(saida) if CAB2 in saida else saida) == x,
          "modo IA nunca piora e volta igual: " + repr(x[:20]))
    return ok, len(linhas), linhas


def main():
    ok, tot, linhas = autoteste()
    print("=" * 46); print(" CLXD2_PONTE - autoteste {} de {}".format(ok, tot)); print("=" * 46)
    for l in linhas:
        print(" " + l)
    try:
        import clipboard
        texto = clipboard.get() or ""
    except Exception:
        texto = input("\nCole o texto aqui: ")
    texto = texto.strip("\n")
    print("\n" + "-" * 46)
    if not texto.strip():
        print("A area de transferencia esta vazia. Copie um texto e aperte Play de novo.")
        return
    if CAB2 in texto:
        try:
            print("ABERTO (volta igual):\n" + abrir(texto))
        except ValueError as e:
            print("Nao abriu: {}".format(e))
        return
    gu, (ia, comprimiu) = comprimir(texto), para_ia(texto)
    print("TEXTO:\n" + texto)
    print("\n[1] GUARDAR  " + medida(texto, gu) + "\n" + gu)
    print("\n[2] IA       " + (medida(texto, ia) if comprimiu else
          "nao compensa comprimir: vai o texto puro (mais barato para a IA)") + "\n" + ia)
    try:
        import clipboard
        r = input("\nCopiar qual? 1 = guardar, 2 = IA, Enter = nada: ").strip()
        if r in ("1", "2"):
            clipboard.set(gu if r == "1" else ia); print("Copiado.")
    except Exception:
        pass


if __name__ == "__main__":
    main()
