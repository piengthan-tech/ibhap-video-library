'use strict';
(() => {
  const isEnglish = document.documentElement.lang.toLowerCase().startsWith('en');
  const archiveRoot = '/pmnapan-library/';
  const lastSegment = location.pathname.split('/').filter(Boolean).pop() || '';
  const pageFile = /\.html$/i.test(lastSegment) ? lastSegment : 'index.html';

  function setSwitchLinks() {
    document.querySelectorAll('[data-lang-choice]').forEach(link => {
      const lang = link.dataset.langChoice;
      const target = lang === 'en'
        ? archiveRoot + 'en/' + pageFile
        : archiveRoot + pageFile;
      link.href = target + location.search + location.hash;
      const active = (lang === 'en') === isEnglish;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  }

  if (!isEnglish) {
    setSwitchLinks();
    return;
  }

  let dictionary = {};
  const knownPages = new Set([
    'index.html','ven-napan.html','categories.html','featured.html','shorts.html',
    'quotes.html','press.html','external-media.html','library.html','saved.html',
    'four-ps.html','about.html','category.html','video.html','404.html'
  ]);

  function translateValue(value) {
    const trimmed = String(value || '').trim();
    if (dictionary[trimmed]) return dictionary[trimmed];
    let m;
    if ((m = trimmed.match(/^(\d[\d,]*) คลิป( ↗)?$/))) return m[1] + ' videos' + (m[2] || '');
    if ((m = trimmed.match(/^(\d[\d,]*) ภาพ( ↗)?$/))) return m[1] + ' images' + (m[2] || '');
    if ((m = trimmed.match(/^(\d[\d,]*) นาที$/))) return m[1] + ' min';
    if ((m = trimmed.match(/^พบ (\d[\d,]*) คลิป$/))) return 'Found ' + m[1] + ' videos';
    if ((m = trimmed.match(/^พบ (\d[\d,]*) ภาพคำคมธรรมะ$/))) return 'Found ' + m[1] + ' Dhamma quote images';
    if ((m = trimmed.match(/^บันทึกไว้ (\d[\d,]*) คลิปในเบราว์เซอร์นี้$/))) return m[1] + ' videos saved in this browser';
    if ((m = trimmed.match(/^พบ (\d[\d,]*) จาก (\d[\d,]*) รายการ$/))) return 'Showing ' + m[1] + ' of ' + m[2] + ' items';
    if ((m = trimmed.match(/^ค้นหาข้อความได้ (\d[\d,]*) จาก (\d[\d,]*) ภาพ โดยเปิดดูภาพทั้งหมดได้ตามปกติ$/))) return 'Searchable text is available for ' + m[1] + ' of ' + m[2] + ' images; all images remain viewable.';
    if ((m = trimmed.match(/^(\d[\d,]*) หมวดวิดีโอ · 1 หมวดคำคมธรรมะ · 1 หมวดพิเศษ$/))) return m[1] + ' video series · 1 quote collection · 1 special collection';
    if ((m = trimmed.match(/^พ\.ศ\. (\d{4})$/))) return String(Number(m[1]) - 543);
    if ((m = trimmed.match(/^แสดง (\d+) จาก (\d+) เหตุการณ์ · (\d+) แหล่งอ้างอิง$/))) return 'Showing ' + m[1] + ' of ' + m[2] + ' events · ' + m[3] + ' sources';
    if ((m = trimmed.match(/^(\d+) ข่าว\/บทความ$/))) return m[1] + ' news/articles';
    if ((m = trimmed.match(/^(\d+) ข่าว\/บทความ · (\d+) คลิป$/))) return m[1] + ' news/articles · ' + m[2] + ' videos';
    if ((m = trimmed.match(/^ข่าว \/ บทความ · (.+)$/))) return 'News / article · ' + m[1];
    if ((m = trimmed.match(/^คลิปข่าวและรายการ · (.+)$/))) return 'News clip / program · ' + m[1];
    if ((m = trimmed.match(/^รายงานวิเคราะห์ · (.+)$/))) return 'Analytical report · ' + m[1];
    if ((m = trimmed.match(/^ภาพประกอบจากข่าว · (.+)$/))) return 'News image · ' + m[1];
    if ((m = trimmed.match(/^ภาพประกอบจาก (.+)$/))) return 'Image from ' + m[1];
    if ((m = trimmed.match(/^ดูเพิ่มเติมอีก (\d+) รายการ/))) return 'Show ' + m[1] + ' more items';
    return null;
  }

  function translateTextNode(node) {
    if (!node || node.nodeType !== Node.TEXT_NODE) return;
    const raw = node.nodeValue || '';
    const translated = translateValue(raw);
    if (!translated) return;
    const lead = raw.match(/^\s*/)?.[0] || '';
    const trail = raw.match(/\s*$/)?.[0] || '';
    node.nodeValue = lead + translated + trail;
  }

  function translateElement(el) {
    if (!(el instanceof Element)) return;
    for (const attr of ['aria-label','placeholder','title']) {
      if (!el.hasAttribute(attr)) continue;
      const translated = translateValue(el.getAttribute(attr));
      if (translated) el.setAttribute(attr, translated);
    }
    if (el.tagName === 'INPUT' && ['button','submit'].includes((el.type || '').toLowerCase())) {
      const translated = translateValue(el.value);
      if (translated) el.value = translated;
    }
    if (el.tagName === 'A') {
      const raw = el.getAttribute('href') || '';
      const match = raw.match(/^\.\/([^/?#]+\.html)([?#].*)?$/);
      if (match && knownPages.has(match[1]) && !raw.startsWith('./en/')) {
        el.setAttribute('href', './en/' + match[1] + (match[2] || ''));
      }
    }
  }

  function walk(root) {
    if (!root) return;
    if (root.nodeType === Node.TEXT_NODE) {
      translateTextNode(root);
      return;
    }
    if (!(root instanceof Element) && root !== document.body) return;
    if (root instanceof Element) translateElement(root);
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT);
    let node;
    while ((node = walker.nextNode())) {
      if (node.nodeType === Node.TEXT_NODE) translateTextNode(node);
      else translateElement(node);
    }
  }

  fetch('./data/i18n-en.json', {cache:'no-cache'})
    .then(r => {
      if (!r.ok) throw new Error('i18n HTTP ' + r.status);
      return r.json();
    })
    .then(data => {
      dictionary = data || {};
      walk(document.body);
      setSwitchLinks();
      const observer = new MutationObserver(records => {
        for (const record of records) {
          for (const node of record.addedNodes) walk(node);
        }
        setSwitchLinks();
      });
      observer.observe(document.body, {subtree:true, childList:true});
    })
    .catch(err => {
      console.warn('English translation catalog unavailable', err);
      setSwitchLinks();
    });
})();
