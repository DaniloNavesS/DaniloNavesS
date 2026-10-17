#!/usr/bin/env python3
"""Gera um portfólio estático com a biblioteca padrão do Python."""
from pathlib import Path
import html, json, re
ROOT = Path(__file__).resolve().parent
config = json.loads((ROOT/'conteudo/site.json').read_text())
e = html.escape
css = (ROOT/'assets/style.css').read_text()
js = (ROOT/'assets/app.js').read_text()

def page(title, description, content, prefix='./'):
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#222b1b"><meta name="description" content="{e(description,quote=True)}"><meta property="og:title" content="{e(title,quote=True)}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:type" content="website"><title>{e(title)}</title><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><style>{css}</style></head><body>
<a class="skip" href="#principal">Pular para o conteúdo</a><div class="shell">

{content}
<footer><span>© 2026 {e(config['nome'])}<br>Feito de ideias, código e curiosidade.</span><a href="{e(config['github'],quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></footer></div><script>{js}</script></body></html>'''

def md(text):
    # Subconjunto seguro: títulos ##, parágrafos, listas e `código`.
    out=[]; paragraph=[]; in_list=False
    def inline(s): return re.sub(r'`([^`]+)`',r'<code>\1</code>',e(s))
    def flush():
        if paragraph: out.append('<p>'+inline(' '.join(paragraph))+'</p>'); paragraph.clear()
    for line in text.splitlines()+['']:
        if not line.startswith('- ') and in_list: out.append('</ul>'); in_list=False
        if line.startswith('## '): flush(); out.append('<h2>'+inline(line[3:])+'</h2>')
        elif line.startswith('- '):
            flush()
            if not in_list: out.append('<ul>'); in_list=True
            out.append('<li>'+inline(line[2:])+'</li>')
        elif not line.strip(): flush()
        else: paragraph.append(line)
    return '\n'.join(out)

def art(kind):
    if kind=='inflow':return '<div class="inflow-word">inflow<span aria-hidden="true">↗</span><small>Da fonte à descoberta.</small></div><div class="stack" aria-hidden="true"><div class="slab"></div><div class="slab"></div><div class="slab">{ dados }</div></div>'
    if kind=='ml':return '<div class="matrix" aria-hidden="true">'+'<i></i>'*64+'</div><div class="ml-title" aria-hidden="true">learn.<br>iterate.</div>'
    positions=[(40,130),(135,55),(145,210),(255,130),(355,40),(370,235),(460,135)]
    edges=[(0,1),(0,2),(1,2),(1,3),(2,3),(3,4),(3,5),(4,6),(5,6),(4,5)]
    svg='<svg viewBox="0 0 500 280" aria-hidden="true">'
    for a,b in edges:
        x,y=positions[a]; u,v=positions[b];svg+=f'<path class="link" d="M{x} {y}L{u} {v}"/>'
    svg+='<path class="link strong" d="M40 130L135 55L255 130L370 235L460 135"/>'
    for x,y in positions:svg+=f'<circle class="graph-node" cx="{x}" cy="{y}" r="7"/><circle cx="{x}" cy="{y}" r="18" fill="none" stroke="#aabd6e" stroke-opacity=".25"/>'
    return svg+'</svg>'

cards=[]
for i,p in enumerate(config['projetos'],1):
    if p.get('imagem'):
        visual=f'<img src="./{e(p["imagem"],quote=True)}" alt="Interface do projeto {e(p["titulo"],quote=True)}" loading="lazy">'
    else:
        visual=art(p['arte'])
    visual_class='inflow-art' if p.get('arte')=='inflow' else 'screenshot-art'
    cards.append(f'''<article class="project-card"><div class="project-visual {visual_class}"><span class="visual-label">{e(p['rotulo'])}</span><span class="visual-index">0{i} / PROJETO</span>{visual}</div><div class="project-card-body"><div><span class="project-kicker">PROJETO PESSOAL / 0{i}</span><h3>{e(p['titulo'])}</h3><p>{e(p['resumo'])}</p></div><div class="project-card-bottom"><div class="tags">{''.join('<span>'+e(t)+'</span>' for t in p['tags'])}</div><a class="project-link" href="{e(p['repositorio'],quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Ver {e(p['titulo'],quote=True)} no GitHub">Ver no GitHub <span aria-hidden="true">↗</span></a></div></div></article>''')
notes=[]
for p in config['textos']:
    notes.append(f'''<a class="note" href="./textos/{e(p['slug'])}.html"><div class="note-meta">{e(p['categoria'])}<br>{e(p['status'])}</div><div><h3>{e(p['titulo'])}</h3><p>{e(p['resumo'])}</p></div><span aria-hidden="true">↗</span></a>''')
