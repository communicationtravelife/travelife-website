(function(){
  var header=document.querySelector('.site-header');
  var onScroll=function(){ if(header) header.classList.toggle('is-scrolled', window.scrollY>8); };
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();

  // Menu mobile
  var burger=document.querySelector('.burger'), nav=document.getElementById('nav');
  if(burger&&nav){
    burger.addEventListener('click',function(){
      var open=nav.classList.toggle('open');
      burger.setAttribute('aria-expanded',open);
      document.body.style.overflow=open?'hidden':'';
    });
  }
  // Sous-menus (clic = mobile + clavier)
  document.querySelectorAll('.has-dd > .nav-link').forEach(function(btn){
    btn.addEventListener('click',function(e){
      var li=btn.parentElement, open=!li.classList.contains('open');
      document.querySelectorAll('.has-dd.open').forEach(function(x){ if(x!==li){x.classList.remove('open');x.firstElementChild.setAttribute('aria-expanded','false');} });
      li.classList.toggle('open',open); btn.setAttribute('aria-expanded',open);
      e.stopPropagation();
    });
  });
  document.addEventListener('click',function(e){
    if(!e.target.closest('.has-dd')) document.querySelectorAll('.has-dd.open').forEach(function(x){x.classList.remove('open');});
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){ document.querySelectorAll('.has-dd.open').forEach(function(x){x.classList.remove('open');}); if(nav&&nav.classList.contains('open')) burger.click(); }
  });

  // Apparition au défilement
  var els=document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(entries){ entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target);} }); },{rootMargin:'0px 0px -60px 0px'});
    els.forEach(function(el){io.observe(el);});
  } else els.forEach(function(el){el.classList.add('in');});

  // Onglets FAQ
  document.querySelectorAll('.faq-tabs').forEach(function(tabs){
    var btns=tabs.querySelectorAll('button');
    btns.forEach(function(b){
      b.addEventListener('click',function(){
        btns.forEach(function(x){x.setAttribute('aria-selected', x===b);});
        document.querySelectorAll('.faq-group').forEach(function(g){ g.hidden = g.id!==b.getAttribute('aria-controls'); });
      });
    });
  });

  // Formulaires : aperçu local (pas d'envoi réel)
  document.querySelectorAll('form[data-demo]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var ok=f.querySelector('.form-success'); if(ok){ ok.style.display='block'; }
      f.reset();
    });
  });

  // Logos : duplication pour défilement continu
  document.querySelectorAll('.logos-track').forEach(function(t){ t.innerHTML += t.innerHTML; t.querySelectorAll('img').forEach(function(img,i){ if(i>=t.children.length/2) img.setAttribute('aria-hidden','true'); }); });

  var y=document.getElementById('year'); if(y) y.textContent=new Date().getFullYear();
})();
// Onglets de fonctionnalités (.ftabs)
(function(){
  document.querySelectorAll('.ftabs').forEach(function(box){
    var tabs=box.querySelectorAll('.ftab'), panels=box.querySelectorAll('.ftab-panel');
    tabs.forEach(function(t,i){
      t.addEventListener('click',function(){
        tabs.forEach(function(x){x.setAttribute('aria-selected', x===t);});
        panels.forEach(function(p,j){p.hidden = j!==i;});
      });
    });
  });
  var st=document.querySelector('.hero-stage'); if(st) setTimeout(function(){st.classList.add('in');},250);
})();
// Sélecteur de langue
(function(){
  document.querySelectorAll('.lang-sw').forEach(function(sw){
    var b=sw.querySelector('.lang-btn');
    b.addEventListener('click',function(e){ var o=sw.classList.toggle('open'); b.setAttribute('aria-expanded',o); e.stopPropagation(); });
  });
  document.addEventListener('click',function(e){ if(!e.target.closest('.lang-sw')) document.querySelectorAll('.lang-sw.open').forEach(function(x){x.classList.remove('open');}); });
})();
