const fs=require('fs'),http=require('http'),path=require('path'),{JSDOM}=require('jsdom');
const ROOT=path.join(__dirname,'..');
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css'};
const srv=http.createServer((req,res)=>{const rel=decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/,'')||'index.html';
 const abs=path.join(ROOT,rel);if(!abs.startsWith(ROOT)||!fs.existsSync(abs)){res.writeHead(404);return res.end();}
 res.writeHead(200,{'content-type':MIME[path.extname(abs)]||'application/octet-stream'});res.end(fs.readFileSync(abs));});
(async()=>{
 await new Promise(r=>srv.listen(0,'127.0.0.1',r));const P=srv.address().port;
 const pages=fs.readdirSync(ROOT).filter(f=>f.endsWith('.html'));
 let bad=0;
 for(const p of pages){
  const errs=[];
  const vc=new (require('jsdom').VirtualConsole)();
  vc.on('jsdomError',e=>errs.push('jsdomError: '+e.message));
  const dom=await JSDOM.fromURL(`http://127.0.0.1:${P}/${p}`,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,virtualConsole:vc});
  await new Promise(r=>{if(dom.window.document.readyState==='complete')return r();dom.window.addEventListener('load',r);setTimeout(r,3500);});
  const doc=dom.window.document;
  const rows=doc.querySelectorAll('table tbody tr').length;
  // dead relative links + broken in-page anchors
  const dead=[],anch=[];
  for(const a of doc.querySelectorAll('a[href]')){
   const h=a.getAttribute('href');
   if(!h||h.startsWith('http')||h.startsWith('mailto:')||h.startsWith('tel:'))continue;
   if(h.startsWith('#')){if(h!=='#'&&!doc.querySelector('[id="'+h.slice(1)+'"]'))anch.push(h);continue;}
   const [file,frag]=h.split('#');
   if(file&&!fs.existsSync(path.join(ROOT,file.split('?')[0])))dead.push(h);
   else if(frag&&file&&fs.existsSync(path.join(ROOT,file))){
     const html=fs.readFileSync(path.join(ROOT,file),'utf8');
     if(!new RegExp('id="'+frag.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'"').test(html))anch.push(h);
   }
  }
  const out=[];
  if(errs.length)out.push(...new Set(errs));
  if(dead.length)out.push('dead links: '+[...new Set(dead)].join(', '));
  if(anch.length)out.push('broken anchors: '+[...new Set(anch)].join(', '));
  console.log((out.length?'FAIL ':'ok   ')+p.padEnd(22)+' tbody rows='+rows+(out.length?'\n       '+out.join('\n       '):''));
  if(out.length)bad++;
  dom.window.close();
 }
 console.log('\n'+pages.length+' pages, '+bad+' with problems');
 srv.close();
})().catch(e=>{console.error(e);srv.close();process.exit(1);});
