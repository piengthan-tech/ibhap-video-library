#!/usr/bin/env python3
"""Generate actual separate HTML pages; all navigation is page-to-page, no scroll menus."""
from pathlib import Path
from html import escape
root=Path(__file__).resolve().parent.parent
name="PMNapan Library Dhamma Archive"
nav=[
 ('index.html','หน้าแรก','home'),
 ('ven-napan.html','รู้จักพระมหานภันต์','profile'),
 ('library.html','คลังวิดีโอ','library'),
 ('shorts.html','ธรรมะคลิปสั้น','shorts'),
 ('quotes.html','คำคมธรรมะ','quotes'),
 ('press.html','ข่าวและผลงาน','press'),
 ('four-ps.html','คลังพิเศษ','fourps')
]
page_files={key:file for file,label,key in nav}
page_files.update({'categories':'categories.html','featured':'featured.html','category':'category.html','video':'video.html','saved':'saved.html','external-media':'external-media.html','about':'about.html','notfound':'404.html'})
def header(active,lang='th'):
 nav_active={'categories':'library','featured':'library','category':'library','video':'library','saved':'library','external-media':'press'}.get(active,active)
 current_file=page_files.get(active,'index.html')
 links=''.join(f'<a href="./{file}" class="nav-link{" active" if key==nav_active else ""}" {"aria-current=\"page\"" if key==nav_active else ""}>{label}</a>' for file,label,key in nav)
 mobile=''.join(f'<a href="./{file}" {"aria-current=\"page\"" if key==nav_active else ""}>{label}</a>' for file,label,key in nav)
 th_active=' active' if lang=='th' else ''
 en_active=' active' if lang=='en' else ''
 th_current=' aria-current="true"' if lang=='th' else ''
 en_current=' aria-current="true"' if lang=='en' else ''
 language=f'''<nav class="language-switcher" aria-label="ภาษา">
<a class="lang-option{th_active}" data-lang-choice="th" lang="th" hreflang="th" href="./{current_file}"{th_current}>TH</a>
<span aria-hidden="true">/</span>
<a class="lang-option{en_active}" data-lang-choice="en" lang="en" hreflang="en" href="./en/{current_file}"{en_current}>EN</a>
</nav>'''
 return f'''<header class="site-header" id="top"><div class="container header-wrap">
<a href="./index.html" class="brand" aria-label="{name} กลับหน้าแรก">
<img src="./assets/mascot.png" alt="" width="51" height="51">
<span class="brand-label"><strong>PMNapan Library</strong><span>Dhamma Archive</span></span></a>
<nav class="desktop-nav" aria-label="เมนูหลัก">{links}</nav>
{language}
<a class="header-cta" href="./library.html">ค้นหาวิดีโอ <span aria-hidden="true">↗</span></a>
<button type="button" class="mobile-toggle" id="mobileToggle" aria-controls="mobileMenu" aria-expanded="false" aria-label="เปิดเมนู"><span></span><span></span><span></span></button>
</div><nav id="mobileMenu" class="mobile-menu" aria-label="เมนูโทรศัพท์" hidden>{mobile}</nav></header>'''
def footer():
 return f'''<footer class="site-footer" id="ydml-contact">
 <div class="container ydml-footer-main">
  <section class="footer-company" aria-label="ผู้จัดทำเว็บไซต์">
   <a class="footer-ydml-brand" href="https://www.ydml.co.th/" target="_blank" rel="noopener noreferrer" aria-label="เว็บไซต์ YDML อยู่ ดี มี ลาภ">
    <img src="./assets/ydml-logo.png" alt="โลโก้ อยู่ ดี มี ลาภ YDML" width="56" height="56" decoding="async">
    <span><strong>อยู่ ดี มี ลาภ | YDML</strong><small>Co(ol) working Spaces เพื่อสังคม</small></span>
   </a>
   <p class="footer-production"><span>จัดทำโดย</span><strong>YDML x IBHAP</strong></p>
  </section>
  <section class="footer-contact-column" aria-label="ข้อมูลติดต่อ YDML">
   <h2>ติดต่อ YDML</h2>
   <a class="footer-contact-link" href="https://lin.ee/nx8yPVP" target="_blank" rel="noopener noreferrer">
    <span class="footer-contact-icon footer-line-icon" aria-hidden="true">LINE</span>
    <span class="footer-contact-copy"><small>LINE Official</small><strong>@ydml</strong></span>
   </a>
   <a class="footer-contact-link" href="mailto:hi@ydml.co.th">
    <span class="footer-contact-icon footer-mail-icon" aria-hidden="true"><svg viewBox="0 0 24 18"><rect x="1" y="1" width="22" height="16" rx="3"></rect><path d="M3 4.5 12 11l9-6.5"></path></svg></span>
    <span class="footer-contact-copy"><small>อีเมล</small><strong>hi@ydml.co.th</strong></span>
   </a>
  </section>
  <nav class="footer-ydml-navigation" aria-label="ช่องทางและบริการ YDML">
   <h2>ช่องทาง YDML</h2>
   <a href="https://www.facebook.com/YouDeMeLarp" target="_blank" rel="noopener noreferrer">Facebook <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/#contact" target="_blank" rel="noopener noreferrer">ติดต่อเรา <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/#booking" target="_blank" rel="noopener noreferrer">จองพื้นที่ <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/meaningful-giving/" target="_blank" rel="noopener noreferrer">สิ่งนี้...มีความหมาย <span aria-hidden="true">↗</span></a>
   <a href="https://www.ydml.co.th/sustainability/" target="_blank" rel="noopener noreferrer">ความยั่งยืนและ SDGs <span aria-hidden="true">↗</span></a>
  </nav>
  <section class="footer-ydml-location" aria-label="สถานที่และช่องทางติดต่อ">
   <h2>บริษัท อยู่ ดี มี ลาภ จำกัด</h2>
   <address>46/6-7 ซอยบรมบรรพต แขวงบ้านบาตร<br>เขตป้อมปราบศัตรูพ่าย กรุงเทพมหานคร 10100</address>
   <a class="footer-map-link" href="https://maps.app.goo.gl/rRLRzxnE8usLgtC97" target="_blank" rel="noopener noreferrer">ดูแผนที่ตั้ง ↗</a>
   <div class="footer-actions">
    <a class="footer-line-pill" href="https://lin.ee/nx8yPVP" target="_blank" rel="noopener noreferrer">
     <span class="footer-contact-icon footer-line-icon" aria-hidden="true">LINE</span>
     <strong>LINE @ydml</strong><span class="footer-line-arrow" aria-hidden="true">↗</span>
    </a>
   </div>
  </section>
 </div>
 <div class="container footer-bottom">
  <p>© <span id="copyrightYear"></span> บริษัท อยู่ ดี มี ลาภ จำกัด (You De Me Larp Co., Ltd.) · สงวนลิขสิทธิ์ทุกประการ</p>
  <button type="button" class="footer-analytics-preferences" id="analyticsPreferences">ตั้งค่าคุกกี้</button>
  <div class="footer-reading-controls" role="group" aria-label="ปรับขนาดตัวอักษร"><span>ขนาดตัวอักษร</span><button type="button" data-reading-adjust="-1" aria-label="ลดขนาดตัวอักษร">A−</button><span id="readingSizeStatus" aria-live="polite">ปกติ</span><button type="button" data-reading-adjust="1" aria-label="เพิ่มขนาดตัวอักษร">A+</button></div>
  <a href="#top" class="footer-back-top">↑ กลับขึ้นด้านบน</a>
 </div>
 </footer>'''

SEO_TITLES={'home': 'พระมหานภันต์ สนฺติภทฺโท | คลังธรรมะ PMNapan Library', 'categories': 'หมวดรายการธรรมะ | พระมหานภันต์ สนฺติภทฺโท', 'featured': 'คลิปธรรมะและรายการย้อนหลัง | พระมหานภันต์', 'shorts': 'คลิปธรรมะสั้น TikTok | พระมหานภันต์ สนฺติภทฺโท', 'quotes': 'คำคมธรรมะจากภาพต้นฉบับ | พระมหานภันต์', 'press': 'ข่าว บทสัมภาษณ์ และผลงาน | พระมหานภันต์', 'external-media': 'สื่อจากแหล่งเผยแพร่ภายนอก | พระมหานภันต์', 'library': 'คลังวิดีโอธรรมะ YouTube และ TikTok | พระมหานภันต์', 'category': 'หมวดคลิปธรรมะ | PMNapan Library', 'video': 'รายละเอียดวิดีโอธรรมะ | PMNapan Library', 'about': 'แหล่งข้อมูลและที่มาคลังธรรมะ | PMNapan Library'}
SEO_TITLES['saved']='คลิปที่บันทึกไว้ | PMNapan Library'
SEO_TITLES['fourps']='ปรากฏการณ์ 4 พส. | เส้นเวลาข่าว คลิป และบทบาทพระมหานภันต์'
SEO_TITLES['profile']='ประวัติพระมหานภันต์ สนฺติภทฺโท | Ven. Napan · PMNapan Library'
SEO_DESCRIPTIONS={'home': 'รวมคลิปธรรมะ คำคม ข่าวและบทสัมภาษณ์ที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) พร้อมลิงก์วิดีโอและแหล่งเผยแพร่ต้นฉบับ', 'categories': 'สำรวจหมวดรายการธรรมะของพระมหานภันต์ สนฺติภทฺโท ทั้งอาสาหาธรรม รายการย้อนหลัง ธรรมบรรยาย และสื่อที่เกี่ยวข้องจากแหล่งเผยแพร่จริง', 'featured': 'เลือกชมรายการธรรมะและคลิปย้อนหลังที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมภาพหน้าปกและลิงก์ไปยังผู้เผยแพร่ต้นฉบับ', 'shorts': 'รวบรวมคลิปธรรมะสั้นที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท จาก TikTok โดยรักษาลิงก์และคำบรรยายตามแหล่งเผยแพร่ต้นฉบับ', 'quotes': 'รวบรวมภาพคำคมธรรมะที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมแหล่งเผยแพร่และภาพสำหรับรับชมขนาดเต็ม', 'press': 'รวบรวมข่าว บทสัมภาษณ์ กิจกรรม และผลงานย้อนหลังที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมสรุปสั้นและลิงก์ไปยังสำนักข่าวต้นฉบับ', 'external-media': 'รวมรายการจากหน่วยงานภายนอกที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท พร้อมลิงก์ต้นทางและข้อมูลประกอบสำหรับการค้นคว้า', 'library': 'ค้นหาวิดีโอธรรมะของพระมหานภันต์ สนฺติภทฺโท และสื่อที่เกี่ยวข้อง เลือกหมวด ปี และแหล่งเผยแพร่ YouTube หรือ TikTok', 'category': 'ค้นหาและเลือกชมวิดีโอจากหมวดรายการธรรมะของพระมหานภันต์ สนฺติภทฺโท พร้อมลิงก์ต้นฉบับและข้อมูลการเผยแพร่', 'video': 'อ่านรายละเอียดวิดีโอที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท ตรวจชื่อเรื่องและเปิดวิดีโอจากแหล่งเผยแพร่ต้นฉบับ', 'about': 'ข้อมูลเกี่ยวกับ PMNapan Library แหล่งเผยแพร่วิดีโอ คำคม ข่าว และแนวทางการอ้างอิงเนื้อหาของพระมหานภันต์ สนฺติภทฺโท'}
SEO_DESCRIPTIONS['saved']='ดูคลิปที่บันทึกไว้เฉพาะในเบราว์เซอร์นี้ สามารถจัดการรายการที่สนใจได้โดยไม่ต้องสมัครบัญชี'
SEO_DESCRIPTIONS['fourps']='เปิดคลังพิเศษปรากฏการณ์ 4 พส. ปี 2564–2565 เรียงข่าวและคลิปตามเหตุการณ์ พร้อมบทบาทพระมหานภันต์ในช่วงให้กำลังใจมหาสมปองและพิธีลาสิกขา'
SEO_DESCRIPTIONS['profile']='ประวัติพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) ผู้ช่วยเจ้าอาวาสวัดสระเกศ ประธานผู้ก่อตั้ง IBHAP และเลขาธิการ Religions for Peace Thailand พร้อมเส้นทางการศึกษา งานสันติภาพ สิทธิมนุษยชน SDGs และสื่อที่เกี่ยวข้อง'
SEO_PATHS={'home': '', 'categories': 'categories.html', 'featured': 'featured.html', 'shorts': 'shorts.html', 'quotes': 'quotes.html', 'press': 'press.html', 'external-media': 'external-media.html', 'library': 'library.html', 'category': 'category.html', 'video': 'video.html', 'about': 'about.html'}
SEO_PATHS['saved']='saved.html'
SEO_PATHS['fourps']='four-ps.html'
SEO_PATHS['profile']='ven-napan.html'
SEO_PATHS['notfound']='404.html'
SEO_PERSON={'@type': 'Person', '@id': 'https://www.ydml.co.th/pmnapan-library/#ven-napan', 'name': 'พระมหานภันต์ สนฺติภทฺโท', 'alternateName': ['Ven. Napan Santibhaddo', 'Venerable Napan Thawornbanjob', 'PM Napan'], 'url': 'https://www.ydml.co.th/pmnapan-library/ven-napan.html', 'image': 'https://www.ydml.co.th/pmnapan-library/assets/profile/ven-napan-profile-v2.webp', 'jobTitle': 'ผู้ช่วยเจ้าอาวาสวัดสระเกศราชวรมหาวิหาร', 'sameAs': ['https://www.kaiciid.org/who-we-are/fellows/ven-napan-thawornbanjob','https://ibhap.org/old/committee-members/','https://www.gchumanrights.org/gc-news/from-temple-to-classroom-how-a-buddhist-monk-is-bridging-faith-and-human-rights/']}
SEO_WEBSITE={'@type': 'WebSite', '@id': 'https://www.ydml.co.th/pmnapan-library/#website', 'url': 'https://www.ydml.co.th/pmnapan-library/', 'name': 'PMNapan Library Dhamma Archive', 'inLanguage': 'th', 'description': 'รวมคลิปธรรมะ คำคม ข่าวและบทสัมภาษณ์ที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) พร้อมลิงก์วิดีโอและแหล่งเผยแพร่ต้นฉบับ'}

