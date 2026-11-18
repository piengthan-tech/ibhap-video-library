(()=>{'use strict';
const $=id=>document.getElementById(id);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtDate=s=>{if(!/^\d{4}-\d{2}-\d{2}$/.test(s||''))return '';const [y,m,d]=s.split('-').map(Number);return new Intl.DateTimeFormat('th-TH',{day:'numeric',month:'short',year:'numeric'}).format(new Date(y,m-1,d))};
const minLabel=n=>Number(n)>0?Math.round(Number(n))+' นาที':'';

function videoCard(v){
 const thumb=v.thumbnail||'./assets/monk-watering-620.webp';
 return '<article class="video-card"><div class="video-image"><a href="./video.html?id='+encodeURIComponent(v.key)+'" aria-label="'+esc(v.title)+'">'
  +'<img src="'+esc(thumb)+'" alt="" loading="lazy" decoding="async"></a>'
  +'<span class="platform-tag">'+esc(v.platform||'Video')+'</span>'+(v.minutes?'<span class="duration-tag">'+esc(minLabel(v.minutes))+'</span>':'')+'</div>'
  +'<div class="video-info"><p class="video-meta">'+esc(v.category||'')+(v.published_at?' <span>•</span> '+esc(fmtDate(v.published_at)):'')+'</p>'
  +'<h3><a href="./video.html?id='+encodeURIComponent(v.key)+'">'+esc(v.title)+'</a></h3>'
  +'<div class="video-actions"><a href="./video.html?id='+encodeURIComponent(v.key)+'">รายละเอียด</a><a href="'+esc(v.url)+'" target="_blank" rel="noopener noreferrer">ต้นฉบับ ↗</a></div></div></article>';
}
const profilePressThumb={N001:'./assets/profile/ven-napan-human-rights.webp','hands-on-leeds-2018':'./assets/profile/ven-napan-leeds.webp',N002:'./assets/profile/ven-napan-interfaith.webp'};
function pressCard(x){
 const imgSrc=profilePressThumb[x.id]||x.thumbnail||'';
 const thumb=imgSrc?'<a class="press-thumbnail '+(x.thumbnail_fit==='contain'?'press-thumbnail-contain':'')+'" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer"><img src="'+esc(imgSrc)+'" alt="" loading="lazy" decoding="async"></a>':'';
 return '<article class="press-card">'+thumb+'<div class="press-meta"><span class="press-kind">'+esc(x.category||'ข่าวและผลงาน')+'</span>'+(x.published_at?'<time>'+esc(fmtDate(x.published_at))+'</time>':'')+'</div>'
  +'<h2>'+esc(x.title)+'</h2><p class="press-summary">'+esc(x.summary||'')+'</p><div class="press-source"><span>แหล่งเผยแพร่</span><strong>'+esc(x.source||'')+'</strong></div>'
  +'<a class="press-outbound" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer">อ่านต้นฉบับ ↗</a></article>';
}
function quoteCard(x){
 return '<article class="quote-card"><a class="quote-image" href="'+esc(x.image)+'" target="_blank" rel="noopener noreferrer" aria-label="เปิดภาพคำคมขนาดเต็ม"><img src="'+esc(x.image)+'" alt="ภาพคำคมพระมหานภันต์ สนฺติภทฺโท" loading="lazy" decoding="async"></a>'
  +'<div class="quote-body"><p class="quote-text">'+esc(x.text||'')+'</p><div class="quote-footer"><span>'+esc(x.speaker||'พระมหานภันต์ สนฺติภทฺโท')+'</span><a href="./quotes.html">ดูคลังคำคม ↗</a></div></div></article>';
}
async function getJson(url){const r=await fetch(url,{cache:'no-cache'});if(!r.ok)throw new Error(url+' '+r.status);return r.json()}
async function init(){
 try{
  const [vd,pd,qd]=await Promise.all([getJson('./data/videos.json'),getJson('./data/press.json'),getJson('./data/quotes.json')]);
  const videos=vd.items||[],press=pd.items||[],quotes=qd.items||[];
  const vtotal=$('profileVideoTotal'),ptotal=$('profilePressTotal'),qtotal=$('profileQuoteTotal');
  if(vtotal)vtotal.textContent=videos.length.toLocaleString('th-TH');
  if(ptotal)ptotal.textContent=press.length.toLocaleString('th-TH');
  if(qtotal)qtotal.textContent=quotes.length.toLocaleString('th-TH');

  const asa=videos.filter(v=>v.category==='อาสาหาธรรม').sort((a,b)=>(b.published_at||'').localeCompare(a.published_at||'')).slice(0,3);
  const vg=$('profileVideoGrid');if(vg)vg.innerHTML=asa.length?asa.map(videoCard).join(''):'<div class="empty"><p>ยังไม่มีวิดีโอที่ตรงกับเงื่อนไข</p></div>';

  const priority=['N001','hands-on-leeds-2018','N002'];
  const selected=priority.map(id=>press.find(x=>x.id===id)).filter(Boolean);
  const pg=$('profilePressGrid');if(pg)pg.innerHTML=selected.map(pressCard).join('');

  const quoteTests=[/SDGs|เป้าหมายการพัฒนา/i,/ความรุนแรง/i,/ฟัง|พูด/i];
  const seen=new Set(),chosen=[];
  for(const re of quoteTests){const q=quotes.find(x=>!seen.has(x.id)&&re.test(x.text||''));if(q){seen.add(q.id);chosen.push(q)}}
  for(const q of quotes){if(chosen.length>=3)break;if(!seen.has(q.id)){seen.add(q.id);chosen.push(q)}}
  const qg=$('profileQuoteGrid');if(qg)qg.innerHTML=chosen.slice(0,3).map(quoteCard).join('');
 }catch(err){
  console.error(err);
  for(const id of ['profileVideoGrid','profilePressGrid','profileQuoteGrid']){const el=$(id);if(el)el.innerHTML='<div class="empty"><p>ไม่สามารถโหลดรายการที่เกี่ยวข้องได้ในขณะนี้</p></div>'}
 }
}
document.addEventListener('DOMContentLoaded',init);
})();