(function(){try{if(location.protocol==='file:')return;
var ua=navigator.userAgent||'';
if(navigator.webdriver||/bot|crawl|spider|slurp|lighthouse|headless|preview|facebookexternalhit|whatsapp|telegram|linkedin|embedly|pinterest/i.test(ua))return;
var K='tl_lang',cur=(document.documentElement.lang||'fr').slice(0,2),LS={};
try{LS=window.localStorage}catch(_){LS=null}
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('.lang-dd a[hreflang]');if(a&&LS)try{LS.setItem(K,a.getAttribute('hreflang'))}catch(_){}},true);
if(document.referrer){try{if(new URL(document.referrer).host===location.host)return}catch(_){}}
if(/[?&]lang=no/.test(location.search))return;
var want=LS&&LS.getItem(K);
if(!want){
 var tz='';try{tz=Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(_){}
 var FR=/^(Africa\/(Casablanca|El_Aaiun|Algiers|Tunis|Dakar|Abidjan|Bamako|Ouagadougou|Niamey|Lome|Porto-Novo|Libreville|Douala|Kinshasa|Lubumbashi|Brazzaville|Nouakchott|Conakry|Bangui|Ndjamena|Malabo)|Europe\/(Paris|Brussels|Luxembourg|Monaco)|Indian\/(Reunion|Antananarivo|Mayotte|Comoro)|America\/(Martinique|Guadeloupe|Cayenne|Port-au-Prince)|Pacific\/(Noumea|Tahiti))$/;
 var ES=/^(Europe\/Madrid|Atlantic\/Canary|Africa\/Ceuta|America\/(Mexico_City|Cancun|Merida|Monterrey|Tijuana|Hermosillo|Chihuahua|Mazatlan|Bogota|Lima|Santiago|Caracas|Guayaquil|Montevideo|Asuncion|La_Paz|Panama|Costa_Rica|Guatemala|El_Salvador|Tegucigalpa|Managua|Havana|Santo_Domingo|Puerto_Rico|Argentina\/.*|Buenos_Aires|Cordoba|Punta_Arenas))$/;
 var AR=/^(Asia\/(Riyadh|Dubai|Qatar|Kuwait|Bahrain|Muscat|Baghdad|Amman|Beirut|Damascus|Aden|Gaza|Hebron)|Africa\/(Cairo|Tripoli|Khartoum))$/;
 if(FR.test(tz))want='fr';else if(ES.test(tz))want='es';else if(AR.test(tz))want='ar';
 else{var L=(navigator.languages&&navigator.languages.length?navigator.languages:[navigator.language||'en']);want='en';
  for(var i=0;i<L.length;i++){var l=String(L[i]).slice(0,2).toLowerCase();if(l==='fr'||l==='es'||l==='ar'||l==='en'){want=l;break}}}
 try{LS&&LS.setItem(K,want)}catch(_){}
}
if(want===cur)return;
try{if(sessionStorage.getItem('tl_geo'))return;sessionStorage.setItem('tl_geo','1')}catch(_){}
var alt=document.querySelector('link[rel=alternate][hreflang="'+want+'"]');
if(alt&&alt.href&&alt.href!==location.href)location.replace(alt.href.replace(/^https?:\/\/[^/]+/,'')+location.hash);
}catch(e){}})();
