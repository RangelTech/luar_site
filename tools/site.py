"""Gera o site institucional da LUAR (páginas comerciais) em public/. Sem dependências.

Uso: python tools/site.py   (depois, python tools/build.py gera as páginas legais)
Direção de arte escolhida: "Noite", azul-noite #0A1733 com a lua #75C8F2; as fases da lua
são a metáfora dos planos. Tema claro e escuro; sem gradiente, sem estrela no logo.
"""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
WA = "5562985613482"
EMAIL = "comercial@rangeltech.net"
LOGIN = "https://ia.rangeltech.net/app/login"
SITE = "https://luar.rangeltech.net"
SUPORTE = "Suporte com pessoas, por WhatsApp e e-mail, de segunda a sexta, das 9h às 18h"


def wa(msg: str) -> str:
    from urllib.parse import quote

    return f"https://wa.me/{WA}?text={quote(msg)}"


# ---------------------------------------------------------------- planos (espelha rt_plans.yml)
PLANOS = [
    dict(k="nova", nome="Nova", preco="197", fase="🌑", p="Para começar a atender com IA num canal.",
         itens=["1 canal conectado", "1 agente com skills", "Filas e Kanban", "Espaço de trabalho mínimo", "Suporte com pessoas"]),
    dict(k="crescente", nome="Crescente", preco="397", fase="🌒", p="Atendimento completo, em todos os canais.",
         itens=["Todos os canais (oficiais e não oficiais)", "Agentes por skills, com arquivos", "Filas, Kanban e repasse IA↔pessoa",
                "Espaço de trabalho pequeno e restrito", "Seus computadores conectados", "Suporte com pessoas"]),
    dict(k="quarto", nome="Quarto", preco="597", fase="🌓", p="Seu próprio servidor, só da sua empresa.",
         itens=["Tudo do Crescente", "Servidor próprio com IP público", "O agente cria e publica sites e sistemas", "Seus computadores conectados", "Suporte com pessoas"]),
    dict(k="cheia", nome="Cheia", preco="797", fase="🌔", p="Servidor próprio e a IA mais flexível.",
         itens=["Tudo do Quarto", "Modelo próprio de baixa restrição de recusa", "Limites por janela de uso", "Suporte com pessoas"], destaque=True),
    dict(k="eclipse", nome="Eclipse", preco="997", fase="🌕", p="Tudo, inclusive vídeo, imagem e voz.",
         itens=["Tudo da Cheia", "Estúdio de vídeo, imagem e voz sob demanda", "Avatar com a sua própria imagem", "Limites por janela de uso", "Suporte prioritário"]),
]

EXEMPLOS = [
    ("ACME Alimentos", "delivery", "#E4572E"), ("Orbita Odonto", "clínica", "#2E86AB"), ("Vértice Contabilidade", "escritório", "#3B7A57"),
    ("Nimbus Imóveis", "imobiliária", "#7A5C99"), ("Pixel Moda", "loja", "#C2185B"), ("Delta Auto Peças", "varejo", "#F0A202"),
]

PEDIDOS = [
    ("Conecte no sistema da minha empresa e crie um painel de vendas por região e por vendedor.", "O agente usa a credencial do seu banco, monta o painel e publica no espaço da empresa."),
    ("Crie um site para a minha empresa no domínio minhaempresa.com.br.", "O site é criado, publicado no seu espaço de trabalho e você recebe o passo a passo do domínio."),
    ("Suba um sistema simples de cadastro de clientes.", "Formulário, lista, busca e login, no ar, sem você comprar hospedagem."),
    ("No meu computador tem uma planilha na Área de Trabalho. Tire a coluna S e crie a coluna Valor Total no final.", "O agente edita o arquivo no próprio computador. O arquivo não sai de lá; só texto trafega."),
    ("Todo dia às 8h, me mande o resumo das vendas de ontem.", "Tarefa agendada: o resultado aparece no seu chat no horário."),
    ("Responda os clientes do Instagram sobre o cardápio e passe para uma pessoa se pedirem desconto.", "Atendimento com repasse: a IA resume a conversa e a pessoa continua de onde parou."),
    ("Edite este vídeo, tire o silêncio e coloque legenda.", "Estúdio de vídeo sob demanda, no plano Eclipse."),
]

