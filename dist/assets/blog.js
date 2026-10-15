/* Charge le contenu de l'article depuis l'API WordPress de travelife.ma et l'affiche dans le nouveau design. */
(function(){
  var box=document.getElementById('article-body'); if(!box) return;
  var id=box.getAttribute('data-id'), root=box.getAttribute('data-root')||'', url=box.getAttribute('data-url');
  var known=window.TL_KNOWN||[];
  var pages=['logiciel-de-gestion-commerciale','manage-travelife','systeme-de-reservation-b2b','site-internet-pour-agence-de-voyages','site-web-pour-agence-de-voyages','agent-ia-travelife-smartcrm','travelife-omra','nos-clients','nos-partenaires','tarifs-logiciel-travelife','creation-site-web-agence-de-voyage','contactez','formulaire-site-internet-agences-de-voyages','politique-de-confidentialite','guide-travelife','articles'];
  function localHref(h){
    var m=h.match(/^https?:\/\/(?:www\.)?travelife\.ma\/(?:index\.php\/)?([^?#]*)(#.*)?$/); if(!m) return null;
    var path=m[1].replace(/\/$/,''), anchor=m[2]||'';
    if(path==='') return root+'index.html'+anchor;
    if(path==='contact') path='contactez';
    var first=path.split('/')[0];
    if(known.indexOf(path)>-1||pages.indexOf(path)>-1||first==='category') return root+path+'/index.html'+anchor;
    return null;
  }
  function clean(html){
    var doc=new DOMParser().parseFromString(html,'text/html'), b=doc.body;
    b.querySelectorAll('script,style,noscript,link,meta,form,button,svg').forEach(function(e){e.remove();});
    b.querySelectorAll('img').forEach(function(img){
      var s=img.getAttribute('data-lazy-src')||img.getAttribute('data-src')||img.getAttribute('src');
      if(!s||s.indexOf('data:')===0){img.remove();return;}
      var alt=img.getAttribute('alt')||''; 
      [].slice.call(img.attributes).forEach(function(a){img.removeAttribute(a.name);});
      img.setAttribute('src',s); img.setAttribute('alt',alt); img.setAttribute('loading','lazy');
    });
    b.querySelectorAll('h1').forEach(function(h){ var n=doc.createElement('h2'); n.innerHTML=h.innerHTML; h.replaceWith(n); });
    b.querySelectorAll('iframe').forEach(function(f){ var s=f.getAttribute('data-lazy-src')||f.getAttribute('src')||''; if(!/youtube|vimeo/.test(s)){f.remove();return;} var w=doc.createElement('div'); w.className='video'; var n=doc.createElement('iframe'); n.src=s; n.setAttribute('allowfullscreen',''); n.setAttribute('loading','lazy'); w.appendChild(n); f.replaceWith(w); });
    var keep={A:['href'],IMG:['src','alt','loading'],TD:['colspan','rowspan'],TH:['colspan','rowspan'],IFRAME:['src','allowfullscreen','loading'],DIV:['class']};
    b.querySelectorAll('*').forEach(function(el){
      var k=keep[el.tagName]||[];
      [].slice.call(el.attributes).forEach(function(a){ if(k.indexOf(a.name)<0) el.removeAttribute(a.name); });
      if(el.tagName==='DIV'&&el.className!=='video') el.removeAttribute('class');
    });
    b.querySelectorAll('a[href]').forEach(function(a){ var l=localHref(a.getAttribute('href')); if(l) a.setAttribute('href',l); else if(/^https?:/.test(a.getAttribute('href'))){a.setAttribute('target','_blank');a.setAttribute('rel','noopener');} });
    // Déballe les conteneurs inutiles (div/section/span/article d'Elementor)
    var changed=true, guard=0;
    while(changed&&guard++<30){ changed=false;
      b.querySelectorAll('div:not(.video),section,article,span,font,center').forEach(function(el){ el.replaceWith.apply(el,[].slice.call(el.childNodes)); changed=true; });
    }
    b.querySelectorAll('p,li,h2,h3,h4,h5,h6,strong,b,i,em,a').forEach(function(el){ if(!el.textContent.trim()&&!el.querySelector('img,iframe')) el.remove(); });
    // Regroupe le texte orphelin en paragraphes
    [].slice.call(b.childNodes).forEach(function(n){ if(n.nodeType===3&&n.textContent.trim()){ var p=doc.createElement('p'); p.textContent=n.textContent.trim(); n.replaceWith(p);} else if(n.nodeType===3) n.remove(); });
    return b.innerHTML;
  }
  fetch('https://travelife.ma/wp-json/wp/v2/posts/'+id+'?_fields=content').then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
  .then(function(j){ box.innerHTML=clean(j.content.rendered); })
  .catch(function(){
    var l=box.querySelector('.loading'); if(l) l.outerHTML='<div class="article-fallback"><p><strong>Aperçu local :</strong> le texte de l’article est chargé depuis travelife.ma et n’a pas pu être récupéré (connexion internet requise).</p><p><a href="'+url+'" target="_blank" rel="noopener">Lire l’article sur travelife.ma →</a></p></div>';
  });
})();
