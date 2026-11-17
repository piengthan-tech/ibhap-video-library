#!/usr/bin/env python3
"""Generate actual separate HTML pages; all navigation is page-to-page, no scroll menus."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parent.parent
name="PMNapan Library Dhamma Archive"
nav=[
 ('index.html','หน้าแรก','home'),
 ('categories.html','หมวดรายการ','categories'),
 ('featured.html','คลิปจากรายการ','featured'),
 ('shorts.html','ธรรมะคลิปสั้น','shorts'),
 ('quotes.html','คำคมธรรมะ','quotes'),
 ('press.html','ข่าวและผลงาน','press'),
 ('library.html','คลังวิดีโอ','library'),
 ('about.html','แหล่งข้อมูล','about')
]
def header(active):
 links=''.join(f'<a href="./{file}" class="nav-link{" active" if key==active else ""}" {"aria-current=\"page\"" if key==active else ""}>{label}</a>' for file,label,key in nav)
 mobile=''.join(f'<a href="./{file}" {"aria-current=\"page\"" if key==active else ""}>{label}</a>' for file,label,key in nav)
 return f'''<header class="site-header" id="top"><div class="container header-wrap">
<a href="./index.html" class="brand" aria-label="{name} กลับหน้าแรก">
<img src="./assets/mascot.png" alt="" width="51" height="51">
<span class="brand-label"><strong>PMNapan Library</strong><span>Dhamma Archive</span></span></a>
<nav class="desktop-nav" aria-label="เมนูหลัก">{links}</nav>
<a class="header-cta" href="./library.html">ค้นหาวิดีโอ <span aria-hidden="true">↗</span></a>
<button type="button" class="mobile-toggle" id="mobileToggle" aria-controls="mobileMenu" aria-expanded="false" aria-label="เปิดเมนู"><span></span><span></span><span></span></button>
</div><nav id="mobileMenu" class="mobile-menu" aria-label="เมนูโทรศัพท์" hidden>{mobile}</nav></header>'''
def footer():
 return f'''<footer class="site-footer" id="ydml-contact">
 <div class="container ydml-footer-main">
  <section class="footer-company" aria-label="ผู้จัดทำเว็บไซต์">
   <a class="footer-ydml-brand" href="https://www.ydml.co.th/" target="_blank" rel="noopener noreferrer" aria-label="เว็บไซต์ YDML อยู่ ดี มี ลาภ">
    <img src="./assets/ydml-logo.png" alt="โลโก้ อยู่ ดี มี ลาภ YDML" width="60" height="60" loading="lazy" decoding="async">
    <span><strong>อยู่ ดี มี ลาภ | YDML</strong><small>Co(ol) working Spaces เพื่อสังคม</small></span>
   </a>
   <div class="footer-production"><span>จัดทำโดย</span><strong>YDML x IBHAP</strong></div>
  </section>
  <section class="footer-contact-column" aria-label="ข้อมูลติดต่อ YDML">
   <h2>ติดต่อ YDML</h2>
   <a class="footer-contact-link" href="tel:0929694423"><span>โทรศัพท์</span><strong>092 969 4423</strong></a>
   <a class="footer-contact-link" href="https://lin.ee/nx8yPVP" target="_blank" rel="noopener noreferrer"><span>LINE Official</span><strong>@ydml</strong></a>
   <a class="footer-contact-link" href="mailto:hi@ydml.co.th"><span>อีเมล</span><strong>hi@ydml.co.th</strong></a>
  </section>
  <nav class="footer-ydml-navigation" aria-label="ช่องทางและบริการ YDML">
   <h2>ช่องทาง YDML</h2>
   <a href="https://www.facebook.com/YouDeMeLarp" target="_blank" rel="noopener noreferrer">Facebook <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/#contact" target="_blank" rel="noopener noreferrer">ติดต่อเรา <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/#booking" target="_blank" rel="noopener noreferrer">จองพื้นที่ <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/meaningful-giving/" target="_blank" rel="noopener noreferrer">สิ่งนี้...มีความหมาย <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/sustainability/" target="_blank" rel="noopener noreferrer">ความยั่งยืนและ SDGs <span aria-hidden="true">↗</span></a>
  </nav>
  <section class="footer-ydml-location" aria-label="สถานที่และติดต่อจองพื้นที่">
   <h2>บริษัท อยู่ ดี มี ลาภ จำกัด</h2>
   <address>46/6-7 ซอยบรมบรรพต แขวงบ้านบาตร<br>เขตป้อมปราบศัตรูพ่าย กรุงเทพมหานคร 10100</address>
   <a class="footer-map-link" href="https://maps.app.goo.gl/rRLRzxnE8usLgtC97" target="_blank" rel="noopener noreferrer">ดูแผนที่ตั้ง ↗</a>
   <div class="footer-actions">
    <a class="footer-btn footer-line" href="https://lin.ee/nx8yPVP" target="_blank" rel="noopener noreferrer">LINE @ydml <span aria-hidden="true">↗</span></a>
    <a class="footer-btn footer-call" href="tel:0929694423">โทรจอง <span aria-hidden="true">↗</span></a>
   </div>
  </section>
 </div>
 <div class="container footer-bottom">
  <p>© <span id="copyrightYear"></span> บริษัท อยู่ ดี มี ลาภ จำกัด (You De Me Larp Co., Ltd.) · สงวนลิขสิทธิ์ทุกประการ</p>
  <button type="button" class="footer-analytics-preferences" id="analyticsPreferences">ตั้งค่าคุกกี้</button>
  <a href="#top" class="footer-back-top">↑ กลับขึ้นด้านบน</a>
 </div>
 <div class="footer-design-credit">Design By Opkip</div>
 </footer>'''
SEO_TITLES={'home': 'พระมหานภันต์ สนฺติภทฺโท | คลังธรรมะ PMNapan Library', 'categories': 'หมวดรายการธรรมะ | พระมหานภันต์ สนฺติภทฺโท', 'featured': 'คลิปธรรมะและรายการย้อนหลัง | พระมหานภันต์', 'shorts': 'คลิปธรรมะสั้น TikTok | พระมหานภันต์ สนฺติภทฺโท', 'quotes': 'คำคมธรรมะจากภาพต้นฉบับ | พระมหานภันต์', 'press': 'ข่าว บทสัมภาษณ์ และผลงาน | พระมหานภันต์', 'external-media': 'สื่อจากแหล่งเผยแพร่ภายนอก | พระมหานภันต์', 'library': 'คลังวิดีโอธรรมะ YouTube และ TikTok | พระมหานภันต์', 'category': 'หมวดคลิปธรรมะ | PMNapan Library', 'video': 'รายละเอียดวิดีโอธรรมะ | PMNapan Library', 'about': 'แหล่งข้อมูลและที่มาคลังธรรมะ | PMNapan Library'}
SEO_DESCRIPTIONS={'home': 'รวมคลิปธรรมะ คำคม ข่าวและบทสัมภาษณ์ที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) พร้อมลิงก์วิดีโอและแหล่งเผยแพร่ต้นฉบับ', 'categories': 'สำรวจหมวดรายการธรรมะของพระมหานภันต์ สนฺติภทฺโท ทั้งอาสาหาธรรม รายการย้อนหลัง ธรรมบรรยาย และสื่อที่เกี่ยวข้องจากแหล่งเผยแพร่จริง', 'featured': 'เลือกชมรายการธรรมะและคลิปย้อนหลังที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมภาพหน้าปกและลิงก์ไปยังผู้เผยแพร่ต้นฉบับ', 'shorts': 'รวบรวมคลิปธรรมะสั้นที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท จาก TikTok โดยรักษาลิงก์และคำบรรยายตามแหล่งเผยแพร่ต้นฉบับ', 'quotes': 'รวมภาพคำคมธรรมะของพระมหานภันต์ สนฺติภทฺโท จากภาพต้นฉบับที่ตรวจสอบแล้ว เปิดดูรูปภาพขนาดเต็มและสำรวจคำสอนจากแหล่งจริง', 'press': 'รวบรวมข่าว บทสัมภาษณ์ กิจกรรม และผลงานย้อนหลังที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมสรุปสั้นและลิงก์ไปยังสำนักข่าวต้นฉบับ', 'external-media': 'คลิปจากหน่วยงานภายนอกที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมแยกสถานะสื่อที่ตรวจสอบได้และเบาะแสที่ยังต้องตรวจสอบ', 'library': 'ค้นหาวิดีโอธรรมะของพระมหานภันต์ สนฺติภทฺโท และสื่อที่เกี่ยวข้อง เลือกหมวด ปี และแหล่งเผยแพร่ YouTube หรือ TikTok', 'category': 'ค้นหาและเลือกชมวิดีโอจากหมวดรายการธรรมะของพระมหานภันต์ สนฺติภทฺโท พร้อมลิงก์ต้นฉบับและข้อมูลการเผยแพร่', 'video': 'อ่านรายละเอียดวิดีโอที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท ตรวจชื่อเรื่องและเปิดวิดีโอจากแหล่งเผยแพร่ต้นฉบับ', 'about': 'ตรวจสอบแหล่งเผยแพร่วิดีโอ คำคม และข้อมูลอ้างอิงใน PMNapan Library เพื่อให้เข้าถึงคลังธรรมะของพระมหานภันต์ สนฺติภทฺโท ได้อย่างถูกต้อง'}
SEO_PATHS={'home': '', 'categories': 'categories.html', 'featured': 'featured.html', 'shorts': 'shorts.html', 'quotes': 'quotes.html', 'press': 'press.html', 'external-media': 'external-media.html', 'library': 'library.html', 'category': 'category.html', 'video': 'video.html', 'about': 'about.html'}
SEO_PERSON={'@type': 'Person', 'name': 'พระมหานภันต์ สนฺติภทฺโท', 'alternateName': ['Ven. Napan', 'PM Napan']}
SEO_WEBSITE={'@type': 'WebSite', '@id': 'https://www.ydml.co.th/pmnapan-library/#website', 'url': 'https://www.ydml.co.th/pmnapan-library/', 'name': 'PMNapan Library Dhamma Archive', 'inLanguage': 'th', 'description': 'รวมคลิปธรรมะ คำคม ข่าวและบทสัมภาษณ์ที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) พร้อมลิงก์วิดีโอและแหล่งเผยแพร่ต้นฉบับ'}

def seo_tags(active,title,description):
    import json
    from html import escape as _escape
    base='https://www.ydml.co.th/pmnapan-library/'
    canonical=base+SEO_PATHS[active]
    graph=[SEO_WEBSITE,{'@type':'CollectionPage' if active not in ('video','about') else 'WebPage',
        '@id':canonical+'#webpage','url':canonical,'name':title,'description':description,
        'inLanguage':'th','isPartOf':{'@id':base+'#website'},'about':SEO_PERSON}]
    if active in ('category','video'):
        graph=[SEO_WEBSITE]
    if active not in ('home','category','video'):
        graph.append({'@type':'BreadcrumbList','@id':canonical+'#breadcrumbs',
          'itemListElement':[{'@type':'ListItem','position':1,'name':'หน้าแรก','item':base},
          {'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':canonical}]})
    tags=['<meta name="robots" content="index,follow,max-image-preview:large">',
      '<meta property="og:site_name" content="PMNapan Library Dhamma Archive">',
      '<meta property="og:locale" content="th_TH">',
      '<meta property="og:image" content="'+base+'assets/monk-watering-960.webp">',
      '<meta property="og:image:alt" content="PMNapan Library คลังธรรมะพระมหานภันต์">',
      '<meta name="twitter:card" content="summary_large_image">']
    if active in ('category','video'):
        tags.append("""<script>