def seo_tags(active,title,description,lang='th'):
    import json
    from html import escape as _escape
    base='https://www.ydml.co.th/pmnapan-library/'
    path=SEO_PATHS[active]
    canonical=base+('en/'+(path or 'index.html') if lang=='en' else path)
    page_type='ProfilePage' if active=='profile' else ('CollectionPage' if active not in ('video','about','notfound') else 'WebPage')
    website_node=dict(SEO_WEBSITE)
    website_node['inLanguage']=lang
    if lang=='en':
        website_node['description']='A source-linked archive of Dhamma videos, quotes, news and interviews related to Ven. Napan Santibhaddo.'
    person_node=dict(SEO_PERSON)
    if lang=='en':
        person_node['jobTitle']='Assistant Abbot, Wat Saket Ratchaworamahawihan'
    page_node={'@type':page_type,'@id':canonical+'#webpage','url':canonical,'name':title,'description':description,
        'inLanguage':lang,'isPartOf':{'@id':base+'#website'},'about':person_node}
    if active=='profile':
        page_node['mainEntity']=person_node
    graph=[website_node,page_node]
    if active in ('category','video'):
        graph=[website_node]
    if active not in ('home','category','video'):
        graph.append({'@type':'BreadcrumbList','@id':canonical+'#breadcrumbs',
          'itemListElement':[{'@type':'ListItem','position':1,'name':('Home' if lang=='en' else 'หน้าแรก'),'item':(base+'en/index.html' if lang=='en' else base)},
          {'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':canonical}]})
    social_image=base+('assets/archive/four-ps-original.webp' if active=='fourps' else ('assets/profile/ven-napan-profile-v2.webp' if active=='profile' else 'assets/monk-watering-960.webp'))
    if lang=='en':
        social_alt='Original image from the Four Monks archive' if active=='fourps' else ('Ven. Napan Santibhaddo' if active=='profile' else 'PMNapan Library Dhamma Archive')
    else:
        social_alt='ภาพต้นฉบับพระสงฆ์สี่รูปในการสนทนา 4 พส.' if active=='fourps' else ('พระมหานภันต์ สนฺติภทฺโท ในงานเสวนาระหว่างศาสนา' if active=='profile' else 'PMNapan Library คลังธรรมะพระมหานภันต์')
    tags=['<meta name="robots" content="index,follow,max-image-preview:large">',
      '<meta property="og:site_name" content="PMNapan Library Dhamma Archive">',
      '<meta property="og:locale" content="'+('en_US' if lang=='en' else 'th_TH')+'">',
      '<meta property="og:image" content="'+social_image+'">',
      '<meta property="og:image:alt" content="'+social_alt+'">',
      '<meta name="twitter:card" content="summary_large_image">']
    if active=='fourps':
        tags.extend(['<meta property="og:image:width" content="1200">',
          '<meta property="og:image:height" content="630">',
          '<meta name="twitter:image" content="'+social_image+'">'])
    if active in ('saved','notfound'):
        tags[0]='<meta name="robots" content="noindex,follow">'
    th_url=base+path
    en_url=base+'en/'+(path or 'index.html')
    tags.extend([
      '<link rel="alternate" hreflang="th" href="'+th_url+'">',
      '<link rel="alternate" hreflang="en" href="'+en_url+'">',
      '<link rel="alternate" hreflang="x-default" href="'+th_url+'">'
    ])
    if active in ('category','video'):
        tags.append("""<script>
(function(){
  const p=new URLSearchParams(location.search);
  const filename=location.pathname.split('/').pop();
  const root='https://www.ydml.co.th/pmnapan-library/';
  const isEn=document.documentElement.lang.toLowerCase().startsWith('en');
  const target=new URL((isEn?'en/':'')+filename, root);
  const thTarget=new URL(filename,root);
  const enTarget=new URL('en/'+filename,root);
  if(filename==='video.html'){
    const id=p.get('id')||p.get('clip');
    if(id && /^(YouTube|TikTok):[A-Za-z0-9_-]{8,35}$/.test(id)){
      target.searchParams.set('id',id);thTarget.searchParams.set('id',id);enTarget.searchParams.set('id',id);
    }
  }
  if(filename==='category.html'){
    const name=p.get('name');
    if(name && name.length<110){
      target.searchParams.set('name',name);thTarget.searchParams.set('name',name);enTarget.searchParams.set('name',name);
    }
  }
  const link=document.createElement('link');link.rel='canonical';link.href=target.href;document.head.appendChild(link);
  const og=document.createElement('meta');og.setAttribute('property','og:url');og.content=target.href;document.head.appendChild(og);
  const thAlt=document.querySelector('link[rel="alternate"][hreflang="th"]');if(thAlt)thAlt.href=thTarget.href;
  const enAlt=document.querySelector('link[rel="alternate"][hreflang="en"]');if(enAlt)enAlt.href=enTarget.href;
  const xdAlt=document.querySelector('link[rel="alternate"][hreflang="x-default"]');if(xdAlt)xdAlt.href=thTarget.href;
})();
</script>""")
    else:
        tags.extend(['<link rel="canonical" href="'+canonical+'">','<meta property="og:url" content="'+canonical+'">'])
    tags.append('<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>')
    return '\n'.join(tags)

