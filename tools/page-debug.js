const fs=require('fs'), vm=require('vm'), path=require('path');
const P=path.join(__dirname,'..')+'/';
const srcs=['assets/data.js','assets/app.js'].map(f=>[f,fs.readFileSync(P+f,'utf8')]);
function el(id){const e={id,style:{},classList:{add(){},remove(){},toggle(){},contains:()=>false},dataset:{},
  addEventListener(){},appendChild(){},setAttribute(){},removeAttribute(){},getAttribute:()=>null,
  querySelectorAll:()=>[],querySelector(sel){return e['_q'+sel]||(e['_q'+sel]=el(sel))},insertAdjacentHTML(){},focus(){},remove(){},
  children:[],firstChild:null,textContent:'',checked:false,value:'',offsetWidth:800,clientWidth:800,
  getBoundingClientRect:()=>({width:800,height:400,left:0,top:0})};
  Object.defineProperty(e,'innerHTML',{get(){return e._h||''},set(v){e._h=v}});return e;}
const page=process.argv[2];
const txt=fs.readFileSync(P+page,'utf8');
const m=[...txt.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const inline=m[m.length-1][1];
const bodies={};
const document={documentElement:el('html'),body:el('body'),
  getElementById(id){return bodies[id]||(bodies[id]=el(id));},
  querySelectorAll:()=>[],querySelector(sel){return bodies['sel:'+sel]||(bodies['sel:'+sel]=el(sel))},
  createElement:t=>el(t),addEventListener(){},createElementNS:(n,t)=>el(t),head:el('head')};
const Lp=new Proxy(function(){return Lp},{get:()=>Lp,apply:()=>Lp,construct:()=>Lp});
const ctx={console,document,L:Lp,location:{search:'',hash:'',href:''},
  localStorage:{getItem:()=>null,setItem(){}},matchMedia:()=>({matches:false,addEventListener(){}}),
  addEventListener(){},setTimeout,clearTimeout,
  getComputedStyle:()=>({getPropertyValue:()=>'#f9f9f7'}),requestAnimationFrame:f=>f(),
  URLSearchParams,Math,JSON,Date,navigator:{userAgent:'node'}};
ctx.window=ctx; ctx.globalThis=ctx;
const c=vm.createContext(ctx);
for(const [f,s] of srcs) vm.runInContext(s,c,{filename:f});
try{ vm.runInContext(inline,c,{filename:page+':inline'}); console.log('inline script: OK'); }
catch(e){ console.log('inline script THREW:', e.message); console.log(e.stack.split('\n').slice(0,4).join('\n')); }
for(const k of Object.keys(bodies)){
  const h=bodies[k]._h;
  if(h!==undefined) console.log(('  '+k).padEnd(28), 'html len', h.length, '| rows', (h.match(/<tr/g)||[]).length);
  else if(bodies[k].textContent) console.log(('  '+k).padEnd(28), 'text', JSON.stringify(bodies[k].textContent));
}