CSS = """
:root{--bg:#fff;--bg2:#f4f8fb;--text:#0a1733;--muted:#43536e;--line:#dbe5ee;--brand:#2c8fc4;--moon:#75c8f2;--ink:#0a1733;--link:#1d6fa3}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0a1733;--bg2:#0f2147;--text:#e8f0fa;--muted:#a9bad2;--line:#223a66;--brand:#75c8f2;--link:#75c8f2}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:17px/1.65 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--link)}img{max-width:100%}
.w{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line)}
header.top .w{display:flex;align-items:center;gap:22px;height:64px}
header.top img{height:30px;display:block}
.logo-d{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .logo-l{display:none}:root:not([data-theme=light]) .logo-d{display:block}}
nav.m{display:flex;gap:6px 22px;margin-left:auto;font-size:15px;flex-wrap:wrap}
nav.m a{color:var(--muted);text-decoration:none}nav.m a:hover,nav.m a[aria-current]{color:var(--text)}
.btn{display:inline-block;padding:11px 22px;border-radius:999px;font-weight:600;text-decoration:none;font-size:16px;border:1.5px solid var(--brand);color:var(--text)}
.btn.p{background:var(--moon);border-color:var(--moon);color:#0a1733}
.btn.s{padding:7px 16px;font-size:14px}
.hero{padding:88px 0 72px;display:grid;grid-template-columns:1.15fr .85fr;gap:48px;align-items:center}
h1{font-size:clamp(38px,6vw,68px);line-height:1.04;letter-spacing:-.03em;margin:0 0 20px}
h2{font-size:clamp(28px,4vw,42px);line-height:1.1;letter-spacing:-.02em;margin:0 0 14px}
h3{font-size:20px;margin:0 0 6px}
.lead{font-size:20px;color:var(--muted);max-width:34em;margin:0 0 28px}
.cta{display:flex;gap:12px;flex-wrap:wrap}
.moon{aspect-ratio:1;border-radius:50%;background:var(--moon);position:relative;box-shadow:0 0 0 1px var(--line);max-width:380px;margin:auto;width:100%}
.moon:after{content:"";position:absolute;right:-7%;top:-3%;width:78%;height:78%;border-radius:50%;background:var(--bg)}
section.b{padding:72px 0;border-top:1px solid var(--line)}
section.b.alt{background:var(--bg2)}
.kick{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;font-weight:600}
.g2{display:grid;grid-template-columns:repeat(2,1fr);gap:28px}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.card{border:1px solid var(--line);border-radius:18px;padding:24px;background:var(--bg)}
.card p{margin:0;color:var(--muted)}
.chat{border:1px solid var(--line);border-radius:18px;overflow:hidden;background:var(--bg)}
.chat .u{padding:16px 20px;background:var(--bg2);font-weight:600}.chat .a{padding:16px 20px;color:var(--muted)}
.ill{font-size:13px;color:var(--muted);margin-top:14px}
.plans{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
.plan{border:1px solid var(--line);border-radius:18px;padding:22px 18px;display:flex;flex-direction:column;background:var(--bg)}
.plan.d{border:2px solid var(--moon)}
.plan .f{font-size:30px}.plan .pr{font-size:34px;font-weight:700;letter-spacing:-.02em;margin:6px 0 2px}.plan .pr small{font-size:14px;font-weight:400;color:var(--muted)}
.plan ul{padding-left:18px;margin:12px 0 18px;color:var(--muted);font-size:15px;flex:1}.plan li{margin:5px 0}
.ex{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.ex .c{border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;gap:14px;align-items:center;background:var(--bg)}
.ex .lg{width:44px;height:44px;border-radius:12px;flex:none}
.faq details{border-top:1px solid var(--line);padding:16px 0}.faq summary{cursor:pointer;font-weight:600;font-size:18px}.faq p{color:var(--muted);margin:10px 0 0}
footer{border-top:1px solid var(--line);background:var(--bg2);color:var(--muted);font-size:14px;padding:32px 0}
footer .w{display:flex;gap:24px 56px;flex-wrap:wrap;justify-content:space-between}footer a{color:var(--muted)}
@media (max-width:900px){.hero,.g2,.g3,.ex{grid-template-columns:1fr}.plans{grid-template-columns:1fr 1fr}.hero{padding:48px 0}.moon{max-width:220px}header.top .w{flex-wrap:wrap;height:auto;padding:10px 20px}nav.m{margin:0;order:3;width:100%}}
@media (max-width:520px){.plans{grid-template-columns:1fr}}
"""

