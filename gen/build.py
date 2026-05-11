import json, os

base = os.path.dirname(os.path.abspath(__file__))

chars = json.load(open(os.path.join(base,'chars.json'),'r',encoding='utf-8'))
questions = json.load(open(os.path.join(base,'questions.json'),'r',encoding='utf-8'))
stories = json.load(open(os.path.join(base,'stories.json'),'r',encoding='utf-8'))

out = os.path.join(base, '..', 'index.html')

# Build character JS
cj = 'const CHARS={'
for k,v in chars.items():
    cid = k.replace('_m','').replace('_f','')
    g = 'male' if k.endswith('_m') else 'female'
    h = v.get('house','')
    hc = 'house-g' if h in ('格兰芬多','Gryffindor') else 'house-s' if h in ('斯莱特林','Slytherin') else 'house-r' if h in ('拉文克劳','Ravenclaw') else 'house-h'
    sp = json.dumps(v.get('sp',{}),ensure_ascii=False)
    tr = json.dumps(v.get('traits',[]),ensure_ascii=False)
    nm = json.dumps(v['name'],ensure_ascii=False)
    hs = json.dumps(h,ensure_ascii=False)
    st = stories.get(k,{})
    stj = json.dumps(st.get('title',''),ensure_ascii=False)
    sb = json.dumps(st.get('body',''),ensure_ascii=False)
    rj = json.dumps(v.get('reason',''),ensure_ascii=False)
    cj += '%s:{n:%s,h:%s,hc:"%s",g:"%s",s:%s,t:%s,r:%s,tt:%s,tb:%s},' % (cid,nm,hs,hc,g,sp,tr,rj,stj,sb)
cj = cj.rstrip(',') + '};'

