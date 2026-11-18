#!/usr/bin/env python3
"""Build a private browser-based review packet for one subtitle draft."""
from __future__ import annotations

import argparse, html, json, re
from pathlib import Path
from urllib.parse import urlencode

ROOT=Path(__file__).resolve().parents[1]
VIDEOS=ROOT/"data"/"videos.json"
TIME_RE=re.compile(r"(?:(\d+):)?(\d{2}):(\d{2})[,.](\d{3})\s*-->\s*(?:(\d+):)?(\d{2}):(\d{2})[,.](\d{3})")

def sec(h,m,s,ms): return int(h or 0)*3600+int(m)*60+int(s)+int(ms)/1000

def parse_srt(path:Path):
    raw=path.read_text("utf-8-sig")
    blocks=re.split(r"\n\s*\n",raw.strip())
    cues=[]
    for block in blocks:
        lines=block.splitlines()
        if len(lines)<2: continue
        idx=0
        if lines[0].strip().isdigit(): idx=1
        if idx>=len(lines): continue
        mt=TIME_RE.match(lines[idx].strip())
        if not mt: continue
        g=mt.groups()
        start=sec(g[0],g[1],g[2],g[3]); end=sec(g[4],g[5],g[6],g[7])
        text=" ".join(x.strip() for x in lines[idx+1:] if x.strip())
        text=re.sub(r"<[^>]+>","",text)
        text=html.unescape(text).strip()
        if text:cues.append({"start":start,"end":end,"text":text})
    return cues

