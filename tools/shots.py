import asyncio, sys
from playwright.async_api import async_playwright
pages=sys.argv[2].split(','); w=int(sys.argv[1]); out=sys.argv[3]
FONTCSS=open('/tmp/fonts.css').read(); PH=open('/tmp/ph.jpg','rb').read()
async def handle(r):
    u=r.request.url
    if u.startswith('file:'): return await r.continue_()
    if 'fonts.googleapis.com' in u: return await r.fulfill(status=200,content_type='text/css',body=FONTCSS)
    if r.request.resource_type=='image': return await r.fulfill(status=200,content_type='image/jpeg',body=PH)
    return await r.abort()
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); ctx=await b.new_context(viewport={'width':w,'height':900})
        pg=await ctx.new_page(); errs=[]
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.route("**/*", handle)
        for name in pages:
            await pg.goto('file:///home/claude/travelife/dist/'+name+'index.html'); await pg.wait_for_timeout(400)
            await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>{e.style.transition='none';e.classList.add('in')})")
            await pg.wait_for_timeout(300)
            sw=await pg.evaluate("document.documentElement.scrollWidth")
            if sw>w: errs.append(f'{name}: overflow {sw}')
            await pg.screenshot(path=f'{out}/{w}_{name.replace("/","_") or "home"}.png', full_page=True)
        print('\n'.join(errs) or 'no errors'); await b.close()
asyncio.run(main())
