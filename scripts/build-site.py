"""Render the static site from shared templates and the verified project catalogue."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'assets/work/projects.json').read_text())
P={p['id']:p for p in DATA}
PHOTO_COUNT=len(DATA)
VER='20261113'
ARROW='<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 19 19 5M5 5h14v14"/></svg>'
SERVICES=[
 {'slug':'interior-painting','name':'Interior painting','short':'Interiors','category':'painting','image':3,'heading':'Colour that feels<br>like home.','description':'A considered palette can change the way a room feels. Explore interior painting for bedrooms, living rooms and workspaces, from a quiet refresh to a playful accent.','points':['Room and full-home painting','Colour and finish selection','Surface preparation and repainting'],'lead':'Fresh colour. A more personal space.','enquiry':'Interior painting'},
 {'slug':'exterior-painting','name':'Exterior painting','short':'Exteriors','category':'exteriors','image':10,'heading':'A better first<br>impression.','description':'Bring a fresh perspective to the outside of your home. Discuss your existing surfaces, colour combinations and preparation needs before choosing the right finish.','points':['Residential exterior painting','Surface assessment and preparation','Facade colour combinations'],'lead':'Thoughtful finishes, from the outside in.','enquiry':'Exterior painting'},
 {'slug':'wall-textures','name':'Decorative textures','short':'Textures','category':'textures','image':18,'heading':'More depth.<br>More character.','description':'Marble-inspired veining, architectural stone effects, ornamental patterns and softly textured surfaces. Find a direction in our work and talk to us about bringing it to your space.','points':['Marble and stone-inspired effects','Ornamental and metallic finishes','Feature walls and subtle textures'],'lead':'A surface worth a closer look.','enquiry':'Decorative textures'},
 {'slug':'wall-art','name':'Wall art & murals','short':'Wall art','category':'artwork','image':12,'heading':'Your wall.<br>A work of art.','description':'Explore devotional scenes, tree-inspired compositions and sculptural wall features. Share a reference or an idea and discuss the style, scale and surface with our team.','points':['Decorative and devotional artwork','Tree and nature-inspired compositions','Dimensional wall features'],'lead':'A personal statement, made part of the room.','enquiry':'Wall artwork'},
 {'slug':'wood-finishes','name':'Wood finishes','short':'Wood finishes','category':None,'image':None,'heading':'Details that bring<br>a space together.','description':'Explore finishing options for doors, frames and wooden features. Share the existing surface and the appearance you have in mind so we can discuss a suitable approach.','points':['Doors, frames and wooden features','Finish and colour consultation','Refinishing options'],'lead':'A considered finish for your wooden features.','enquiry':'Wood finishes'},
 {'slug':'wallpaper','name':'Wallpaper','short':'Wallpaper','category':None,'image':None,'heading':'A fresh layer<br>of personality.','description':'Discuss wall coverings for a feature wall or a complete room. Bring a pattern you love, your wall measurements and photographs of the space to start the conversation.','points':['Feature walls and room schemes','Pattern and colour selection','Wall preparation and installation'],'lead':'Pattern and colour, chosen around your room.','enquiry':'Wallpaper'}
]
S={s['slug']:s for s in SERVICES}
STYLES={'marble':'Marble effects','stone':'Stone & concrete','pattern':'Patterned finishes','subtle':'Subtle textures','metallic':'Gold details','special':'Sculptural textures'}
ORDER=[27,28,39,29,38,30,31,40,41,32,34,35,36,37,33,18,12,10,17,3,25,21,24,20,23,26,6,0,2,7,8,11,1,14,15,16,19,22,5,9,4]
from urllib.parse import quote

def e(value):return html.escape(str(value),quote=True)
def whatsapp(service=''):
 text='Hello Painters & Textures, I would like to discuss '+(service.lower() if service else 'a painting project')+'.'
 return 'https://wa.me/917026193396?text='+quote(text)
def contact(service='',label='Chat on WhatsApp'):
 return f'<a class="button" href="{whatsapp(service)}" target="_blank" rel="noopener">{label} <span aria-hidden="true"></span></a>'
def image(i,eager=False):
 p=P[i]
 return f'<img src="{p["src"] if eager else p["thumbnail"]}" alt="{e(p["title"])}" width="{p["width"]}" height="{p["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}>'
def card(i):
 p=P[i]
 return f'<button class="photo" data-project="{i}" data-service="{p["service"]}" data-full="{p["src"]}" data-title="{e(p["title"])}" data-reference="{p["reference"]}" aria-label="View {e(p["title"])}">{image(i)}<span>{e(p["title"])}</span></button>'
def gallery(ids,filters=False,limit=12):
 buttons='<div class="filters" role="group" aria-label="Filter photos"><button data-filter="all" aria-pressed="true">All</button>'+''.join(f'<button data-filter="{s["slug"]}" aria-pressed="false">{s["short"]}</button>' for s in SERVICES[:4])+'</div>' if filters else ''
 return buttons+f'<div class="photos" data-limit="{limit}">'+''.join(card(i) for i in ids)+'</div>'+('<button class="button secondary load-more" id="load-more">Show more photos</button>' if len(ids)>limit else '')
def service_cards():
 return '<div class="services-grid">'+''.join(f'<a class="service-card" href="/services/{s["slug"]}/"><h3>{s["name"]}<span aria-hidden="true"></span></h3><p>{e(s["summary"])}</p></a>' for s in SERVICES)+'</div>'
summaries={
 'interior-painting':'Fresh colour for your home or workspace.',
 'exterior-painting':'A fresh, well-finished exterior.',
 'wall-textures':'Marble effects, subtle textures and decorative patterns.',
 'wall-art':'Murals, stencils and sculptural wall features.',
 'wood-finishes':'Finishing options for doors, frames and wooden details.',
 'wallpaper':'Patterns and wall coverings to suit your room.'}
for s in SERVICES:s['summary']=summaries[s['slug']]
def viewer():return '<dialog id="lightbox" aria-labelledby="photo-title"><div class="viewer-top"><span id="photo-counter" aria-live="polite"></span><button id="close-photo" aria-label="Close photo">×</button></div><div class="viewer-stage"><button id="previous-photo" aria-label="Previous photo">←</button><img id="lightbox-image" alt=""><button id="next-photo" aria-label="Next photo">→</button></div><div class="viewer-bottom"><h2 id="photo-title"></h2><a id="ask-photo" class="button" href="https://wa.me/917026193396" target="_blank" rel="noopener">Ask about this finish </a></div></dialog>'
def page(title,description,body,path='/'):
 header=(ROOT/'templates/header.html').read_text();footer=(ROOT/'templates/footer.html').read_text()
 schema={'@context':'https://schema.org','@type':'HousePainter','name':'Painters & Textures','url':'https://paintersandtextures.com','telephone':'+917026193396','email':'paintersandtextures@gmail.com','address':{'@type':'PostalAddress','streetAddress':'84/2, 4th Cross, LG Ramanna Layout, Rajarajeshwari Nagar, Laggere','addressLocality':'Bengaluru','addressRegion':'Karnataka','addressCountry':'IN'}}
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#142b3f"><title>{e(title)} | Painters & Textures</title><meta name="description" content="{e(description)}"><link rel="canonical" href="https://paintersandtextures.com{path}"><meta property="og:title" content="{e(title)} | Painters & Textures"><meta property="og:description" content="{e(description)}"><meta property="og:image" content="https://paintersandtextures.com/assets/work/project-27.webp"><link rel="icon" href="/assets/pt-logo.png"><link rel="stylesheet" href="/assets/simple.css?v=20261114-compact"><script src="/assets/simple.js?v=20261114-compact" defer></script><script type="application/ld+json">{json.dumps(schema)}</script></head><body id="top">'+header+'<main id="main">'+body+'</main>'+footer+viewer()+'</body></html>'
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
home='<section class="hero wrap"><div><p class="eyebrow">PAINTERS & TEXTURES · BENGALURU</p><h1>Beautiful walls.<br>Made for your space.</h1><p>Interior and exterior painting, decorative textures and wall art.</p>'+contact()+'</div><div class="hero-photo">'+image(27,True)+'</div></section>'
home+='<section class="section wrap" id="services"><div class="section-heading"><h2>Our services</h2></div>'+service_cards()+'</section>'
home+='<section class="section work-section" id="work"><div class="wrap"><div class="section-heading"><h2>Our work</h2><a class="text-link" href="/projects/">View all photos →</a></div>'+gallery([27,28,12,10,3,29],limit=6)+'</div></section>'
write('index.html',page('Painting & Wall Textures in Bengaluru','Painting, decorative textures and wall art in Bengaluru. View our work and contact Painters & Textures.',home))
write('services/index.html',page('Our Services','Explore painting, wall textures, wall art, wood finishes and wallpaper.', '<section class="section wrap page-intro"><h1>Our services</h1><p>Find the right finish for your space.</p>'+service_cards()+'</section>','/services/'))
for s in SERVICES:
 ids=[i for i in ORDER if P[i]['service']==s['slug']]
 body=f'<section class="section wrap page-intro"><a class="back" href="/services/">← All services</a><h1>{s["name"]}</h1><p>{s["summary"]}</p>'
 if ids:body+=gallery(ids)
 else:body+='<div class="consultation"><h2>Tell us what you have in mind.</h2><p>Share a photo of your space to discuss colours, materials and a quotation.</p>'+contact(s['enquiry'])+'</div>'
 body+='</section>'
 write('services/'+s['slug']+'/index.html',page(s['name']+' in Bengaluru',s['summary'],body,'/services/'+s['slug']+'/'))
write('projects/index.html',page('Our Work','View our painting, decorative textures and wall-art projects.', '<section class="section wrap page-intro"><h1>Our work</h1><p>Choose a service or open a photo for a closer look.</p>'+gallery(ORDER,True)+'</section>','/projects/'))
write('404.html',page('Page not found','Explore our services and work.','<section class="section wrap page-intro"><h1>Page not found</h1><p><a class="text-link" href="/">Back to home →</a></p></section>'))
urls=['/','/services/','/projects/']+[f'/services/{s["slug"]}/' for s in SERVICES]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://paintersandtextures.com{p}</loc></url>' for p in urls)+'</urlset>')
write('data/services.json',json.dumps(SERVICES,indent=2)+'\n')
print('Rendered simplified website; all',len(DATA),'photos retained.')
