'use strict';

const DATA_URL = './data/videos.json';
const PAGE_SIZE = 12;
const favoriteKey = 'ven-napan-library-favorites-v1';
const state = {
  items: [], query: '', category: 'all', year: 'all', platform: 'all', sort: 'new',
  favoritesOnly: false, shown: PAGE_SIZE, ready: false, favorites: new Set(),
};
const el = (id) => document.getElementById(id);
const q = (selector) => document.querySelector(selector);
const qa = (selector) => Array.from(document.querySelectorAll(selector));
const escapeHtml = (value = '') => String(value).replace(/[&<>"']/g, (c) => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
const normalized = (s) => String(s || '').normalize('NFC').toLocaleLowerCase('th').replace(/[\u200b\u200c\u200d]/g, '').trim();
const validId = (x) => /^[-_a-zA-Z0-9]{11}$/.test(String(x || ''));
const isSafeSource = (url) => { try { const x = new URL(url); return x.protocol === 'https:' && /(^|\.)(youtube\.com|youtu\.be|facebook\.com|fb\.watch)$/.test(x.hostname); } catch {return false;} };
const escAttr = escapeHtml;
const clamp = (num, a, b) => Math.min(b, Math.max(a, num));
function dateLabel(iso, opts = {day:'numeric', month:'short', year:'numeric'}) {
  if (!iso || !/^\d{4}-\d{2}-\d{2}$/.test(iso)) return 'ไม่ระบุวัน';
  const d = new Date(iso + 'T12:00:00+07:00');
  if (Number.isNaN(d.getTime())) return 'ไม่ระบุวัน';
  return new Intl.DateTimeFormat('th-TH', opts).format(d);
}
function minutesToClock(minutes) {
  const total = Math.round(Number(minutes || 0) * 60);
  if (!total) return '';
  const s = Math.floor(total/60), sec = String(total%60).padStart(2,'0');
  if(s >= 60) return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}:${sec}`;
  return `${s}:${sec}`;
}
function detectYear(item) { return item.published_at ? item.published_at.slice(0,4) : 'ไม่ทราบปี'; }
function cleanDescription(text, max = 180) {
  let s = String(text || '').replace(/https?:\/\/\S+/g,'').replace(/#[^\s#]+/g,'').replace(/\s+/g,' ').trim();
  if(!s) return '';
  return s.length > max ? s.slice(0,max-1).trimEnd()+'…' : s;
}
function thumbUrl(item) {
  // Thumbnail for อาสาหาธรรม is a verified video frame from the matching original file.
  if (item.thumbnail && /^\.\/assets\/episode-stills\/[-_a-zA-Z0-9]{11}\.jpg$/.test(item.thumbnail)) return item.thumbnail;
  return item.platform === 'YouTube' && validId(item.video_id) ? `https://i.ytimg.com/vi/${item.video_id}/hqdefault.jpg` : '';
}
function favoriteId(item) { return `${item.platform}:${item.video_id}`; }
function loadFavorites() { try { const v = JSON.parse(localStorage.getItem(favoriteKey) || '[]'); state.favorites = new Set(Array.isArray(v)? v : []); } catch { state.favorites = new Set(); } }
function saveFavorites() { try {localStorage.setItem(favoriteKey,JSON.stringify([...state.favorites]));}catch{} }
let toastTimeout;
function toast(message) {const t = el('toast'); t.textContent=message; t.classList.add('show'); clearTimeout(toastTimeout);toastTimeout=setTimeout(()=>t.classList.remove('show'),2800);}
function getFiltered() {
  const words = normalized(state.query).split(/\s+/).filter(Boolean);
  const records = state.items.filter(item => {
    if(state.category !== 'all' && item.category !== state.category) return false;
    if(state.year !== 'all' && detectYear(item) !== state.year) return false;
    if(state.platform !== 'all' && item.platform !== state.platform) return false;
    if(state.favoritesOnly && !state.favorites.has(favoriteId(item))) return false;
    if(words.length) {
      const haystack = normalized([item.title,item.category,item.description,item.published_at,item.video_id].join(' '));
      if(!words.every(word => haystack.includes(word))) return false;
    }
    return true;
  });
  records.sort((a,b)=>{
    if(state.sort==='old') return (a.published_at||'9999').localeCompare(b.published_at||'9999') || a.title.localeCompare(b.title,'th');
    if(state.sort==='title') return a.title.localeCompare(b.title,'th');
    if(state.sort==='length') return (b.minutes||0)-(a.minutes||0);
    return (b.published_at||'').localeCompare(a.published_at||'') || a.title.localeCompare(b.title,'th');
  });
  return records;
}
function buildCard(item) {
  const src = thumbUrl(item);
  const isFav = state.favorites.has(favoriteId(item));
  const date = dateLabel(item.published_at);
  const link = isSafeSource(item.url) ? item.url : '';
  const categoryShort = item.category;
  return `<article class="video-card" data-id="${escAttr(item.key)}">
    <div class="video-thumb ${src?'':'no-image'}">
      ${src ? `<img loading="lazy" decoding="async" src="${escAttr(src)}" alt="ภาพตัวอย่างคลิป ${escAttr(item.title)}">` : ''}
      <span class="thumb-vignette"></span>
      <span class="thumb-platform">${escAttr(item.platform)}${item.kind==='คลิปพร้อมคำบรรยาย'?' · Subtitled':''}</span>
      ${item.minutes ? `<span class="thumb-duration">${minutesToClock(item.minutes)}</span>` : ''}
      <button class="favorite-button ${isFav?'is-favorite':''}" type="button" data-action="favorite" data-id="${escAttr(item.key)}" aria-pressed="${isFav}" aria-label="${isFav?'นำออกจากรายการที่บันทึก':'บันทึกคลิปนี้'}" title="${isFav?'นำออกจากรายการที่บันทึก':'บันทึกคลิปนี้'}">${isFav?'♥':'♡'}</button>
    </div>
    <div class="video-body">
      <div class="video-meta"><span class="category-dot ${item.category==='อาสาหาธรรม'?'':'mam'}"></span>${escapeHtml(categoryShort)}<span aria-hidden="true">·</span>${escapeHtml(date)}</div>
      <h3 class="video-title">${escapeHtml(item.title)}</h3>
      <div class="video-foot">
        <button class="video-details" type="button" data-action="details" data-id="${escAttr(item.key)}">รายละเอียด <span aria-hidden="true">→</span></button>
        ${link ? `<a class="watch-link" href="${escAttr(link)}" target="_blank" rel="noopener noreferrer" aria-label="รับชม ${escAttr(item.title)} จาก ${escAttr(item.platform)}">รับชมคลิป <span aria-hidden="true">↗</span></a>` : ''}
      </div>
    </div>
  </article>`;
}
function render() {
  if(!state.ready) return;
  const all = getFiltered();
  const page = all.slice(0,state.shown);
  el('resultsCount').innerHTML = `พบ <strong>${all.length.toLocaleString('th-TH')}</strong> คลิป${state.query ? ` จากคำค้น “${escapeHtml(state.query)}”`:''}`;
  el('videoGrid').innerHTML = page.map(buildCard).join('');
  el('emptyState').hidden = all.length > 0;
  el('showMore').hidden = all.length <= state.shown;
  const filtered = !!state.query || state.category !== 'all' || state.year !== 'all' || state.platform !== 'all' || state.favoritesOnly;
  el('resetFilters').hidden = !filtered;
  el('clearSearch').hidden = !state.query;
  el('favoritesToggle').setAttribute('aria-pressed', String(state.favoritesOnly));
  el('favoritesToggle').querySelector('span').textContent = state.favoritesOnly ? '♥' : '♡';
  qa('#seriesTabs .tab').forEach(btn=>{
    const selected = btn.dataset.series === state.category;
    btn.classList.toggle('active',selected);
    btn.setAttribute('aria-pressed',String(selected));
  });
  qa('.video-thumb img').forEach(img => img.addEventListener('error', () => {
    img.parentElement.classList.add('no-image');img.remove();
  }, {once:true}));
}
function updateFilters() {
 el('librarySearch').value=state.query;el('heroSearch').value=state.query;
 el('yearFilter').value=state.year;el('platformFilter').value=state.platform;el('sortSelect').value=state.sort;
 render();
}
function resetFilters() {
 state.query='';state.category='all';state.year='all';state.platform='all';state.sort='new';state.favoritesOnly=false;state.shown=PAGE_SIZE;updateFilters();
}
function chooseCategory(category) {
 state.category=category;state.shown=PAGE_SIZE;updateFilters();
 el('library').scrollIntoView({behavior:'smooth'});
}
function sanitizeData(raw) {
 const arr=Array.isArray(raw.items)?raw.items:[];
 const seen=new Set();
 return arr.map(x=>{
  const item={
    key:String(x.key||`${x.platform}:${x.video_id}`),
    title:String(x.title||'ไม่มีชื่อเรื่อง'),description:String(x.description||''),
    category:String(x.category||'รายการอื่น'),platform:String(x.platform||'YouTube'),
    url:String(x.url||''),video_id:String(x.video_id||''),published_at:String(x.published_at||''),
    minutes:Number(x.minutes||0),kind:String(x.kind||'ตอนเต็ม/ไลฟ์'),thumbnail:String(x.thumbnail||'')
  };
  return item;
 }).filter(x=>{
  if(!x.video_id || !isSafeSource(x.url) || seen.has(x.key)) return false;
  seen.add(x.key);return true;
 });
}
function renderCategories() {
  const map=new Map();
  for(const v of state.items){
    if(!map.has(v.category))map.set(v.category,[]);
    map.get(v.category).push(v);
  }
  const categories=[...map.entries()];
  el('categoryGrid').innerHTML=categories.map(([name,items],i)=>{
    const selected=items.find(x=>x.thumbnail)||items[0];
    const src=thumbUrl(selected);
    return `<button class="category-card" type="button" data-category="${escapeHtml(name)}">
      <span class="category-cover">${src?`<img src="${escapeHtml(src)}" alt="" loading="lazy">`:''}</span>
      <span class="category-content"><span class="category-index">0${i+1} / SERIES</span><strong>${escapeHtml(name)}</strong><span class="category-count">${items.length.toLocaleString('th-TH')} คลิป <span aria-hidden="true">→</span></span></span>
    </button>`;
  }).join('');
  el('seriesTabs').innerHTML=`<button class="tab active" data-series="all" aria-pressed="true" type="button">ทั้งหมด</button>`+
    categories.map(([name])=>`<button class="tab" type="button" data-series="${escapeHtml(name)}" aria-pressed="false">${escapeHtml(name)}</button>`).join('');
}
function renderFeatured(){
  const featured=[];
  const categories=[...new Set(state.items.map(x=>x.category))];
  for(const category of categories){
    const group=state.items.filter(x=>x.category===category).sort((a,b)=>b.published_at.localeCompare(a.published_at));
    featured.push(...group.slice(0,3));
  }
  el('featuredGrid').innerHTML=featured.map(buildCard).join('');
}

function populateStats(raw) {
 const count=state.items.length;
 const years=[...new Set(state.items.map(x=>detectYear(x)).filter(x=>/^\d{4}$/.test(x)))].sort();
 el('heroVideoCount').textContent=count.toLocaleString('th-TH');
 renderCategories();
 renderFeatured();
 el('yearFilter').innerHTML='<option value="all">ทุกปี</option>'+years.reverse().map(y=>`<option value="${y}">พ.ศ. ${Number(y)+543}</option>`).join('');
 const date=raw.generated_at ? new Date(raw.generated_at) : null;
 el('updatedPill').textContent=date && !Number.isNaN(date.getTime()) ? 'ข้อมูลล่าสุด '+new Intl.DateTimeFormat('th-TH',{day:'numeric',month:'short',year:'numeric'}).format(date) : 'รายการจากแหล่งข้อมูลต้นทาง';
 el('copyrightYear').textContent=new Date().getFullYear();
}
function detailLink(item){const url=new URL(location.href);url.searchParams.set('clip',item.key);url.hash='';return url.href;}
let activeItem;
function openDetails(key,{updateHistory=true}={}) {
 const item=state.items.find(x=>x.key===key);
 if(!item)return;
 activeItem=item;
 const src=thumbUrl(item);
 const preview=el('dialogImage');
 preview.classList.toggle('placeholder',!src);
 preview.innerHTML=src?`<img src="${escAttr(src)}" alt="ภาพตัวอย่างคลิป ${escAttr(item.title)}">`:'';
 const img=preview.querySelector('img');
 if(img)img.addEventListener('error',()=>{img.remove();preview.classList.add('placeholder');},{once:true});
 el('dialogTags').innerHTML=`<span>${escapeHtml(item.category)}</span><span>${escapeHtml(item.platform)}</span><span>${escapeHtml(item.kind)}</span>`;
 el('dialogTitle').textContent=item.title;
 el('dialogFacts').textContent=`เผยแพร่ ${dateLabel(item.published_at)}${item.minutes ? ' · ความยาว '+minutesToClock(item.minutes):''}`;
 el('dialogDescription').textContent=item.description || 'ไม่พบคำอธิบายจากผู้เผยแพร่ โปรดดูรายละเอียดเพิ่มเติมที่ต้นทาง';
 const url=el('dialogWatch');url.href=item.url;url.textContent='เปิดดูวิดีโอต้นทาง ↗';
 if(updateHistory){const link=new URL(location.href);link.searchParams.set('clip',item.key);history.replaceState(null,'',link);}
 if(!el('videoDialog').open)el('videoDialog').showModal();
}
function closeDetails() {
 el('videoDialog').close();
 const url=new URL(location.href);url.searchParams.delete('clip');history.replaceState(null,'',url);
 activeItem=null;
}
async function copyText(text){
 try {await navigator.clipboard.writeText(text);return true;}catch{
  try{const input=document.createElement('textarea');input.value=text;input.style.position='fixed';input.style.left='-100vw';document.body.appendChild(input);input.select();const ok=document.execCommand('copy');input.remove();return ok;}catch{return false;}
 }
}
function bindEvents() {
 el('heroSearchForm').addEventListener('submit',(e)=>{e.preventDefault();state.query=el('heroSearch').value.trim();state.shown=PAGE_SIZE;updateFilters();el('library').scrollIntoView({behavior:'smooth'});});
 el('librarySearch').addEventListener('input',(e)=>{state.query=e.target.value.trim();state.shown=PAGE_SIZE;el('heroSearch').value=state.query;render();});
 el('clearSearch').addEventListener('click',()=>{state.query='';state.shown=PAGE_SIZE;updateFilters();el('librarySearch').focus();});
 el('seriesTabs').addEventListener('click',e=>{
  const b=e.target.closest('[data-series]');
  if(b)chooseCategory(b.dataset.series);
 });
 el('categoryGrid').addEventListener('click',e=>{
  const b=e.target.closest('[data-category]');
  if(b)chooseCategory(b.dataset.category);
 });
 el('yearFilter').addEventListener('change',e=>{state.year=e.target.value;state.shown=PAGE_SIZE;render();});
 el('platformFilter').addEventListener('change',e=>{state.platform=e.target.value;state.shown=PAGE_SIZE;render();});
 el('sortSelect').addEventListener('change',e=>{state.sort=e.target.value;state.shown=PAGE_SIZE;render();});
 el('favoritesToggle').addEventListener('click',()=>{state.favoritesOnly=!state.favoritesOnly;state.shown=PAGE_SIZE;render();});
 el('resetFilters').addEventListener('click',resetFilters);
 el('emptyReset').addEventListener('click',resetFilters);
 el('showMore').addEventListener('click',()=>{state.shown+=PAGE_SIZE;render();});
 [el('videoGrid'),el('featuredGrid')].forEach(container=>container.addEventListener('click',e=>{
  const button=e.target.closest('[data-action]');if(!button)return;
  const item=state.items.find(x=>x.key===button.dataset.id);if(!item)return;
  if(button.dataset.action==='details')openDetails(item.key);
  if(button.dataset.action==='favorite'){
   const key=favoriteId(item);
   if(state.favorites.has(key)){state.favorites.delete(key);toast('นำคลิปออกจากรายการที่บันทึกแล้ว');}
   else {state.favorites.add(key);toast('บันทึกคลิปไว้ในเบราว์เซอร์นี้แล้ว');}
   saveFavorites();render();renderFeatured();
  }
  }));
 el('closeDialog').addEventListener('click',closeDetails);
 el('videoDialog').addEventListener('click',(e)=>{if(e.target===el('videoDialog'))closeDetails();});
 el('videoDialog').addEventListener('cancel',(e)=>{e.preventDefault();closeDetails();});
 el('dialogCopy').addEventListener('click',async()=>{if(activeItem){const copied=await copyText(detailLink(activeItem));toast(copied?'คัดลอกลิงก์คลิปแล้ว':'ไม่สามารถคัดลอกอัตโนมัติได้');}});
 el('menuToggle').addEventListener('click',()=>{const nav=el('mobileNav'),open=nav.hidden;nav.hidden=!open;el('menuToggle').setAttribute('aria-expanded',String(open));});
 qa('.mobile-nav a').forEach(a=>a.addEventListener('click',()=>{el('mobileNav').hidden=true;el('menuToggle').setAttribute('aria-expanded','false');}));
 window.addEventListener('popstate',()=>{const key=new URLSearchParams(location.search).get('clip');if(key)openDetails(key,{updateHistory:false});else if(el('videoDialog').open)el('videoDialog').close();});
}
async function initialize() {
 loadFavorites();bindEvents();
 try{
  const response=await fetch(DATA_URL,{cache:'no-cache'});
  if(!response.ok)throw new Error('HTTP '+response.status);
  const data=await response.json();
  state.items=sanitizeData(data);
  state.ready=true;populateStats(data);render();
  const deep=new URLSearchParams(location.search).get('clip');
  if(deep)openDetails(deep,{updateHistory:false});
 }catch(err){
  console.error('ไม่สามารถโหลดสารบัญ:',err);
  el('videoGrid').innerHTML='<div class="loading">ขณะนี้ไม่สามารถโหลดสารบัญวิดีโอได้ กรุณาลองรีเฟรชหน้านี้อีกครั้ง</div>';
  el('resultsCount').textContent='ไม่สามารถโหลดข้อมูล';
  el('updatedPill').textContent='ข้อมูลไม่พร้อมใช้งาน';
 }
}
initialize();
