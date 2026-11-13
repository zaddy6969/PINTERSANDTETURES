"""Render the static site from shared templates and the verified project catalogue."""
from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((ROOT/'assets/work/projects.json').read_text())
P={p['id']:p for p in DATA}
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
ORDER=[18,12,10,17,3,25,21,24,20,23,26,6,0,2,7,8,11,1,14,15,16,19,22,5,9,4]
def e(x):return html.escape(str(x),quote=True)
def image(i,eager=False,cls='',thumb=False):
 p=P[i];src=p['thumbnail'] if thumb else p['src']
 responsive=f' srcset="{p["thumbnail"]} {p["thumbnailWidth"]}w, {p["src"]} {p["width"]}w" sizes="(max-width:600px) 90vw, (max-width:900px) 45vw, 30vw"' if not eager and p['width']>720 else ''
 return f'<img class="{cls}" src="{src}"{responsive} alt="{e(p["title"])}" width="{p["width"]}" height="{p["height"]}" loading="{"eager" if eager else "lazy"}" decoding="async" {"fetchpriority=high" if eager else ""}>'
def card(i):
 p=P[i];service=S[p['service']];status=f'<span class="work-status">{p["status"]}</span>' if p['status'] else ''
 return f'''<button class="work-card" data-project="{i}" data-reference="{p['reference']}" data-service="{p['service']}" data-category="{p['category']}" data-style="{p['style']}" data-full="{p['src']}" data-title="{e(p['title'])}" data-description="{e(p['description'])}" data-enquiry-service="{e(service['enquiry'])}" aria-label="View {e(p['title'])}"><span class="work-photo">{image(i,thumb=True)}{status}<span class="work-expand" aria-hidden="true">{ARROW}</span></span><span class="work-meta"><span>{service['short']}</span><span>{p['reference']}</span></span><span class="work-title">{e(p['title'])}</span></button>'''
def filterbar(items,mode='service'):
 out='<div class="gallery-toolbar"><div class="gallery-filters" role="group" aria-label="Filter project photographs"><button data-filter="all" aria-pressed="true">All photos <span>'+str(len(items))+'</span></button>'
 options=[(s['slug'],s['short']) for s in SERVICES if s['category']] if mode=='service' else list(STYLES.items())
 field='service' if mode=='service' else 'style'
 for key,name in options:
  count=sum(p[field]==key for p in items)
  if count:out+=f'<button data-filter="{key}" aria-pressed="false">{name} <span>{count}</span></button>'
 return out+f'</div><p class="gallery-count" aria-live="polite"><span id="filter-status">{len(items)} photos</span></p></div>'
def gallery(ids,filtermode=None):
 items=[P[i] for i in ids];bar=filterbar(items,filtermode) if filtermode else f'<p class="collection-count">{len(ids)} {"photograph" if len(ids)==1 else "photographs"} · Select a photo to take a closer look</p>'
 return f'<div class="gallery-collection" data-filter-mode="{filtermode or "none"}">{bar}<div class="portfolio-grid {"single-photo" if len(ids)==1 else ""}">'+''.join(card(i) for i in ids)+'</div></div>'
def service_card(s,number):
 count=sum(p['service']==s['slug'] for p in DATA)
 return f'''<a class="offering" href="/services/{s['slug']}/"><span class="offering-photo">{image(s['image'],thumb=True)}<span class="offering-index">0{number}</span><span class="offering-arrow">{ARROW}</span></span><span class="offering-label"><strong>{s['name']}</strong><small>{count} {"photo" if count==1 else "photos"}</small></span><span class="offering-description">{s['lead']}</span></a>'''
def consult_card(s):return f'''<a class="additional-service" href="/services/{s['slug']}/"><span><strong>{s['name']}</strong><small>{s['lead']}</small></span>{ARROW}</a>'''
def cta(service='General enquiry'):
 return f'<section class="project-invite"><div><p class="eyebrow">LET’S TALK ABOUT YOUR SPACE</p><h2>Found a finish you love?</h2><p>Share your favourite photo, your location and a little about your project.</p></div><button class="button" data-enquire="{e(service)}">Discuss your project {ARROW}</button></section>'
