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
  <a href="#top" class="footer-back-top">↑ กลับขึ้นด้านบน</a>
 </div>
 </footer>'''
def shell(active,title,description,content):
 return f'''<!doctype html>
<html lang="th"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="{escape(description,quote=True)}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}">
<title>{escape(title)}</title>
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
<script defer src="./assets/site.js"></script>
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
<section class="section"><div class="container"><div class="heading-row"><div><p class="kicker">SERIES COLLECTION</p><h2>หมวดรายการ</h2></div><a href="./categories.html" class="text-link">ดูทุกหมวด →</a></div>
<div id="homeCategories" class="series-grid"><div class="loading">กำลังโหลด...</div></div></div></section>
<section class="section tinted"><div class="container"><div class="heading-row"><div><p class="kicker">FROM ORIGINAL VIDEOS</p><h2>คลิปจากรายการ</h2></div><a href="./featured.html" class="text-link">ดูเพิ่มเติม →</a></div>
 {grid('คลิปจากรายการ','homeFeatured')}</div></section>
<section class="section shorts-spotlight"><div class="container">
<div class="heading-row"><div><p class="kicker">SHORT-FORM VIDEO · TIKTOK</p><h2>ธรรมะคลิปสั้น</h2></div><a href="./shorts.html" class="text-link">ดูคลิปทั้งหมด ↗</a></div>
<div id="homeShorts" class="shorts-grid"><div class="loading">กำลังโหลดคลิปสั้น...</div></div>
</div></section>
<section class="section"><div class="container"><div class="heading-row"><div><p class="kicker">DHAMMA QUOTES · ORIGINAL IMAGES</p><h2>คำคมธรรมะ</h2></div><a href="./quotes.html" class="text-link">ดูคำคมทั้งหมด ↗</a></div>
<div id="homeQuotes" class="quote-grid"><div class="loading">กำลังโหลดคำคมธรรมะ...</div></div></div></section>'''
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
