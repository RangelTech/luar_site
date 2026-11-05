# luar_site

Site público do produto LUAR (`https://luar.rangeltech.net`): páginas do produto, páginas legais e versão em inglês. HTML estático servido por nginx sem privilégios (`Dockerfile`, `nginx.conf`).

- `public/`: o site publicado (início, atendimento, estúdio, espaço de trabalho, contato, cookies, exclusão de dados, `en/`).
- `content/pt` e `content/en`: textos legais em Markdown.
- `tools/build.py`: gera as páginas legais estáticas (`content/*.md` para `public/<rota>/index.html`) sem dependências. Rode `python tools/build.py` depois de editar um texto. `tools/site.py` monta o restante.

Versão: tag `v*` publica a imagem e o manifesto; o deploy é só pelo `vps_rt_infra` (`deploy.yml -f service=luar-site`).

Mapa geral do ecossistema: skill `ecossistema_rt` (repositório `personal-skills`).