def lightbox():return f'''<dialog id="lightbox" class="viewer" aria-labelledby="lightbox-title"><div class="viewer-top"><span id="viewer-counter" aria-live="polite"></span><button class="close" aria-label="Close project">×</button></div><div class="viewer-layout"><div class="viewer-stage"><button class="viewer-nav prev" id="previous-photo" aria-label="Previous photo">←</button><img id="lightbox-image" alt=""><button class="viewer-nav next" id="next-photo" aria-label="Next photo">→</button></div><div class="viewer-info"><p class="eyebrow" id="viewer-category"></p><h2 id="lightbox-title"></h2><p id="viewer-description"></p><p class="photo-reference" id="viewer-reference"></p><button class="button" id="ask-finish">Ask about this finish {ARROW}</button><a id="viewer-service" class="text-link" href="/services/">Explore this service {ARROW}</a><button class="copy-photo" id="copy-photo">Copy photo link</button><p id="copy-status" role="status"></p></div></div></dialog>'''
def page(title,description,body,path='/'):
 schema={'@context':'https://schema.org','@type':'HousePainter','name':'Painters & Textures','url':'https://paintersandtextures.com','telephone':'+917026193396','email':'paintersandtextures@gmail.com','address':{'@type':'PostalAddress','streetAddress':'84/2, 4th Cross, LG Ramanna Layout, Rajarajeshwari Nagar, Laggere','addressLocality':'Bengaluru','addressRegion':'Karnataka','addressCountry':'IN'}}
 header=(ROOT/'templates/header.html').read_text();footer=(ROOT/'templates/footer.html').read_text();enquiry=(ROOT/'templates/enquiry.html').read_text()
 head=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#142b3f"><title>{e(title)} | Painters & Textures</title><meta name="description" content="{e(description)}"><link rel="canonical" href="https://paintersandtextures.com{path}"><meta property="og:title" content="{e(title)} | Painters & Textures"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><meta property="og:url" content="https://paintersandtextures.com{path}"><meta property="og:image" content="https://paintersandtextures.com/assets/work/project-18.webp"><link rel="icon" type="image/png" href="/assets/pt-logo.png"><link rel="stylesheet" href="/assets/site-v2.css?v=20261105-footer2"><link rel="stylesheet" href="/assets/site-v3.css?v={VER}"><script src="/assets/site-v3.js?v={VER}" defer></script><script type="application/ld+json">{json.dumps(schema)}</script></head><body id="top">'''
 return head+header+'<main id="main">'+body+'</main>'+footer+enquiry+lightbox()+'</body></html>'