def fmt(t):
    h=int(t//3600);m=int((t%3600)//60);s=int(t%60)
    return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def main():
    ap=argparse.ArgumentParser(description="สร้าง HTML Review Packet จาก SRT Draft")
    ap.add_argument("--key",required=True)
    ap.add_argument("--file",required=True,type=Path)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()
    vids={x["key"]:x for x in json.load(open(VIDEOS,encoding="utf-8"))["items"]}
    v=vids.get(args.key)
    if not v: raise SystemExit("ไม่พบ video key ในทะเบียน")
    cues=parse_srt(args.file)
    if not cues: raise SystemExit("ไม่พบ subtitle cue ที่อ่านได้")
    out=args.out or (ROOT/".transcript-drafts"/"review-packets"/(v["video_id"]+".html"))
    out.parent.mkdir(parents=True,exist_ok=True)

    rows=[]
    for i,c in enumerate(cues,1):
        ts=int(c["start"])
        url=v["url"]+("&" if "?" in v["url"] else "?")+urlencode({"t":ts})
        rows.append(f'''<article class="cue" data-text="{html.escape(c["text"].lower(),quote=True)}">
<label><input type="checkbox" data-cue="{i}"><span class="checkmark">ตรวจแล้ว</span></label>
<a class="time" href="{html.escape(url,quote=True)}" target="_blank" rel="noopener">{fmt(c["start"])}</a>
<p>{html.escape(c["text"])}</p>
<button type="button" data-copy="{html.escape(c["text"],quote=True)}">คัดลอก</button>
</article>''')
    page=f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Transcript Review · {html.escape(v["title"])}</title>
<style>
:root{{--ink:#183b56;--muted:#6b8294;--line:#dbe7ef;--bg:#f5f9fc;--accent:#fca311;--blue:#0e5b8a}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);font-family:system-ui,-apple-system,"Noto Sans Thai",sans-serif;color:var(--ink)}}main{{max-width:1050px;margin:auto;padding:28px 18px 80px}}
header{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px;position:sticky;top:8px;z-index:4;box-shadow:0 8px 25px rgba(16,64,96,.08)}}
.kicker{{font-size:12px;letter-spacing:.08em;color:#6c879a;font-weight:700}}h1{{font-size:22px;line-height:1.5;margin:5px 0 8px}}.meta{{display:flex;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:13px}}
.warning{{margin:14px 0 0;padding:10px 12px;background:#fff7e8;border-left:4px solid var(--accent);font-size:13px;line-height:1.7}}
.controls{{display:grid;grid-template-columns:1fr auto;gap:10px;margin-top:14px}}input[type=search]{{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:9px;font-size:14px}}.progress{{padding:9px 12px;border-radius:9px;background:#edf5fa;color:#325e7b;font-weight:700;font-size:13px}}
.cues{{display:grid;gap:9px;margin-top:18px}}.cue{{display:grid;grid-template-columns:90px 70px minmax(0,1fr) auto;gap:12px;align-items:start;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px}}
.cue.reviewed{{opacity:.58;background:#f8fafb}}.cue label{{font-size:11px;color:var(--muted);display:flex;gap:5px;align-items:center}}.time{{color:var(--blue);font-weight:750;text-decoration:none;font-variant-numeric:tabular-nums}}.cue p{{margin:0;line-height:1.75;overflow-wrap:anywhere}}button{{border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 9px;color:#3f6178;cursor:pointer}}
.hidden{{display:none!important}}
@media(max-width:700px){{header{{position:static}}.cue{{grid-template-columns:75px 1fr}}.cue label{{grid-column:1}}.time{{grid-column:2}}.cue p{{grid-column:1/-1}}.cue button{{grid-column:1/-1;justify-self:start}}.controls{{grid-template-columns:1fr}}}}
</style></head><body><main><header>
<div class="kicker">PRIVATE EDITORIAL REVIEW · NOT PUBLIC</div><h1>{html.escape(v["title"])}</h1>
<div class="meta"><span>{len(cues):,} cues</span><span>{v.get("minutes","")} นาที</span><a href="{html.escape(v["url"],quote=True)}" target="_blank" rel="noopener">เปิดวิดีโอต้นฉบับ ↗</a></div>
<div class="warning">ข้อความนี้เป็น Draft subtitle และยังไม่ถือเป็นคำพูดที่ตรวจสอบแล้ว การติ๊ก “ตรวจแล้ว” เป็นเพียงสถานะใน browser ของเครื่องนี้ ต้องตรวจเทียบกับเสียง/วิดีโอต้นฉบับก่อนนำเข้าเป็น verified</div>
<div class="controls"><input id="q" type="search" placeholder="ค้นคำใน Draft..."><div class="progress" id="progress">0 / {len(cues):,} cues</div></div>
</header><section class="cues">{''.join(rows)}</section></main>
<script>
const KEY='pmnapan-review-{v["video_id"]}-v1';
const saved=new Set(JSON.parse(localStorage.getItem(KEY)||'[]'));
const boxes=[...document.querySelectorAll('[data-cue]')];
function paint(){{
 boxes.forEach(b=>{{b.checked=saved.has(b.dataset.cue);b.closest('.cue').classList.toggle('reviewed',b.checked)}});
 document.querySelector('#progress').textContent=saved.size.toLocaleString('th-TH')+' / {len(cues):,} cues';
 localStorage.setItem(KEY,JSON.stringify([...saved]));
}}
boxes.forEach(b=>b.addEventListener('change',()=>{{b.checked?saved.add(b.dataset.cue):saved.delete(b.dataset.cue);paint()}}));
document.querySelector('#q').addEventListener('input',e=>{{const q=e.target.value.trim().toLowerCase();document.querySelectorAll('.cue').forEach(c=>c.classList.toggle('hidden',q&&!c.dataset.text.includes(q)))}})
document.querySelectorAll('[data-copy]').forEach(b=>b.addEventListener('click',async()=>{{await navigator.clipboard.writeText(b.dataset.copy);const old=b.textContent;b.textContent='คัดลอกแล้ว';setTimeout(()=>b.textContent=old,1000)}}));
paint();
</script></body></html>'''
    out.write_text(page,encoding="utf-8")
    print(f"Packet: {out}")
    print(f"Cues: {len(cues)}")
if __name__=="__main__": main()
