'use strict';
/* PMNapan Library — standalone pages on GitHub Pages, grounded in data/videos.json */
const $ = id => document.getElementById(id);
const page = document.body.dataset.page;
const DATA_URL = './data/videos.json';
const QUOTES_URL = './data/quotes.json';
const PAGE_SIZE = 15;
const storageKey = 'ven-napan-library-favorites-v1';
let items = [], quotes = [], favorites = new Set(), visibleCount = PAGE_SIZE, activeCategory = '', selected = [];
const esc = value => String(value ?? '').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const norm = value => String(value || '').normalize('NFC').toLocaleLowerCase('th').replace(/[\u200b\u200c\u200d]/g,'').trim();
const safeLink = url => {try{const u=new URL(url);return u.protocol==='https:' && /(^|\.)(youtube\.com|youtu\.be|facebook\.com|fb\.watch|tiktok\.com)$/.test(u.hostname)}catch{return false}};
const idSafe = id=>/^[-_A-Za-z0-9]{11}$/.test(id);
const uri = (file,params={}) => {
 const query=new URLSearchParams(params).toString();
 return './'+file+(query?'?'+query:'');
};
function thumb(x){
 if(x.thumbnail && /^\.\/assets\/episode-stills\/[-_A-Za-z0-9]{11}\.jpg$/.test(x.thumbnail))return x.thumbnail;
 if(x.platform==='TikTok' && x.thumbnail==='./assets/tiktok-covers/'+x.video_id+'.webp' && /^\d{19}$/.test(x.video_id))return x.thumbnail;
 return x.platform==='YouTube' && idSafe(x.video_id) ? 'https://i.ytimg.com/vi/'+x.video_id+'/hqdefault.jpg' : '';
}
function formatDate(value){
 if(!/^\d{4}-\d{2}-\d{2}$/.test(value||''))return 'ไม่ระบุวันที่เผยแพร่';
 const d=new Date(value+'T12:00:00+07:00');
 return Number.isNaN(d.getTime())?'ไม่ระบุวันที่เผยแพร่':new Intl.DateTimeFormat('th-TH',{day:'numeric',month:'short',year:'numeric'}).format(d);
}
function duration(minutes){
 const seconds=Math.round(Number(minutes||0)*60);
 if(seconds<1)return '';
 const h=Math.floor(seconds/3600),m=Math.floor(seconds%3600/60),s=seconds%60;
 return h? h+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0'):m+':'+String(s).padStart(2,'0');
}
let DISCOVERY_TOPICS=[];
const legacyTopicNames={listening:'family',life:'mind',mindfulness:'meditation',
 relationships:'family',volunteer:'society',everyday:'mind'};
const discoveryTopic = id => DISCOVERY_TOPICS.find(t=>t.id===id);
function resolveTopicId(id){return discoveryTopic(id)?id:(legacyTopicNames[id]||null)}
function topicMatches(item,topicId){
 if(!topicId)return true;
 const topic=discoveryTopic(topicId);
 return !!topic && topic.keys.has(item.key);
}
async function loadCuratedTopics(){
 const response=await fetch('./data/discovery-topics.json',{cache:'no-cache'});
 if(!response.ok)throw new Error('Curated topic index HTTP '+response.status);
 const raw=await response.json();
 const validKeys=new Set(items.map(x=>x.key));
 DISCOVERY_TOPICS=(Array.isArray(raw.topics)?raw.topics:[]).filter(t=>
  /^[a-z]+$/.test(t.id||'')&&typeof t.label==='string'&&Array.isArray(t.keys)
 ).map(t=>({id:t.id,label:t.label,description:t.description||'',
  keys:new Set(t.keys.filter(key=>validKeys.has(key)))
 })).filter(t=>t.keys.size>0);
}
const categoryNames = () => [...new Set(items.map(x=>x.category))];
const byDateDesc=(a,b)=>(b.published_at||'').localeCompare(a.published_at||'') || a.title.localeCompare(b.title,'th');
const favoriteKey=x=>x.platform+':'+x.video_id;
const related = x=>x.relation==='ibhap_subtitles';
function openVideoHref(x){return uri('video.html',{id:x.key})}
function card(x){
 const preview=thumb(x),liked=favorites.has(favoriteKey(x));
 return `<article class="video-card ${x.platform==='TikTok'?'short-video-card':''}" data-key="${esc(x.key)}">
 <div class="video-image">
   <a href="${esc(openVideoHref(x))}" aria-label="รายละเอียดวิดีโอ ${esc(x.title)}">
   ${preview?`<img src="${esc(preview)}" alt="ภาพปกจากวิดีโอ ${esc(x.title)}" loading="lazy" decoding="async">`:'<span class="image-fallback">▶</span>'}
   </a>
   <span class="platform-tag">${esc(x.platform)}</span>
   ${x.minutes ? `<span class="duration-tag">${duration(x.minutes)}</span>` : ''}
   <button type="button" class="save-btn ${liked?'saved':''}" data-save="${esc(x.key)}" aria-label="${liked?'นำออกจากรายการที่บันทึก':'บันทึกวิดีโอ'}" aria-pressed="${liked}">${liked?'♥':'♡'}</button>
 </div>
 <div class="video-info">
 <p class="video-meta">${esc(x.category)} <span aria-hidden="true">·</span> ${esc(formatDate(x.published_at))}</p>
 <h3><a href="${esc(openVideoHref(x))}">${esc(x.title)}</a></h3>
 ${related(x)?'<span class="related-label">งานซับไตเติลของมูลนิธิ สกพ.</span>':''}
 <div class="video-actions"><a href="${esc(openVideoHref(x))}">รายละเอียด →</a><a href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">วิดีโอต้นฉบับ ↗</a></div>
 </div></article>`;
}
// Covers manually reviewed from the ORIGINAL YouTube thumbnails or footage stills;
 // identifiers must belong to that exact category, otherwise fall back to a real clip.