qj = 'const QS=' + json.dumps(questions,ensure_ascii=False) + ';'

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>哈利波特 - 命运羁绊测试</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:#0a0a1a;color:#e8d5b7;min-height:100vh;overflow-x:hidden}
.screen{display:none;min-height:100vh;padding:20px;position:relative}
.screen.active{display:flex;flex-direction:column;align-items:center;justify-content:center}
.screen::before{content:"";position:fixed;top:0;left:0;right:0;bottom:0;background:radial-gradient(ellipse at 50% 0%,rgba(75,0,130,.3) 0%,transparent 70%);pointer-events:none;z-index:0}
.screen>*{position:relative;z-index:1}
h1{font-size:clamp(2rem,6vw,4rem);color:#ffd700;text-shadow:0 0 40px rgba(255,215,0,.5);margin-bottom:10px;text-align:center}
h2{font-size:clamp(1.2rem,4vw,2rem);color:#ffd700;margin-bottom:15px;text-align:center}
.sub{color:#c4a882;font-size:clamp(.9rem,2.5vw,1.1rem);text-align:center;line-height:1.8;margin:20px 0 40px;max-width:500px}
.btn{background:linear-gradient(135deg,#ffd700,#e6a800);color:#1a1a2e;border:none;padding:15px 40px;font-size:1.1rem;border-radius:50px;cursor:pointer;transition:all .3s;font-family:inherit;margin:10px}
.btn:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(255,215,0,.3)}
.prog{width:100%;max-width:500px;height:6px;background:rgba(255,255,255,.1);border-radius:3px;margin-bottom:30px;overflow:hidden}
.prog-bar{height:100%;background:linear-gradient(90deg,#ffd700,#ff8c00);transition:width .4s;border-radius:3px}
.qcard{background:rgba(255,255,255,.05);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:clamp(20px,4vw,40px);max-width:600px;width:100%;margin-bottom:20px}
.qtext{font-size:clamp(1rem,3vw,1.3rem);line-height:1.8;margin-bottom:25px;color:#fff}
.opts{display:flex;flex-direction:column;gap:12px}
.opt{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.15);border-radius:12px;padding:15px 20px;cursor:pointer;transition:all .3s;font-size:clamp(.9rem,2.5vw,1.05rem);color:#e8d5b7;font-family:inherit;text-align:left;width:100%}
.opt:hover{background:rgba(255,215,0,.1);border-color:rgba(255,215,0,.4);transform:translateX(5px)}
.opt.sel{background:rgba(255,215,0,.15);border-color:#ffd700;color:#ffd700}
.gsel{display:flex;gap:30px;margin:30px 0;flex-wrap:wrap;justify-content:center}
.gcard{background:rgba(255,255,255,.05);border:2px solid rgba(255,255,255,.15);border-radius:20px;padding:30px 40px;cursor:pointer;transition:all .3s;text-align:center;min-width:140px}
.gcard:hover,.gcard.sel{border-color:#ffd700;background:rgba(255,215,0,.1)}
.gicon{font-size:3rem;margin-bottom:10px}
.glabel{font-size:1.1rem;color:#e8d5b7}
.rcard{background:rgba(255,255,255,.05);backdrop-filter:blur(15px);border:1px solid rgba(255,215,0,.3);border-radius:25px;padding:clamp(25px,5vw,45px);max-width:650px;width:100%;text-align:center}
.mpct{font-size:clamp(3rem,10vw,6rem);color:#ffd700;font-weight:bold;text-shadow:0 0 30px rgba(255,215,0,.5)}
.mlbl{font-size:1rem;color:#c4a882;margin-bottom:20px}
.cname{font-size:clamp(1.5rem,5vw,2.5rem);color:#ffd700;margin:10px 0}
.house-g{color:#ff4444}.house-s{color:#44aa44}.house-r{color:#4488ff}.house-h{color:#ffaa00}
.trs{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:15px 0}
.tr{background:rgba(255,215,0,.15);color:#ffd700;padding:5px 15px;border-radius:20px;font-size:.85rem}
.story{margin-top:25px;text-align:left;background:rgba(0,0,0,.2);border-radius:15px;padding:20px;line-height:2;font-size:clamp(.9rem,2.5vw,1rem);color:#d4c4a8;max-height:60vh;overflow-y:auto}
.story::-webkit-scrollbar{width:4px}
.story::-webkit-scrollbar-thumb{background:rgba(255,215,0,.3);border-radius:2px}
.stitle{font-size:1.3rem;color:#ffd700;text-align:center;margin-bottom:15px}
.cpbtn{margin-top:18px;background:rgba(255,215,0,.15);border:1px solid rgba(255,215,0,.3);color:#ffd700;border-radius:25px;padding:12px 20px;font-size:.95rem;cursor:pointer;text-align:center;transition:all .3s}
.cpbtn:hover{background:rgba(255,215,0,.25);transform:translateY(-1px)}
.cpbtn:active{transform:scale(.97)}
.ld{font-size:1.5rem;color:#ffd700;text-align:center}
.ld .dots::after{content:"";animation:dots 1.5s infinite}
@keyframes dots{0%{content:""};25%{content:"."};50%{content:".."};75%{content:"..."}}
@keyframes fi{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.fi{animation:fi .6s ease-out}
.stars{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
.star{position:absolute;background:#fff;border-radius:50%;animation:tw var(--d,3s) infinite alternate}
@keyframes tw{from{opacity:.2}to{opacity:.8}}
.rbtn{background:transparent;border:1px solid rgba(255,215,0,.3);color:#ffd700;padding:10px 30px;border-radius:50px;cursor:pointer;font-family:inherit;font-size:.9rem;margin-top:20px;transition:all .3s}
.rbtn:hover{background:rgba(255,215,0,.1);border-color:#ffd700}
</style>
</head>
<body>
<div class="stars" id="stars"></div>

<div id="intro" class="screen active">
<h1>哈利波特</h1>
<h2>命运羁绊测试</h2>
<p class="sub">在魔法世界里，有一个人正在等你。<br>回答10个问题，找到那个与你灵魂最契合的人。<br>你的答案，将决定你们的命运。</p>
<button class="btn" onclick="start()">开启命运之门</button>
</div>

<div id="quiz" class="screen">
<div class="prog"><div class="prog-bar" id="pb"></div></div>
<div class="qcard fi" id="qc">
<div class="qtext" id="qt"></div>
<div class="opts" id="os"></div>
</div>
<p style="color:rgba(255,255,255,.3);font-size:.8rem;margin-top:10px" id="qn"></p>
</div>

<div id="loading" class="screen">
<div class="ld">命运之线正在编织<span class="dots"></span></div>
<p style="color:rgba(255,255,255,.3);margin-top:20px">魔法正在寻找那个与你最契合的灵魂</p>
</div>

<div id="result" class="screen">
<div class="rcard fi" id="rc"></div>
<button class="rbtn" onclick="restart()">重新开始</button>
</div>

<script>
''' + cj + '\n' + qj + r'''
const D=['loyalty','depth','bravery','rebel','humor','adventure','morals','wisdom'];
let qi=0,sc={},cqs=[];
function sh(a){let b=[...a];for(let i=b.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]]}return b}
function start(){
    document.getElementById('intro').classList.remove('active');
    document.getElementById('quiz').classList.add('active');
    let genderQs=QS.filter(q=>q.o[0]&&q.o[0].s&&q.o[0].s._sel);
    let normalQs=QS.filter(q=>!(q.o[0]&&q.o[0].s&&q.o[0].s._sel));
    let picked=sh(genderQs).slice(0,2);
    picked=picked.concat(sh(normalQs).slice(0,8));
    cqs=sh(picked);
    sc={};D.forEach(d=>sc[d]=0);window._gm=0;window._gf=0;qi=0;showQ();
}
function showQ(){
    let q=cqs[qi];
    document.getElementById('qt').textContent=q.t;
    document.getElementById('pb').style.width=(qi/10*100)+'%';
    document.getElementById('qn').textContent='第'+(qi+1)+'/10题';
    let od=document.getElementById('os');od.innerHTML='';
    let so=sh(q.o);
    so.forEach(opt=>{
        let b=document.createElement('button');b.className='opt';b.textContent=opt.t;
        b.onclick=()=>pick(opt.s,b);od.appendChild(b);
    });
    let c=document.getElementById('qc');c.classList.remove('fi');void c.offsetWidth;c.classList.add('fi');
}
function pick(s,btn){
    document.querySelectorAll('.opt').forEach(b=>b.classList.remove('sel'));
    btn.classList.add('sel');
    for(let k in s){
        if(k==='_sel'){
            if(s[k]==='m')window._gm=(window._gm||0)+1;
            else if(s[k]==='f')window._gf=(window._gf||0)+1;
        }else{
            sc[k]=(sc[k]||0)+s[k];
        }
    }
    setTimeout(()=>{qi++;if(qi>=10)calc();else showQ()},400);
}
function calc(){
    document.getElementById('quiz').classList.remove('active');
    document.getElementById('loading').classList.add('active');
    setTimeout(()=>{
        let gm=window._gm||0,gf=window._gf||0;
        let tg=gm>gf?'female':gm<gf?'male':(Math.random()>0.5?'male':'female');
        let candidates=Object.keys(CHARS).filter(id=>CHARS[id].g===tg);
        let dists={};
        for(let id of candidates){
            let c=CHARS[id],d=0;
            for(let dim of D){let cw=c.s[dim]||0,uw=sc[dim]||0;d+=(cw-uw)*(cw-uw);}
            dists[id]=d;
        }
        let weights={};
        for(let id of candidates)weights[id]=1.0/(dists[id]+1.0);
        let avgW=Object.values(weights).reduce((a,b)=>a+b,0)/candidates.length;
        let minW=avgW*0.25;
        for(let id of candidates)weights[id]=Math.max(weights[id],minW);
        let totalW=Object.values(weights).reduce((a,b)=>a+b,0);
        let r=Math.random(),cum=0;
        let best=candidates[0];
        for(let id of candidates){cum+=weights[id]/totalW;if(r<=cum){best=id;break;}}
        let c=CHARS[best];
        let pct=Math.round(70+Math.random()*25);
        showR({...c,id:best},pct);
    },2500);
}
function showR(c,pct){
    document.getElementById('loading').classList.remove('active');
    document.getElementById('result').classList.add('active');
    let h='';
    h+='<div class="mpct">'+pct+'%</div>';
    h+='<div class="mlbl">命运羁绊匹配度</div>';
    h+='<div class="cname">'+c.n+'</div>';
    h+='<div class="'+c.hc+'">'+c.h+'</div>';
    h+='<div class="trs">'+c.t.map(t=>'<span class="tr">'+t+'</span>').join('')+'</div>';
    h+='<div style="margin:20px 0;color:#c4a882;line-height:1.8;font-size:1rem">'+c.r+'</div>';
    if(c.tb){
        h+='<div class="story">';
        h+='<div class="stitle">'+c.tt+'</div>';
        c.tb.split('\\n').forEach(p=>{if(p)h+='<p style="margin-bottom:15px">'+p+'</p>';});
        window._cs=c.tb;
        window._cn=c.n;
        window._ct=c.tt;
        h+='<div class="cpbtn" id="cpbtn">📋 复制故事，去小红书分享</div>';
        h+='</div>';
    }
    document.getElementById('rc').innerHTML=h;
    let btn=document.getElementById('cpbtn');
    if(btn)btn.onclick=copyStory;
}
function copyStory(){
    let body=window._cs||'';
    let name=window._cn||'';
    let title=window._ct||'';
    let txt='🕯️ 哈利波特角色匹配测试\n\n我匹配到了'+name+'！\n\n'+title+'\n\n'+body.replace(/\\n/g,'\n')+'\n\n—— 测测你匹配到了谁？👆';
    if(navigator.clipboard){
        navigator.clipboard.writeText(txt).then(()=>{
            let b=document.getElementById('cpbtn');
            if(b){b.textContent='✅ 已复制！快去小红书分享吧';setTimeout(()=>{b.textContent='📋 复制故事，去小红书分享';},3000);}
        });
    }else{
        let ta=document.createElement('textarea');ta.value=txt;document.body.appendChild(ta);
        ta.select();document.execCommand('copy');document.body.removeChild(ta);
        let b=document.getElementById('cpbtn');
        if(b){b.textContent='✅ 已复制！快去小红书分享吧';}
    }
}
function restart(){
    document.getElementById('result').classList.remove('active');
    document.getElementById('intro').classList.add('active');
}
(function(){
    let c=document.getElementById('stars');
    for(let i=0;i<80;i++){
        let s=document.createElement('div');s.className='star';
        s.style.cssText='left:'+Math.random()*100+'%;top:'+Math.random()*100+'%;width:'+(Math.random()*2+1)+'px;height:'+(Math.random()*2+1)+'px;--d:'+(Math.random()*3+2)+'s;animation-delay:'+Math.random()*3+'s';
        c.appendChild(s);
    }
})();
/* 微信小程序 WebView 通信补丁 */
(function(){var e="miniprogram"===window.__wxjs_environment||navigator.userAgent.indexOf("miniProgram")>-1;if(!e)return;!function e(t){void 0!==window.wx&&window.wx.miniProgram?t():setTimeout(function(){e(t)},100)}(function(){var e=window.showResult;"function"==typeof e&&(window.showResult=function(t,n){e(t,n),window.wx.miniProgram.postMessage({data:{type:"test_result",result:{charId:t,match:n,timestamp:Date.now()}}})});new MutationObserver(function(e){e.forEach(function(e){if(e.addedNodes.length>0)for(var t=0;t<e.addedNodes.length;t++){var n=e.addedNodes[t];if(1===n.nodeType&&"result-screen"===n.id){setTimeout(function(){var e=document.querySelector(".cname"),t=document.querySelector(".mpct");e&&t&&window.wx.miniProgram.postMessage({data:{type:"test_result",result:{charId:e.textContent.trim(),match:parseInt(t.textContent)||0,timestamp:Date.now()}}})},500);break}}})}).observe(document.body,{childList:!0,subtree:!0})})})();
</script>
</body>
</html>'''

with open(out,'w',encoding='utf-8') as f:
    f.write(html)
print(f'Written {len(html)} bytes to {out}')
