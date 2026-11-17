'use strict';
/* Curated historical archive: date events, real news links and video news;
   neither the news links nor the previews are described as a complete original live. */
(()=>{
 const $=id=>document.getElementById(id);
 if(document.body.dataset.page!=='fourps')return;
 const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const norm=v=>String(v??'').normalize('NFC').toLocaleLowerCase('th').replace(/[\u200b\u200c\u200d]/g,'').trim();
 const months=['','มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม','กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม'];
 const topics={viral:'สีสันและกระแส',debate:'ข้อถกเถียง',napan:'พระมหานภันต์',change:'ช่วงเปลี่ยนผ่าน'};
 const state={events:[],people:[],pending:[],query:'',filter:'all'};
 const isNews=s=>s.kind!=='video';
 function thaiDate(date,precision){
  const p=String(date||'').split('-'),y=Number(p[0]),m=Number(p[1]),d=Number(p[2]);
  if(!y||!m||m>12)return 'ไม่ระบุวัน';
  return (precision==='month'||!d?'':d+' ')+months[m]+' '+(y+543);
 }
 function monthLabel(date){const p=String(date).split('-');return months[Number(p[1])]+' '+(Number(p[0])+543);}
 function ordered(a,b){
  const ma=a.date.slice(0,7),mb=b.date.slice(0,7);
  if(ma!==mb)return ma.localeCompare(mb);
  return (a.date.length===10?Number(a.date.slice(8)):99)-(b.date.length===10?Number(b.date.slice(8)):99);
 }
 function https(url){try{return new URL(url).protocol==='https:'}catch{return false}}
 function youtubeId(url){
  try{const u=new URL(url),host=u.hostname;
   if(host!=='youtu.be'&&host!=='www.youtube.com'&&host!=='youtube.com')return '';
   const id=host==='youtu.be'?u.pathname.slice(1):u.searchParams.get('v')||'';
   return /^[A-Za-z0-9_-]{11}$/.test(id)?id:'';
  }catch{return ''}
 }
 function sourceCard(s){
  if(!https(s.url))return '';
  const video=s.kind==='video',id=video?youtubeId(s.url):'';
  const label=video?'คลิปข่าว / รายการ':s.kind==='report'?'รายงานวิเคราะห์':'ข่าว / บทความ';
  const image=id?'<span class="ps-source-thumb"><img src="https://i.ytimg.com/vi/'+id+'/mqdefault.jpg" loading="lazy" decoding="async" alt="" referrerpolicy="no-referrer"><span class="ps-video-mark" aria-hidden="true">▶</span></span>':'<span class="ps-source-icon" aria-hidden="true">'+(video?'▶':'▤')+'</span>';
  return '<a class="ps-source '+(video?'ps-source-video':'ps-source-news')+'" href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer" aria-label="เปิดแหล่งอ้างอิง '+esc(s.source)+': '+esc(s.title)+'">'
   +image+'<span class="ps-source-copy"><span class="ps-source-meta">'+esc(label)+' · '+esc(s.source)+'</span>'
   +'<strong>'+esc(s.title)+'</strong><span class="ps-source-note">'+esc(s.note||'เปิดดูจากผู้เผยแพร่ต้นทาง')+'</span></span>'
   +'<span class="ps-source-arrow" aria-hidden="true">↗</span></a>';
 }
 function personCard(p,i){
  const role=p.short==='นภันต์'?'พระอาจารย์ที่มีบทบาทในเหตุการณ์และยังครองสมณเพศเมื่อกลุ่ม 4 พส. ถูกกล่าวถึง':'พระนักเทศน์ในกระแส 2564–2565';
  return '<article class="ps-person"><span class="ps-person-index">'+String(i+1).padStart(2,'0')+'</span>'
   +'<strong class="ps-person-name">'+esc(p.name)+'</strong><span class="ps-person-role">'+esc(role)+'</span></article>';
 }
 function highlightCard(e){
  return '<a class="ps-focus-card" href="#'+esc(e.id)+'"><span class="ps-focus-icon" aria-hidden="true">✦</span>'
   +'<span class="ps-focus-date">'+esc(thaiDate(e.date,e.datePrecision))+'</span>'
   +'<strong>'+esc(e.title)+'</strong><span class="ps-focus-link">ไปยังเหตุการณ์ ↗</span></a>';
 }
 function eventCard(e){
  const numVideo=e.sources.filter(x=>x.kind==='video').length,numNews=e.sources.length-numVideo;
  const items=state.filter==='video'?e.sources.filter(x=>x.kind==='video'):state.filter==='news'?e.sources.filter(isNews):e.sources;
  const limit=state.filter==='video'?6:e.napan?4:3;
  const first=items.slice(0,limit),more=items.slice(limit);
  return '<article class="ps-event '+(e.napan?'ps-event-featured':'')+'" id="'+esc(e.id)+'">'
   +'<div class="ps-event-marker"><span class="ps-timeline-dot" aria-hidden="true"></span><span class="ps-event-date">'+esc(thaiDate(e.date,e.datePrecision))+'</span></div>'
   +'<div class="ps-event-main"><div class="ps-event-upper"><span class="ps-event-category">'+esc(topics[e.category]||'เหตุการณ์')+'</span>'
   +(e.napan?'<span class="ps-event-napan">✦ พระมหานภันต์มีส่วนร่วม</span>':'')+'</div>'
   +'<h3>'+esc(e.title)+'</h3><p class="ps-event-desc">'+esc(e.summary)+'</p>'
   +'<div class="ps-event-people"><span>บุคคลในเหตุการณ์</span>'+e.people.map(p=>'<span class="ps-person-tag">'+esc(p)+'</span>').join('')+'</div>'
   +'<div class="ps-event-source-title"><strong>หลักฐานและแหล่งเผยแพร่</strong><span>'+(numNews?numNews+' ข่าว/บทความ':'')
   +(numNews&&numVideo?' · ':'')+(numVideo?numVideo+' คลิป':'')+'</span></div>'
   +'<div class="ps-source-list">'+first.map(sourceCard).join('')+'</div>'
   +(more.length?'<details class="ps-more-sources"><summary>แสดงแหล่งอ้างอิงเพิ่มเติมอีก '+more.length+' รายการ <span aria-hidden="true">⌄</span></summary><div class="ps-source-list">'+more.map(sourceCard).join('')+'</div></details>':'')
   +'</div></article>';
 }
 function renderPending(){
  $('psPending').innerHTML=state.pending.map(p=>'<article class="ps-pending-card"><span class="ps-pending-state">◌ ยังไม่พบต้นฉบับที่ยืนยันได้</span>'
   +'<h3>'+esc(p.title)+'</h3><span class="ps-pending-date">'+esc(p.date)+'</span>'
   +'<p>'+esc(p.note)+'</p>'+(https(p.evidence)?'<a target="_blank" rel="noopener noreferrer" href="'+esc(p.evidence)+'">อ่านข่าวอ้างอิง ↗</a>':'')+'</article>').join('');
 }
 function matching(e){
  const f=state.filter;
  if(f==='napan'&&!e.napan)return false;
  if(f==='news'&&!e.sources.some(isNews))return false;
  if(f==='video'&&!e.sources.some(s=>s.kind==='video'))return false;
  if(['viral','debate','change'].includes(f)&&e.category!==f)return false;
  const q=norm(state.query);
  if(!q)return true;
  return norm([e.title,e.summary,e.date,thaiDate(e.date,e.datePrecision)]
   .concat(e.people,e.sources.flatMap(s=>[s.source,s.title,s.note])).join(' ')).includes(q);
 }
 function render(){
  const selected=state.events.filter(matching);
  let previous='';
  $('psTimeline').innerHTML=selected.map(e=>{
   const month=e.date.slice(0,7),separator=month!==previous?'<h3 class="ps-month-heading">'+esc(monthLabel(e.date))+'</h3>':'';
   previous=month;
   return separator+eventCard(e);
  }).join('');
  $('psEmpty').hidden=selected.length!==0;
  const count=selected.reduce((n,e)=>n+e.sources.filter(s=>state.filter!=='video'||s.kind==='video').length,0);
  $('psResultCount').textContent='แสดง '+selected.length+' จาก '+state.events.length+' เหตุการณ์ · '+count+' แหล่งอ้างอิง';
  $('psReset').hidden=!(norm(state.query)||state.filter!=='all');
  document.querySelectorAll('[data-ps-filter]').forEach(b=>{
   const active=b.dataset.psFilter===state.filter;
   b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));
  });
  $('psTimeline').querySelectorAll('.ps-source-thumb img').forEach(img=>{
   img.addEventListener('error',()=>img.parentElement.classList.add('ps-no-thumb'),{once:true});
  });
 }
 function reset(){
  state.filter='all';state.query='';$('psSearch').value='';render();
 }
 function wire(){
  $('psSearch').addEventListener('input',e=>{state.query=e.target.value;render();});
  $('psFilters').addEventListener('click',e=>{
   const button=e.target.closest('[data-ps-filter]');
   if(button){state.filter=button.dataset.psFilter;render();}
  });
  $('psReset').addEventListener('click',reset);
  $('psEmptyReset').addEventListener('click',reset);
 }
 async function load(){
  wire();
  try{
   const response=await fetch('./data/four-ps.json',{cache:'no-cache'});
   if(!response.ok)throw new Error('Archive HTTP '+response.status);
   const data=await response.json();
   if(!Array.isArray(data.events)||!Array.isArray(data.people)||!Array.isArray(data.pending))throw new Error('Invalid archive data');
   state.events=data.events.filter(e=>/^\d{4}-\d{2}(-\d{2})?$/.test(e.date||'')&&Array.isArray(e.sources)&&e.title).sort(ordered);
   state.people=data.people;state.pending=data.pending;
   $('psPeople').innerHTML=state.people.map(personCard).join('');
   $('psSpotlightGrid').innerHTML=state.events.filter(e=>e.napan&&e.featured).map(highlightCard).join('');
   $('psEventTotal').textContent=state.events.length;
   const allSources=state.events.flatMap(e=>e.sources);
   $('psNewsTotal').textContent=allSources.filter(isNews).length;
   $('psVideoTotal').textContent=allSources.filter(s=>s.kind==='video').length;
   $('psNapanTotal').textContent=state.events.filter(e=>e.napan).length;
   renderPending();render();
   if(/^#ps-\d+$/.test(location.hash))document.getElementById(location.hash.slice(1))?.scrollIntoView({block:'start'});
  }catch(error){
   console.error('Cannot load editorial archive',error);
   $('psTimeline').innerHTML='<p class="ps-load-error">ไม่สามารถโหลดเส้นเวลาได้ กรุณาลองรีเฟรช หรือเปิด <a href="./press.html">ข่าวและผลงาน ↗</a></p>';
   $('psPeople').innerHTML='';$('psSpotlightGrid').innerHTML='';$('psPending').innerHTML='';
   $('psResultCount').textContent='ไม่สามารถโหลดข้อมูลได้';
  }
 }
 load();
})();
