'use strict';
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');menu.textContent='☰';}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';nav.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');menu.textContent=open?'×':'☰';});
nav.querySelectorAll('a').forEach(a=>{a.addEventListener('click',closeMenu);if(a.getAttribute('href')===location.pathname)a.setAttribute('aria-current','page');});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){closeMenu();menu.focus();}});
const cards=[...document.querySelectorAll('[data-project]')],filters=[...document.querySelectorAll('[data-filter]')],grid=document.querySelector('.photos'),more=document.querySelector('#load-more'),viewer=document.querySelector('#lightbox');
const batch=Number(grid?.dataset.limit||12);let shown=batch,matched=cards,index=0,lastTrigger=null;
function updateCards(){cards.forEach(card=>{card.hidden=!matched.slice(0,shown).includes(card);});if(more)more.hidden=shown>=matched.length;}
function filter(value,updateUrl=true){const valid=filters.some(b=>b.dataset.filter===value)?value:'all';filters.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===valid)));matched=cards.filter(c=>valid==='all'||c.dataset.service===valid);shown=batch;updateCards();if(updateUrl){const url=new URL(location.href);url.searchParams.delete('service');if(valid!=='all')url.searchParams.set('service',valid);history.replaceState(null,'',url.pathname+url.search);}}
filters.forEach(b=>b.addEventListener('click',()=>filter(b.dataset.filter)));
if(filters.length)filter(new URLSearchParams(location.search).get('service')||'all',false);else updateCards();
more?.addEventListener('click',()=>{const next=shown;shown+=batch;updateCards();matched[next]?.focus({preventScroll:true});});
function render(){const card=matched[index],p=card.dataset;document.querySelector('#lightbox-image').src=p.full;document.querySelector('#lightbox-image').alt=p.title;document.querySelector('#photo-title').textContent=p.title;document.querySelector('#photo-counter').textContent=(index+1)+' / '+matched.length;document.querySelector('#previous-photo').disabled=index===0;document.querySelector('#next-photo').disabled=index===matched.length-1;const message='Hello Painters & Textures, I am interested in '+p.title+'.\nhttps://paintersandtextures.com/projects/#'+p.reference;document.querySelector('#ask-photo').href='https://wa.me/917026193396?text='+encodeURIComponent(message);history.replaceState(null,'',location.pathname+location.search+'#'+p.reference);}
function open(card){lastTrigger=card;if(!matched.includes(card)){filter('all',false);matched=cards;}index=matched.indexOf(card);render();viewer.showModal();}
cards.forEach(card=>card.addEventListener('click',()=>open(card)));
function move(delta){if(index+delta<0||index+delta>=matched.length)return;index+=delta;render();}
document.querySelector('#previous-photo').addEventListener('click',()=>move(-1));document.querySelector('#next-photo').addEventListener('click',()=>move(1));document.querySelector('#close-photo').addEventListener('click',()=>viewer.close());
viewer.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();move(1);}if(e.key==='ArrowLeft'){e.preventDefault();move(-1);}});
viewer.addEventListener('click',e=>{if(e.target===viewer){const r=viewer.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)viewer.close();}});
viewer.addEventListener('close',()=>{if(location.hash.startsWith('#PT-'))history.replaceState(null,'',location.pathname+location.search);if(lastTrigger&&!lastTrigger.hidden)lastTrigger.focus({preventScroll:true});});
const requested=cards.find(c=>'#'+c.dataset.reference===location.hash);if(requested)open(requested);
