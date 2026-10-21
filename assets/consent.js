/* Travelife — cookies (Google Analytics, Pixel Meta) avec consentement + bouton WhatsApp (désactivé tant que WHATSAPP est vide).
   Les outils de mesure ne se chargent qu'après « Accepter ». Le choix est gardé 6 mois. */
(function(){
  var GA_ID = 'G-YCP5KBSJG3';
  var PIXEL_ID = '1167280197414116';
  var WHATSAPP = ''; // numéro WhatsApp au format international sans + (ex. 2126XXXXXXXX) ; vide = pas de bouton
  var KEY = 'tl_consent', MAX_AGE = 1000*60*60*24*182;

  var lang = (document.documentElement.lang || 'fr').slice(0,2);
  var ALL = {
    fr:{txt:'Nous utilisons des cookies de mesure d’audience (Google Analytics) et publicitaires (Meta) pour améliorer le site. Vous pouvez les accepter ou les refuser.', more:'En savoir plus', ok:'Accepter', no:'Refuser', manage:'Gérer les cookies', wa:'Écrivez-nous sur WhatsApp', policy:'/politique-de-confidentialite/#cookies'},
    en:{txt:'We use audience measurement (Google Analytics) and advertising (Meta) cookies to improve the site. You can accept or refuse them.', more:'Learn more', ok:'Accept', no:'Refuse', manage:'Manage cookies', wa:'Message us on WhatsApp', policy:'/en/privacy-policy/#cookies'},
    es:{txt:'Utilizamos cookies de medición de audiencia (Google Analytics) y publicitarias (Meta) para mejorar el sitio. Puede aceptarlas o rechazarlas.', more:'Más información', ok:'Aceptar', no:'Rechazar', manage:'Gestionar cookies', wa:'Escríbanos por WhatsApp', policy:'/es/politica-de-privacidad/#cookies'},
    ar:{txt:'نستعمل ملفات تعريف الارتباط لقياس الزيارات (Google Analytics) وللإعلانات (Meta) من أجل تحسين الموقع. يمكنكم قبولها أو رفضها.', more:'معرفة المزيد', ok:'قبول', no:'رفض', manage:'إدارة ملفات تعريف الارتباط', wa:'راسلونا عبر واتساب', policy:'/ar/privacy-policy/#cookies'}
  };
  var T = ALL[lang] || ALL.fr;

  function read(){ try{ var v=JSON.parse(localStorage.getItem(KEY)); if(v && Date.now()-v.t < MAX_AGE) return v.c; }catch(e){} return null; }
  function save(c){ try{ localStorage.setItem(KEY, JSON.stringify({c:c, t:Date.now()})); }catch(e){} }

  var loaded=false;
  function loadTrackers(){
    if(loaded || location.protocol==='file:') return; loaded=true;
    var s=document.createElement('script'); s.async=true; s.src='https://www.googletagmanager.com/gtag/js?id='+GA_ID; document.head.appendChild(s);
    window.dataLayer=window.dataLayer||[]; window.gtag=function(){dataLayer.push(arguments);};
    gtag('js', new Date()); gtag('config', GA_ID);
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
      if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;
      s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', PIXEL_ID); fbq('track', 'PageView');
  }

  var banner=null;
  function hideBanner(){ if(banner){ banner.remove(); banner=null; document.body.classList.remove('has-ck'); } }
  function showBanner(){
    if(banner) return;
    banner=document.createElement('div');
    banner.className='ck'; banner.setAttribute('role','dialog'); banner.setAttribute('aria-live','polite'); banner.setAttribute('aria-label',T.manage);
    banner.innerHTML='<p>'+T.txt+' <a href="'+T.policy+'">'+T.more+'</a></p><div class="ck-btns"><button type="button" class="ck-no">'+T.no+'</button><button type="button" class="ck-ok">'+T.ok+'</button></div>';
    banner.querySelector('.ck-ok').onclick=function(){ save('all'); hideBanner(); loadTrackers(); };
    banner.querySelector('.ck-no').onclick=function(){ save('none'); hideBanner(); };
    document.body.appendChild(banner); document.body.classList.add('has-ck');
  }

  function init(){
    var c=read();
    if(c==='all') loadTrackers(); else if(c===null) showBanner();

    // lien « Gérer les cookies » en bas de page
    var fb=document.querySelector('.footer-bottom');
    if(fb){ var b=document.createElement('button'); b.type='button'; b.className='ck-manage'; b.textContent=T.manage;
      b.onclick=function(){ try{ localStorage.removeItem(KEY); }catch(e){} showBanner(); };
      fb.appendChild(b); }

    // bouton WhatsApp flottant (affiché seulement si un numéro est renseigné)
    if(!WHATSAPP) return;
    var wa=document.createElement('a');
    wa.className='wa-float'; wa.href='https://wa.me/'+WHATSAPP; wa.target='_blank'; wa.rel='noopener'; wa.setAttribute('aria-label',T.wa); wa.title=T.wa;
    wa.innerHTML='<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.36 4 14.97c0 2.11.56 4.17 1.62 5.99L4 29l8.25-1.6a12.1 12.1 0 0 0 3.79.6C22.68 28 28 22.64 28 16.03 28 9.42 22.68 3 16.04 3zm0 22.97c-1.2 0-2.38-.2-3.5-.6l-.25-.09-4.9.95.98-4.73-.16-.26a9.93 9.93 0 0 1-1.54-5.27c0-5.5 4.5-9.97 10.04-9.97 5.53 0 9.95 4.64 9.95 10.03 0 5.5-4.5 9.94-10.62 9.94zm5.47-7.43c-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.68.15-.2.3-.78.97-.96 1.17-.18.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.49-.9-.8-1.5-1.78-1.67-2.08-.18-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.47 1.07 2.88 1.22 3.08.15.2 2.1 3.2 5.08 4.48.71.31 1.27.49 1.7.63.72.23 1.37.2 1.88.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.13-.27-.2-.57-.35z"/></svg>';
    document.body.appendChild(wa);
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
