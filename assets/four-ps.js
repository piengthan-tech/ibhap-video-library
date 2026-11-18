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
 function sourceCard(s,event){
  if(!https(s.url))return '';
  const video=s.kind==='video',id=video?youtubeId(s.url):'';
  const label=video?(s.video_type==='channel_upload'?'วิดีโอจากช่องผู้เผยแพร่':'คลิปข่าวและรายการ'):s.kind==='report'?'รายงานวิเคราะห์':'ข่าว / บทความ';
  // Where the specific article has no accessible photograph, show a verified related
  // article photo from the SAME dated event. Label its actual publisher explicitly.
  const related=(!video&&!https(s.thumbnail))?illustrationSource(event,'news'):null;
  const borrowed=related && https(related.thumbnail)?related:null;
  const imageSrc=id?'https://i.ytimg.com/vi/'+id+'/mqdefault.jpg':https(s.thumbnail)?s.thumbnail:borrowed?borrowed.thumbnail:'';
  const imageCredit=borrowed?'ภาพประกอบจาก '+borrowed.source:'';
  const image=imageSrc?
   '<span class="ps-source-thumb '+(id?'ps-source-thumb-video':'ps-source-thumb-news')+'"><img src="'+esc(imageSrc)+'" loading="lazy" decoding="async" alt="" referrerpolicy="no-referrer" width="120" height="72">'
    +(video?'<span class="ps-video-mark" aria-hidden="true">▶</span>':'')+'<span class="ps-thumb-fallback" aria-hidden="true">▤</span></span>':
   '<span class="ps-source-icon" aria-hidden="true">'+(video?'▶':'▤')+'</span>';
  return '<a class="ps-source '+(video?'ps-source-video':'ps-source-news')+'" href="'+esc(s.url)+'" target="_blank" rel="noopener noreferrer" aria-label="เปิดแหล่งอ้างอิง '+esc(s.source)+': '+esc(s.title)+'">'
   +image+'<span class="ps-source-copy"><span class="ps-source-meta">'+esc(label)+' · '+esc(s.source)+'</span>'
   +'<strong>'+esc(s.title)+'</strong><span class="ps-source-note">'+esc(s.note||'เปิดดูจากผู้เผยแพร่ต้นทาง')+'</span>'
   +(imageCredit?'<span class="ps-source-image-attribution">'+esc(imageCredit)+'</span>':'')+'</span>'
   +'<span class="ps-source-arrow" aria-hidden="true">↗</span></a>';
 }
 function illustrationSource(event,mode){
  if(mode==='video'){
   const video=event.sources.find(s=>s.kind==='video'&&youtubeId(s.url));
   if(video)return {url:video.url,title:video.title,source:video.source,thumbnail:'https://i.ytimg.com/vi/'+youtubeId(video.url)+'/hqdefault.jpg',video:true};
  }
  const report=event.sources.find(s=>s.id===event.featured_source_id&&s.kind!=='video'&&https(s.thumbnail)&&https(s.url))
    ||event.sources.find(s=>s.kind!=='video'&&https(s.thumbnail)&&https(s.url));
  if(report)return {...report,video:false};
  const video=event.sources.find(s=>s.kind==='video'&&youtubeId(s.url));
  if(video)return {url:video.url,title:video.title,source:video.source,thumbnail:'https://i.ytimg.com/vi/'+youtubeId(video.url)+'/hqdefault.jpg',video:true};
  return null;
 }
 function eventPhoto(event,mode){
  const report=illustrationSource(event,mode);
  if(!report)return '';
  const caption=(report.video?'ภาพปกคลิปข่าว · ':'ภาพประกอบจากข่าว · ')+report.source;
  return '<a class="ps-event-illustration" target="_blank" rel="noopener noreferrer" href="'+esc(report.url)+'" aria-label="เปิดแหล่งข่าวต้นทางของภาพประกอบ '+esc(report.source)+'">'
    +'<span class="ps-event-illustration-media"><img src="'+esc(report.thumbnail)+'" alt="" width="480" height="270" loading="lazy" decoding="async" referrerpolicy="no-referrer">'
    +'<span class="ps-event-image-fallback" aria-hidden="true">ดูรายละเอียดจากแหล่งข่าว</span></span>'
    +'<span class="ps-event-illustration-caption"><span>'+esc(caption)+'</span><span aria-hidden="true">↗</span></span></a>';
 }
 function personCard(p,i){
  const role=p.short==='นภันต์'?'พระนักเทศน์และผู้ร่วมเหตุการณ์สำคัญ':'พระนักเทศน์ที่เกี่ยวข้องกับปรากฏการณ์ พส.';
  return '<article class="ps-person"><span class="ps-person-index">'+String(i+1).padStart(2,'0')+'</span>'
   +'<strong class="ps-person-name">'+esc(p.name)+'</strong><span class="ps-person-role">'+esc(role)+'</span></article>';
 }
 function highlightCard(e){
  const cover=eventPhoto(e,'news');
  return '<a class="ps-focus-card" href="#'+esc(e.id)+'">'
   +(cover?'<span class="ps-focus-photo"><img src="'+esc(illustrationSource(e,'news').thumbnail)+'" width="480" height="270" loading="eager" decoding="async" alt="" referrerpolicy="no-referrer"><span class="ps-focus-photo-fallback">ดูเหตุการณ์ในเส้นเวลา</span></span>':'')
   +'<span class="ps-focus-body"><span class="ps-focus-date">'+esc(thaiDate(e.date,e.datePrecision))+'</span>'
   +'<strong>'+esc(e.title)+'</strong><span class="ps-focus-link">อ่านรายละเอียด <span aria-hidden="true">↗</span></span></span></a>';
 }
 function eventCard(e){
  const numVideo=e.sources.filter(x=>x.kind==='video').length,numNews=e.sources.length-numVideo;
  const items=state.filter==='video'?e.sources.filter(x=>x.kind==='video'):state.filter==='news'?e.sources.filter(isNews):e.sources;
  const limit=state.filter==='video'?6:e.napan?4:3;
  const first=items.slice(0,limit),more=items.slice(limit);
  const category=['viral','debate','napan','change'].includes(e.category)?e.category:'general';
  return '<article class="ps-event ps-event--'+category+' '+(e.napan?'ps-event-featured':'')+'" id="'+esc(e.id)+'">'
   +'<div class="ps-event-marker"><span class="ps-timeline-dot" aria-hidden="true"></span><span class="ps-event-date">'+esc(thaiDate(e.date,e.datePrecision))+'</span></div>'
   +'<div class="ps-event-main"><div class="ps-event-overview"><div class="ps-event-story">'
   +'<div class="ps-event-upper"><span class="ps-event-category">'+esc(topics[e.category]||'เหตุการณ์')+'</span>'
   +(e.napan?'<span class="ps-event-napan">เกี่ยวข้องกับพระมหานภันต์</span>':'')+'</div>'
   +'<h3>'+esc(e.title)+'</h3><p class="ps-event-desc">'+esc(e.summary)+'</p>'
   +'<div class="ps-event-people"><span>บุคคลที่เกี่ยวข้อง</span>'+e.people.map(p=>'<span class="ps-person-tag">'+esc(p)+'</span>').join('')+'</div></div>'
   +eventPhoto(e,state.filter)+'</div>'
   +'<div class="ps-event-source-title"><strong>ข่าวและสื่อที่เกี่ยวข้อง</strong><span>'+(numNews?numNews+' ข่าว/บทความ':'')
   +(numNews&&numVideo?' · ':'')+(numVideo?numVideo+' คลิป':'')+'</span></div>'
   +'<div class="ps-source-list">'+first.map(source=>sourceCard(source,e)).join('')+'</div>'
   +(more.length?'<details class="ps-more-sources"><summary>ดูเพิ่มเติมอีก '+more.length+' รายการ <span aria-hidden="true">⌄</span></summary><div class="ps-source-list">'+more.map(source=>sourceCard(source,e)).join('')+'</div></details>':'')
   +'</div></article>';
 }
 function renderVideoHighlights(){
  const target=$('psVideoFeatured');
  if(!target)return;
  const result=[],seen=new Set();
  // Only one source per event; the editorially selected official upload gets first priority.
  const prioritized=state.events.slice().sort((a,b)=>{
   const ap=Number(!!a.featured_video_source_id),bp=Number(!!b.featured_video_source_id);
   return bp-ap || Number(!!b.napan)-Number(!!a.napan) || a.date.localeCompare(b.date);
  });
  for(const event of prioritized){
   const item=event.sources.find(source=>source.id===event.featured_video_source_id&&source.kind==='video'&&youtubeId(source.url)&&!seen.has(source.url))
    ||event.sources.find(source=>source.kind==='video'&&youtubeId(source.url)&&!seen.has(source.url));
   if(!item)continue;
   seen.add(item.url);
   result.push({event,source:item,id:youtubeId(item.url)});
   if(result.length===3)break;
  }
  result.sort((a,b)=>a.event.date.localeCompare(b.event.date));
  if(!result.length){
    target.innerHTML='<p class="ps-loading">ยังไม่มีวิดีโอสำหรับแสดงในส่วนนี้ <a href="#psTimelineSection">ดูข้อมูลเหตุการณ์ทั้งหมด ↗</a></p>';
    return;
  }
  target.innerHTML=result.map(({event,source,id})=>{
   return '<a class="ps-video-teaser" href="'+esc(source.url)+'" target="_blank" rel="noopener noreferrer" aria-label="เปิดคลิปข่าว '+esc(source.title)+' จาก '+esc(source.source)+'">'
    +'<span class="ps-video-teaser-photo"><img src="https://i.ytimg.com/vi/'+id+'/hqdefault.jpg" width="480" height="270" loading="lazy" decoding="async" alt="" referrerpolicy="no-referrer">'
    +'<span class="ps-video-teaser-play" aria-hidden="true">▶</span></span>'
    +'<span class="ps-video-teaser-body"><span class="ps-video-teaser-meta"><span class="ps-teaser-dot" aria-hidden="true"></span>'
    +esc(source.source)+' · '+esc(thaiDate(event.date,event.datePrecision))+'</span>'
    +'<strong>'+esc(source.title)+'</strong>'
    +'<span class="ps-video-teaser-cta">'+(source.video_type==='channel_upload'?'รับชมวิดีโอ':'รับชมคลิปจากผู้เผยแพร่')+' <span aria-hidden="true">↗</span></span></span></a>';
  }).join('');
  target.querySelectorAll('.ps-video-teaser-photo img').forEach(img=>
    img.addEventListener('error',()=>img.parentElement.classList.add('ps-teaser-no-thumb'),{once:true}));
 }
 function renderPending(){
  $('psPending').innerHTML=state.pending.map(p=>'<article class="ps-pending-card"><span class="ps-pending-state">อยู่ระหว่างรวบรวมข้อมูล</span>'
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
   const fail=()=>img.parentElement.classList.add('ps-no-thumb');
   img.addEventListener('error',fail,{once:true});
   img.addEventListener('load',()=>img.parentElement.classList.remove('ps-no-thumb'),{once:true});
  });
  $('psTimeline').querySelectorAll('.ps-event-illustration-media img').forEach(img=>{
   const fail=()=>img.parentElement.classList.add('ps-event-image-error');
   img.addEventListener('error',fail,{once:true});
   img.addEventListener('load',()=>img.parentElement.classList.remove('ps-event-image-error'),{once:true});
  });
 }
 function reset(){
  state.filter='all';state.query='';$('psSearch').value='';render();
 }

 function setupArchiveNavigation(){
  const nav=$('psSectionNav'),bar=$('psProgressBar');
  if(!nav||!bar)return;
  const links=[...nav.querySelectorAll('[data-ps-section]')];
  const sections=links.map(link=>document.getElementById(link.dataset.psSection)).filter(Boolean);
  let ticking=false;
  function update(){
   ticking=false;
   const headerH=document.querySelector('.site-header')?.getBoundingClientRect().height||0;
   const navH=nav.getBoundingClientRect().height||0;
   const marker=window.scrollY+headerH+navH+24;
   let active=sections[0];
   for(const section of sections)if(section.offsetTop<=marker)active=section;
   links.forEach(link=>{
    const on=link.dataset.psSection===active?.id;
    link.classList.toggle('active',on);
    if(on)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');
   });
   const start=sections[0]?.offsetTop||0;
   const end=(sections.at(-1)?.offsetTop||document.body.scrollHeight)+(sections.at(-1)?.offsetHeight||0)-window.innerHeight;
   const progress=end>start?Math.max(0,Math.min(1,(window.scrollY-start)/(end-start))):0;
   bar.style.width=(progress*100).toFixed(1)+'%';
  }
  function requestUpdate(){if(!ticking){ticking=true;requestAnimationFrame(update)}}
  window.addEventListener('scroll',requestUpdate,{passive:true});
  window.addEventListener('resize',requestUpdate);
  links.forEach(link=>link.addEventListener('click',()=>{
    try{window.pmnapanTrack?.('archive_4ps_section',{section_id:link.dataset.psSection})}catch(_){}
    setTimeout(requestUpdate,80);
  }));
  requestUpdate();
 }

 function wire(){
  $('psSearch').addEventListener('input',e=>{state.query=e.target.value;render();});
  $('psSearch').addEventListener('change',e=>{const q=e.target.value.trim();if(q)try{window.pmnapanTrack?.('archive_4ps_search',{search_term:q})}catch(_){}});
  $('psFilters').addEventListener('click',e=>{
   const button=e.target.closest('[data-ps-filter]');
   if(button){state.filter=button.dataset.psFilter;try{window.pmnapanTrack?.('archive_4ps_filter',{filter_value:state.filter})}catch(_){}render();}
  });
  $('psReset').addEventListener('click',reset);
  $('psEmptyReset').addEventListener('click',reset);
 }
 async function load(){
  wire();
  setupArchiveNavigation();
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
   renderPending();renderVideoHighlights();render();
   $('psSpotlightGrid').querySelectorAll('.ps-focus-photo img').forEach(img=>{
     const fail=()=>img.parentElement.classList.add('ps-focus-photo-error');
     img.addEventListener('error',fail,{once:true});
     img.addEventListener('load',()=>img.parentElement.classList.remove('ps-focus-photo-error'),{once:true});
   });
   if(/^#ps-\d+$/.test(location.hash))document.getElementById(location.hash.slice(1))?.scrollIntoView({block:'start'});
  }catch(error){
   console.error('Cannot load editorial archive',error);
   $('psTimeline').innerHTML='<p class="ps-load-error">ไม่สามารถแสดงข้อมูลได้ในขณะนี้ กรุณาโหลดหน้าใหม่หรือดู <a href="./press.html">ข่าวและผลงาน ↗</a></p>';
   $('psPeople').innerHTML='';$('psSpotlightGrid').innerHTML='';$('psPending').innerHTML='';
   $('psResultCount').textContent='ไม่สามารถโหลดข้อมูลได้';
  }
 }
 load();
})();