def write(path,text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
# Homepage: keep the established branding; make the work and services easier to explore.
home=(ROOT/'templates/home-hero.html').read_text().replace('<span>WALLPAPER</span>','<span>WALL ART & MURALS</span>')
home+='''<section class="section offerings-section" id="services"><div class="section-heading"><div><p class="eyebrow">01 — OUR SERVICES</p><h2>Different surfaces.<br><em>The same attention to detail.</em></h2></div><a class="text-link" href="/services/">Explore all services '''+ARROW+'''</a></div><div class="offering-grid">'''+''.join(service_card(S[k],n+1) for n,k in enumerate(['wall-textures','interior-painting','exterior-painting','wall-art']))+'</div><div class="additional-services">'+consult_card(S['wood-finishes'])+consult_card(S['wallpaper'])+'</div></section>'
home+='<section class="section selected-section" id="work"><div class="section-heading"><div><p class="eyebrow">02 — A CLOSER LOOK AT OUR WORK</p><h2>The details make<br><em>the difference.</em></h2></div><div><p>Real photographs. Real surfaces.<br>Explore a finish from every angle.</p><a href="/projects/" class="text-link">Browse all 26 photographs '+ARROW+'</a></div></div>'+gallery([18,17,12,10,3,25])+'</section>'
home+=(ROOT/'templates/home-approach.html').read_text()
write('index.html',page('Painting & Decorative Wall Finishes in Bengaluru','Explore our painting, wall textures and murals in Bengaluru. Browse 26 project photographs by service and discuss your space.',home))
# Service directory.
body='<section class="section directory-intro"><p class="eyebrow">PAINTERS & TEXTURES / OUR SERVICES</p><h1>Find the finish<br><em>that feels like you.</em></h1><p>From a complete repaint to one remarkable wall. Explore the possibilities for your home or workspace.</p></section><section class="section directory-list"><div class="offering-grid">'+''.join(service_card(s,i+1) for i,s in enumerate(SERVICES[:4]))+'</div><div class="additional-services">'+''.join(consult_card(s) for s in SERVICES[4:])+'</div></section>'+cta()
write('services/index.html',page('Our Services','Interior painting, exterior painting, decorative wall textures, murals, wood finishes and wallpaper in Bengaluru.',body,'/services/'))
# Every supplied photograph appears on its matching service page.
for n,s in enumerate(SERVICES):
 slug=s['slug'];ids=[i for i in ORDER if P[i]['service']==slug]
 if s['image'] is not None:
  visual='<div class="service-cover">'+image(s['image'],eager=True)+f'<span class="cover-label">{e(P[s["image"]]["title"])}</span></div>'
 else:
  visual=f'<aside class="service-note"><p class="eyebrow">A FINISH CHOSEN AROUND YOU</p><h2>{"The beauty<br>is in the details." if slug=="wood-finishes" else "A pattern.<br>A palette.<br>A possibility."}</h2><p>{"Share photos of your doors, frames or wooden features to discuss suitable finishing options." if slug=="wood-finishes" else "Bring your pattern ideas and room photographs. We can discuss wall covering and installation requirements."}</p><a class="text-link" href="https://wa.me/917026193396" target="_blank" rel="noopener">Share your ideas on WhatsApp {ARROW}</a></aside>'
 body=f'<section class="service-intro"><div class="service-intro-copy"><a class="breadcrumb" href="/services/">← All services</a><p class="eyebrow">0{n+1} / {s["name"].upper()}</p><h1>{s["heading"]}</h1><p>{s["description"]}</p><div class="service-actions"><button class="button" data-enquire="{s["enquiry"]}">Discuss your project {ARROW}</button>'+ (f'<a href="#service-gallery" class="text-link">View {len(ids)} {"photo" if len(ids)==1 else "photos"} ↓</a>' if ids else '')+f'</div></div>{visual}</section>'
 body+='<div class="service-highlights">'+''.join(f'<span><i aria-hidden="true">✦</i>{p}</span>' for p in s['points'])+'</div>'
 if ids:
  body+='<section class="section service-gallery" id="service-gallery"><div class="section-heading"><div><p class="eyebrow">THE '+s['name'].upper()+' COLLECTION</p><h2>Explore the work.<br><em>Find your inspiration.</em></h2></div><p>Open any photo for the full view.<br>Ask us about the finish you like.</p></div>'+gallery(ids,'style' if slug=='wall-textures' else None)+'</section>'
 body+=cta(s['enquiry'])
 body+='<section class="related-services section"><p class="eyebrow">KEEP EXPLORING</p><div class="related-links">'+''.join(f'<a href="/services/{other["slug"]}/">{other["name"]} {ARROW}</a>' for other in SERVICES if other['slug']!=slug)+'</div></section>'
 write(f'services/{slug}/index.html',page(s['name']+' in Bengaluru',s['description'],body,f'/services/{slug}/'))
body='<section class="section portfolio-intro"><div><p class="eyebrow">THE PROJECT GALLERY</p><h1>Craft you can see.<br><em>Character you can feel.</em></h1><p>Explore our painting, decorative finishes and wall art. Every photograph is a starting point for a conversation about your space.</p></div><div class="gallery-stamp"><strong>26</strong><span>PROJECT PHOTOGRAPHS</span></div></section><section class="section portfolio-section">'+gallery(ORDER,'service')+'</section>'+cta()
write('projects/index.html',page('Project Gallery','Explore 26 project photographs by service: interior painting, exteriors, decorative wall textures and wall art.',body,'/projects/'))
write('404.html',page('Page not found','Explore Painters & Textures services and project photographs.','<section class="section directory-intro"><p class="eyebrow">404 / PAGE NOT FOUND</p><h1>Let’s find a<br>better direction.</h1><p>This page may have moved.</p><a class="button" href="/">Back to home '+ARROW+'</a></section>'))
urls=['/','/services/','/projects/']+[f'/services/{s["slug"]}/' for s in SERVICES]
write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://paintersandtextures.com{p}</loc></url>' for p in urls)+'</urlset>')
write('data/services.json',json.dumps(SERVICES,indent=2)+'\n')
print('Rendered 9 public pages, 404, shared templates and sitemap.')