NAV = [("/produto/", "Produto"), ("/atendimento/", "Atendimento"), ("/espaco-de-trabalho/", "Espaço de trabalho"),
       ("/estudio/", "Estúdio"), ("/planos/", "Planos"), ("/contato/", "Contato")]


def page(route: str, title: str, desc: str, body: str) -> None:
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == route else ""}>{t}</a>' for h, t in NAV)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{SITE}{route}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png"><style>{CSS}</style></head><body>
<header class="top"><div class="w"><a href="/" aria-label="LUAR"><img class="logo-l" src="/assets/logo.svg" alt="LUAR"><img class="logo-d" src="/assets/logo_dark.svg" alt="LUAR"></a>
<nav class="m" aria-label="Principal">{nav}</nav><a class="btn s" href="{LOGIN}">Entrar</a></div></header>
<main>{body}</main>
<footer><div class="w"><div><strong>LUAR</strong><br>Rangel Tecnologia e Informação Ltda · CNPJ 65.505.647/0001-10<br>Av. Rio Grande do Sul, 343, sala 03, Setor Campinas, Goiânia/GO · CEP 74.520-070</div>
<div><a href="/politica-de-privacidade/">Privacidade</a> · <a href="/termos-de-uso/">Termos de uso</a> · <a href="/uso-aceitavel/">Uso aceitável</a> · <a href="/exclusao-de-dados/">Exclusão de dados</a> · <a href="/cookies/">Cookies</a><br>
<a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="https://wa.me/{WA}">WhatsApp +55 62 98561-3482</a><br>{SUPORTE}.</div></div></footer></body></html>"""
    out = PUBLIC / route.strip("/") / "index.html" if route != "/" else PUBLIC / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print("ok", route)


def cta(txt="Falar no WhatsApp", msg="Olá! Quero conhecer a LUAR."):
    return f'<a class="btn p" href="{wa(msg)}">{txt}</a>'


def planos_html() -> str:
    cards = ""
    for p in PLANOS:
        li = "".join(f"<li>{html.escape(i)}</li>" for i in p["itens"])
        cards += (f'<div class="plan{" d" if p.get("destaque") else ""}"><div class="f" aria-hidden="true">{p["fase"]}</div><h3>{p["nome"]}</h3>'
                  f'<div class="pr">R$ {p["preco"]}<small>/mês</small></div><p style="margin:0;color:var(--muted);font-size:15px">{p["p"]}</p><ul>{li}</ul>'
                  f'<a class="btn s p" href="{wa("Olá! Quero saber mais sobre o plano " + p["nome"] + " da LUAR.")}">Falar no WhatsApp</a></div>')
    return f'<div class="plans">{cards}</div><p class="ill">Valores de lançamento, a partir de, sujeitos a confirmação. Implantação cobrada à parte. Limites de uso conforme o plano.</p>'


def chat_html(items) -> str:
    return "".join(f'<div class="chat" style="margin-bottom:14px"><div class="u">{html.escape(u)}</div><div class="a">{html.escape(a)}</div></div>' for u, a in items) + \
        '<p class="ill">Exemplo ilustrativo.</p>'


def ex_html() -> str:
    cs = "".join(f'<div class="c"><div class="lg" style="background:{c}" aria-hidden="true"></div><div><strong>{n}</strong><br><span style="color:var(--muted)">{s}</span></div></div>' for n, s, c in EXEMPLOS)
    return f'<div class="ex">{cs}</div><p class="ill">Exemplo ilustrativo: empresas fictícias.</p>'


FAQ = [
    ("Preciso entender de tecnologia?", "Não. Você escreve o que quer no chat, em português, e a LUAR faz. Nós conectamos seus canais e ajudamos a ensinar seus agentes."),
    ("Os dados da minha empresa ficam separados das outras?", "Sim. Cada empresa tem o seu ambiente, e uma empresa nunca acessa os dados de outra."),
    ("E se a IA errar?", "Ações sensíveis pedem a sua aprovação, tudo fica registrado no histórico e uma pessoa da sua equipe pode assumir a conversa a qualquer momento."),
    ("Posso falar com uma pessoa?", f"Sim. {SUPORTE}."),
    ("Como cancelo?", "Quando quiser. Ao cancelar você exporta os seus dados em até 30 dias."),
    ("Meu computador precisa de algo especial?", "Não. Você instala um pequeno programa, dá um nome ao computador e ele aparece na plataforma. Funciona em Windows e Linux."),
]


def faq_html() -> str:
    return '<div class="faq">' + "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ) + "</div>"


def home() -> None:
    body = f"""<div class="w"><div class="hero"><div><div class="kick">Atendimento e operação com IA</div>