(function(){
  const p=new URLSearchParams(location.search);
  const filename=location.pathname.split('/').pop();
  const target=new URL(filename, 'https://www.ydml.co.th/pmnapan-library/');
  if(filename==='video.html'){
    const id=p.get('id')||p.get('clip');
    if(id && /^(YouTube|TikTok):[A-Za-z0-9_-]{8,35}$/.test(id))target.searchParams.set('id',id);
  }
  if(filename==='category.html'){
    const name=p.get('name');
    if(name && name.length<110)target.searchParams.set('name',name);
  }
  const link=document.createElement('link');link.rel='canonical';link.href=target.href;document.head.appendChild(link);
  const og=document.createElement('meta');og.setAttribute('property','og:url');og.content=target.href;document.head.appendChild(og);
})();
</script>""")
    else:
        tags.extend(['<link rel="canonical" href="'+canonical+'">','<meta property="og:url" content="'+canonical+'">'])
    tags.append('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>')
    return '\n'.join(tags)

def shell(active,title,description,content):
 title=SEO_TITLES.get(active,title)
 description=SEO_DESCRIPTIONS.get(active,description)
 return f'''<!doctype html>
<html lang="th"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="{escape(description,quote=True)}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}">
<title>{escape(title)}</title>
{seo_tags(active,title,description)}
<!-- Keep the public address clean; preserve functional search and video parameters. -->
<script>
(() => {{
 const url = new URL(location.href);
 let changed = false;
 if (url.pathname === '/pmnapan-library') {{
  url.pathname = '/pmnapan-library/';
  changed = true;
 }}
 const source = url.searchParams.get('utm_source') || '';
 if (['chatgpt.com', 'chatgpt', 'chat.openai.com'].includes(source.toLowerCase())) {{
  url.searchParams.delete('utm_source');
  changed = true;
 }}
 if (changed) history.replaceState(null, '', url.pathname + url.search + url.hash);
}})();
</script>
<link rel="icon" type="image/png" href="./assets/mascot.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Prompt:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./assets/site.css">
<link rel="stylesheet" href="./assets/ydml-footer.css">
<link rel="stylesheet" href="./assets/analytics.css">
<script defer src="./assets/site.js"></script>
<script defer src="./assets/analytics.js"></script>
</head><body data-page="{active}">
<a href="#main" class="skip-link">ข้ามไปยังเนื้อหา</a>
{header(active)}
<main id="main">{content}</main>
{footer()}<div role="status" aria-live="polite" class="toast" id="toast"></div></body></html>'''
def intro(kicker,title,description='',back='index.html',back_text='หน้าแรก'):
 return f'''<section class="page-intro"><div class="container">
<nav class="crumbs" aria-label="ตำแหน่งหน้า"><a href="./{back}">{back_text}</a><span aria-hidden="true">/</span><span id="currentCrumb">{escape(title)}</span></nav>
<div class="page-intro-row"><div><p class="kicker">{escape(kicker)}</p><h1 class="page-title" id="pageTitle">{escape(title)}</h1>{f'<p class="subline" id="pageSubline">{escape(description)}</p>' if description else '<p class="subline" id="pageSubline"></p>'}</div>
<div class="intro-icon" aria-hidden="true"><img src="./assets/mascot.png" alt=""></div></div></div></section>'''
def grid(name,id):
 return f'<div id="{id}" class="video-grid" aria-label="{escape(name)}"><div class="loading"><span class="spinner" aria-hidden="true"></span>กำลังโหลดข้อมูลวิดีโอ...</div></div>'
def tabs_bar():
 return '''<div class="filter-panel">
<div class="search-row">
<label class="input-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.5"/><path d="m16 16 5 5"/></svg><span class="sr-only">ค้นหาวิดีโอ</span><input type="search" id="searchInput" placeholder="ค้นหาชื่อเรื่องหรือคำสำคัญจากต้นทาง" autocomplete="off"></label>
<button class="fav-filter" id="favoriteFilter" type="button" aria-pressed="false">♡ รายการที่บันทึก</button>
</div><div class="filter-controls">
<label>หมวดรายการ<select id="categoryFilter"><option value="all">ทุกหมวด</option></select></label>
<label>ปีเผยแพร่<select id="yearFilter"><option value="all">ทุกปี</option></select></label>
<label>ช่องทาง<select id="platformFilter"><option value="all">ทุกช่องทาง</option><option value="YouTube">YouTube</option><option value="TikTok">TikTok</option><option value="Facebook">Facebook</option></select></label>
<label>เรียงลำดับ<select id="sortFilter"><option value="new">ใหม่ล่าสุด</option><option value="old">เก่าสุด</option><option value="title">ชื่อเรื่อง ก–ฮ</option><option value="length">วิดีโอยาวที่สุด</option></select></label>
</div><div class="filter-footer"><p id="resultCount" aria-live="polite">กำลังโหลด...</p><button type="button" class="reset-filter" id="resetFilters" hidden>ล้างตัวกรอง ↺</button></div></div>'''
home=f'''<section class="hero"><div class="container hero-row"><div class="hero-copy">
<p class="hero-kicker"><span></span> VIDEO ARCHIVE</p>
<h1>PMNapan Library<br><span>Dhamma Archive</span></h1>
<h2>คลังวิดีโอพระมหานภันต์ สนฺติภทฺโท</h2>
<div class="hero-actions"><a class="btn primary" href="./library.html">▶ เข้าสู่คลังวิดีโอ</a><a class="btn secondary" href="./categories.html">เลือกหมวดรายการ ↗</a></div>
<p class="hero-total"><strong id="homeTotal">—</strong> วิดีโอในคลัง</p>

</div><div class="hero-visual"><span class="blue-orbit"></span><img src="./assets/monk-watering-960.webp" srcset="./assets/monk-watering-620.webp 620w, ./assets/monk-watering-960.webp 960w" sizes="(max-width: 650px) 300px, (max-width: 910px) 400px, 540px" alt="การ์ตูนพระรดน้ำต้นไม้ พร้อมสัญลักษณ์การพัฒนาที่ยั่งยืน" width="960" height="919" fetchpriority="high" decoding="async"></div></div></section>
<section class="quick-search"><div class="container"><form id="homeSearchForm" class="quick-search-form" role="search">
<label for="homeSearch">ค้นหาวิดีโอ</label><input id="homeSearch" type="search" placeholder="พิมพ์ชื่อคลิปหรือคำสำคัญ" autocomplete="off">
<button type="submit">ค้นหา →</button></form></div></section>
<section class="section home-series-section"><div class="container"><div class="heading-row"><div><p class="kicker">EXPLORE THE COLLECTION</p><h2>หมวดรายการ</h2><p class="home-section-hint">เลือกหมวดที่สนใจ เพื่อดูวิดีโอทั้งหมดในหมวดนั้น</p></div><a href="./categories.html" class="text-link">ดูทุกหมวด →</a></div>
<div id="homeCategories" class="home-topic-grid" aria-label="เลือกหมวดวิดีโอ"><div class="loading">กำลังโหลดหมวดรายการ...</div></div></div></section>
<section class="section tinted home-featured-section"><div class="container"><div class="heading-row"><div><p class="kicker">FROM ORIGINAL VIDEOS</p><h2>คลิปจากรายการ</h2><p class="home-section-hint">เลือกชมตัวอย่างวิดีโอ พร้อมลิงก์ไปยังคลิปต้นฉบับ</p></div><a href="./featured.html" class="text-link">ดูคลิปทั้งหมด →</a></div>
 {grid('คลิปจากรายการ','homeFeatured')}</div></section>
<section class="section shorts-spotlight"><div class="container">
<div class="heading-row"><div><p class="kicker">SHORT-FORM VIDEO · TIKTOK</p><h2>ธรรมะคลิปสั้น</h2></div><a href="./shorts.html" class="text-link">ดูคลิปทั้งหมด ↗</a></div>
<div id="homeShorts" class="shorts-grid"><div class="loading">กำลังโหลดคลิปสั้น...</div></div>
</div></section>
<section class="section"><div class="container"><div class="heading-row"><div><p class="kicker">DHAMMA QUOTES · ORIGINAL IMAGES</p><h2>คำคมธรรมะ</h2></div><a href="./quotes.html" class="text-link">ดูคำคมทั้งหมด ↗</a></div>
<div id="homeQuotes" class="quote-grid"><div class="loading">กำลังโหลดคำคมธรรมะ...</div></div></div></section>'''
home += '<section class="section seo-discovery" aria-labelledby="archiveExploreHeading"><div class="container"><div class="seo-discovery-inner"><h2 id="archiveExploreHeading">ค้นหาธรรมะและผลงานของพระมหานภันต์ สนฺติภทฺโท</h2><p>PMNapan Library รวบรวมรายการธรรมะและสื่อที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท หรือ Ven. Napan เพื่อให้ค้นหาคลิปเต็มจากผู้เผยแพร่ต้นฉบับได้สะดวก พร้อมแยกข้อมูลคำคม ข่าว และบทสัมภาษณ์ออกจากกันอย่างชัดเจน แหล่งข้อมูลมีทั้ง YouTube, TikTok และเว็บไซต์ของหน่วยงานต่าง ๆ โดยระบุที่มาและเก็บเฉพาะรายการที่ตรวจสอบได้</p><nav class="seo-discovery-links" aria-label="สำรวจคลังธรรมะ"><a href="./library.html">ค้นหาคลิปและธรรมบรรยาย</a><a href="./categories.html">เลือกหมวดรายการธรรมะ</a><a href="./shorts.html">ดูธรรมะคลิปสั้น</a><a href="./quotes.html">ดูภาพคำคมธรรมะ</a><a href="./press.html">อ่านข่าวและบทสัมภาษณ์</a><a href="./about.html">ตรวจสอบแหล่งเผยแพร่</a></nav></div></div></section>'
categories=f'''{intro('ALL SERIES','หมวดรายการ','หมวดที่มีอยู่จริงในสารบัญวิดีโอ')}
<section class="section"><div class="container"><div class="category-summary" id="categorySummary"></div>
<div id="allCategories" class="series-grid"><div class="loading">กำลังโหลดหมวดรายการ...</div></div>
<aside class="program-note" id="relatedNotice" hidden><strong>เกี่ยวกับ “หลวงพี่ช่วยด้วย”</strong><p>รายการต้นฉบับ Workpoint ดำเนินรายการโดยพระมหาสมปอง ตาลปุตฺโต คลิปในหมวดนี้เป็นงานซับไตเติลของมูลนิธิ สกพ. ไม่ใช่วิดีโอที่พระมหานภันต์เป็นผู้บรรยาย</p><a href="https://www.youtube.com/playlist?list=PLFU5BMWz_rx10E1AiFivlOPsVO8qQFvmx" target="_blank" rel="noopener noreferrer">เพลย์ลิสต์ต้นทาง ↗</a></aside>
</div></section>'''
quotes=f'''{intro('DHAMMA QUOTES','คำคมธรรมะ','รวมภาพคำคมธรรมะจากคลังผู้ดูแลและจากเพจต้นทาง โดยรักษาข้อความตามภาพต้นฉบับ')}
<section class="section"><div class="container">
<div class="quote-toolbar">
<label for="quoteSearch">ค้นหาข้อความคำคมที่ถอดไว้</label><input type="search" id="quoteSearch" placeholder="ค้นหาในรายการที่มีข้อความถอดแล้ว" autocomplete="off">
<p id="quotesCount" role="status" aria-live="polite">กำลังตรวจสอบ...</p></div>
<div class="quote-grid" id="quoteGrid"><div class="loading">กำลังโหลดภาพคำคมธรรมะ...</div></div>
<div class="empty" id="quoteEmpty" hidden>ไม่พบข้อความที่ตรงกับคำค้น</div>
</div></section>'''
press=f'''{intro('PRESS · INTERVIEWS · ARCHIVE','ข่าว บทสัมภาษณ์ และผลงาน','หลักฐานการทำงานและเนื้อหาย้อนหลังจากแหล่งเผยแพร่ต้นฉบับ ตรวจสอบและแยกประเภทก่อนรวบรวม')}
<section class="section"><div class="container">
<div class="press-tools">
<label class="press-search-label" for="pressSearch">ค้นหาเนื้อหา<input id="pressSearch" type="search" placeholder="ค้นหาชื่อเรื่อง แหล่งข่าว หรือคำสำคัญ" autocomplete="off"></label>
<label class="press-select-label" for="pressCategory">ประเภท<select id="pressCategory"><option value="">ทุกประเภท</option></select></label>
<p id="pressCount" role="status" aria-live="polite">กำลังโหลดข้อมูล...</p></div>
<div id="pressGrid" class="press-grid"><p class="loading">กำลังโหลดข่าวและผลงาน...</p></div>
<p id="pressEmpty" class="empty" hidden>ไม่พบข้อมูลตรงกับคำค้น</p>
<p class="press-media-link">ต้องการดูวิดีโอที่เผยแพร่โดยหน่วยงานอื่น? <a href="./external-media.html">สื่อจากแหล่งภายนอกและรายการตรวจสอบ ↗</a></p>\n<p class="press-source-note">ข้อมูลชุดนี้เป็นทะเบียนแหล่งอ้างอิง ไม่ใช่การเผยแพร่บทความต้นฉบับซ้ำ กรุณาอ่านฉบับเต็มจากเว็บไซต์ผู้เผยแพร่โดยตรง วันที่ที่แสดงเป็นวันที่เผยแพร่บทความ ไม่ใช่วันที่จัดกิจกรรมเสมอไป และข้อมูลโครงการย้อนหลังไม่ใช่ประกาศรับสมัครในปัจจุบัน</p>
</div></section>'''
external_media=f'''{intro('EXTERNAL MEDIA · SOURCE REVIEW','สื่อจากแหล่งภายนอก','คลิปที่เผยแพร่โดยหน่วยงานอื่นและรายการเบาะแสจากแชตเก่า แยกสถานะการตรวจสอบอย่างชัดเจน')}
<section class="section"><div class="container">
<div class="press-tools">
<label class="press-search-label" for="externalMediaSearch">ค้นหาสื่อ<input id="externalMediaSearch" type="search" placeholder="ค้นหาชื่อรายการหรือหน่วยงาน" autocomplete="off"></label>
<label class="press-select-label" for="externalMediaStatus">สถานะการตรวจสอบ
<select id="externalMediaStatus"><option value="verified">ตรวจสอบแหล่งเผยแพร่แล้ว</option><option value="needs_review">คลิปจากทะเบียนเก่าที่ยังต้องยืนยัน</option><option value="lead">เบาะแสและเอกสารที่ยังไม่ใช่คลิปยืนยัน</option><option value="all">แสดงทั้งหมด</option></select></label>
<p id="externalMediaCount" role="status" aria-live="polite">กำลังโหลดข้อมูล...</p></div>
<div id="externalMediaGrid" class="press-grid"><p class="loading">กำลังโหลดสื่อ...</p></div>
<p id="externalMediaEmpty" class="empty" hidden>ไม่พบรายการที่ตรงกับเงื่อนไข</p>
<p class="press-source-note">สถานะ “ตรวจสอบแหล่งเผยแพร่แล้ว” หมายถึงพบหน้าสื่อหรือหลักฐานผู้จัด ไม่ได้ยืนยันว่า Facebook เปิดรับชมได้โดยไม่เข้าสู่ระบบ ส่วนรายการ “เบาะแส” เป็นข้อมูลสำหรับค้นหาต่อ ไม่ใช่คลิปที่ตรวจสอบเนื้อหาสำเร็จแล้ว</p>
</div></section>'''
shorts=f'''{intro('SHORT-FORM VIDEO · TIKTOK','ธรรมะคลิปสั้น','Dhamma Shorts · คลิปจาก TikTok @domskyline21')}
<section class="shorts-credit-banner"><div class="container"><aside class="source-credit" aria-label="ขอบคุณแหล่งเผยแพร่วิดีโอสั้น">
 <div class="source-credit-mark" aria-hidden="true">♫</div>
 <div class="source-credit-copy">
 <span class="source-credit-eyebrow">ขอบคุณแหล่งเผยแพร่วิดีโอสั้น</span>
 <p>ขอขอบคุณ คุณลิงจั๊กจั๊ก (@domskyline21) สำหรับการเผยแพร่วิดีโอสั้นที่เกี่ยวข้องกับพระมหานภันต์</p>
 </div>
 <a class="source-credit-link" href="https://www.tiktok.com/@domskyline21" target="_blank" rel="noopener noreferrer" aria-label="เปิดบัญชี TikTok คุณลิงจั๊กจั๊ก">@domskyline21 <span aria-hidden="true">↗</span></a>
 </aside></div></section>
<section class="section"><div class="container">
<div class="shorts-search-bar"><label for="shortsSearch">ค้นหาคลิปสั้น</label><input type="search" id="shortsSearch" placeholder="ค้นหาคำสำคัญจากคำบรรยายต้นฉบับ" autocomplete="off"><span id="shortsCount" aria-live="polite" role="status"></span></div>
<div id="shortsGrid" class="shorts-grid"><div class="loading">กำลังโหลดคลิปสั้น...</div></div>
<div id="shortsEmpty" class="empty" hidden>ไม่พบคลิปสั้นที่ตรงกับคำค้น</div>
<div class="load-wrap"><button id="loadShorts" type="button" class="btn secondary" hidden>ดูคลิปเพิ่มเติม ↓</button></div>
</div></section>'''
featured=f'''{intro('ORIGINAL VIDEO THUMBNAILS','คลิปจากรายการ','ภาพที่แสดงเป็นภาพจากคลิปต้นฉบับ ไม่ใช่ภาพที่สร้างขึ้นใหม่')}
<section class="section"><div class="container"><div id="featuredSections"><div class="loading">กำลังโหลดคลิปจากรายการ...</div></div></div></section>'''
library=f'''{intro('VIDEO LIBRARY','คลังวิดีโอ','ค้นหาชื่อเรื่องจากแหล่งเผยแพร่ต้นฉบับ และเปิดรับชมได้โดยตรง')}
<section class="section"><div class="container">{tabs_bar()}
<p class="press-media-link">ต้องการดูวิดีโอที่เผยแพร่โดยหน่วยงานอื่น? <a href="./external-media.html">สื่อจากแหล่งภายนอกและรายการตรวจสอบ ↗</a></p>
{grid('คลังวิดีโอทั้งหมด','libraryGrid')}<div class="empty" id="emptyResults" hidden><h2>ไม่พบรายการที่ตรงกับคำค้น</h2><button type="button" id="clearAll">ดูวิดีโอทั้งหมด</button></div>
<div class="load-wrap"><button id="loadMore" type="button" class="btn secondary" hidden>ดูวิดีโอเพิ่มเติม ↓</button></div></div></section>'''
category=f'''{intro('SERIES','หมวดรายการ','','categories.html','หมวดรายการ')}
<section class="section"><div class="container"><div class="heading-row"><span id="categoryCount" class="category-total"></span><a href="./categories.html" class="text-link">← ทุกหมวดรายการ</a></div>
<div class="program-note" id="categoryRelationNote" hidden></div>
{grid('วิดีโอในหมวดรายการ','categoryGrid')}
<div class="load-wrap"><button id="loadMore" type="button" class="btn secondary" hidden>ดูวิดีโอเพิ่มเติม ↓</button></div></div></section>'''
video=f'''{intro('VIDEO DETAILS','รายละเอียดวิดีโอ','','library.html','คลังวิดีโอ')}
<section class="section"><div class="container"><div id="videoDetail" class="detail-layout"><div class="loading">กำลังโหลดรายละเอียดวิดีโอ...</div></div></div></section>'''
about=f'''{intro('SOURCE INFORMATION','แหล่งข้อมูล')}
<section class="section"><div class="container about-layout about-sources-only"><div class="about-panel"><p class="kicker">OFFICIAL SOURCE CHANNELS</p>
<h2>แหล่งเผยแพร่ต้นฉบับ</h2><div class="source-links">
<a href="https://www.youtube.com/@Napan" target="_blank" rel="noopener noreferrer">YouTube · PM Napan <span>↗</span></a>
<a href="https://www.youtube.com/channel/UCjScesRz_L16aIs-Kdtsh_g" target="_blank" rel="noopener noreferrer">YouTube · IBHAP Foundation <span>↗</span></a>
<a href="https://www.facebook.com/NapanIBHAP/photos" target="_blank" rel="noopener noreferrer">Facebook · พระมหานภันต์ สกพ. - Ven.Napan IBHAP · รูปภาพ <span>↗</span></a>
</div></div></div></section>'''
about += '\n<section class="section analytics-privacy-section" id="analytics-privacy">\n<div class="container about-layout"><div class="about-panel">\n<h2>การวัดผลการใช้งานและความเป็นส่วนตัว</h2>\n<p>เว็บไซต์ PMNapan Library ใช้ Google Analytics 4 เพื่อวิเคราะห์จำนวนผู้เข้าชม จำนวนครั้งที่เปิดหน้าเว็บ หน้าที่ได้รับความนิยม และการคลิกลิงก์ไปยังคลิปหรือบทความต้นฉบับ การวัดผลนี้เริ่มทำงานเฉพาะเมื่อผู้เข้าชมกด “ยินยอม” เท่านั้น</p>\n<p>เมื่อยินยอม ข้อมูลการใช้งานบางส่วนจะถูกส่งให้ Google เพื่อจัดทำรายงานสถิติ โดยระบบอาจใช้คุกกี้เพื่อจดจำการเข้าชม ไม่ใช้ระบบนี้เพื่อแสดงโฆษณาแบบเจาะจง ผู้เข้าชมสามารถเปลี่ยนความยินยอมได้จากปุ่ม “ตั้งค่าคุกกี้” ที่ส่วนท้ายทุกหน้า การถอนความยินยอมจะหยุดการส่งข้อมูลครั้งต่อไป ไม่ลบข้อมูลที่ส่งไปแล้ว</p>\n<p>การคลิกไปยังเว็บไซต์ YouTube, TikTok หรือสื่อภายนอกไม่ได้หมายความว่ามีการรับชมวิดีโอจริง สถิติอาจไม่รวมผู้ที่ไม่ยินยอม ใช้ระบบบล็อกการติดตาม หรือถูกจำกัดจากเบราว์เซอร์</p>\n</div></div></section>'
pages=[
 ('index.html','home',name,'สารบัญวิดีโอพระมหานภันต์ สนฺติภทฺโท และงานสื่อที่เกี่ยวข้อง',home),
 ('categories.html','categories','หมวดรายการ | '+name,'หมวดรายการทั้งหมดจากทะเบียนวิดีโอต้นฉบับ',categories),
 ('featured.html','featured','คลิปจากรายการ | '+name,'คลิปจากรายการพร้อมภาพปกจากแหล่งเผยแพร่จริง',featured),
 ('shorts.html','shorts','ธรรมะคลิปสั้น | '+name,'คลิปสั้นต้นฉบับจากบัญชี TikTok @domskyline21 ที่ตรวจสอบแหล่งและภาพปก',shorts),
 ('quotes.html','quotes','คำคมธรรมะ | '+name,'รวบรวมภาพคำคมธรรมะของพระมหานภันต์จากคลังภาพที่ผู้ดูแลจัดเตรียมและโพสต์ต้นฉบับที่ตรวจสอบได้',quotes),
 ('press.html','press','ข่าว บทสัมภาษณ์ และผลงาน | '+name,'คลังข่าว บทสัมภาษณ์ ประวัติ และผลงานย้อนหลังของพระมหานภันต์ พร้อมอ้างอิงแหล่งเผยแพร่ต้นฉบับ',press),
 ('external-media.html','external-media','สื่อจากแหล่งภายนอก | '+name,'คลิปจากหน่วยงานภายนอกและเบาะแสที่แยกสถานะตรวจสอบ',external_media),
 ('library.html','library','คลังวิดีโอ | '+name,'ค้นหาและเลือกชมวิดีโอต้นฉบับ แยกหมวด ปี และช่องทาง',library),
 ('category.html','category','หมวดรายการ | '+name,'รายการคลิปตามหมวดหมู่จากทะเบียนจริง',category),
 ('video.html','video','รายละเอียดวิดีโอ | '+name,'รายละเอียดคลิปและลิงก์วิดีโอของผู้เผยแพร่ต้นฉบับ',video),
 ('about.html','about','แหล่งข้อมูล | '+name,'ข้อมูลแหล่งเผยแพร่และหลักเกณฑ์ของคลังวิดีโอ',about)
]
for filename,key,title,description,body in pages:
 (root/filename).write_text(shell(key,title,description,body),encoding='utf-8')
 print("GENERATED",filename)