const preferredCategoryCover={
 'อาสาหาธรรม':'PDLdpx3H1vo',
 'มามองพุทธ มุมมองพระ':'TofNdwjXy_E',
 'คุยธรรมะสารพัน':'wZ71gbMrkbc',
 'งานต่างประเทศและสื่อสากล':'4u00ey9RtIY',
 'ธรรมบรรยายและสื่อย้อนหลัง':'FAH3e_YK5pE',
 'เพื่อนกันวันติดโควิด':'9STk1xCxNGA',
 'สวัสดีความสุข':'NP3IrZzSRkw'
};
function chooseCover(group){
 const preferred=preferredCategoryCover[group[0]?.category];
 const verified=group.find(x=>x.video_id===preferred);
 if(verified)return verified;
 const originals=group.filter(x=>x.thumbnail).sort(byDateDesc);
 return originals[0] || [...group].sort(byDateDesc)[0];
}
function quoteCard(q){
 const image=esc(q.image);
 const quoteText=typeof q.text==='string'?q.text.trim():'';
 const alt=quoteText
   ? 'ภาพคำคมธรรมะพระมหานภันต์ ข้อความ: '+quoteText.replace(/\s+/g,' ').slice(0,110)
   : 'ภาพคำคมธรรมะพระมหานภันต์ สนฺติภทฺโท';
 return '<article class="quote-card" data-photo-id="'+esc(q.id)+'">'+
   '<a class="quote-image" href="'+image+'" target="_blank" rel="noopener noreferrer" aria-label="เปิดภาพคำคมธรรมะขนาดเต็ม">'+
   '<img src="'+image+'" alt="'+esc(alt)+'" loading="lazy" decoding="async"></a>'+
   '</article>';
}
function quoteCategoryCard(){
 if(!quotes.length)return '';
 const q=quotes[0];
 return `<a class="series-card quote-series-card" href="./quotes.html">
  <div class="series-image"><img src="${esc(q.image)}" alt="ภาพคำคมธรรมะจากเพจพระมหานภันต์" loading="lazy"><span class="series-number">10</span></div>
  <div class="series-info"><strong>คำคมธรรมะ</strong><span>${quotes.length.toLocaleString('th-TH')} ภาพ <b aria-hidden="true">↗</b></span></div>
 </a>`;
}
function renderHomeQuotes(){
 const target=$('homeQuotes');
 if(target)target.innerHTML=quotes.length?quotes.slice(0,2).map(quoteCard).join(''):'<p class="empty">ยังไม่มีภาพคำคมที่ผ่านการตรวจสอบ</p>';
}
function renderQuotesPage(){
 const input=$('quoteSearch');
 const available=quotes.filter(item=>!!item.text.trim()).length;
 const coverage=$('quoteSearchCoverage');
 if(coverage)coverage.textContent='ค้นหาจากข้อความที่ตรวจสอบแล้ว '+available.toLocaleString('th-TH')+' จาก '+quotes.length.toLocaleString('th-TH')+' ภาพ ส่วนภาพอื่นยังเปิดดูได้ตามปกติ';
 const clear=$('clearQuoteSearch');
 if(clear)clear.addEventListener('click',()=>{input.value='';render();input.focus()});
 function render(){
   const q=norm(input.value);
   const filtered=quotes.filter(item=>!q||norm(item.text).includes(q));
   $('quoteGrid').innerHTML=filtered.map(quoteCard).join('');
   $('quoteEmpty').hidden=filtered.length>0;
   $('quotesCount').textContent='พบ '+filtered.length.toLocaleString('th-TH')+' ภาพคำคมธรรมะ';
 }
 input.addEventListener('input',render);
 render();
}
function validateQuotes(raw){
 const seen=new Set(),hashes=new Set();
 const entries=Array.isArray(raw?.items)?raw.items:[];
 return entries.filter(x=>{
  if(typeof x.text!=='string'||! /^[0-9a-f]{64}$/.test(x.sha256||''))return false;
  const id=String(x.id||''), img=String(x.image||'');
  const curated=/^\d{10,18}$/.test(id)
    && img==='./assets/quotes/'+id+'.jpg'
    && x.source_url==='https://www.facebook.com/photo.php?fbid='+id
    && !!x.text.trim();
  const imported=/^local-[0-9a-f]{20}$/.test(id)
    && img==='./assets/quotes/'+id+'.jpg'
    && x.sha256.startsWith(id.slice(6))
    && x.origin==='local_folder'
    && x.source_url==='' && x.text==='';
  if((!curated&&!imported)||seen.has(id)||hashes.has(x.sha256))return false;
  seen.add(id);hashes.add(x.sha256);return true;
 });
}
function categoryCard(name,group,i){
 const image=thumb(chooseCover(group));
 return `<a class="series-card ${name.includes('Dhamma Shorts')?'short-series-card':''}" href="${esc(name.includes('Dhamma Shorts')?'./shorts.html':uri('category.html',{name}))}">
  <div class="series-image">${image?`<img loading="lazy" decoding="async" src="${esc(image)}" alt="ภาพจากรายการ ${esc(name)}">`:'<span class="image-fallback">▶</span>'}<span class="series-number">0${i+1}</span></div>
  <div class="series-info"><strong>${esc(name)}</strong><span>${group.length.toLocaleString('th-TH')} คลิป <b aria-hidden="true">↗</b></span></div>
  </a>`;
}
function categoryCards(names){
 return names.map((name,i)=>categoryCard(name,items.filter(x=>x.category===name),i)).join('');
}
// Home-only category navigation: intentionally no video cover images.
// The separate "คลิปจากรายการ" section displays actual clip thumbnails.
function homeCategoryCard(name, i){
 const count=items.filter(x=>x.category===name).length;
 const href=name.includes('Dhamma Shorts')?'./shorts.html':uri('category.html',{name});
 const serial=String(i+1).padStart(2,'0');
 return `<a class="home-topic-card" href="${esc(href)}" aria-label="เปิดหมวด ${esc(name)} มี ${count} คลิป">
   <span class="home-topic-mark" aria-hidden="true"><span>${serial}</span></span>
   <span class="home-topic-copy">
     <span class="home-topic-eyebrow">หมวดวิดีโอ</span>
     <strong class="home-topic-name">${esc(name)}</strong>
     <span class="home-topic-count">${count.toLocaleString('th-TH')} คลิปในหมวดนี้</span>
   </span>
   <span class="home-topic-action" aria-hidden="true">↗</span>
  </a>`;
}
function homeCategoryCards(names){
 return names.map((name,i)=>homeCategoryCard(name,i)).join('');
}
function relatedNote(){
 return '<strong>เกี่ยวกับรายการ “หลวงพี่ช่วยด้วย”</strong><p>รายการต้นฉบับ Workpoint ดำเนินรายการโดยพระมหาสมปอง ตาลปุตฺโต คลิปหมวดนี้เป็นงานซับไตเติลของมูลนิธิ สกพ. ไม่ใช่คลิปที่พระมหานภันต์เป็นผู้บรรยาย</p><a href="https://www.youtube.com/playlist?list=PLFU5BMWz_rx10E1AiFivlOPsVO8qQFvmx" target="_blank" rel="noopener noreferrer">ดูเพลย์ลิสต์ต้นทาง ↗</a>';
}
function renderDiscoveryTopics(){
 const el=$('homeDiscoveryTopics');if(!el)return;
 const visible=DISCOVERY_TOPICS.map(t=>({...t,total:t.keys.size}));
 if(!visible.length){
  el.innerHTML='<p class="discovery-empty">ยังไม่สามารถแสดงหัวข้อที่คัดเลือกได้ <a href="./library.html">เปิดคลังวิดีโอทั้งหมด ↗</a></p>';
  return;
 }
 el.innerHTML=visible.map(t=>
  '<a class="discovery-topic" href="'+esc(uri('library.html',{topic:t.id}))+'">'
  +'<strong>'+esc(t.label)+'</strong><span>'+t.total.toLocaleString('th-TH')+' คลิป ↗</span></a>'
 ).join('');
}
function renderHomeLatest(){
 const target=$('homeLatest');
 if(!target)return;
 const recent=items.filter(x=>/^\d{4}-\d{2}-\d{2}$/.test(x.published_at||''))
   .sort(byDateDesc).slice(0,3);
 target.innerHTML=recent.length?recent.map(card).join(''):'<p class="empty">ยังไม่มีข้อมูลวันที่เผยแพร่จากต้นฉบับ</p>';
 target.querySelectorAll('.video-image img').forEach(attachImageFallback);
}
function renderHome(){
 $('homeTotal').textContent=items.length.toLocaleString('th-TH');
 renderHomeShorts();
 renderHomeQuotes();
 renderDiscoveryTopics();
 renderHomeLatest();
 const randomButton=$('randomArchiveClip');
 if(randomButton)randomButton.addEventListener('click',()=>{
  if(!items.length)return;
  location.href=openVideoHref(items[Math.floor(Math.random()*items.length)]);
 });
 $('homeCategories').innerHTML=homeCategoryCards(categoryNames().slice(0,6));
 const selections=categoryNames().slice(0,6).map(name=>chooseCover(items.filter(x=>x.category===name))).filter(Boolean);
 $('homeFeatured').innerHTML=selections.map(card).join('');
 $('homeSearchForm').addEventListener('submit',e=>{
  e.preventDefault();const q=$('homeSearch').value.trim();
  location.href=uri('library.html',q?{q}:{});
 });
}
function renderCategories(){
 const categories=categoryNames();
 $('categorySummary').textContent=categories.length.toLocaleString('th-TH')+' หมวดวิดีโอ'+(quotes.length?' · 1 หมวดคำคมธรรมะ':'');
 $('allCategories').innerHTML=categoryCards(categories)+quoteCategoryCard();
 const note=$('relatedNotice');note.hidden=!categories.some(n=>n.includes('หลวงพี่ช่วยด้วย'));
}
function renderFeatured(){
 const sections=categoryNames().map(name=>{
  const group=items.filter(x=>x.category===name).sort(byDateDesc);
  const cover=chooseCover(group);
  const featured=[cover,...group.filter(x=>x.key!==cover.key).slice(0,2)];
  return `<section class="featured-section"><div class="heading-row"><h2>${esc(name)}</h2><a href="${esc(name.includes('Dhamma Shorts')?'./shorts.html':uri('category.html',{name}))}" class="text-link">ดูหมวดนี้ทั้งหมด ↗</a></div><div class="video-grid">${featured.map(card).join('')}</div></section>`;
 });
 $('featuredSections').innerHTML=sections.join('');
}
const SHORTS_CATEGORY='ธรรมะคลิปสั้น | Dhamma Shorts';
let shortsVisible=16, shortsFiltered=[];
function shortCard(x){
 const image=thumb(x);
 return `<article class="short-card">
 <div class="short-cover"><a href="${esc(openVideoHref(x))}" aria-label="ดูรายละเอียดคลิปสั้น ${esc(x.title)}"><img src="${esc(image)}" alt="ภาพปกต้นฉบับ TikTok ${esc(x.title.slice(0,80))}" loading="lazy" decoding="async"></a>
  <span class="short-platform">TikTok</span><span class="short-duration">${duration(x.minutes)}</span></div>
 <div class="short-info"><p class="short-date">${esc(formatDate(x.published_at))}</p>
 <h3><a href="${esc(openVideoHref(x))}">${esc(x.title)}</a></h3>
 <div class="short-links"><a href="${esc(openVideoHref(x))}">รายละเอียด →</a><a target="_blank" rel="noopener noreferrer" href="${esc(x.url)}">ดูบน TikTok ↗</a></div></div>
 </article>`;
}
function renderHomeShorts(){
 const section=$('homeShorts');if(!section)return;
 const list=items.filter(x=>x.platform==='TikTok').sort(byDateDesc).slice(0,4);
 section.innerHTML=list.map(shortCard).join('') || '<div class="empty">ยังไม่มีวิดีโอสั้นในคลัง</div>';
}
function renderShorts(){
 const input=$('shortsSearch'),grid=$('shortsGrid'),more=$('loadShorts');
 function display(){
  grid.innerHTML=shortsFiltered.slice(0,shortsVisible).map(shortCard).join('');
  more.hidden=shortsVisible>=shortsFiltered.length;
  $('shortsEmpty').hidden=shortsFiltered.length>0;
  $('shortsCount').textContent=shortsFiltered.length.toLocaleString('th-TH')+' คลิป';
 }
 function search(){
  const q=norm(input.value).split(/\s+/).filter(Boolean);
  shortsFiltered=items.filter(x=>x.platform==='TikTok' && x.category===SHORTS_CATEGORY
   && q.every(t=>norm(x.title+' '+x.description+' '+x.published_at).includes(t))).sort(byDateDesc);
  shortsVisible=16;display();
 }
 input.addEventListener('input',search);
 more.addEventListener('click',()=>{shortsVisible+=16;display()});
 search();
}
function selectCategory(){
 const name=new URLSearchParams(location.search).get('name')||'';
 const options=categoryNames();
 if(!options.includes(name)){
  $('pageTitle').textContent='ไม่พบหมวดรายการ';
  $('categoryGrid').innerHTML='<div class="empty"><p>ไม่มีหมวดรายการนี้ในทะเบียน</p><a class="btn secondary" href="./categories.html">กลับไปหมวดรายการ</a></div>';
  return;
 }
 activeCategory=name;
 updateDynamicSeo(name,'วิดีโอในหมวด '+name+' จากคลังธรรมะของพระมหานภันต์ สนฺติภทฺโท');
 $('pageTitle').textContent=name;
 $('currentCrumb').textContent=name;
 const group=items.filter(x=>x.category===name).sort(byDateDesc);
 $('categoryCount').textContent=group.length.toLocaleString('th-TH')+' คลิป';
 const note=$('categoryRelationNote');
 note.hidden=!group.some(related);
 if(!note.hidden)note.innerHTML=relatedNote();
 selected=group;visibleCount=PAGE_SIZE;
 drawPaged($('categoryGrid'));
}
function updateDynamicSeo(title, description, thumbnail){
 if(title)document.title=title+' | PMNapan Library';
 if(description){
  const cleaned=String(description).replace(/\s+/g,' ').slice(0,180);
  for(const selector of ['meta[name="description"]','meta[property="og:description"]']){
   const el=document.querySelector(selector);if(el)el.content=cleaned;
  }
 }
 const canonical=document.querySelector('link[rel="canonical"]')?.href;
 if(canonical&&title&&description){
  let schema=document.getElementById('pmnapan-dynamic-schema');
  if(!schema){
   schema=document.createElement('script');
   schema.id='pmnapan-dynamic-schema';
   schema.type='application/ld+json';
   document.head.appendChild(schema);
  }
  schema.textContent=JSON.stringify({
   '@context':'https://schema.org',
   '@type':'WebPage',
   '@id':canonical+'#webpage',
   url:canonical,
   name:title,
   description:String(description).replace(/\s+/g,' ').slice(0,450),
   inLanguage:'th',
   isPartOf:{'@id':'https://www.ydml.co.th/pmnapan-library/#website'}
  });
 }
 const ogTitle=document.querySelector('meta[property="og:title"]');
 if(ogTitle&&title)ogTitle.content=title+' | PMNapan Library';
 if(thumbnail&&(thumbnail.startsWith('https://')||thumbnail.startsWith('http://'))){
  const ogImage=document.querySelector('meta[property="og:image"]');
  if(ogImage)ogImage.content=thumbnail;
 }
}
function renderVideoDetail(){
 const params=new URLSearchParams(location.search);
 const key=params.get('id')||params.get('clip')||'';
 const x=items.find(x=>x.key===key);
 if(!x){
  $('pageTitle').textContent='ไม่พบวิดีโอ';
  $('videoDetail').innerHTML='<div class="empty"><p>ไม่มีข้อมูลวิดีโอนี้ในทะเบียน</p><a class="btn secondary" href="./library.html">กลับไปคลังวิดีโอ</a></div>';
  return;
 }
 updateDynamicSeo(x.title, x.description||('วิดีโอจาก '+x.category+' บน PMNapan Library'), (thumb(x)||'').startsWith('https://') ? thumb(x) : '');
 $('pageTitle').textContent='รายละเอียดวิดีโอ';
 $('currentCrumb').textContent='รายละเอียดวิดีโอ';
 const src=thumb(x);
 const showSourceCredit=x.platform==='TikTok' && x.url.startsWith('https://www.tiktok.com/@domskyline21/video/');
 const sourceCredit=showSourceCredit ? `<aside class="source-credit video-source-credit" aria-label="ขอบคุณแหล่งเผยแพร่วิดีโอสั้น">
 <span class="source-credit-mark" aria-hidden="true">♫</span>
 <div class="source-credit-copy">
 <span class="source-credit-eyebrow">ขอบคุณแหล่งเผยแพร่วิดีโอสั้น</span>
 <p>ขอขอบคุณ คุณลิงจั๊กจั๊ก (@domskyline21) สำหรับการเผยแพร่วิดีโอสั้นที่เกี่ยวข้องกับพระมหานภันต์</p>
 </div>
 <a class="source-credit-link" href="https://www.tiktok.com/@domskyline21" target="_blank" rel="noopener noreferrer" aria-label="เปิดบัญชี TikTok คุณลิงจั๊กจั๊ก">@domskyline21 <span aria-hidden="true">↗</span></a>
 </aside>` : '';
 $('videoDetail').innerHTML=`<div class="detail-poster ${x.platform==='TikTok'?'short-detail-poster':''}">${src?`<img src="${esc(src)}" alt="ภาพปกวิดีโอ ${esc(x.title)}">`:''}</div>
 <div class="detail-content"><div class="detail-badges"><a href="${esc(x.platform==='TikTok'?'./shorts.html':uri('category.html',{name:x.category}))}">${esc(x.category)}</a><span>${esc(x.platform)}</span></div>
 <h2>${esc(x.title)}</h2>${sourceCredit}<dl><div><dt>วันที่เผยแพร่</dt><dd>${esc(formatDate(x.published_at))}</dd></div>
 ${x.minutes?'<div><dt>ความยาว</dt><dd>'+duration(x.minutes)+'</dd></div>':''}
 ${x.sourceChannel?'<div><dt>ช่องเผยแพร่</dt><dd>'+esc(x.sourceChannel)+'</dd></div>':''}
 </dl>
 ${x.sourceNote?'<aside class="detail-note">'+esc(x.sourceNote)+'</aside>':''}
 <h3>คำอธิบายจากผู้เผยแพร่</h3>
 <p class="detail-description">${esc(x.description||'ไม่มีคำอธิบายจากผู้เผยแพร่')}</p>
 <div class="detail-actions"><a class="btn primary" href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">เปิดวิดีโอต้นฉบับ ↗</a>
 <button class="btn secondary" data-save="${esc(x.key)}" type="button">${favorites.has(favoriteKey(x))?'♥ บันทึกแล้ว':'♡ บันทึกวิดีโอ'}</button>
 <button class="btn minimal" id="copyVideoLink" type="button">คัดลอกลิงก์ ↗</button></div></div>`;
 const sameCategory=items.filter(y=>y.key!==x.key && y.category===x.category)
   .sort(byDateDesc).slice(0,3);
 if(sameCategory.length){
   $('videoDetail').insertAdjacentHTML('beforeend',
    '<section class="detail-related" aria-labelledby="detailRelatedTitle">'
    +'<div class="heading-row"><div><p class="kicker">MORE FROM THIS SERIES</p>'
    +'<h2 id="detailRelatedTitle">คลิปอื่นในหมวดเดียวกัน</h2>'
    +'<p class="home-section-hint">คัดจากหมวดรายการเดียวกัน ไม่ได้หมายความว่าเนื้อหาในคลิปเหมือนกัน</p>'
    +'</div><a class="text-link" href="'
    +esc(x.platform==='TikTok'?'./shorts.html':uri('category.html',{name:x.category}))
    +'">ดูหมวดนี้ทั้งหมด →</a></div>'
    +'<div class="video-grid">'+sameCategory.map(card).join('')+'</div>'
    +'</section>');
   $('videoDetail').querySelectorAll('.detail-related .video-image img').forEach(attachImageFallback);
 }
 $('copyVideoLink').addEventListener('click',async()=>{
  const text=location.href;
  try{await navigator.clipboard.writeText(text);showToast('คัดลอกลิงก์แล้ว')}catch{showToast('ไม่สามารถคัดลอกลิงก์โดยอัตโนมัติ')}
 });
}
function drawPaged(grid){
 const subset=selected.slice(0,visibleCount);
 grid.innerHTML=subset.map(card).join('');
 const button=$('loadMore');
 if(button)button.hidden=visibleCount>=selected.length;
 for(const image of grid.querySelectorAll('.video-image img'))attachImageFallback(image);
}
function attachImageFallback(img){
 img.addEventListener('error',()=>{img.remove();const span=document.createElement('span');span.className='image-fallback';span.textContent='▶';img.parentElement.append(span);},{once:true});
}
let filterState={q:'',category:'all',year:'all',platform:'all',sort:'new',fav:false,topic:null};
function populateLibrary(){
 const params=new URLSearchParams(location.search);
 const category=params.get('category');
 filterState.topic=resolveTopicId(params.get('topic'));
 filterState.q=params.get('q')||'';
 filterState.category=categoryNames().includes(category)?category:'all';
 filterState.year=/^\d{4}$/.test(params.get('year')||'')?params.get('year'):'all';
 $('categoryFilter').innerHTML='<option value="all">ทุกหมวด</option>'+categoryNames().map(n=>`<option value="${esc(n)}">${esc(n)}</option>`).join('');
 const years=[...new Set(items.map(x=>x.published_at?.slice(0,4)).filter(x=>/^\d{4}$/.test(x||'')))].sort().reverse();
 $('yearFilter').innerHTML='<option value="all">ทุกปี</option>'+years.map(y=>'<option value="'+y+'">พ.ศ. '+(Number(y)+543)+'</option>').join('');
 $('searchInput').value=filterState.q;
 $('categoryFilter').value=filterState.category;
 $('yearFilter').value=filterState.year;
 $('searchInput').addEventListener('input',e=>{filterState.q=e.target.value.trim();refreshLibrary()});
 $('categoryFilter').addEventListener('change',e=>{filterState.category=e.target.value;refreshLibrary()});
 $('yearFilter').addEventListener('change',e=>{filterState.year=e.target.value;refreshLibrary()});
 $('platformFilter').addEventListener('change',e=>{filterState.platform=e.target.value;refreshLibrary()});
 $('sortFilter').addEventListener('change',e=>{filterState.sort=e.target.value;refreshLibrary()});
 $('favoriteFilter').addEventListener('click',()=>{filterState.fav=!filterState.fav;refreshLibrary()});
 $('resetFilters').addEventListener('click',resetLibrary);
 const clearTopic=$('clearTopic');
 if(clearTopic)clearTopic.addEventListener('click',()=>{filterState.topic=null;refreshLibrary()});
 $('clearAll').addEventListener('click',resetLibrary);
 refreshLibrary();
}
function resetLibrary(){
 filterState={q:'',category:'all',year:'all',platform:'all',sort:'new',fav:false,topic:null};
 for(const key of ['searchInput','categoryFilter','yearFilter','platformFilter','sortFilter']){
  const e=$(key);
  e.value=key==='searchInput'?'':'all';
 }
 $('sortFilter').value='new';
 refreshLibrary();
}
function refreshLibrary(){
 const query=norm(filterState.q).split(/\s+/).filter(Boolean);
 selected=items.filter(x=>
  (filterState.category==='all'||x.category===filterState.category)&&
  (!filterState.topic||topicMatches(x,filterState.topic))&&
  (filterState.year==='all'||x.published_at?.startsWith(filterState.year))&&
  (filterState.platform==='all'||x.platform===filterState.platform)&&
  (!filterState.fav||favorites.has(favoriteKey(x)))&&
  query.every(q=>norm([x.title,x.category,x.description,x.video_id].join(' ')).includes(q))
 );
 selected.sort((a,b)=>{
  if(filterState.sort==='old')return (a.published_at||'9999').localeCompare(b.published_at||'9999');
  if(filterState.sort==='title')return a.title.localeCompare(b.title,'th');
  if(filterState.sort==='length')return (b.minutes||0)-(a.minutes||0);
  return byDateDesc(a,b);
 });
 visibleCount=PAGE_SIZE;
 $('resultCount').textContent='พบ '+selected.length.toLocaleString('th-TH')+' คลิป';
 const empty=$('emptyResults'),emptyHeading=$('emptyResultsHeading'),emptyHelp=$('emptyResultsHelp');
 empty.hidden=selected.length!==0;
 if(!selected.length && emptyHeading && emptyHelp){
  if(filterState.fav && !favorites.size){
   emptyHeading.textContent='ยังไม่มีคลิปที่บันทึกไว้';
   emptyHelp.textContent='กดสัญลักษณ์หัวใจบนคลิปที่สนใจ เพื่อบันทึกไว้ดูภายหลังในเบราว์เซอร์นี้';
  }else if(filterState.fav){
   emptyHeading.textContent='ไม่มีคลิปที่บันทึกไว้ตรงกับตัวกรอง';
   emptyHelp.textContent='ลองเปลี่ยนเงื่อนไข หรือกดแสดงคลิปทั้งหมด';
  }else{
   emptyHeading.textContent='ไม่พบคลิปที่ตรงกับเงื่อนไข';
   emptyHelp.textContent='ลองใช้คำที่สั้นลง เปลี่ยนหัวข้อ หรือเลือกดูคลิปทั้งหมด';
  }
 }
 const topicPanel=$('topicFilterStatus');
 if(topicPanel){
  topicPanel.hidden=!filterState.topic;
  const name=$('topicFilterName');
  if(name)name.textContent=discoveryTopic(filterState.topic)?.label||'';
  const hint=$('topicFilterExplanation');
  if(hint)hint.textContent='หัวข้อนี้คัดจากชื่อคลิปต้นฉบับ ไม่ได้ตรวจสอบคำพูดภายในคลิป';
 }
 $('resetFilters').hidden=!(filterState.q||filterState.category!=='all'||filterState.year!=='all'||filterState.platform!=='all'||filterState.sort!=='new'||filterState.fav||!!filterState.topic);
 $('favoriteFilter').setAttribute('aria-pressed',String(filterState.fav));
 drawPaged($('libraryGrid'));
 const u=new URL(location.href);
 for(const key of ['q','category','year','topic'])u.searchParams.delete(key);
 if(filterState.q)u.searchParams.set('q',filterState.q);
 if(filterState.category!=='all')u.searchParams.set('category',filterState.category);
 if(filterState.year!=='all')u.searchParams.set('year',filterState.year);
 if(filterState.topic)u.searchParams.set('topic',filterState.topic);
 history.replaceState(null,'',u.pathname+u.search);
}
function showToast(value){
 const el=$('toast');el.textContent=value;el.classList.add('show');
 clearTimeout(showToast.timer);showToast.timer=setTimeout(()=>el.classList.remove('show'),2300);
}
function toggleFavorite(key){
 const x=items.find(x=>x.key===key);if(!x)return;
 const id=favoriteKey(x);
 if(favorites.has(id)){favorites.delete(id);showToast('นำออกจากรายการที่บันทึกแล้ว')}
 else{favorites.add(id);showToast('บันทึกวิดีโอแล้ว')}
 try{localStorage.setItem(storageKey,JSON.stringify([...favorites]))}catch{}
 if(page==='library')refreshLibrary();
 else if(page==='saved')renderSaved();
 else if(page==='video')renderVideoDetail();
 else if(page==='featured')renderFeatured();
 else if(page==='home')renderHomeCardsOnly();
 else if(page==='category')drawPaged($('categoryGrid'));
}
function renderSaved(){
 const target=$('savedGrid');
 if(!target)return;
 const savedLookup=new Map(items.map(x=>[favoriteKey(x),x]));
 selected=[...favorites].reverse().map(key=>savedLookup.get(key)).filter(Boolean);
 const count=$('savedCount'),empty=$('savedEmpty');
 if(count)count.textContent='บันทึกไว้ '+selected.length.toLocaleString('th-TH')+' คลิปในเบราว์เซอร์นี้';
 if(empty)empty.hidden=selected.length!==0;
 if(!target)return;
 visibleCount=PAGE_SIZE;
 drawPaged(target);
}
function renderHomeCardsOnly(){
 const featured=categoryNames().slice(0,6).map(name=>chooseCover(items.filter(x=>x.category===name))).filter(Boolean);
 $('homeFeatured').innerHTML=featured.map(card).join('');
}
function initializeReadingControls(){
 const key='pmnapan-reading-size-v1';
 const status=$('readingSizeStatus');
 const buttons=[...document.querySelectorAll('[data-reading-adjust]')];
 if(!status||!buttons.length)return;
 let level=0;
 try{level=Math.max(0,Math.min(2,Number(localStorage.getItem(key))||0))}catch(_){}
 const update=()=>{
  document.documentElement.dataset.readingSize=String(level);
  status.textContent=['ปกติ','ใหญ่','ใหญ่มาก'][level];
  buttons.forEach(b=>{
   const d=Number(b.dataset.readingAdjust);
   b.disabled=d<0?level===0:level===2;
  });
 };
 buttons.forEach(b=>b.addEventListener('click',()=>{
  level=Math.max(0,Math.min(2,level+Number(b.dataset.readingAdjust)));
  try{localStorage.setItem(key,String(level))}catch(_){}
  update();
 }));
 update();
}
function bindShared(){
 $('copyrightYear').textContent=new Date().getFullYear();
 initializeReadingControls();
 const toggle=$('mobileToggle'),menu=$('mobileMenu');
 toggle.addEventListener('click',()=>{menu.hidden=!menu.hidden;toggle.setAttribute('aria-expanded',String(!menu.hidden))});
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.hidden=true;toggle.setAttribute('aria-expanded','false')}));
 document.addEventListener('click',e=>{
  const target=e.target.closest('[data-save]');if(target){e.preventDefault();toggleFavorite(target.dataset.save)}
 });
 try{const saved=JSON.parse(localStorage.getItem(storageKey)||'[]');favorites=new Set(Array.isArray(saved)?saved:[])}catch{favorites=new Set()}
}
function renderPressArchive(entries){
 const list=$('pressGrid'), search=$('pressSearch'), category=$('pressCategory');
 const count=$('pressCount'), empty=$('pressEmpty');
 const allowed=new Set(["https://blog.cofact.org","https://fb.mcu.ac.th","https://fmtint.com","https://hands-on.co.th","https://mgronline.com","https://monitor.co.id","https://theactive.thaipbs.or.th","https://thebuddh.com","https://thethaiger.com","https://watchakdaeng.com","https://www.dailynews.co.th","https://www.gchumanrights.org","https://www.gotoknow.org","https://www.iccgc.kr","https://www.nhrc.or.th","https://www.opsmoac.go.th","https://www.peacemakersnetwork.org","https://www.soiciety.com","https://www.thaipbs.or.th","https://www.tnews.co.th"]);
 const imageHosts=new Set(["blog.cofact.org","content-images.thaipbs.or.th","fb.mcu.ac.th","files.wp.thaipbs.or.th","fmtint.com","image.tnews.co.th","lh3.googleusercontent.com","media.beehiiv.com","monitor.co.id","mpics-cdn.mgronline.com","static.nhrc.or.th","thebuddh.com","thethaiger.com","watchakdaeng.com","www.gchumanrights.org","www.hands-on.co.th","www.opsmoac.go.th"]);

 function thumbnailUrl(raw){
  if(typeof raw!=='string'||!raw)return '';
  if(/^\.\/assets\/press\/[a-z0-9-]+\.webp$/.test(raw))return raw;
  try{const url=new URL(raw);return url.protocol==='https:'&&imageHosts.has(url.hostname)?url.href:''}catch{return ''}
 }
 const rows=(Array.isArray(entries)?entries:[]).filter(x=>{
  try{
   const u=new URL(x.url);
   return allowed.has(u.origin) && typeof x.title==='string' && !!x.title
       && typeof x.summary==='string' && !!x.summary && !!x.category && !!x.source;
  }catch{return false}
 }).sort((a,b)=>(b.published_at||'').localeCompare(a.published_at||''));
 [...new Set(rows.map(x=>x.category))].sort((a,b)=>a.localeCompare(b,'th')).forEach(name=>{
  const opt=document.createElement('option');opt.value=name;opt.textContent=name;category.appendChild(opt);
 });
 function draw(){
  const query=norm(search.value), selected=category.value;
  const selectedRows=rows.filter(x=>(!selected||x.category===selected)
    && (!query||norm([x.title,x.summary,x.source,x.category,x.relation].join(' ')).includes(query)));
  list.innerHTML=selectedRows.map(x=>{
   const image=thumbnailUrl(x.thumbnail);
   const thumb=image
     ? '<a class="press-thumbnail'+(x.thumbnail_fit==='contain'?' press-thumbnail-contain':'')+'" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer" aria-label="อ่านบทความต้นฉบับ: '+esc(x.title)+'">'
        +'<img src="'+esc(image)+'" alt="ภาพประกอบต้นฉบับ: '+esc(x.title)+'" loading="lazy" decoding="async" referrerpolicy="no-referrer"></a>'
     : '';
   return '<article class="press-card">'
   +thumb
   +'<div class="press-meta"><span class="press-kind">'+esc(x.category)+'</span><span>'+esc(x.published_at?formatDate(x.published_at):'ไม่ระบุวันที่เผยแพร่')+'</span></div>'
   +'<h2>'+esc(x.title)+'</h2>'
   +'<p class="press-summary">'+esc(x.summary)+'</p>'
   +'<div class="press-source"><span>แหล่งเผยแพร่</span><strong>'+esc(x.source)+'</strong></div>'
   +'<a class="press-outbound" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer">อ่านต้นฉบับ ↗</a>'
   +'</article>'
  }).join('');
  list.querySelectorAll('.press-thumbnail img').forEach(img=>{
   const hide=()=>img.closest('.press-thumbnail')?.remove();
   img.addEventListener('error',hide,{once:true});
   if(img.complete&&img.naturalWidth===0)hide();
  });
  count.textContent='พบ '+selectedRows.length.toLocaleString('th-TH')+' จาก '+rows.length.toLocaleString('th-TH')+' รายการ';
  empty.hidden=selectedRows.length!==0;
 }
 search.addEventListener('input',draw);
 category.addEventListener('change',draw);
 draw();
}
function renderExternalMedia(entries){
 const grid=$('externalMediaGrid'), search=$('externalMediaSearch'), status=$('externalMediaStatus'), count=$('externalMediaCount'), empty=$('externalMediaEmpty');
 const allowed=new Set(['www.trueplookpanya.com','www.facebook.com','www.thaipbs.or.th','lnkd.in','www.traffic.org','watchakdaeng.com','www.opsmoac.go.th','www.kaiciid.org','social-mgr.mgronline.com','www.youtube.com']);
 const records=(Array.isArray(entries)?entries:[]).filter(x=>{
  try{const u=new URL(x.url);
   return u.protocol==='https:' && allowed.has(u.hostname) && ['verified','needs_review','lead'].includes(x.status) && !!x.title && !!x.source && !!x.note;
  }catch{return false}
 });
 function draw(){
  const q=norm(search.value), filter=status.value;
  const visible=records.filter(x=>(filter==='all'||x.status===filter) && (!q||norm([x.title,x.source,x.note].join(' ')).includes(q)));
  grid.innerHTML=visible.map(x=>{
   const isVideo=x.status==='verified',label=isVideo?'ตรวจสอบแหล่งเผยแพร่แล้ว':x.status==='needs_review'?'คลิปจากทะเบียนเก่า · รอตรวจ':'เบาะแส · ยังไม่ยืนยันคลิป';
   const linkLabel=isVideo?'เปิดสื่อต้นฉบับ ↗':'ดูแหล่งอ้างอิง ↗';
   return '<article class="press-card"><div class="press-meta"><span class="press-kind">'+esc(label)+'</span></div>'
    +'<h2>'+esc(x.title)+'</h2><p class="press-summary">'+esc(x.note)+'</p>'
    +'<div class="press-source"><span>แหล่งข้อมูล</span><strong>'+esc(x.source)+'</strong></div>'
    +'<a class="press-outbound" href="'+esc(x.url)+'" target="_blank" rel="noopener noreferrer">'+linkLabel+'</a></article>';
  }).join('');
  count.textContent='พบ '+visible.length.toLocaleString('th-TH')+' จาก '+records.length.toLocaleString('th-TH')+' รายการ';
  empty.hidden=visible.length>0;
 }
 search.addEventListener('input',draw);status.addEventListener('change',draw);draw();
}
async function boot(){
 bindShared();
 if(page==='external-media'){
  try{
   const response=await fetch('./data/external-media.json',{cache:'no-cache'});
   if(!response.ok)throw new Error('External media HTTP '+response.status);
   const catalog=await response.json();renderExternalMedia(catalog.items);
  }catch(error){console.error('Cannot load external media',error);$('externalMediaGrid').innerHTML='<p class="empty">ไม่สามารถโหลดทะเบียนสื่อภายนอกได้ กรุณาลองรีเฟรชหน้าเว็บ</p>';}
  return;
 }
 if(page==='press'){
  try{
   const response=await fetch('./data/press.json',{cache:'no-cache'});
   if(!response.ok)throw new Error('Press HTTP '+response.status);
   const catalog=await response.json();
   renderPressArchive(catalog.items);
  }catch(error){
   console.error('Cannot load press archive',error);
   $('pressGrid').innerHTML='<p class="empty">ไม่สามารถโหลดทะเบียนข่าวและผลงานได้ กรุณาลองรีเฟรชหน้าเว็บ</p>';
  }
  return;
 }
 if(page==='home' && location.hash){
  const redirects={'#library':'library.html','#categories':'categories.html','#featured':'featured.html','#shorts':'shorts.html','#about':'about.html'};
  const destination=redirects[location.hash];
  if(destination){location.replace('./'+destination);return}
 }
 const oldClip=page==='home'?new URLSearchParams(location.search).get('clip'):null;
 if(oldClip){location.replace(uri('video.html',{id:oldClip}));return}
 try{
  const res=await fetch(DATA_URL,{cache:'no-cache'});
  if(!res.ok)throw new Error('HTTP '+res.status);
  const raw=await res.json();const seen=new Set();
  items=(Array.isArray(raw.items)?raw.items:[]).filter(x=>{
   if(!x.key||!x.title||!x.category||!safeLink(x.url)||seen.has(x.key))return false;
   seen.add(x.key);return true;
  });
  if(['home','library'].includes(page)){
    try{await loadCuratedTopics()}catch(error){
      DISCOVERY_TOPICS=[];
      console.warn('Curated topics unavailable',error);
    }
  }
  if(['home','categories','quotes'].includes(page)){
    const qres=await fetch(QUOTES_URL,{cache:'no-cache'});
    if(!qres.ok)throw new Error('Quote catalog HTTP '+qres.status);
    quotes=validateQuotes(await qres.json());
  }
  switch(page){
   case 'home':renderHome();break;
   case 'quotes':renderQuotesPage();break;
   case 'categories':renderCategories();break;
   case 'featured':renderFeatured();break;
   case 'shorts':renderShorts();break;
   case 'library':populateLibrary();break;
   case 'saved':renderSaved();break;
   case 'category':selectCategory();break;
   case 'video':renderVideoDetail();break;
  }
  document.querySelectorAll('.video-image img,.series-image img').forEach(attachImageFallback);
  if(['library','category','saved'].includes(page)){
   const load=$('loadMore');load.addEventListener('click',()=>{
    visibleCount+=PAGE_SIZE;drawPaged(page==='library'?$('libraryGrid'):page==='saved'?$('savedGrid'):$('categoryGrid'));
   });
  }
 }catch(error){
  console.error('Unable to load catalog',error);
  document.querySelectorAll('.loading').forEach(el=>el.textContent='ไม่สามารถโหลดสารบัญได้ กรุณาลองรีเฟรชหน้าเว็บ');
 }
}
boot();
