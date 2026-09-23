// Dump the board's data objects to JSON so python tooling can read them.
const vm=require('vm'),fs=require('fs');
const path=require('path');
// Derived from this file's location so the pipeline runs from a clone.
const R=path.join(__dirname,'..')+'/';
const WORK=path.join(__dirname,'.work');
fs.mkdirSync(WORK,{recursive:true});
let src=fs.readFileSync(R+'assets/data.js','utf8')+'\n'+fs.readFileSync(R+'assets/detail.js','utf8')
  +';__out={SCHOOLS,REMOVED,NO_TRACK,NO_PROGRAM,ATHLETE,XCRACES,T1500,VENUES,MEETS,SCHED,METROS,TOWNPOP};';
const ctx={console};vm.createContext(ctx);vm.runInContext(src,ctx);
fs.writeFileSync(path.join(WORK,'board.json'),JSON.stringify(ctx.__out,null,1));
const o=ctx.__out;
console.log('SCHOOLS',o.SCHOOLS.length,'XCRACES',Object.keys(o.XCRACES).length,
            'races',Object.values(o.XCRACES).flat().length);