content=f'''<main id="principal">
<section class="hero" aria-labelledby="titulo"><div class="hero-glow" aria-hidden="true"></div><canvas id="field" aria-hidden="true"></canvas><div class="hero-content"><div class="hero-navigation"><a class="hero-brand" href="./index.html" aria-label="Danilo Naves — início"><span class="monogram" aria-hidden="true">dn.</span><span>Danilo Naves</span></a><nav class="card-nav" aria-label="Navegação principal"><a href="#projetos"><span aria-hidden="true">▦</span><span>Projetos</span></a><a href="#sobre"><span aria-hidden="true">◉</span><span>Sobre</span></a><a href="#textos"><span aria-hidden="true">≡</span><span>Textos</span></a><a href="#contato" class="nav-contact"><span aria-hidden="true">↗</span><span>Contato</span></a></nav><a class="hero-github" href="{e(config['github'],quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a></div><div class="hero-top eyebrow"><span class="status"><i aria-hidden="true"></i> Engenharia · Dados · Pesquisa</span><span>Brasília, Brasil / 15°47′S 47°52′W</span></div><h1 id="titulo">Dados em<br><em>movimento.</em><br>Ideias em construção.</h1><p class="hero-description">{e(config['apresentacao'])}</p><div><a class="pill lime" href="#projetos">Explore meu trabalho <span aria-hidden="true">↗</span></a></div><div class="hero-bottom"><span class="hero-meta">CURIOSIDADE COMO PONTO DE PARTIDA.<br>CÓDIGO COMO FORMA DE EXPLORAR.</span><a class="scroll-cue" href="#projetos">Continue explorando <span aria-hidden="true">↓</span></a></div></div><div class="orbit-label" aria-hidden="true">input: curiosidade<br>process: <b>aprender & construir</b><br>output: novas possibilidades ↗</div></section>
<div class="ticker" aria-hidden="true"><span>01 / ENGENHARIA DE DADOS</span><span>02 / MACHINE LEARNING</span><span>03 / SISTEMAS & PESQUISA</span><span>SEMPRE EM CONSTRUÇÃO ↗</span></div>
<section class="section" id="projetos"><div class="section-head"><div><span class="eyebrow">01 / Projetos pessoais</span><h2>Ideias que viraram<br><em>projetos.</em></h2></div><p>Um pouco do que construí, com a proposta e as tecnologias de cada projeto. O código está no GitHub.</p></div><div class="project-grid">{''.join(cards)}</div></section>
<section class="section about" id="sobre"><div><span class="eyebrow">02 / Um pouco sobre mim</span><h2>Entre sistemas,<br>dados e <em>perguntas.</em></h2><div class="about-caption">Engenharia de Software · UnB<br>Brasília, Distrito Federal</div></div><div class="about-copy"><p>{e(config['sobre'])}</p><p>{e(config['complemento'])}</p><div class="skills" aria-label="Tecnologias">{''.join('<span>'+e(s)+'</span>' for s in config['skills'])}</div><div class="experiences"><details><summary>CIIA · Machine Learning e Dados <span>2025 — 2026 ＋</span></summary><p>Preparação e limpeza de dados, engenharia de atributos, tratamento de desbalanceamento, modelos preditivos e APIs com FastAPI.</p></details><details><summary>Softure · Desenvolvimento Fullstack <span>＋</span></summary><p>Desenvolvimento com Java, Laravel e JavaScript, integração com PostgreSQL e atendimento a necessidades de profissionais da saúde.</p></details><details><summary>HBR · Sistemas Embarcados <span>2025 ＋</span></summary><p>Atividades com C/C++, comunicação UART e MQTT e sistemas de tempo real.</p></details></div></div></section>
<section class="notes-section" id="textos"><div class="section-head"><div><span class="eyebrow">03 / Caderno aberto</span><h2>Escrever para<br><em>entender melhor.</em></h2></div><p>Espaço para textos e anotações.<br>Os dois textos iniciais são rascunhos para revisão antes da publicação.</p></div>{''.join(notes)}</section>
<section class="contact" id="contato"><div><span class="eyebrow">04 / Próxima conexão</span><h2>Boas ideias começam<br>com uma <em>conversa.</em></h2></div><div><p>Projetos, pesquisa ou uma troca sobre tecnologia. Você me encontra no GitHub.</p><a class="pill lime" href="{e(config['github'],quote=True)}" target="_blank" rel="noopener noreferrer">Meu perfil no GitHub <span aria-hidden="true">↗</span></a></div></section></main>'''
(ROOT/'index.html').write_text(page(config['nome']+' — Dados, software e pesquisa',config['apresentacao'],content))
for p in config['textos']:
    category=p.get('rotulo',p.get('categoria',''))
    status=p.get('status','APRESENTAÇÃO DO TRABALHO')
    c=f'''<main id="principal" class="article-wrap"><a class="back" href="../index.html#textos">← Voltar ao portfólio</a><div class="eyebrow">{e(category)} / {e(status)}</div><h1>{e(p['titulo'])}</h1><p class="lead">{e(p['resumo'])}</p><article class="prose">{md((ROOT/'conteudo'/p['arquivo']).read_text())}</article>'''
    if p.get('repositorio'):c+=f'<div class="article-end"><a class="pill dark" href="{e(p["repositorio"],quote=True)}" target="_blank" rel="noopener noreferrer">Explorar o repositório ↗</a></div>'
    c+='</main>'
    (ROOT/'textos'/(p['slug']+'.html')).write_text(page(p['titulo']+' — '+config['nome'],p['resumo'],c,'../'))
print(f"Geradas: index.html e {len(config['textos'])} páginas de texto.")
