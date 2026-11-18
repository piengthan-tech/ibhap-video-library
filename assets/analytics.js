(() => {
  'use strict';
  const MEASUREMENT_ID = 'G-FE674RJ7BN';
  const CONSENT_KEY = 'pmnapan_ga4_consent_v1';
  let enabled = false, configured = false;

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('consent', 'default', {
    analytics_storage: 'denied', ad_storage: 'denied',
    ad_user_data: 'denied', ad_personalization: 'denied'
  });

  function loadChoice() {
    try { const c = localStorage.getItem(CONSENT_KEY); return c === 'granted' || c === 'denied' ? c : null; }
    catch (_) { return null; }
  }
  function saveChoice(c) { try { localStorage.setItem(CONSENT_KEY, c); } catch (_) {} }
  function clearOwnCookies() {
    const names = document.cookie.split(';').map(x => x.trim().split('=')[0]);
    for (const name of names) {
      if (!name.startsWith('pmnapan_ga')) continue;
      for (const path of ['/pmnapan-library/', '/']) {
        document.cookie = name + '=;Max-Age=0;path=' + path + ';SameSite=Lax;Secure';
        document.cookie = name + '=;Max-Age=0;path=' + path + ';domain=' + location.hostname + ';SameSite=Lax;Secure';
      }
    }
  }
  function activate() {
    if (enabled) return;
    enabled = true;
    window['ga-disable-' + MEASUREMENT_ID] = false;
    window.gtag('consent', 'update', {
      analytics_storage:'granted',ad_storage:'denied',
      ad_user_data:'denied',ad_personalization:'denied'
    });
    if (configured) return;
    configured = true;
    window.gtag('js', new Date());
    window.gtag('config', MEASUREMENT_ID, {
      send_page_view:true,allow_google_signals:false,
      allow_ad_personalization_signals:false,
      cookie_prefix:'pmnapan',cookie_path:'/pmnapan-library/',
      cookie_expires:60*60*24*90
    });
    const googleTag = document.createElement('script');
    googleTag.id = 'pmnapan-google-tag';
    googleTag.async = true;
    googleTag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(MEASUREMENT_ID);
    document.head.appendChild(googleTag);
  }
  function deactivate() {
    enabled = false;
    window['ga-disable-' + MEASUREMENT_ID] = true;
    window.gtag('consent', 'update', {
      analytics_storage:'denied',ad_storage:'denied',
      ad_user_data:'denied',ad_personalization:'denied'
    });
    clearOwnCookies();
  }
  function initialize() {
    const banner = document.createElement('section');
    banner.id = 'analyticsConsentBanner';
    banner.className = 'analytics-consent-banner';
    banner.setAttribute('aria-label','การตั้งค่าสถิติผู้เข้าชม');
    banner.hidden = true;
    banner.innerHTML = [
      '<div class="analytics-consent-copy"><strong>การเก็บสถิติผู้เข้าชม</strong>',
      '<p>เราใช้ Google Analytics เพื่อวัดจำนวนผู้เข้าชมและพัฒนาเว็บไซต์ โดยเริ่มเก็บข้อมูลเมื่อคุณยินยอมเท่านั้น ไม่ใช้เพื่อโฆษณา ',
      '<a href="./about.html#analytics-privacy">รายละเอียด</a></p></div>',
      '<div class="analytics-consent-actions">',
      '<button type="button" id="analyticsReject" class="analytics-consent-decline">ไม่ยินยอม</button>',
      '<button type="button" id="analyticsAccept" class="analytics-consent-accept">ยินยอม</button>',
      '</div>'
    ].join('');
    document.body.appendChild(banner);

    function showBanner() { banner.hidden = false; }
    function hideBanner() { banner.hidden = true; }
    function choose(c) {
      saveChoice(c);
      if (c === 'granted') activate(); else deactivate();
      hideBanner();
    }
    banner.querySelector('#analyticsAccept').addEventListener('click', () => choose('granted'));
    banner.querySelector('#analyticsReject').addEventListener('click', () => choose('denied'));
    const prefs = document.getElementById('analyticsPreferences');
    if (prefs) prefs.addEventListener('click', showBanner);
    const saved = loadChoice();
    if (saved === 'granted') activate();
    else if (saved !== 'denied') showBanner();

    document.addEventListener('click', event => {
      if (!enabled || typeof window.gtag !== 'function') return;
      const link = event.target instanceof Element ? event.target.closest('a[href]') : null;
      if (!link) return;
      let u;
      try { u = new URL(link.href, location.href); } catch (_) { return; }
      if (!['http:', 'https:'].includes(u.protocol) || u.hostname === location.hostname) return;
      let type = 'other';
      if (/(^|\.)youtube\.com$|(^|\.)youtu\.be$|(^|\.)tiktok\.com$/.test(u.hostname)) type = 'video';
      else if (/(^|\.)facebook\.com$|(^|\.)fb\.watch$/.test(u.hostname)) type = 'social_media';
      else if (document.body.dataset.page === 'press') type = 'article';
      window.gtag('event','archive_outbound_click',{
        destination_type:type,destination_host:u.hostname,
        source_section:document.body.dataset.page||'unknown'
      });
    },true);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded',initialize,{once:true});
  } else initialize();
})();