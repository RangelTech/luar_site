"""Gera as páginas legais estáticas (content/*.md -> public/<rota>/index.html).

Sem dependências: conversor mínimo de Markdown (títulos, parágrafos, listas, tabelas,
negrito, código e links). Uso: python tools/build.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
PUBLIC = ROOT / "public"

WHATSAPP = "5562985613482"
EMAIL = "comercial@rangeltech.net"
SITE = "https://luar.rangeltech.net"

# (idioma, arquivo, rota, rótulo do menu)
PAGES = [
    ("pt", "politica-de-privacidade", "/politica-de-privacidade", "Privacidade"),
    ("pt", "termos-de-uso", "/termos-de-uso", "Termos de uso"),
    ("pt", "uso-aceitavel", "/uso-aceitavel", "Uso aceitável"),
    ("pt", "exclusao-de-dados", "/exclusao-de-dados", "Exclusão de dados"),
    ("pt", "cookies", "/cookies", "Cookies"),
    ("en", "privacy-policy", "/en/privacy-policy", "Privacy"),
    ("en", "data-deletion", "/en/data-deletion", "Data deletion"),
]
# versão equivalente em outro idioma (para o seletor PT/EN)
ALT = {
    "/politica-de-privacidade": ("/en/privacy-policy", "English"),
    "/exclusao-de-dados": ("/en/data-deletion", "English"),
    "/en/privacy-policy": ("/politica-de-privacidade", "Português"),
    "/en/data-deletion": ("/exclusao-de-dados", "Português"),
}
UPDATED = {"pt": "Última atualização: 22 de outubro de 2026", "en": "Last updated: October 22, 2026"}


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"(?<![\w/@>\"])(/(?:politica-de-privacidade|termos-de-uso|uso-aceitavel|exclusao-de-dados|cookies|planos|contato))\b",
                  r'<a href="\1">\1</a>', text)
    text = re.sub(r"([\w.+-]+@[\w-]+(?:\.[\w-]+)+)", r'<a href="mailto:\1">\1</a>', text)
    return text


def render(md: str) -> tuple[str, str, list[tuple[str, str]]]:
    lines = md.split("\n")
    out: list[str] = []
    title = ""
    toc: list[tuple[str, str]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("## "):
            text = line[3:].strip()
            slug = re.sub(r"[^a-z0-9]+", "-", re.sub(r"^\d+\.\s*", "", text).lower().encode("ascii", "ignore").decode()).strip("-") or "s"
            toc.append((slug, text))
            out.append(f'<h2 id="{slug}">{inline(text)}</h2>')
        elif line.startswith("**Última atualização") or line.startswith("**Last updated"):
            pass
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[2:]]
            t = "<div class=\"tbl\"><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body:
                t += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>")
            continue
        elif re.match(r"^\d+\.\s", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i]):
                items.append(re.sub(r"^\d+\.\s", "", lines[i]))
                i += 1
            out.append("<ol>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ol>")
            continue
        elif line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        else:
            out.append(f"<p>{inline(line)}</p>")
        i += 1
    return title, "\n".join(out), toc


CSS = """
:root{--bg:#ffffff;--bg2:#f4f8fb;--text:#14213d;--muted:#4a5a73;--line:#dbe5ee;--brand:#2c8fc4;--brand-ink:#0a1733;--link:#1d6fa3}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0a1733;--bg2:#0f2147;--text:#e8f0fa;--muted:#a9bad2;--line:#223a66;--brand:#75c8f2;--brand-ink:#0a1733;--link:#75c8f2}}
:root[data-theme=dark]{--bg:#0a1733;--bg2:#0f2147;--text:#e8f0fa;--muted:#a9bad2;--line:#223a66;--brand:#75c8f2;--brand-ink:#0a1733;--link:#75c8f2}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--text);font:16px/1.7 -apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--link)}
.top{border-bottom:1px solid var(--line);background:var(--bg)}
.top .in{max-width:1080px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.top img{height:30px;display:block}
.top img.logo-dark{display:none}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .top img.logo-light{display:none}:root:not([data-theme=light]) .top img.logo-dark{display:block}}
:root[data-theme=dark] .top img.logo-light{display:none}:root[data-theme=dark] .top img.logo-dark{display:block}
.top nav{display:flex;gap:6px 16px;flex-wrap:wrap;margin-left:auto;font-size:14px}
.top nav a{color:var(--muted);text-decoration:none}.top nav a[aria-current=page],.top nav a:hover{color:var(--text)}
.wrap{max-width:1080px;margin:0 auto;padding:40px 20px 80px;display:grid;grid-template-columns:230px minmax(0,1fr);gap:48px}
aside{position:sticky;top:20px;align-self:start;font-size:14px}
aside strong{display:block;margin-bottom:8px;color:var(--muted);font-weight:600;text-transform:uppercase;letter-spacing:.06em;font-size:12px}
aside a{display:block;padding:4px 0;color:var(--muted);text-decoration:none}aside a:hover{color:var(--text)}
main{min-width:0}
h1{font-size:clamp(28px,4vw,40px);line-height:1.15;margin:0 0 8px;letter-spacing:-.02em}
.meta{color:var(--muted);font-size:14px;margin:0 0 28px;display:flex;gap:16px;flex-wrap:wrap}
h2{font-size:21px;margin:36px 0 8px;letter-spacing:-.01em;scroll-margin-top:20px}
p{margin:0 0 14px}ul,ol{margin:0 0 14px;padding-left:22px}li{margin:4px 0}
code{background:var(--bg2);border:1px solid var(--line);border-radius:4px;padding:1px 5px;font-size:.9em}
.tbl{overflow-x:auto;margin:0 0 18px}table{border-collapse:collapse;width:100%;font-size:15px}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top}th{background:var(--bg2)}
footer{border-top:1px solid var(--line);background:var(--bg2);color:var(--muted);font-size:14px}
footer .in{max-width:1080px;margin:0 auto;padding:28px 20px;display:flex;gap:24px 48px;flex-wrap:wrap;justify-content:space-between}
footer a{color:var(--muted)}
.cta{display:inline-block;margin-top:6px;background:var(--brand);color:var(--brand-ink);font-weight:600;padding:9px 16px;border-radius:999px;text-decoration:none}
@media (max-width:820px){.wrap{grid-template-columns:1fr;gap:20px}aside{position:static;border-bottom:1px solid var(--line);padding-bottom:14px}.top nav{margin-left:0}}
"""


def page(lang: str, fname: str, route: str, label: str) -> None:
    md = (CONTENT / lang / f"{fname}.md").read_text(encoding="utf-8")
    title, body, toc = render(md)
    nav = "".join(
        f'<a href="{r}"{" aria-current=\"page\"" if r == route else ""}>{html.escape(l)}</a>'
        for lg, _, r, l in PAGES if lg == lang
    )
    alt = ALT.get(route)
    alt_link = f'<a href="{alt[0]}" hreflang="{"en" if lang == "pt" else "pt-BR"}">{alt[1]}</a>' if alt else ""
    toc_html = "".join(f'<a href="#{s}">{html.escape(t)}</a>' for s, t in toc)
    contents = "Nesta página" if lang == "pt" else "On this page"
    foot_h = "Contato" if lang == "pt" else "Contact"
    home = "Voltar ao site" if lang == "pt" else "Back to site"
    doc = f"""<!doctype html>
<html lang="{'pt-BR' if lang == 'pt' else 'en'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · LUAR</title>
<meta name="description" content="{html.escape(title)} da LUAR, plataforma de atendimento e agentes de IA da Rangel Tecnologia e Informação Ltda.">
<link rel="canonical" href="{SITE}{route}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">
<style>{CSS}</style>
</head>
<body>
<header class="top"><div class="in">
<a href="/" aria-label="LUAR"><img class="logo-light" src="/assets/logo.svg" alt="LUAR"><img class="logo-dark" src="/assets/logo_dark.svg" alt="LUAR"></a>
<nav aria-label="Páginas legais">{nav}</nav>
</div></header>
<div class="wrap">
<aside><strong>{contents}</strong>{toc_html}</aside>
<main>
<h1>{html.escape(title)}</h1>
<p class="meta"><span>{UPDATED[lang]}</span>{alt_link}</p>
{body}
</main>
</div>
<footer><div class="in">
<div><strong>LUAR</strong><br>Rangel Tecnologia e Informação Ltda · CNPJ 65.505.647/0001-10<br>Av. Rio Grande do Sul, 343, sala 03, Setor Campinas, Goiânia/GO · CEP 74.520-070</div>
<div><strong>{foot_h}</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="https://wa.me/{WHATSAPP}">WhatsApp +55 62 98561-3482</a><br><a href="/">{home}</a></div>
</div></footer>
</body>
</html>
"""
    out = PUBLIC / route.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print("ok", route, len(doc))


if __name__ == "__main__":
    for p in PAGES:
        page(*p)
    # sitemap simples das páginas legais
    urls = "".join(f"<url><loc>{SITE}{r}</loc></url>" for _, _, r, _ in PAGES)
    (PUBLIC / "sitemap-legal.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
