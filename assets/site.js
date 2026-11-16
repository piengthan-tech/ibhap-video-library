'use strict';
/* PMNapan Library — standalone pages on GitHub Pages, grounded in data/videos.json */
const $ = id => document.getElementById(id);
const page = document.body.dataset.page;
const DATA_URL = './data/videos.json';
const PAGE_SIZE = 15;
const storageKey = 'ven-napan-library-favorites-v1';
let items = [], favorites = new Set(), visibleCount = PAGE_SIZE, activeCategory = '', selected = [];
const esc = value => String(value ?? '').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
const norm = value => String(value || '').normalize('NFC').toLocaleLowerCase('th').replace(/[\u200b\u200c\u200d]/g,'').trim();
const safeLink = url => {try{const u=new URL(url);return u.protocol==='https:' && /(^|\.)(youtube\.com|youtu\.be|facebook\.com|fb\.watch)$/.test(u.hostname)}catch{return false}};
const idSafe = id=>/^[-_A-Za-z0-9]{11}$/.test(id);
const uri = (file,params={}) => {
 const query=new URLSearchParams(params).toString();
 return './'+file+(query?'?'+query:'');
};
function thumb(x){
 if(x.thumbnail && /^\.\/assets\/episode-stills\/[-_A-Za-z0-9]{11}\.jpg$/.test(x.thumbnail))return x.thumbnail;
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
const categoryNames = () => [...new Set(items.map(x=>x.category))];
const byDateDesc=(a,b)=>(b.published_at||'').localeCompare(a.published_at||'') || a.title.localeCompare(b.title,'th');
const favoriteKey=x=>x.platform+':'+x.video_id;
const related = x=>x.relation==='ibhap_subtitles';
function openVideoHref(x){return uri('video.html',{id:x.key})}
function card(x){
 const preview=thumb(x),liked=favorites.has(favoriteKey(x));
 return `<article class="video-card" data-key="${esc(x.key)}">
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
function categoryCard(name,group,i){
 const image=thumb(chooseCover(group));
 return `<a class="series-card" href="${esc(uri('category.html',{name}))}">
  <div class="series-image">${image?`<img loading="lazy" decoding="async" src="${esc(image)}" alt="ภาพจากรายการ ${esc(name)}">`:'<span class="image-fallback">▶</span>'}<span class="series-number">0${i+1}</span></div>
  <div class="series-info"><strong>${esc(name)}</strong><span>${group.length.toLocaleString('th-TH')} คลิป <b aria-hidden="true">↗</b></span></div>
  </a>`;
}
function categoryCards(names){
 return names.map((name,i)=>categoryCard(name,items.filter(x=>x.category===name),i)).join('');
}
function relatedNote(){
 return '<strong>เกี่ยวกับรายการ “หลวงพี่ช่วยด้วย”</strong><p>รายการต้นฉบับ Workpoint ดำเนินรายการโดยพระมหาสมปอง ตาลปุตฺโต คลิปหมวดนี้เป็นงานซับไตเติลของมูลนิธิ สกพ. ไม่ใช่คลิปที่พระมหานภันต์เป็นผู้บรรยาย</p><a href="https://www.youtube.com/playlist?list=PLFU5BMWz_rx10E1AiFivlOPsVO8qQFvmx" target="_blank" rel="noopener noreferrer">ดูเพลย์ลิสต์ต้นทาง ↗</a>';
}
function renderHome(){
 $('homeTotal').textContent=items.length.toLocaleString('th-TH');
 $('homeCategories').innerHTML=categoryCards(categoryNames().slice(0,6));
 const selections=categoryNames().slice(0,6).map(name=>chooseCover(items.filter(x=>x.category===name))).filter(Boolean);
 $('homeFeatured').innerHTML=selections.map(card).join('');
 $('homeSearchForm').addEventListener('submit',e=>{
  e.preventDefault();const q=$('homeSearch').value.trim();
  location.href=uri('library.html',q?{q}:{});
 });
}
function renderCategories(){
 const categories=categoryNames();
 $('categorySummary').textContent=categories.length.toLocaleString('th-TH')+' หมวดรายการ';
 $('allCategories').innerHTML=categoryCards(categories);
 const note=$('relatedNotice');note.hidden=!categories.some(n=>n.includes('หลวงพี่ช่วยด้วย'));
}
function renderFeatured(){
 const sections=categoryNames().map(name=>{
  const group=items.filter(x=>x.category===name).sort(byDateDesc);
  const cover=chooseCover(group);
  const featured=[cover,...group.filter(x=>x.key!==cover.key).slice(0,2)];
  return `<section class="featured-section"><div class="heading-row"><h2>${esc(name)}</h2><a href="${esc(uri('category.html',{name}))}" class="text-link">ดูหมวดนี้ทั้งหมด ↗</a></div><div class="video-grid">${featured.map(card).join('')}</div></section>`;
 });
 $('featuredSections').innerHTML=sections.join('');
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
 document.title=name+' | PMNapan Library Dhamma Archive';
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
function renderVideoDetail(){
 const params=new URLSearchParams(location.search);
 const key=params.get('id')||params.get('clip')||'';
 const x=items.find(x=>x.key===key);
 if(!x){
  $('pageTitle').textContent='ไม่พบวิดีโอ';
  $('videoDetail').innerHTML='<div class="empty"><p>ไม่มีข้อมูลวิดีโอนี้ในทะเบียน</p><a class="btn secondary" href="./library.html">กลับไปคลังวิดีโอ</a></div>';
  return;
 }
 document.title=x.title+' | PMNapan Library Dhamma Archive';
 $('pageTitle').textContent='รายละเอียดวิดีโอ';
 $('currentCrumb').textContent='รายละเอียดวิดีโอ';
 const src=thumb(x);
 $('videoDetail').innerHTML=`<div class="detail-poster">${src?`<img src="${esc(src)}" alt="ภาพปกวิดีโอ ${esc(x.title)}">`:''}</div>
 <div class="detail-content"><div class="detail-badges"><a href="${esc(uri('category.html',{name:x.category}))}">${esc(x.category)}</a><span>${esc(x.platform)}</span></div>
 <h2>${esc(x.title)}</h2><dl><div><dt>วันที่เผยแพร่</dt><dd>${esc(formatDate(x.published_at))}</dd></div>
 ${x.minutes?'<div><dt>ความยาว</dt><dd>'+duration(x.minutes)+'</dd></div>':''}
 ${x.sourceChannel?'<div><dt>ช่องเผยแพร่</dt><dd>'+esc(x.sourceChannel)+'</dd></div>':''}
 </dl>
 ${x.sourceNote?'<aside class="detail-note">'+esc(x.sourceNote)+'</aside>':''}
 <h3>คำอธิบายจากผู้เผยแพร่</h3>
 <p class="detail-description">${esc(x.description||'ไม่มีคำอธิบายจากผู้เผยแพร่')}</p>
 <div class="detail-actions"><a class="btn primary" href="${esc(x.url)}" target="_blank" rel="noopener noreferrer">เปิดวิดีโอต้นฉบับ ↗</a>
 <button class="btn secondary" data-save="${esc(x.key)}" type="button">${favorites.has(favoriteKey(x))?'♥ บันทึกแล้ว':'♡ บันทึกวิดีโอ'}</button>
 <button class="btn minimal" id="copyVideoLink" type="button">คัดลอกลิงก์ ↗</button></div></div>`;
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
let filterState={q:'',category:'all',year:'all',platform:'all',sort:'new',fav:false};
function populateLibrary(){
 const params=new URLSearchParams(location.search);
 const category=params.get('category');
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
 $('clearAll').addEventListener('click',resetLibrary);
 refreshLibrary();
}
function resetLibrary(){
 filterState={q:'',category:'all',year:'all',platform:'all',sort:'new',fav:false};
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
 $('emptyResults').hidden=selected.length!==0;
 $('resetFilters').hidden=!(filterState.q||filterState.category!=='all'||filterState.year!=='all'||filterState.platform!=='all'||filterState.sort!=='new'||filterState.fav);
 $('favoriteFilter').setAttribute('aria-pressed',String(filterState.fav));
 drawPaged($('libraryGrid'));
 const u=new URL(location.href);
 for(const key of ['q','category','year'])u.searchParams.delete(key);
 if(filterState.q)u.searchParams.set('q',filterState.q);
 if(filterState.category!=='all')u.searchParams.set('category',filterState.category);
 if(filterState.year!=='all')u.searchParams.set('year',filterState.year);
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
 else if(page==='video')renderVideoDetail();
 else if(page==='featured')renderFeatured();
 else if(page==='home')renderHomeCardsOnly();
 else if(page==='category')drawPaged($('categoryGrid'));
}
function renderHomeCardsOnly(){
 const featured=categoryNames().slice(0,6).map(name=>chooseCover(items.filter(x=>x.category===name))).filter(Boolean);
 $('homeFeatured').innerHTML=featured.map(card).join('');
}
function bindShared(){
 $('copyrightYear').textContent=new Date().getFullYear();
 const toggle=$('mobileToggle'),menu=$('mobileMenu');
 toggle.addEventListener('click',()=>{menu.hidden=!menu.hidden;toggle.setAttribute('aria-expanded',String(!menu.hidden))});
 menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.hidden=true;toggle.setAttribute('aria-expanded','false')}));
 document.addEventListener('click',e=>{
  const target=e.target.closest('[data-save]');if(target){e.preventDefault();toggleFavorite(target.dataset.save)}
 });
 try{const saved=JSON.parse(localStorage.getItem(storageKey)||'[]');favorites=new Set(Array.isArray(saved)?saved:[])}catch{favorites=new Set()}
}
async function boot(){
 bindShared();
 if(page==='home' && location.hash){
  const redirects={'#library':'library.html','#categories':'categories.html','#featured':'featured.html','#about':'about.html'};
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
  switch(page){
   case 'home':renderHome();break;
   case 'categories':renderCategories();break;
   case 'featured':renderFeatured();break;
   case 'library':populateLibrary();break;
   case 'category':selectCategory();break;
   case 'video':renderVideoDetail();break;
  }
  document.querySelectorAll('.video-image img,.series-image img').forEach(attachImageFallback);
  if(['library','category'].includes(page)){
   const load=$('loadMore');load.addEventListener('click',()=>{
    visibleCount+=PAGE_SIZE;drawPaged(page==='library'?$('libraryGrid'):$('categoryGrid'));
   });
  }
 }catch(error){
  console.error('Unable to load catalog',error);
  document.querySelectorAll('.loading').forEach(el=>el.textContent='ไม่สามารถโหลดสารบัญได้ กรุณาลองรีเฟรชหน้าเว็บ');
 }
}
boot();
