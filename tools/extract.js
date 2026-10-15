// Coller tel quel dans mcp__remote-devices__Claude_Browser__javascript_tool (tabId "seed", page https://travelife.ma/ ouverte)
// puis appeler : await ORIG('https://travelife.ma/<slug>/')
window.ORIG = async function(url){
 const html = await fetch(url).then(r=>r.text());
 const d = new DOMParser().parseFromString(html,'text/html');
 const root = d.querySelector('[data-elementor-type="wp-page"], [data-elementor-type="wp-post"], .entry-content, main') || d.body;
 root.querySelectorAll('script,style,noscript,svg,header,footer,[data-elementor-type="header"],[data-elementor-type="footer"]').forEach(e=>e.remove());
 const out=[]; const seen=new Set();
 for(const el of root.querySelectorAll('*')){
  if(el.tagName==='IMG'){ const s=el.getAttribute('data-lazy-src')||el.getAttribute('src'); if(s&&!s.startsWith('data:')&&!seen.has(s)){seen.add(s); out.push('IMG '+s+' | '+(el.alt||''));} continue;}
  if(!/^(P|LI|H[1-6]|BLOCKQUOTE|TD|TH|DIV|SPAN|A|BUTTON|SUMMARY)$/.test(el.tagName)) continue;
  const hasBlock=[...el.children].some(c=>/^(P|LI|H[1-6]|DIV|UL|OL|SECTION|TABLE|DETAILS)$/.test(c.tagName));
  let own=''; for(const n of el.childNodes) if(n.nodeType===3) own+=n.textContent;
  if(hasBlock && !own.trim()) continue;
  let a=el.parentElement, skip=false; while(a&&a!==root){ if(a.__d){skip=true;break;} a=a.parentElement;} if(skip) continue;
  const t=el.textContent.replace(/\s+/g,' ').trim(); if(!t) continue; el.__d=true;
  if(seen.has(t)) continue; seen.add(t);
  out.push((/^H[1-6]$/.test(el.tagName)?el.tagName+': ':el.tagName==='LI'?'- ':'')+t);
 }
 return out.join('\n');
};
'ORIG prêt'