<h1>Peça no chat.<br>A LUAR faz.</h1><p class="lead">Atenda seus clientes no WhatsApp, Instagram e mais, e peça ao seu agente para criar sites, sistemas e relatórios, num espaço de trabalho só da sua empresa. Sem comprar servidor, sem contratar time de TI.</p>
<div class="cta">{cta("Agendar demonstração", "Olá! Quero agendar uma demonstração da LUAR.")}<a class="btn" href="/planos/">Ver planos</a></div></div><div class="moon" role="img" aria-label="Lua"></div></div></div>
<section class="b"><div class="w"><div class="kick">O problema</div><h2>Canais soltos, tarefas manuais, contexto perdido.</h2>
<p class="lead">O cliente chama no WhatsApp, o pedido vira planilha e o time vive atrás de quem sabe fazer o site, o relatório, o sistema. A LUAR junta tudo e coloca um agente de IA para trabalhar com você.</p></div></section>
<section class="b alt"><div class="w"><div class="kick">Como funciona</div><h2>Três passos.</h2><div class="g3">
<div class="card"><h3>1. Conecte seus canais</h3><p>WhatsApp, Instagram, Facebook, TikTok e site numa só caixa de entrada.</p></div>
<div class="card"><h3>2. Ensine seus agentes</h3><p>Suba o cardápio, a tabela de preços, as regras. O agente aprende sem você programar.</p></div>
<div class="card"><h3>3. Peça e acompanhe</h3><p>Converse com o Sr Moon, o assistente do dono, e veja tudo no histórico.</p></div></div></div></section>
<section class="b"><div class="w"><div class="kick">Atendimento</div><h2>IA e pessoas, na mesma fila.</h2><p class="lead">A IA atende, resolve ou passa para uma pessoa com um resumo escrito. Filas por assunto, Kanban de negócios ao lado das conversas.</p><a class="btn" href="/atendimento/">Ver o atendimento</a></div></section>
<section class="b alt"><div class="w"><div class="kick">Peça no chat</div><h2>Do pedido ao resultado.</h2>{chat_html(PEDIDOS[:4])}<a class="btn" href="/espaco-de-trabalho/">Conhecer o espaço de trabalho</a></div></section>
<section class="b"><div class="w"><div class="kick">Empresas de exemplo</div><h2>Para cada tipo de negócio.</h2>{ex_html()}</div></section>
<section class="b alt"><div class="w"><div class="kick">Planos</div><h2>Cinco fases. Escolha a sua.</h2>{planos_html()}</div></section>
<section class="b"><div class="w"><div class="kick">Dúvidas</div><h2>Perguntas frequentes.</h2>{faq_html()}</div></section>
<section class="b alt"><div class="w" style="text-align:center"><h2>Vamos conversar?</h2><p class="lead" style="margin:0 auto 24px">Uma conversa de 20 minutos para entender seus canais e o que você quer automatizar.</p>{cta("Falar no WhatsApp")}</div></section>"""
    page("/", "LUAR · Atendimento e operação com IA", "Atenda clientes em vários canais e peça ao seu agente de IA para criar sites, sistemas e relatórios, num espaço de trabalho só da sua empresa.", body)


def produto() -> None:
    cards = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in [
        ("Vários canais, uma caixa", "WhatsApp, Instagram, Facebook, TikTok, e-mail e site, com a distinção entre conexão oficial e não oficial."),
        ("Agentes por skills", "Cada empresa ensina o que o agente sabe, com texto e arquivos. Um agente usa uma ou várias skills."),
        ("Filas e Kanban", "Conversas organizadas por assunto e negócios em quadro, lado a lado."),
        ("Tarefas agendadas", "O agente executa sozinho no horário e o resultado aparece no seu chat."),
        ("Espaço de trabalho", "Um ambiente só da sua empresa, onde o agente trabalha e publica."),
        ("Seus computadores", "Conecte seus computadores, até um antigo, e o agente trabalha neles, com o seu arquivo no seu computador."),
        ("Controle", "Aprovação de ações sensíveis, histórico de tudo e permissões por pessoa."),
        ("Sr Moon", "O assistente do dono, com todo o poder dentro da sua empresa, no chat.")])
    page("/produto/", "Produto · LUAR", "Canais, agentes, filas, Kanban, tarefas agendadas e espaço de trabalho num só lugar.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Produto</div><h1 style="font-size:clamp(34px,5vw,54px)">Tudo o que o seu atendimento precisa.</h1><div class="g2" style="margin-top:32px">{cards}</div><p style="margin-top:32px">{cta()}</p></div>')


def atendimento() -> None:
    demo = chat_html([("Cliente: Oi, vocês entregam hoje à noite?", "IA: Entregamos até as 22h. Quer ver o cardápio? Posso anotar o pedido."),
                      ("Cliente: Quero um desconto no combo.", "IA passa para uma pessoa e escreve o resumo: cliente pede desconto no combo, já escolheu 2 itens."),
                      ("Atendente (vê o histórico e as notas internas)", "Fechamos por R$ 10 de desconto. A nota interna não é repetida ao cliente. Com um clique, devolve para a IA.")])
    page("/atendimento/", "Atendimento · LUAR", "IA e pessoas na mesma fila, filas por assunto, Kanban e vários canais.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Atendimento</div><h1 style="font-size:clamp(34px,5vw,54px)">IA que atende. Pessoas que assumem.</h1><p class="lead">A IA resolve o que dá e passa o resto para uma pessoa, com resumo escrito. A pessoa lê o histórico inteiro e as notas internas, e devolve para a IA com um clique.</p>{demo}<div class="g3" style="margin-top:28px"><div class="card"><h3>Filas</h3><p>Vendas, suporte, financeiro: cada assunto na sua fila.</p></div><div class="card"><h3>Kanban</h3><p>Seus negócios em quadro, ao lado das conversas.</p></div><div class="card"><h3>Canais</h3><p>WhatsApp, Instagram, Facebook, TikTok, e-mail e site.</p></div></div><p style="margin-top:32px">{cta()}</p></div>')


def espaco() -> None:
    page("/espaco-de-trabalho/", "Espaço de trabalho · LUAR", "Um ambiente só da sua empresa, onde o agente cria sites e sistemas e trabalha nos seus computadores.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Espaço de trabalho</div><h1 style="font-size:clamp(34px,5vw,54px)">Peça. O agente trabalha.</h1><p class="lead">Cada empresa tem o seu espaço, privado. O agente cria sites e sistemas e eles sobem ali, sem você comprar hospedagem nem servidor.</p>{chat_html(PEDIDOS)}<section style="margin-top:48px"><div class="kick">Conecte o seu computador</div><h2>Até um computador antigo vira servidor.</h2><p class="lead">Instale um pequeno programa, dê um nome ao computador e ele aparece na plataforma, online ou offline. Funciona em Windows e Linux, em todos os planos. O agente edita seus arquivos no próprio computador: o arquivo não sai de lá, só texto trafega.</p></section><p style="margin-top:24px">{cta()}</p></div>')


def estudio() -> None:
    page("/estudio/", "Estúdio · LUAR", "Edite e gere vídeos, imagens e voz sob demanda, com avatar da sua própria imagem.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Estúdio</div><h1 style="font-size:clamp(34px,5vw,54px)">Vídeo, imagem e voz, pelo chat.</h1><p class="lead">Peça para editar um vídeo, tirar o silêncio, colocar legenda, gerar um vídeo de apresentação ou criar um avatar com a sua própria imagem. Os recursos rodam sob demanda, com limites por janela de uso, no plano Eclipse.</p><div class="card"><h3>Com a sua imagem, com consentimento</h3><p>O Estúdio usa a sua imagem e a de quem autorizou. A Política de Uso Aceitável proíbe usar imagem ou voz de terceiros sem consentimento.</p></div><p style="margin-top:32px">{cta()}</p></div>')


def solucoes() -> None:
    page("/solucoes/", "Soluções · LUAR", "Para cada tipo de negócio, um atendimento que trabalha de verdade.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Soluções</div><h1 style="font-size:clamp(34px,5vw,54px)">Para o seu tipo de negócio.</h1>{ex_html()}<p style="margin-top:32px">{cta()}</p></div>')


def planos() -> None:
    page("/planos/", "Planos · LUAR", "Nova, Crescente, Quarto, Cheia e Eclipse: do primeiro canal ao estúdio completo.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Planos</div><h1 style="font-size:clamp(34px,5vw,54px)">Cinco fases da lua.</h1><p class="lead">Cada fase acrescenta uma capacidade. A IA de baixa restrição de recusa e o Estúdio têm limites por janela de uso, e o uso é sujeito à <a href="/uso-aceitavel/">Política de Uso Aceitável</a>.</p>{planos_html()}<p class="ill">{SUPORTE}.</p><div style="margin-top:48px">{faq_html()}</div></div>')


def contato() -> None:
    page("/contato/", "Contato · LUAR", "Fale com a LUAR pelo WhatsApp ou por e-mail.",
         f'<div class="w" style="padding:64px 20px"><div class="kick">Contato</div><h1 style="font-size:clamp(34px,5vw,54px)">Vamos conversar.</h1><p class="lead">Uma conversa de 20 minutos para entender seus canais e o que você quer automatizar.</p><p>{cta("Falar no WhatsApp", "Olá! Quero agendar uma demonstração da LUAR.")}</p><p>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a><br>{SUPORTE}.</p></div>')


def notfound() -> None:
    body = '<div class="w" style="padding:96px 20px;text-align:center"><h1>Página não encontrada</h1><p class="lead" style="margin:0 auto 24px">Essa página não existe.</p><a class="btn p" href="/">Voltar ao início</a></div>'
    page("/404", "Página não encontrada · LUAR", "Página não encontrada.", body)
    (PUBLIC / "404.html").write_text((PUBLIC / "404" / "index.html").read_text(encoding="utf-8"), encoding="utf-8")
    (PUBLIC / "404" / "index.html").unlink()
    (PUBLIC / "404").rmdir()


if __name__ == "__main__":
    for fn in (home, produto, atendimento, espaco, estudio, solucoes, planos, contato, notfound):
        fn()
    urls = ["/", "/produto/", "/atendimento/", "/espaco-de-trabalho/", "/estudio/", "/solucoes/", "/planos/", "/contato/",
            "/politica-de-privacidade/", "/termos-de-uso/", "/uso-aceitavel/", "/exclusao-de-dados/", "/cookies/"]
    (PUBLIC / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                        + "".join(f"<url><loc>{SITE}{u}</loc></url>" for u in urls) + "</urlset>", encoding="utf-8")
    (PUBLIC / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