def shell(active,title,description,content,lang='th'):
 extra_css='<link rel="stylesheet" href="./assets/four-ps.css">' if active=='fourps' else ('<link rel="stylesheet" href="./assets/profile.css">' if active=='profile' else '')
 extra_js='<script defer src="./assets/four-ps.js"></script>' if active=='fourps' else ('<script defer src="./assets/profile.js"></script>' if active=='profile' else '')
 if lang=='th':
  title=SEO_TITLES.get(active,title)
  description=SEO_DESCRIPTIONS.get(active,description)
 base_tag='<base href="../">' if lang=='en' else ''
 return f'''<!doctype html>
<html lang="{lang}"><head>
{base_tag}
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#ffffff">
<meta name="description" content="{escape(description,quote=True)}">
<meta property="og:type" content="website"><meta property="og:title" content="{escape(title,quote=True)}"><meta property="og:description" content="{escape(description,quote=True)}">
<title>{escape(title)}</title>
{seo_tags(active,title,description,lang)}
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
<link rel="stylesheet" href="./assets/site.css?v=20261121-press-cards">
{extra_css}
<link rel="stylesheet" href="./assets/ydml-footer.css">
<link rel="stylesheet" href="./assets/analytics.css">
<script defer src="./assets/i18n.js"></script>
<script defer src="./assets/site.js?v=20261121-press-dates"></script>
{extra_js}
<script defer src="./assets/analytics.js"></script>
</head><body data-page="{active}" data-lang="{lang}">
<a href="#main" class="skip-link">ข้ามไปยังเนื้อหา</a>
{header(active,lang)}
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
<div class="topic-filter-status" id="topicFilterStatus" hidden><span>หัวข้อที่เลือก: <strong id="topicFilterName"></strong></span><button id="clearTopic" type="button">ล้างหัวข้อ ×</button></div>
<div class="search-row">
<label class="input-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.5"/><path d="m16 16 5 5"/></svg><span class="sr-only">ค้นหาวิดีโอ</span><input type="search" id="searchInput" placeholder="ค้นหาชื่อคลิป คำอธิบาย หรือหัวข้อ" autocomplete="off"></label>
<button class="fav-filter" id="favoriteFilter" type="button" aria-pressed="false">♡ รายการที่บันทึก</button>
</div><p class="search-scope-note">ผลการค้นหาอ้างอิงข้อมูลชื่อคลิป คำอธิบาย หมวดรายการ และข้อมูลกำกับที่มีอยู่ในคลัง</p><div class="filter-controls">
<label>หมวดรายการ<select id="categoryFilter"><option value="all">ทุกหมวด</option></select></label>
<label>ปีเผยแพร่<select id="yearFilter"><option value="all">ทุกปี</option></select></label>
<label>ช่องทาง<select id="platformFilter"><option value="all">ทุกช่องทาง</option><option value="YouTube">YouTube</option><option value="TikTok">TikTok</option><option value="Facebook">Facebook</option></select></label>
<label>เรียงลำดับ<select id="sortFilter"><option value="new">ใหม่ล่าสุด</option><option value="old">เก่าสุด</option><option value="title">ชื่อเรื่อง ก–ฮ</option><option value="length">วิดีโอยาวที่สุด</option></select></label>
</div><div class="filter-footer"><p id="resultCount" aria-live="polite">กำลังโหลด...</p><a class="saved-view-link" href="./saved.html">♡ หน้าคลิปที่บันทึกไว้ ↗</a><button type="button" class="reset-filter" id="resetFilters" hidden>ล้างตัวกรอง ↺</button></div></div>'''
home=f'''<section class="hero"><div class="container hero-row"><div class="hero-copy">
<p class="hero-kicker"><span></span> VIDEO ARCHIVE</p>
<h1>PMNapan Library<br><span>Dhamma Archive</span></h1>
<h2>คลังวิดีโอพระมหานภันต์ สนฺติภทฺโท</h2>
<div class="hero-actions"><a class="btn primary" href="./library.html">▶ ค้นหาธรรมะและวิดีโอ</a><a class="btn secondary" href="./categories.html">สำรวจหมวดรายการ ↗</a></div>
<p class="hero-total"><strong id="homeTotal">—</strong> วิดีโอในคลัง</p>
<a class="hero-saved-shortcut" href="./saved.html">♡ เปิดคลิปที่บันทึกไว้ <span aria-hidden="true">↗</span></a>

</div><div class="hero-visual"><span class="blue-orbit"></span><img src="./assets/monk-watering-960.webp" srcset="./assets/monk-watering-620.webp 620w, ./assets/monk-watering-960.webp 960w" sizes="(max-width: 650px) 300px, (max-width: 910px) 400px, 540px" alt="การ์ตูนพระรดน้ำต้นไม้ พร้อมสัญลักษณ์การพัฒนาที่ยั่งยืน" width="960" height="919" fetchpriority="high" decoding="async"></div></div></section>
<section class="quick-search"><div class="container"><form id="homeSearchForm" class="quick-search-form" role="search">
<label for="homeSearch">ค้นหาวิดีโอ</label><input id="homeSearch" type="search" placeholder="พิมพ์ชื่อคลิปหรือคำสำคัญ" autocomplete="off">
<button type="submit">ค้นหา →</button></form></div></section>
<section class="profile-home-card" aria-labelledby="homeProfileTitle"><div class="container"><div class="profile-home-card-inner"><span class="profile-home-card-image"><img src="./assets/profile/ven-napan-profile-v2.webp" alt="พระมหานภันต์ สนฺติภทฺโท" width="360" height="360" loading="lazy" decoding="async"></span><span class="profile-home-card-copy"><small>KNOW VEN. NAPAN</small><strong id="homeProfileTitle">รู้จักพระมหานภันต์ สนฺติภทฺโท</strong><p>จากสามเณรและการศึกษาพระปริยัติธรรม สู่การทำงานด้านสันติภาพ สิทธิมนุษยชน SDGs และการเสวนาระหว่างศาสนา</p></span><a href="./ven-napan.html">เปิดหน้าโปรไฟล์ ↗</a></div></div></section>
<section class="ps-home-promo" aria-labelledby="psHomePromoTitle">
<div class="container">
<a href="./four-ps.html" class="ps-home-feature" aria-label="เปิดคลังพิเศษ ปรากฏการณ์ 4 พส. ข่าว คลิป และเหตุการณ์สำคัญ">
<div class="ps-home-feature-image">
<img src="./assets/archive/four-ps-original.webp" alt="ภาพต้นฉบับพระสงฆ์สี่รูปนั่งสนทนาอยู่หน้าโต๊ะ มีไมโครโฟนและของตกแต่ง" width="1200" height="630" loading="lazy" decoding="async">
<div class="ps-home-image-caption"><span class="ps-home-image-dot" aria-hidden="true"></span><span>ภาพประกอบจากคลังภาพ 4 พส.</span></div>
</div>
<div class="ps-home-feature-copy">
<p class="ps-home-feature-overline"><span class="ps-home-feature-mark" aria-hidden="true"></span> SPECIAL COLLECTION · 2564—2565</p>
<h2 id="psHomePromoTitle">ปรากฏการณ์<br><span>4 พส.</span></h2>
<p class="ps-home-feature-subtitle">สำรวจข่าว คลิป และเหตุการณ์สำคัญในปรากฏการณ์ธรรมะออนไลน์</p>
<div class="ps-home-feature-tags"><span>ข่าวและบทวิเคราะห์</span><span>คลิปวิดีโอ</span><span>บทบาทพระมหานภันต์</span></div>
<span class="ps-home-feature-cta">เปิดคลังพิเศษ <span aria-hidden="true">↗</span></span>
</div>
</a>
</div>
</section>
<section class="section home-discovery-section" aria-labelledby="topicDiscoverHeading"><div class="container"><div class="heading-row"><div><p class="kicker">START HERE</p><h2 id="topicDiscoverHeading">เริ่มต้นจากเรื่องที่สนใจ</h2><p class="home-section-hint">เลือกหัวข้อเพื่อสำรวจวิดีโอที่เกี่ยวข้องจากชื่อคลิปและข้อมูลกำกับของแต่ละรายการ</p></div></div><div id="homeDiscoveryTopics" class="discovery-topic-grid"><div class="loading">กำลังค้นหาหัวข้อจากคลัง...</div></div></div></section>
<section class="section home-latest-section" aria-labelledby="homeLatestTitle"><div class="container">
<div class="heading-row"><div><p class="kicker">LATEST BY ORIGINAL PUBLISH DATE</p><h2 id="homeLatestTitle">วิดีโอเผยแพร่ล่าสุด</h2>
<p class="home-section-hint">เรียงตามวันที่เผยแพร่ของวิดีโอ</p></div>
<a href="./library.html" class="text-link">เปิดคลังวิดีโอ →</a></div>
<div id="homeLatest" class="video-grid" aria-label="วิดีโอเผยแพร่ล่าสุด"><div class="loading">กำลังโหลดรายการ...</div></div>
</div></section>
<section class="section shorts-spotlight"><div class="container">
<div class="heading-row"><div><p class="kicker">SHORT-FORM VIDEO · TIKTOK</p><h2>ธรรมะคลิปสั้น</h2></div><a href="./shorts.html" class="text-link">ดูคลิปทั้งหมด ↗</a></div>
<div id="homeShorts" class="shorts-grid"><div class="loading">กำลังโหลดคลิปสั้น...</div></div>
</div></section>
<section class="section"><div class="container"><div class="heading-row"><div><p class="kicker">DHAMMA QUOTES · ORIGINAL IMAGES</p><h2>คำคมธรรมะ</h2></div><a href="./quotes.html" class="text-link">ดูคำคมทั้งหมด ↗</a></div>
<div id="homeQuotes" class="quote-grid"><div class="loading">กำลังโหลดคำคมธรรมะ...</div></div></div></section>'''
home += '<section class="section seo-discovery" aria-labelledby="archiveExploreHeading"><div class="container"><div class="seo-discovery-inner"><h2 id="archiveExploreHeading">ค้นหาธรรมะและผลงานของพระมหานภันต์ สนฺติภทฺโท</h2><p>PMNapan Library เป็นพื้นที่รวบรวมรายการธรรมะ บทสัมภาษณ์ ข่าว และสื่อที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท (Ven. Napan) เพื่อให้ผู้สนใจค้นคว้าและติดตามผลงานย้อนหลังได้อย่างสะดวก พร้อมเชื่อมโยงไปยังแหล่งเผยแพร่ของแต่ละรายการ</p><nav class="seo-discovery-links" aria-label="สำรวจคลังธรรมะ"><a href="./ven-napan.html">รู้จักพระมหานภันต์</a><a href="./library.html">ค้นหาคลิปและธรรมบรรยาย</a><a href="./categories.html">เลือกหมวดรายการธรรมะ</a><a href="./shorts.html">ดูธรรมะคลิปสั้น</a><a href="./quotes.html">ดูภาพคำคมธรรมะ</a><a href="./press.html">อ่านข่าวและบทสัมภาษณ์</a><a href="./about.html">เกี่ยวกับแหล่งข้อมูล</a></nav></div></div></section>'
categories=f'''{intro('ALL SERIES','หมวดรายการ','สำรวจรายการธรรมะและคลังวิดีโอแยกตามหมวดหมู่')}
<section class="section"><div class="container"><div class="category-summary" id="categorySummary"></div>
<a class="ps-category-banner" href="./four-ps.html" aria-label="เปิดหมวดพิเศษ ปรากฏการณ์ 4 พส.">
<span class="ps-category-photo"><img src="./assets/archive/four-ps-original.webp" alt="ภาพต้นฉบับพระสงฆ์สี่รูปนั่งสนทนาอยู่หน้าโต๊ะ มีไมโครโฟนและของตกแต่ง" width="1200" height="630" loading="lazy" decoding="async"></span>
<span class="ps-category-info"><small>FEATURED COLLECTION · 2564–2565</small><strong>ปรากฏการณ์ 4 พส.</strong>
<em>รวบรวมข่าว คลิป และบทบาทของพระมหานภันต์ตามลำดับเวลา</em><span class="ps-category-explore">เปิดดูเส้นเวลาและคลิป</span></span>
<span class="ps-category-arrow" aria-hidden="true">↗</span>
</a>
<div id="allCategories" class="series-grid"><div class="loading">กำลังโหลดหมวดรายการ...</div></div>
<aside class="program-note" id="relatedNotice" hidden><strong>เกี่ยวกับ “หลวงพี่ช่วยด้วย”</strong><p>รายการ “หลวงพี่ช่วยด้วย” เผยแพร่โดย Workpoint และดำเนินรายการโดยพระมหาสมปอง ตาลปุตฺโต วิดีโอในหมวดนี้มีคำบรรยายที่จัดทำโดยมูลนิธิ สกพ.</p><a href="https://www.youtube.com/playlist?list=PLFU5BMWz_rx10E1AiFivlOPsVO8qQFvmx" target="_blank" rel="noopener noreferrer">เพลย์ลิสต์ต้นทาง ↗</a></aside>
</div></section>'''
quotes=f'''{intro('DHAMMA QUOTES','คำคมธรรมะ','รวบรวมภาพคำคมธรรมะที่เกี่ยวข้องกับพระมหานภันต์ พร้อมข้อมูลแหล่งเผยแพร่')}
<section class="section"><div class="container">
<div class="quote-toolbar">
<label for="quoteSearch">ค้นหาข้อความคำคม</label><input type="search" id="quoteSearch" placeholder="ค้นหาคำหรือข้อความ" autocomplete="off">
<p id="quotesCount" role="status" aria-live="polite">กำลังโหลดข้อมูล...</p><p class="quote-search-coverage" id="quoteSearchCoverage" role="note"></p></div>
<div class="quote-grid" id="quoteGrid"><div class="loading">กำลังโหลดภาพคำคมธรรมะ...</div></div>
<div class="empty" id="quoteEmpty" hidden><p>ไม่พบคำคมที่ตรงกับคำค้น ลองใช้คำอื่นหรือเปิดดูภาพทั้งหมด</p><button id="clearQuoteSearch" type="button">ดูภาพคำคมทั้งหมด</button></div>
</div></section>'''
press=f'''{intro('PRESS · INTERVIEWS · ARCHIVE','ข่าว บทสัมภาษณ์ และผลงาน','รวบรวมข่าว บทสัมภาษณ์ และกิจกรรมที่เกี่ยวข้องกับพระมหานภันต์จากสื่อหลากหลายแหล่ง')}
<section class="section"><div class="container">
<aside class="ps-press-crosslink"><strong>ติดตามเรื่องราวปรากฏการณ์ 4 พส. (พ.ศ. 2564–2565)</strong>
<a href="./four-ps.html">อ่านข่าวและชมคลิปตามลำดับเหตุการณ์ ↗</a></aside>
<div class="press-tools">
<label class="press-search-label" for="pressSearch">ค้นหาเนื้อหา<input id="pressSearch" type="search" placeholder="ค้นหาชื่อเรื่อง แหล่งข่าว หรือคำสำคัญ" autocomplete="off"></label>
<label class="press-select-label" for="pressCategory">ประเภท<select id="pressCategory"><option value="">ทุกประเภท</option></select></label>
<p id="pressCount" role="status" aria-live="polite">กำลังโหลดข้อมูล...</p></div>
<div id="pressGrid" class="press-grid"><p class="loading">กำลังโหลดข่าวและผลงาน...</p></div>
<p id="pressEmpty" class="empty" hidden>ไม่พบข้อมูลตรงกับคำค้น</p>
<p class="press-media-link">วิดีโอและรายการจากหน่วยงานภายนอก <a href="./external-media.html">สำรวจสื่อจากแหล่งภายนอก ↗</a></p>\n<p class="press-source-note">การ์ดแต่ละรายการมีคำอธิบายภาษาไทย หัวข้อและบทบาทของพระอาจารย์ วันจัดกิจกรรม (เมื่อมีหลักฐาน) แสดงแยกจากวันที่เผยแพร่ข่าวหรือบทความ และเชื่อมโยงไปยังแหล่งเผยแพร่ต้นฉบับ</p>
</div></section>'''
external_media=f'''{intro('EXTERNAL MEDIA · SOURCE INDEX','สื่อจากแหล่งภายนอก','รวมรายการและสื่อจากหน่วยงานภายนอก พร้อมลิงก์ต้นทางและข้อมูลประกอบสำหรับการค้นคว้า')}
<section class="section"><div class="container">
<div class="press-tools">
<label class="press-search-label" for="externalMediaSearch">ค้นหาสื่อ<input id="externalMediaSearch" type="search" placeholder="ค้นหาชื่อรายการหรือหน่วยงาน" autocomplete="off"></label>
<label class="press-select-label" for="externalMediaStatus">ประเภทข้อมูล
<select id="externalMediaStatus"><option value="all">แสดงทั้งหมด</option><option value="verified">สื่อจากแหล่งต้นทาง</option><option value="needs_review">รายการที่กำลังรวบรวมข้อมูล</option><option value="lead">ข้อมูลประกอบเพิ่มเติม</option></select></label>
<p id="externalMediaCount" role="status" aria-live="polite">กำลังโหลดข้อมูล...</p></div>
<div id="externalMediaGrid" class="press-grid"><p class="loading">กำลังโหลดสื่อ...</p></div>
<p id="externalMediaEmpty" class="empty" hidden>ไม่พบรายการที่ตรงกับเงื่อนไข</p>
<p class="press-source-note">รายการในหน้านี้เชื่อมโยงไปยังแหล่งเผยแพร่หรือเอกสารที่เกี่ยวข้องโดยตรง การเข้าถึงบางรายการอาจขึ้นอยู่กับเงื่อนไขของผู้ให้บริการ</p>
</div></section>'''
shorts=f'''{intro('SHORT-FORM VIDEO · TIKTOK','ธรรมะคลิปสั้น','คลิปธรรมะจากบัญชี TikTok @domskyline21')}
<section class="shorts-credit-banner"><div class="container"><aside class="source-credit" aria-label="ขอบคุณแหล่งเผยแพร่วิดีโอสั้น">
 <div class="source-credit-mark" aria-hidden="true">♫</div>
 <div class="source-credit-copy">
 <span class="source-credit-eyebrow">ขอบคุณแหล่งเผยแพร่วิดีโอสั้น</span>
 <p>ขอขอบคุณ คุณลิงจั๊กจั๊ก (@domskyline21) สำหรับการเผยแพร่วิดีโอสั้นที่เกี่ยวข้องกับพระมหานภันต์</p>
 </div>
 <a class="source-credit-link" href="https://www.tiktok.com/@domskyline21" target="_blank" rel="noopener noreferrer" aria-label="เปิดบัญชี TikTok คุณลิงจั๊กจั๊ก">@domskyline21 <span aria-hidden="true">↗</span></a>
 </aside></div></section>
<section class="section"><div class="container">
<div class="shorts-search-bar"><label for="shortsSearch">ค้นหาคลิปสั้น</label><input type="search" id="shortsSearch" placeholder="ค้นหาชื่อคลิปหรือคำสำคัญ" autocomplete="off"><span id="shortsCount" aria-live="polite" role="status"></span></div>
<div id="shortsGrid" class="shorts-grid"><div class="loading">กำลังโหลดคลิปสั้น...</div></div>
<div id="shortsEmpty" class="empty" hidden>ไม่พบคลิปสั้นที่ตรงกับคำค้น</div>
<div class="load-wrap"><button id="loadShorts" type="button" class="btn secondary" hidden>ดูคลิปเพิ่มเติม ↓</button></div>
</div></section>'''
featured=f'''{intro('VIDEO COLLECTION','คลิปจากรายการ','รวมรายการธรรมะและวิดีโอย้อนหลังจากแหล่งเผยแพร่')}
<section class="section"><div class="container"><div id="featuredSections"><div class="loading">กำลังโหลดคลิปจากรายการ...</div></div></div></section>'''
library=f'''{intro('VIDEO LIBRARY','คลังวิดีโอ','ค้นหาและรับชมวิดีโอตามหัวข้อ หมวดรายการ ปีเผยแพร่ และช่องทาง')}
<section class="section"><div class="container">
<div class="knowledge-search-intro" aria-labelledby="knowledgeSearchTitle"><div><p class="kicker">SEARCH BY INTEREST</p><h2 id="knowledgeSearchTitle">อยากรู้ว่าเรื่องนี้อยู่ในคลิปไหน?</h2><p>พิมพ์เรื่องหรือคำที่สนใจ เช่น ความเครียด การให้ สมาธิ ครอบครัว หรือการทำงาน เพื่อค้นจากชื่อคลิป คำอธิบาย หมวดรายการ และหัวข้อที่เกี่ยวข้อง</p></div><div id="libraryTopicChips" class="library-topic-chips" aria-label="หัวข้อแนะนำ"></div></div>
<p class="press-media-link">วิดีโอและรายการจากหน่วยงานภายนอก <a href="./external-media.html">สำรวจสื่อจากแหล่งภายนอก ↗</a></p>
{tabs_bar()}
{grid('คลังวิดีโอทั้งหมด','libraryGrid')}<div class="empty" id="emptyResults" hidden><h2 id="emptyResultsHeading">ไม่พบคลิปที่ตรงกับเงื่อนไข</h2><p id="emptyResultsHelp">ลองค้นหาใหม่หรือเปลี่ยนตัวกรอง</p><div class="empty-actions"><button type="button" id="clearAll">แสดงคลิปทั้งหมด</button><a class="btn secondary" href="./categories.html">ดูหมวดรายการ</a><a class="btn minimal" href="./shorts.html">ดูธรรมะคลิปสั้น</a></div></div>
<div class="load-wrap"><button id="loadMore" type="button" class="btn secondary" hidden>ดูวิดีโอเพิ่มเติม ↓</button></div></div></section>'''
category=f'''{intro('SERIES','หมวดรายการ','','categories.html','หมวดรายการ')}
<section class="section"><div class="container"><div class="heading-row"><span id="categoryCount" class="category-total"></span><a href="./categories.html" class="text-link">← ทุกหมวดรายการ</a></div>
<div class="program-note" id="categoryRelationNote" hidden></div>
{grid('วิดีโอในหมวดรายการ','categoryGrid')}
<div class="load-wrap"><button id="loadMore" type="button" class="btn secondary" hidden>ดูวิดีโอเพิ่มเติม ↓</button></div></div></section>'''
video=f'''{intro('VIDEO DETAILS','รายละเอียดวิดีโอ','','library.html','คลังวิดีโอ')}
<section class="section"><div class="container"><div id="videoDetail" class="detail-layout"><div class="loading">กำลังโหลดรายละเอียดวิดีโอ...</div></div></div></section>'''
about=f'''{intro('SOURCE INFORMATION','แหล่งข้อมูล','เกี่ยวกับคลังธรรมะและแหล่งเผยแพร่ที่เกี่ยวข้อง')}
<section class="section about-editorial-intro" aria-labelledby="aboutArchiveHeading"><div class="container about-layout about-sources-only">
<div class="about-panel about-editorial-panel">
<p class="kicker">ABOUT THE ARCHIVE</p>
<h2 id="aboutArchiveHeading">เกี่ยวกับ PMNapan Library</h2>
<p>PMNapan Library Dhamma Archive เป็นคลังสื่อดิจิทัลที่รวบรวมวิดีโอธรรมะ คำคม ข่าว บทสัมภาษณ์ และผลงานที่เกี่ยวข้องกับพระมหานภันต์ สนฺติภทฺโท เพื่อการศึกษาและค้นคว้าย้อนหลัง</p>
<p>เนื้อหาจัดแยกตามประเภทสื่อและหมวดรายการ โดยแสดงข้อมูลวันที่เผยแพร่และช่องทางที่เกี่ยวข้องเมื่อมีข้อมูล พร้อมลิงก์ไปยังผู้เผยแพร่แต่ละแห่ง</p>
<h3>การอ้างอิงและการใช้ข้อมูล</h3>
<p>ชื่อวิดีโอและคำอธิบายจากผู้เผยแพร่คงไว้ตามแหล่งข้อมูลเดิม ส่วนบทสรุปข่าวและเหตุการณ์เป็นข้อความเรียบเรียงสำหรับประกอบการค้นคว้า หากต้องการอ้างอิงถ้อยคำหรือเหตุการณ์โดยละเอียด ควรตรวจสอบจากแหล่งต้นทาง</p>
<h3>ขอบเขตการค้นหา</h3>
<p>การค้นหาในคลังครอบคลุมชื่อคลิป คำอธิบาย หมวดรายการ และข้อมูลที่จัดหมวดหมู่ไว้ หากมีคำถอดเสียงที่ผ่านการตรวจทานแล้ว เนื้อหาส่วนนั้นจะใช้ประกอบการค้นหาและแสดงพร้อมข้อมูลแหล่งที่มา</p>
<p>ข้อความคำคมที่ค้นหาได้ถอดจากข้อความที่มองเห็นในภาพคำคมต้นฉบับหรือระเบียนที่ตรวจสอบไว้ และคงชื่อผู้พูดตามที่ปรากฏในภาพเมื่อไม่ใช่พระมหานภันต์</p>
</div></div></section>
<section class="section"><div class="container about-layout about-sources-only"><div class="about-panel"><p class="kicker">OFFICIAL SOURCE CHANNELS</p>
<h2>แหล่งเผยแพร่ต้นฉบับ</h2><div class="source-links">
<a href="https://www.youtube.com/@Napan" target="_blank" rel="noopener noreferrer">YouTube · PM Napan <span>↗</span></a>
<a href="https://www.youtube.com/channel/UCjScesRz_L16aIs-Kdtsh_g" target="_blank" rel="noopener noreferrer">YouTube · IBHAP Foundation <span>↗</span></a>
<a href="https://www.facebook.com/NapanIBHAP/photos" target="_blank" rel="noopener noreferrer">Facebook · พระมหานภันต์ สกพ. - Ven.Napan IBHAP · รูปภาพ <span>↗</span></a>
</div></div></div></section>'''
about += '\n<section class="section analytics-privacy-section" id="analytics-privacy">\n<div class="container about-layout"><div class="about-panel">\n<h2>การวัดผลการใช้งานและความเป็นส่วนตัว</h2>\n<p>เว็บไซต์ PMNapan Library ใช้ Google Analytics 4 เพื่อวิเคราะห์จำนวนผู้เข้าชม จำนวนครั้งที่เปิดหน้าเว็บ หน้าที่ได้รับความนิยม และการคลิกลิงก์ไปยังคลิปหรือบทความต้นฉบับ การวัดผลนี้เริ่มทำงานเฉพาะเมื่อผู้เข้าชมกด “ยินยอม” เท่านั้น</p>\n<p>เมื่อยินยอม ข้อมูลการใช้งานบางส่วนจะถูกส่งให้ Google เพื่อจัดทำรายงานสถิติ โดยระบบอาจใช้คุกกี้เพื่อจดจำการเข้าชม ไม่ใช้ระบบนี้เพื่อแสดงโฆษณาแบบเจาะจง ผู้เข้าชมสามารถเปลี่ยนความยินยอมได้จากปุ่ม “ตั้งค่าคุกกี้” ที่ส่วนท้ายทุกหน้า การถอนความยินยอมจะหยุดการส่งข้อมูลครั้งต่อไป ไม่ลบข้อมูลที่ส่งไปแล้ว</p>\n<p>การคลิกไปยังเว็บไซต์ YouTube, TikTok หรือสื่อภายนอกไม่ได้หมายความว่ามีการรับชมวิดีโอจริง สถิติอาจไม่รวมผู้ที่ไม่ยินยอม ใช้ระบบบล็อกการติดตาม หรือถูกจำกัดจากเบราว์เซอร์</p>\n</div></div></section>'
saved=f'''{intro('SAVED VIDEOS','คลิปที่บันทึกไว้','รวมวิดีโอที่บันทึกไว้เพื่อรับชมภายหลัง')}
<section class="section"><div class="container">
<div class="saved-information">
<div><strong>รายการโปรดของคุณ</strong>
<p>รายการนี้จัดเก็บในเบราว์เซอร์ที่ใช้งาน หากเปลี่ยนอุปกรณ์หรือล้างข้อมูลเว็บไซต์ รายการที่บันทึกไว้อาจไม่ปรากฏ</p></div>
<a class="btn secondary" href="./library.html">ค้นหาคลิปเพิ่มเติม →</a>
</div>
<p id="savedCount" class="category-summary" aria-live="polite">กำลังโหลดรายการที่บันทึก...</p>
{grid('คลิปที่บันทึกไว้','savedGrid')}
<div id="savedEmpty" class="empty" hidden><h2>ยังไม่มีคลิปที่บันทึกไว้</h2><p>กดสัญลักษณ์หัวใจบนวิดีโอที่สนใจ เพื่อบันทึกไว้ดูภายหลัง</p>
<a class="btn primary" href="./library.html">ไปที่คลังวิดีโอ →</a></div>
<div class="load-wrap"><button id="loadMore" type="button" class="btn secondary" hidden>ดูคลิปที่บันทึกเพิ่มเติม ↓</button></div>
</div></section>'''
notfound=f'''{intro('PAGE NOT FOUND','ไม่พบหน้าที่ต้องการ','ลิงก์นี้อาจถูกเปลี่ยน ย้าย หรือไม่มีอยู่ใน PMNapan Library')}
<section class="section"><div class="container"><div class="empty standalone-empty"><h2>ลองเริ่มใหม่จากส่วนที่ต้องการ</h2><p>สามารถค้นหาวิดีโอ สำรวจหมวดรายการ หรือกลับหน้าแรกได้จากตัวเลือกด้านล่าง</p><div class="empty-actions"><a class="btn primary" href="./library.html">ค้นหาในคลังวิดีโอ</a><a class="btn secondary" href="./categories.html">ดูหมวดรายการ</a><a class="btn minimal" href="./index.html">กลับหน้าแรก</a></div></div></div></section>'''
fourps='<section class="ps-hero" aria-labelledby="psHeroTitle"><div class="container ps-hero-container">\n<nav class="ps-breadcrumb" aria-label="ตำแหน่งหน้า"><a href="./index.html">หน้าแรก</a><span aria-hidden="true">/</span><span>ปรากฏการณ์ 4 พส.</span></nav>\n<div class="ps-hero-grid"><div class="ps-hero-content">\n<p class="ps-hero-eyebrow"><span class="ps-status-dot" aria-hidden="true"></span> PMNAPAN LIBRARY · SPECIAL ARCHIVE / 2021–2022</p>\n<h1 id="psHeroTitle">ปรากฏการณ์<br><span>4 พส.</span></h1>\n<p class="ps-hero-lead">ย้อนรอยปรากฏการณ์ธรรมะออนไลน์ใน พ.ศ. 2564–2565 ผ่านข่าว คลิป และเหตุการณ์สำคัญที่เกี่ยวข้องกับพระมหานภันต์</p>\n<div class="ps-hero-actions"><a href="#psSpotlight" class="ps-action-primary">เหตุการณ์ของพระมหานภันต์ <span aria-hidden="true">↘</span></a>\n<a href="#psTimelineSection" class="ps-action-secondary">สำรวจเส้นเวลาทั้งหมด <span aria-hidden="true">↓</span></a></div>\n</div><figure class="ps-hero-visual">\n<div class="ps-hero-photo-frame"><img src="./assets/archive/four-ps-original.webp" alt="ภาพต้นฉบับพระสงฆ์สี่รูปนั่งสนทนาอยู่หน้าโต๊ะ มีไมโครโฟนและของตกแต่ง" width="1200" height="630" fetchpriority="high" decoding="async"></div>\n<figcaption class="ps-hero-photo-caption">\n<span class="ps-image-status" aria-hidden="true"></span>\n<span>ภาพประกอบจากคลังภาพปรากฏการณ์ 4 พส.</span>\n</figcaption>\n</figure></div>\n<div class="ps-hero-stats" aria-label="สถิติคอนเทนต์ในคลังพิเศษ">\n<div><strong id="psEventTotal">—</strong><span>เหตุการณ์</span></div>\n<div><strong id="psNewsTotal">—</strong><span>ข่าว / บทวิเคราะห์</span></div>\n<div><strong id="psVideoTotal">—</strong><span>คลิป / รายการ</span></div>\n<div><strong id="psNapanTotal">—</strong><span>เหตุการณ์เกี่ยวกับพระมหานภันต์</span></div>\n</div></div></section>\n<nav class="ps-section-nav" id="psSectionNav" aria-label="สารบัญคลังพิเศษ 4 พส."><div class="container ps-section-nav-inner"><div class="ps-section-links"><a href="#psPeopleSection" data-ps-section="psPeopleSection">ภาพรวม</a><a href="#psSpotlight" data-ps-section="psSpotlight">เหตุการณ์สำคัญ</a><a href="#psVideoFeature" data-ps-section="psVideoFeature">วิดีโอ</a><a href="#psTimelineSection" data-ps-section="psTimelineSection">เส้นเวลา</a><a href="#psPendingSection" data-ps-section="psPendingSection">อ้างอิงเพิ่มเติม</a><a href="#psSourcesSection" data-ps-section="psSourcesSection">ที่มา</a></div><div class="ps-reading-progress" aria-hidden="true"><span id="psProgressBar"></span></div></div></nav>\n<section class="ps-context" id="psPeopleSection" aria-labelledby="psAboutHeading"><div class="container">\n<div class="ps-context-head"><p class="ps-section-kicker">THE PEOPLE · FOUR MONKS</p><h2 id="psAboutHeading">เรื่องราวของ “4 พส.”</h2>\n<p>ทำความรู้จักพระนักเทศน์ทั้งสี่รูปที่มีบทบาทในปรากฏการณ์ธรรมะออนไลน์ช่วง พ.ศ. 2564–2565</p></div>\n<div id="psPeople" class="ps-people-grid"><p class="ps-loading">กำลังโหลดรายชื่อ...</p></div>\n</div></section>\n<section class="ps-spotlight" id="psSpotlight" aria-labelledby="psSpotlightTitle"><div class="container">\n<div class="ps-section-heading"><div><p class="ps-section-kicker">FEATURED HISTORY · KEY MOMENTS</p><h2 id="psSpotlightTitle">เหตุการณ์สำคัญและบทบาทของพระมหานภันต์</h2>\n<p>เหตุการณ์และข่าวที่สะท้อนบทบาทของพระมหานภันต์ พร้อมภาพประกอบและแหล่งอ้างอิง</p></div></div>\n<div id="psSpotlightGrid" class="ps-spotlight-grid"><p class="ps-loading">กำลังโหลดเหตุการณ์สำคัญ...</p></div>\n</div></section>\n<section class="ps-video-feature" id="psVideoFeature" aria-labelledby="psVideoFeatureTitle"><div class="container">\n<div class="ps-section-heading ps-video-feature-head"><div>\n<p class="ps-section-kicker">WATCH THE MOMENTS · VIDEO ARCHIVE</p>\n<h2 id="psVideoFeatureTitle">วิดีโอและรายการที่เกี่ยวข้อง</h2>\n<p>รวมคลิปวิดีโอจากช่องผู้เผยแพร่และสำนักข่าวที่เกี่ยวข้องกับเหตุการณ์สำคัญ</p></div>\n<a href="#psTimelineSection" class="ps-video-feature-link">ดูคลิปทั้งหมดในเส้นเวลา ↘</a>\n</div>\n<div class="ps-video-feature-grid" id="psVideoFeatured"><p class="ps-loading">กำลังโหลดคลิปจากแหล่งอ้างอิง...</p></div>\n</div></section>\n<section class="ps-timeline-section" id="psTimelineSection" aria-labelledby="psTimelineTitle"><div class="container">\n<div class="ps-section-heading"><div><p class="ps-section-kicker">COMPLETE CHRONOLOGY</p><h2 id="psTimelineTitle">เส้นเวลา ข่าว และคลิป</h2>\n<p>ค้นหาเหตุการณ์ บุคคล หรือสำนักข่าว และเลือกประเภทเนื้อหาที่สนใจ</p></div></div>\n<div class="ps-filter-shell" aria-label="ค้นหาและกรองเหตุการณ์"><div class="ps-filter-row">\n<label class="ps-search-label" for="psSearch"><span aria-hidden="true">⌕</span><input id="psSearch" type="search" placeholder="ค้นหาเหตุการณ์ ข่าว คลิป หรือชื่อบุคคล..." autocomplete="off"></label>\n<button id="psReset" type="button" class="ps-clear" hidden>ล้างตัวกรอง ×</button></div>\n<div class="ps-filter-pills" id="psFilters" role="group" aria-label="เลือกประเภทเหตุการณ์">\n<button class="ps-pill active" data-ps-filter="all" aria-pressed="true" type="button">ทั้งหมด</button>\n<button class="ps-pill" data-ps-filter="napan" aria-pressed="false" type="button">เกี่ยวข้องกับพระมหานภันต์</button>\n<button class="ps-pill" data-ps-filter="news" aria-pressed="false" type="button">ข่าวและบทความ</button>\n<button class="ps-pill" data-ps-filter="video" aria-pressed="false" type="button">คลิปวิดีโอ</button>\n<button class="ps-pill" data-ps-filter="viral" aria-pressed="false" type="button">สีสันและกระแส</button>\n<button class="ps-pill" data-ps-filter="debate" aria-pressed="false" type="button">ข้อถกเถียง</button>\n<button class="ps-pill" data-ps-filter="change" aria-pressed="false" type="button">ช่วงเปลี่ยนผ่าน</button></div>\n<div class="ps-filter-bottom"><p id="psResultCount" role="status" aria-live="polite">กำลังโหลดรายการ...</p>\n<span>ปี 2564–2565 · เรียงตามวันเกิดเหตุการณ์</span></div></div>\n<div class="ps-timeline" id="psTimeline"><p class="ps-loading">กำลังโหลดเส้นเวลา...</p></div>\n<div class="ps-empty" id="psEmpty" hidden><h3>ไม่พบเหตุการณ์ที่ตรงกับเงื่อนไข</h3><p>ลองค้นคำอื่น หรือเปลี่ยนหมวดการกรอง</p><button type="button" id="psEmptyReset">แสดงทั้งหมด</button></div>\n</div></section>\n<section class="ps-pending" id="psPendingSection" aria-labelledby="psPendingHeading"><div class="container">\n<div class="ps-section-heading"><div><p class="ps-section-kicker">ADDITIONAL SOURCES</p><h2 id="psPendingHeading">ข้อมูลอ้างอิงเพิ่มเติม</h2>\n<p>รายการสื่อและเอกสารเพิ่มเติมสำหรับประกอบการค้นคว้า ซึ่งบางรายการยังมีรายละเอียดที่ต้องตรวจทานจากแหล่งต้นทาง</p></div></div>\n<div id="psPending" class="ps-pending-grid"><p class="ps-loading">กำลังโหลดข้อมูลอ้างอิง...</p></div>\n</div></section>\n<section class="ps-note-section" id="psSourcesSection"><div class="container"><div class="ps-note-inner">\n<div class="ps-note-icon" aria-hidden="true">i</div><div><h2>เกี่ยวกับข้อมูลและแหล่งอ้างอิง</h2>\n<p>เนื้อหาเรียบเรียงจากข่าว บทสัมภาษณ์ และวิดีโอของแหล่งเผยแพร่ที่ระบุไว้ วันที่ในเส้นเวลาอ้างอิงวันเกิดเหตุการณ์ ซึ่งอาจแตกต่างจากวันเผยแพร่ข่าว</p>\n<p>ข่าว บทสัมภาษณ์ และคลิปวิดีโอเป็นผลงานของผู้เผยแพร่แต่ละแห่ง สำหรับรายละเอียดหรือคำกล่าวอ้างอิง โปรดอ่านหรือรับชมจากแหล่งต้นทาง</p>\n<a href="./about.html">อ่านแนวทางการอ้างอิงข้อมูลของ PMNapan Library ↗</a></div></div></div></section>'
profile='''<section class="profile-hero" aria-labelledby="profileTitle">
<div class="container profile-hero-inner">
<nav class="profile-breadcrumb" aria-label="ตำแหน่งหน้า"><a href="./index.html">หน้าแรก</a><span aria-hidden="true">/</span><span>รู้จักพระมหานภันต์</span></nav>
<div class="profile-hero-grid">
<div>
<p class="profile-eyebrow">VEN. NAPAN · LIFE & WORK</p>
<h1 id="profileTitle"><span>พระมหานภันต์</span> <span>สนฺติภทฺโท</span></h1>
<p class="profile-roman">Venerable Napan Santibhaddo (Thawornbanjob)</p>
<p class="profile-lead">พระนักพัฒนา นักสร้างสันติภาพ และนักสื่อสารพระพุทธศาสนา ผู้เชื่อมหลักธรรมเข้ากับการพัฒนาคน สังคม สันติภาพ สิทธิมนุษยชน การเสวนาระหว่างศาสนา และการพัฒนาที่ยั่งยืน</p>
<div class="profile-role-pills" aria-label="บทบาทปัจจุบัน">
<span>ผู้ช่วยเจ้าอาวาสวัดสระเกศราชวรมหาวิหาร</span>
<span>ประธานผู้ก่อตั้ง IBHAP Foundation</span>
<span>เลขาธิการ Religions for Peace Thailand</span>
</div>
<div class="profile-hero-actions">
<a class="primary" href="#profileWork">สำรวจผลงานสำคัญ <span aria-hidden="true">↓</span></a>
<a class="secondary" href="./library.html?category=%E0%B8%AD%E0%B8%B2%E0%B8%AA%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1">ชมวิดีโอในคลัง <span aria-hidden="true">↗</span></a>
</div>
</div>
<div class="profile-portrait-wrap">
<div class="profile-portrait-frame"><img src="./assets/profile/ven-napan-profile-v2.webp" alt="พระมหานภันต์ สนฺติภทฺโท" width="360" height="360" fetchpriority="high" decoding="async"></div>
</div>
</div>
</div>
</section>
<nav class="profile-section-nav" aria-label="สารบัญประวัติพระมหานภันต์"><div class="container">
<a href="#profileStory">เรื่องราว</a><a href="#profileWork">งานสำคัญ</a><a href="#profileEducation">การศึกษา</a><a href="#profileTimeline">เส้นทางสำคัญ</a><a href="#profileGlobal">เวทีนานาชาติ</a><a href="#profileMedia">สื่อและคลัง</a><a href="#profileSources">แหล่งอ้างอิง</a>
</div></nav>

<section class="profile-overview" id="profileStory" aria-labelledby="profileStoryTitle"><div class="container profile-overview-grid">
<div>
<p class="profile-section-kicker">FROM NOVICE TO SOCIAL ENGAGEMENT</p>
<h2 class="profile-section-title" id="profileStoryTitle">จากสามเณรภาคฤดูร้อน สู่พระนักพัฒนา</h2>
<p class="profile-copy">พระมหานภันต์บวชสามเณรภาคฤดูร้อนด้วยความสมัครใจตั้งแต่อายุ 7 ปี ก่อนบรรพชาเป็นสามเณรที่วัดสระเกศราชวรมหาวิหารเมื่ออายุ 11 ปี และอุปสมบทเป็นพระภิกษุใน พ.ศ. 2543 โดยได้รับฉายา <strong>“สนฺติภทฺโท”</strong></p>
<p class="profile-copy">ประสบการณ์การไปศึกษาและใช้ชีวิตในต่างจังหวัดตั้งแต่วัยสามเณรทำให้ท่านเห็นความสัมพันธ์ระหว่างวัด ชุมชน และวิถีชีวิตของผู้คนอย่างใกล้ชิด ประสบการณ์นี้กลายเป็นรากฐานของแนวคิดการใช้พระพุทธศาสนาในฐานะทุนทางสังคม เพื่อสร้างการเปลี่ยนแปลงเชิงบวกและพัฒนาสังคมอย่างยั่งยืน</p>
<blockquote class="profile-origin-quote">“ต้องการตอบแทนสังคม” — แรงตั้งต้นที่พระมหานภันต์กล่าวถึงในการอธิบายเหตุผลของการทำงานด้านสังคมและการพัฒนา</blockquote>
</div>
<div class="profile-facts" aria-label="ข้อมูลสำคัญ">
<div class="profile-fact accent"><strong>ป.ธ. 9</strong><span>สำเร็จเปรียญธรรม 9 ประโยค จากสำนักเรียนวัดสระเกศ พ.ศ. 2545</span></div>
<div class="profile-fact"><strong>2001</strong><span>ก่อตั้งกลุ่มเพื่อชีวิตดีงาม (For Beautiful Life Group: FBLG) และดำรงบทบาทประธานถึงปี 2015</span></div>
<div class="profile-fact"><strong>2015</strong><span>ก่อตั้ง Institute of Buddhist Management for Happiness and Peace Foundation (IBHAP)</span></div>
<div class="profile-fact"><strong>2018</strong><span>KAICIID Fellow และกล่าวปาฐกถาในพิธีวิสาขบูชาครั้งแรกที่รัฐสภายุโรป</span></div>
</div>
</div></section>

<section class="profile-band profile-work" id="profileWork" aria-labelledby="profileWorkTitle"><div class="container">
<div class="profile-head"><div><p class="profile-section-kicker">AREAS OF WORK</p><h2 class="profile-section-title" id="profileWorkTitle">งานที่เชื่อมพระพุทธศาสนากับสังคมร่วมสมัย</h2><p>ผลงานของพระมหานภันต์ครอบคลุมตั้งแต่การเผยแผ่ธรรมะและการพัฒนาคน ไปจนถึงสันติภาพ สิทธิมนุษยชน ความร่วมมือระหว่างศาสนา และ SDGs</p></div></div>
<div class="profile-work-grid">
<article class="profile-work-card"><span class="profile-work-num">01</span><h3>การพัฒนาคนและการศึกษา</h3><p>ออกแบบกระบวนการเรียนรู้และฝึกอบรมด้านคุณธรรม จริยธรรม ภาวะผู้นำ และการพัฒนาศักยภาพ โดยเริ่มจากงานกลุ่มเพื่อชีวิตดีงาม (For Beautiful Life Group) ตั้งแต่ พ.ศ. 2544</p><a href="./press.html">ดูข่าวและผลงานที่เกี่ยวข้อง ↗</a></article>
<article class="profile-work-card"><span class="profile-work-num">02</span><h3>สันติภาพและการอยู่ร่วมกัน</h3><p>ทำงานกับชุมชนและผู้นำศาสนาในพื้นที่ภาคใต้ของไทย เพื่อเยียวยาผู้ได้รับผลกระทบ ป้องกันความขัดแย้ง และสร้างพื้นที่อยู่ร่วมกันอย่างสันติ</p><a href="./press.html">สำรวจงานด้านสันติภาพ ↗</a></article>
<article class="profile-work-card"><span class="profile-work-num">03</span><h3>Buddhism for SDGs</h3><p>ขับเคลื่อนแนวคิดการนำคุณค่าทางพระพุทธศาสนามาเชื่อมกับเป้าหมายการพัฒนาที่ยั่งยืน ทั้งในระดับชุมชน ประเทศ และเวทีนานาชาติ</p><a href="./library.html?topic=society">ดูคลิปด้านสังคมและ SDGs ↗</a></article>
<article class="profile-work-card"><span class="profile-work-num">04</span><h3>การเสวนาระหว่างศาสนา</h3><p>สร้างความร่วมมือกับผู้นำและเครือข่ายศาสนาต่าง ๆ ผ่านการสนทนา การฝึกอบรม และเวทีนานาชาติ เพื่อเสริมความเข้าใจและความไว้วางใจ</p><a href="./external-media.html">ดูสื่อจากหน่วยงานภายนอก ↗</a></article>
<article class="profile-work-card"><span class="profile-work-num">05</span><h3>สิทธิมนุษยชน</h3><p>ต่อยอดประสบการณ์งานสันติภาพสู่การศึกษาและทำงานเชิงระบบด้านสิทธิมนุษยชน รวมถึงความร่วมมือกับคณะกรรมการสิทธิมนุษยชนแห่งชาติ</p><a href="./press.html">อ่านบทสัมภาษณ์และข่าว ↗</a></article>
<article class="profile-work-card"><span class="profile-work-num">06</span><h3>สื่อและการสื่อสารธรรมะ</h3><p>ใช้ทั้งโทรทัศน์ สื่อดิจิทัล รายการสนทนา และโซเชียลมีเดียเป็นพื้นที่สื่อสารธรรมะและประเด็นสังคมกับผู้คนหลากหลายกลุ่ม</p><a href="./library.html">เปิดคลังวิดีโอทั้งหมด ↗</a></article>
</div>
</div></section>

<section class="profile-education" id="profileEducation" aria-labelledby="profileEducationTitle"><div class="container profile-education-grid">
<div class="profile-photo-card">
<figure><img src="./assets/profile/ven-napan-leeds.webp" alt="พระมหานภันต์ในช่วงการศึกษาที่ University of Leeds" width="1200" height="801" loading="lazy" decoding="async"><figcaption>ภาพจากบทสัมภาษณ์เรื่องการศึกษาต่อที่ University of Leeds · <a href="https://hands-on.co.th/blog/review-corporate-communications-marketing-public-relations-university-of-leeds/" target="_blank" rel="noopener noreferrer">Hands On Education Consultants ↗</a></figcaption></figure>
</div>
<div>
<p class="profile-section-kicker">EDUCATION & FORMATION</p><h2 class="profile-section-title" id="profileEducationTitle">การศึกษาเพื่อเชื่อมธรรมะกับโลกปัจจุบัน</h2>
<p class="profile-copy">เส้นทางการศึกษาของพระมหานภันต์ครอบคลุมทั้งพระปริยัติธรรม การศึกษา การบริหารรัฐกิจ ภาษา การสื่อสาร สันติศึกษา และสิทธิมนุษยชน</p>
<div class="profile-edu-list">
<div class="profile-edu-row"><div class="profile-edu-year">1998</div><div><strong>B.Ed. (Secondary Education)</strong><span>Sukhothai Thammathirat Open University</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2002</div><div><strong>Pali Studies Level 9 · เปรียญธรรม 9 ประโยค</strong><span>Royal Pali Department / สำนักเรียนวัดสระเกศ</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2006</div><div><strong>B.Ed. (Non-formal Education)</strong><span>Sukhothai Thammathirat Open University</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2009</div><div><strong>Higher Diploma Programme on Promotion of Peaceful Society</strong><span>King Prajadhipok’s Institute</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2013</div><div><strong>Higher Diploma Programme on Public Administration and Public Law</strong><span>King Prajadhipok’s Institute</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2014</div><div><strong>M.A. in Career English</strong><span>Thammasat University</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2017</div><div><strong>Bachelor of Public Administration</strong><span>Sukhothai Thammathirat Open University</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2017</div><div><strong>M.A. in Corporate Communications, Marketing and Public Relations</strong><span>University of Leeds, United Kingdom · Chevening Alumni</span></div></div>
<div class="profile-edu-row"><div class="profile-edu-year">2026</div><div><strong>Master’s Programme in Human Rights and Democratisation in Asia Pacific (APMA)</strong><span>Institute of Human Rights and Peace Studies, Mahidol University · อยู่ระหว่างการศึกษาในข้อมูลที่เผยแพร่ปี 2026</span></div></div>
</div>
</div>
</div></section>

<section class="profile-timeline" id="profileTimeline" aria-labelledby="profileTimelineTitle"><div class="container">
<p class="profile-section-kicker">SELECTED MILESTONES</p><h2 class="profile-section-title" id="profileTimelineTitle">เส้นทางสำคัญของชีวิตและการทำงาน</h2>
<p class="profile-timeline-intro">คัดเลือกเหตุการณ์ที่มีแหล่งข้อมูลรองรับ เพื่อให้เห็นพัฒนาการจากการศึกษาพระธรรม สู่การทำงานพัฒนาคน สันติภาพ และความร่วมมือระดับนานาชาติ</p>
<div class="profile-timeline-list">
<div class="profile-milestone"><div class="profile-milestone-year">2543</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>อุปสมบทเป็นพระภิกษุ</strong><p>ได้รับฉายา “สนฺติภทฺโท” และสืบต่อเส้นทางการศึกษาและการเผยแผ่พระพุทธศาสนา</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2544</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>ก่อตั้งกลุ่มเพื่อชีวิตดีงาม (For Beautiful Life Group)</strong><p>เริ่มต้นงานพัฒนาคนอย่างเป็นระบบผ่านการฝึกอบรม การเรียนรู้เชิงประสบการณ์ และการพัฒนาตนบนฐานไตรสิกขา</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2545</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>สำเร็จเปรียญธรรม 9 ประโยค</strong><p>สำเร็จการศึกษาพระปริยัติธรรมระดับสูงสุดจากสำนักเรียนวัดสระเกศ</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2556</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>งานสื่อ TRUE Little Monks</strong><p>ทำหน้าที่ผู้ดำเนินรายการในโครงการสามเณรปลูกปัญญาธรรม ซึ่งรายการได้รับ Cannes Corporate &amp; Media Awards 2013</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2558</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>ก่อตั้ง IBHAP Foundation</strong><p>ขยายงานจากการพัฒนาคนสู่การประยุกต์พระพุทธศาสนากับความสุข สันติภาพ และการพัฒนาที่ยั่งยืน</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2560</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>University of Leeds</strong><p>สำเร็จ M.A. ด้าน Corporate Communications, Marketing and Public Relations และเป็น Chevening Alumni</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2561</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>รัฐสภายุโรป และ KAICIID Fellow</strong><p>กล่าวปาฐกถาในพิธีวิสาขบูชาครั้งแรกที่รัฐสภายุโรปในหัวข้อเชื่อมสันติภาพภายในกับ SDGs และได้รับคัดเลือกเป็น KAICIID Fellow รุ่นปี 2018</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2567</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>เวทีสิ่งแวดล้อมและการยอมรับจากเครือข่ายศิษย์เก่า</strong><p>มีชื่อเข้าร่วม COP16 ในบทบาทด้าน Spiritual and Faith Communities และได้รับ Chevening Alumni Award 2024 ตามชีวประวัติ ICCS 2025</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2568</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>International Conference on Cohesive Societies</strong><p>ร่วมเวที ICCS 2025 ที่สิงคโปร์ในฐานะผู้ทำงานด้านสังคมพหุวัฒนธรรม สันติภาพ และการเสวนาระหว่างศาสนา</p></div></div>
<div class="profile-milestone"><div class="profile-milestone-year">2569</div><div class="profile-milestone-dot"></div><div class="profile-milestone-copy"><strong>สิทธิมนุษยชนและ Interreligious Dialogue</strong><p>ศึกษาต่อด้าน Human Rights and Democratisation และเป็นผู้นำเสนอหลักในกิจกรรมของ World Council of Churches เรื่องการเสวนาระหว่างศาสนาผ่านมุมมองพุทธ</p></div></div>
</div>
</div></section>

<section class="profile-global" id="profileGlobal" aria-labelledby="profileGlobalTitle"><div class="container">
<div class="profile-head"><div><p class="profile-section-kicker">REGIONAL & GLOBAL ENGAGEMENT</p><h2 class="profile-section-title" id="profileGlobalTitle">จากพื้นที่ชุมชน สู่เวทีความร่วมมือระดับโลก</h2></div></div>
<div class="profile-global-grid">
<figure class="profile-feature-visual"><img src="./assets/profile/ven-napan-wcc.webp" alt="พระมหานภันต์ระหว่างเวทีเสวนาระหว่างศาสนาของ World Council of Churches" width="992" height="661" loading="lazy" decoding="async"><figcaption class="profile-feature-caption"><small>WORLD COUNCIL OF CHURCHES · 2026</small><strong>Seeing Interreligious Dialogue through a Buddhist Lens</strong><a href="https://www.oikoumene.org/news/dialogue-focuses-on-understanding-and-relations-through-a-buddhist-lens" target="_blank" rel="noopener noreferrer">ภาพ: Yakoma PGI / เปิดแหล่งต้นทาง ↗</a></figcaption></figure>
<div class="profile-global-copy">
<h3>เครือข่ายและเวทีที่เกี่ยวข้อง</h3>
<p>ประสบการณ์ของพระมหานภันต์เชื่อมตั้งแต่งานสันติภาพในพื้นที่ภาคใต้ของไทย ไปสู่การทำงานกับเครือข่ายด้านศาสนา สันติภาพ การพัฒนาที่ยั่งยืน และความร่วมมือระหว่างประเทศ</p>
<div class="profile-network-list"><span>Religions for Peace Thailand</span><span>KAICIID Fellow</span><span>World Council of Churches</span><span>PaRD</span><span>Network for Religious and Traditional Peacemakers</span><span>Buddhist Peace Network</span></div>
<p>ชีวประวัติ ICCS 2025 ระบุการมีส่วนร่วมในเวทีสำคัญ อาทิ UN Fez Plan of Action, พิธีวิสาขบูชาที่รัฐสภายุโรป, Interfaith G20 Forum, COP16 และ COP29</p>
<div class="profile-global-links"><a href="https://www.kaiciid.org/who-we-are/fellows/ven-napan-thawornbanjob" target="_blank" rel="noopener noreferrer">KAICIID Profile ↗</a><a href="https://www.oikoumene.org/news/dialogue-focuses-on-understanding-and-relations-through-a-buddhist-lens" target="_blank" rel="noopener noreferrer">WCC Feature ↗</a><a href="./external-media.html">สื่อภายนอกในคลัง ↗</a></div>
</div>
</div>
</div></section>

<section class="profile-human-rights" aria-labelledby="profileHumanTitle"><div class="container profile-human-grid">
<div class="profile-human-copy"><p class="profile-section-kicker">PEACE & HUMAN RIGHTS</p><h2 class="profile-section-title" id="profileHumanTitle">จากงานสันติภาพ สู่สิทธิมนุษยชนเชิงระบบ</h2>
<p class="profile-copy">หลังทำงานกับชุมชนที่ได้รับผลกระทบจากความรุนแรงมาอย่างต่อเนื่อง พระมหานภันต์ต่อยอดประสบการณ์เข้าสู่การศึกษาด้านสิทธิมนุษยชน โดย Global Campus of Human Rights ระบุว่าท่านเข้าศึกษาในหลักสูตร APMA ที่สถาบันสิทธิมนุษยชนและสันติศึกษา มหาวิทยาลัยมหิดล</p>
<p class="profile-copy">หัวข้อวิทยานิพนธ์มุ่งศึกษาการเสริมสร้างความร่วมมือระหว่างองค์กรสิทธิมนุษยชนกับสถาบันพระพุทธศาสนา และการนำการศึกษาด้านสิทธิมนุษยชนเข้าสู่เครือข่ายศาสนา</p>
<div class="profile-global-links"><a href="https://www.gchumanrights.org/gc-news/from-temple-to-classroom-how-a-buddhist-monk-is-bridging-faith-and-human-rights/" target="_blank" rel="noopener noreferrer">อ่านบทสัมภาษณ์ Global Campus ↗</a><a href="./press.html">ดูข่าวสิทธิมนุษยชนในคลัง ↗</a></div>
</div>
<figure class="profile-human-image"><img src="./assets/profile/ven-napan-human-rights.webp" alt="พระมหานภันต์ในบริบทงานสันติภาพและสิทธิมนุษยชน" width="1024" height="683" loading="lazy" decoding="async"><figcaption>ภาพจาก Global Campus of Human Rights · เครดิตภาพ PaRD/GIZ · <a href="https://www.gchumanrights.org/gc-news/from-temple-to-classroom-how-a-buddhist-monk-is-bridging-faith-and-human-rights/" target="_blank" rel="noopener noreferrer">แหล่งต้นทาง ↗</a></figcaption></figure>
</div></section>

<section class="profile-media" id="profileMedia" aria-labelledby="profileMediaTitle"><div class="container">
<div class="profile-head"><div><p class="profile-section-kicker">WATCH & EXPLORE</p><h2 class="profile-section-title" id="profileMediaTitle">จากประวัติ สู่คลังสื่อที่ค้นต่อได้</h2><p>หน้าโปรไฟล์เชื่อมเข้ากับวิดีโอ ข่าว คำคม และคลังพิเศษที่มีอยู่ใน PMNapan Library เพื่อให้สำรวจงานของพระมหานภันต์ตามประเด็นได้ต่อเนื่อง</p></div></div>
<div class="profile-media-grid">
<div class="profile-video-feature"><div class="profile-video-frame"><iframe src="https://www.youtube-nocookie.com/embed/z1uFrp7a294" title="Seeing Interreligious Dialogue through a Buddhist Lens — World Council of Churches" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div><div class="profile-video-copy"><small>FEATURED RECORDING · WCC 2026</small><h3>Seeing Interreligious Dialogue through a Buddhist Lens</h3><p>บันทึกกิจกรรม World Council of Churches ซึ่งพระมหานภันต์เป็นผู้นำเสนอหลักด้านการเสวนาระหว่างศาสนาผ่านมุมมองพุทธ</p></div></div>
<div class="profile-related-links">
<a class="profile-related-card" href="./library.html?category=%E0%B8%AD%E0%B8%B2%E0%B8%AA%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1"><span class="profile-related-thumb"><img src="./assets/episode-stills/bjy001UX7Mc.jpg" alt="" loading="lazy"></span><span><strong>อาสาหาธรรม</strong><span>รายการสนทนาธรรมและคำถามชีวิตในคลังวิดีโอ</span></span><span class="profile-related-arrow">↗</span></a>
<a class="profile-related-card" href="./quotes.html"><span class="profile-related-thumb"><img src="./assets/quotes/local-34e1a4e2cb9bd27cdde2.jpg" alt="" loading="lazy"></span><span><strong>คำคมและข้อคิด</strong><span>ภาพคำคมจากคลังที่ผู้ดูแลจัดเตรียมและตรวจทาน</span></span><span class="profile-related-arrow">↗</span></a>
<a class="profile-related-card" href="./press.html"><span class="profile-related-thumb"><img src="./assets/profile/ven-napan-interfaith.webp" alt="" loading="lazy"></span><span><strong>ข่าว บทสัมภาษณ์ และผลงาน</strong><span>ติดตามกิจกรรมและบทบาทจากแหล่งเผยแพร่ต่าง ๆ</span></span><span class="profile-related-arrow">↗</span></a>
<a class="profile-related-card" href="./four-ps.html"><span class="profile-related-thumb"><img src="./assets/archive/four-ps-original.webp" alt="" loading="lazy"></span><span><strong>ปรากฏการณ์ 4 พส.</strong><span>คลังพิเศษ พ.ศ. 2564–2565 พร้อมเส้นเวลา ข่าว และคลิป</span></span><span class="profile-related-arrow">↗</span></a>
</div>
</div>
</div></section>

<section class="profile-dynamic" aria-labelledby="profileVideosTitle"><div class="container">
<div class="heading-row"><div><p class="profile-section-kicker">LATEST FROM THE ARCHIVE</p><h2 id="profileVideosTitle">วิดีโอ “อาสาหาธรรม” ล่าสุดในคลัง</h2></div><a class="text-link" href="./library.html?category=%E0%B8%AD%E0%B8%B2%E0%B8%AA%E0%B8%B2%E0%B8%AB%E0%B8%B2%E0%B8%98%E0%B8%A3%E0%B8%A3%E0%B8%A1">ดูทั้งหมด ↗</a></div>
<div class="video-grid" id="profileVideoGrid"><div class="loading"><span class="spinner"></span>กำลังโหลดวิดีโอ...</div></div>
</div></section>

<section class="profile-dynamic" aria-labelledby="profilePressTitle"><div class="container">
<div class="heading-row"><div><p class="profile-section-kicker">SELECTED READING</p><h2 id="profilePressTitle">บทสัมภาษณ์และผลงานที่ช่วยทำความรู้จักท่าน</h2></div><a class="text-link" href="./press.html">ดูข่าวและผลงานทั้งหมด ↗</a></div>
<div class="press-grid" id="profilePressGrid"><div class="loading"><span class="spinner"></span>กำลังโหลดบทความ...</div></div>
</div></section>

<section class="profile-dynamic" aria-labelledby="profileQuotesTitle"><div class="container">
<div class="heading-row"><div><p class="profile-section-kicker">WORDS & IDEAS</p><h2 id="profileQuotesTitle">แนวคิดที่สะท้อนงานของพระมหานภันต์</h2></div><a class="text-link" href="./quotes.html">ดูคำคมทั้งหมด ↗</a></div>
<div class="quote-grid" id="profileQuoteGrid"><div class="loading"><span class="spinner"></span>กำลังโหลดคำคม...</div></div>
</div></section>

<section class="profile-sources" id="profileSources" aria-labelledby="profileSourcesTitle"><div class="container">
<div class="profile-head"><div><p class="profile-section-kicker">PRIMARY & INSTITUTIONAL SOURCES</p><h2 class="profile-section-title" id="profileSourcesTitle">แหล่งอ้างอิงหลักของประวัติ</h2><p>ข้อมูลในหน้านี้คัดจากประวัติและเอกสารที่เผยแพร่โดยวัด/มูลนิธิ องค์กรการศึกษา และเครือข่ายระหว่างประเทศที่ทำงานร่วมกับพระมหานภันต์</p></div></div>
<div class="profile-sources-grid">
<a class="profile-source" href="https://ibhap.org/%E0%B8%88%E0%B8%B2%E0%B8%81%E0%B8%AA%E0%B8%B2%E0%B8%A1%E0%B9%80%E0%B8%93%E0%B8%A3%E0%B8%A0%E0%B8%B2%E0%B8%84%E0%B8%A4%E0%B8%94%E0%B8%B9%E0%B8%A3%E0%B9%89%E0%B8%AD%E0%B8%99-%E0%B8%AA%E0%B8%B9/" target="_blank" rel="noopener noreferrer"><small>IBHAP FOUNDATION</small><strong>จากสามเณรภาคฤดูร้อน… สู่การอุปสมบทพรรษาที่ 25</strong><span>เปิดแหล่งต้นทาง ↗</span></a>
<a class="profile-source" href="https://vesak2024.mcu.ac.th/wp-content/uploads/2024/05/%E0%B8%AB%E0%B8%99%E0%B8%B1%E0%B8%87%E0%B8%AA%E0%B8%B7%E0%B8%AD%E0%B8%A7%E0%B8%B4%E0%B8%AA%E0%B8%B2%E0%B8%82-67_12-%E0%B8%9E%E0%B8%84.-67.pdf" target="_blank" rel="noopener noreferrer"><small>MCU · VESAK 2024</small><strong>Curriculum Vitae และผลงานระดับภูมิภาค/นานาชาติ</strong><span>เปิดเอกสาร ↗</span></a>
<a class="profile-source" href="https://www.kaiciid.org/who-we-are/fellows/ven-napan-thawornbanjob" target="_blank" rel="noopener noreferrer"><small>KAICIID</small><strong>Ven. Napan Thawornbanjob · Fellow Profile</strong><span>เปิดแหล่งต้นทาง ↗</span></a>
<a class="profile-source" href="https://www.gchumanrights.org/gc-news/from-temple-to-classroom-how-a-buddhist-monk-is-bridging-faith-and-human-rights/" target="_blank" rel="noopener noreferrer"><small>GLOBAL CAMPUS OF HUMAN RIGHTS</small><strong>Faith, peacebuilding and human rights</strong><span>เปิดแหล่งต้นทาง ↗</span></a>
<a class="profile-source" href="https://www.oikoumene.org/news/dialogue-focuses-on-understanding-and-relations-through-a-buddhist-lens" target="_blank" rel="noopener noreferrer"><small>WORLD COUNCIL OF CHURCHES</small><strong>Interreligious Dialogue through a Buddhist Lens</strong><span>เปิดแหล่งต้นทาง ↗</span></a>
<a class="profile-source" href="https://wp-uploads.g20interfaith.org/app/uploads/2020/09/21155121/ICCS2025_booklet76.pdf" target="_blank" rel="noopener noreferrer"><small>ICCS 2025</small><strong>Speaker Biography · International Conference on Cohesive Societies</strong><span>เปิดเอกสาร ↗</span></a>
</div>
<p class="profile-source-note">หน้าโปรไฟล์เลือกใช้เฉพาะข้อมูลที่มีแหล่งเผยแพร่รองรับ และหลีกเลี่ยงรายละเอียดที่ยังพบข้อมูลไม่สอดคล้องกันระหว่างแหล่งอ้างอิง</p>
</div></section>

<section class="profile-archive-cta"><div class="container"><div class="profile-archive-cta-inner">
<div><h2>สำรวจผลงานใน PMNapan Library ต่อ</h2><p>ปัจจุบันคลังมี <strong id="profileVideoTotal">—</strong> วิดีโอ · <strong id="profilePressTotal">—</strong> ข่าว/บทสัมภาษณ์ · <strong id="profileQuoteTotal">—</strong> ภาพคำคม และคลังพิเศษที่เชื่อมโยงกับงานของพระมหานภันต์</p></div>
<a href="./library.html">เปิดคลังทั้งหมด ↗</a>
</div></div></section>'''


EN_PAGE_META={
 'home':('PMNapan Library Dhamma Archive | Ven. Napan Santibhaddo','A source-linked archive of Dhamma videos, quotes, news and interviews related to Ven. Napan Santibhaddo.'),
 'profile':('Ven. Napan Santibhaddo | Biography, Education & Work','Biography, education, peacebuilding, human rights, SDGs and international engagement of Ven. Napan Santibhaddo.'),
 'categories':('Dhamma Series | PMNapan Library','Browse Dhamma programs and video collections by category.'),
 'featured':('Featured Dhamma Videos | PMNapan Library','Selected Dhamma programs and archived videos linked to original publishers.'),
 'shorts':('Dhamma Shorts | PMNapan Library','Short-form Dhamma videos linked to original publishing sources.'),
 'fourps':('The 4 Monks Phenomenon | Timeline, News & Videos','A special archive of the 2021–2022 Four Monks online Dhamma phenomenon, including Ven. Napan’s role.'),
 'quotes':('Dhamma Quotes | PMNapan Library','Source-backed Dhamma quote images and searchable transcriptions.'),
 'press':('News, Interviews & Work | Ven. Napan','News, interviews, activities and published work related to Ven. Napan Santibhaddo.'),
 'external-media':('External Media | Ven. Napan','Programs and media from external organizations with links to original sources.'),
 'library':('Video Archive | Ven. Napan Santibhaddo','Search the video archive by title, series, year, platform and curated topic.'),
 'saved':('Saved Videos | PMNapan Library','Videos saved in this browser for later viewing.'),
 'category':('Video Series | PMNapan Library','Browse videos from a selected Dhamma series.'),
 'video':('Video Details | PMNapan Library','Video details with links to the original publisher.'),
 'about':('About the Archive & Sources | PMNapan Library','About PMNapan Library, its sources, citation practices, search scope and privacy.'),
 'notfound':('Page Not Found | PMNapan Library','The requested page could not be found in PMNapan Library.')
}

pages=[
 ('index.html','home',name,'สารบัญวิดีโอพระมหานภันต์ สนฺติภทฺโท และงานสื่อที่เกี่ยวข้อง',home),
 ('ven-napan.html','profile','ประวัติพระมหานภันต์ สนฺติภทฺโท | '+name,'ประวัติ การศึกษา งานสันติภาพ สิทธิมนุษยชน SDGs และบทบาทระดับนานาชาติของพระมหานภันต์',profile),
 ('categories.html','categories','หมวดรายการ | '+name,'หมวดรายการทั้งหมดจากทะเบียนวิดีโอต้นฉบับ',categories),
 ('featured.html','featured','คลิปจากรายการ | '+name,'คลิปจากรายการพร้อมภาพปกจากแหล่งเผยแพร่จริง',featured),
 ('shorts.html','shorts','ธรรมะคลิปสั้น | '+name,'คลิปสั้นต้นฉบับจากบัญชี TikTok @domskyline21 ที่ตรวจสอบแหล่งและภาพปก',shorts),
 ('four-ps.html','fourps','ปรากฏการณ์ 4 พส. | '+name,'เส้นเวลา ข่าว คลิป และเหตุการณ์ที่เกี่ยวข้องกับพระมหานภันต์',fourps),
 ('quotes.html','quotes','คำคมธรรมะ | '+name,'รวบรวมภาพคำคมธรรมะของพระมหานภันต์จากคลังภาพที่ผู้ดูแลจัดเตรียมและโพสต์ต้นฉบับที่ตรวจสอบได้',quotes),
 ('press.html','press','ข่าว บทสัมภาษณ์ และผลงาน | '+name,'คลังข่าว บทสัมภาษณ์ ประวัติ และผลงานย้อนหลังของพระมหานภันต์ พร้อมอ้างอิงแหล่งเผยแพร่ต้นฉบับ',press),
 ('external-media.html','external-media','สื่อจากแหล่งภายนอก | '+name,'รวมสื่อจากหน่วยงานภายนอก พร้อมลิงก์ต้นทางและข้อมูลประกอบสำหรับการค้นคว้า',external_media),
 ('library.html','library','คลังวิดีโอ | '+name,'ค้นหาและเลือกชมวิดีโอต้นฉบับ แยกหมวด ปี และช่องทาง',library),
 ('saved.html','saved','คลิปที่บันทึกไว้ | '+name,'รายการวิดีโอที่บันทึกไว้ในเบราว์เซอร์',saved),
 ('category.html','category','หมวดรายการ | '+name,'รายการคลิปตามหมวดหมู่จากทะเบียนจริง',category),
 ('video.html','video','รายละเอียดวิดีโอ | '+name,'รายละเอียดคลิปและลิงก์วิดีโอของผู้เผยแพร่ต้นฉบับ',video),
 ('about.html','about','แหล่งข้อมูล | '+name,'ข้อมูลแหล่งเผยแพร่และหลักเกณฑ์ของคลังวิดีโอ',about),
 ('404.html','notfound','ไม่พบหน้าที่ต้องการ | '+name,'ไม่พบหน้าที่ต้องการใน PMNapan Library',notfound)
]
en_dir=root/'en'
en_dir.mkdir(exist_ok=True)
for filename,key,title,description,body in pages:
 (root/filename).write_text(shell(key,title,description,body,'th'),encoding='utf-8')
 en_title,en_description=EN_PAGE_META[key]
 (en_dir/filename).write_text(shell(key,en_title,en_description,body,'en'),encoding='utf-8')
 print("GENERATED",filename,"+ en/"+filename)
