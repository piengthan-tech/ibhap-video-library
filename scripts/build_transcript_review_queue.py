#!/usr/bin/env python3
"""Build a private transcript review queue from catalog + caption inventory.

The output stays under .transcript-drafts/ and is not public site data.
"""
from __future__ import annotations

import argparse, json
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
VIDEOS=ROOT/"data"/"videos.json"
DEFAULT_INV=ROOT/".transcript-drafts"/"caption-inventory.json"
DEFAULT_OUT=ROOT/".transcript-drafts"/"review-queue.json"
STATUS_RANK={"publisher_subtitle":0,"youtube_auto_caption":1,"none":3,"blocked_by_youtube":4,"error":5}

def main():
    ap=argparse.ArgumentParser(description="สร้างคิวตรวจ Transcript แบบ private")
    ap.add_argument("--category",default="อาสาหาธรรม")
    ap.add_argument("--inventory",type=Path,default=DEFAULT_INV)
    ap.add_argument("--out",type=Path,default=DEFAULT_OUT)
    args=ap.parse_args()

    videos=json.load(open(VIDEOS,encoding="utf-8"))["items"]
    inv={}
    if args.inventory.exists():
        inv={x["key"]:x for x in json.load(open(args.inventory,encoding="utf-8")).get("items",[])}
    rows=[]
    for x in videos:
        if x.get("category")!=args.category or x.get("platform")!="YouTube":
            continue
        status=inv.get(x["key"],{}).get("caption_kind","unknown")
        draft_dir=ROOT/".transcript-drafts"/"captions"
        local=[]
        if draft_dir.exists():
            local=[str(p.relative_to(ROOT)) for p in draft_dir.glob(x["video_id"]+"*.srt")]
        rows.append({
            "key":x["key"],
            "video_id":x["video_id"],
            "title":x["title"],
            "published_at":x.get("published_at",""),
            "minutes":x.get("minutes"),
            "source_url":x["url"],
            "caption_status":status,
            "local_draft_files":local,
            "review_status":"not_reviewed",
            "recommended_action":(
                "review_publisher_subtitle" if status=="publisher_subtitle" else
                "stage_or_review_auto_caption" if status=="youtube_auto_caption" else
                "retry_caption_check" if status in {"blocked_by_youtube","error","unknown"} else
                "manual_transcription_required"
            )
        })
    rows.sort(key=lambda r:(STATUS_RANK.get(r["caption_status"],2), r["minutes"] if r["minutes"] is not None else 99999, r["published_at"]))
    for i,row in enumerate(rows,1): row["priority"]=i
    out={
        "schema":"pmnapan-transcript-review-queue-v1",
        "generated_at":datetime.now(timezone.utc).isoformat(),
        "public":False,
        "category":args.category,
        "sorting":"caption readiness, then shortest duration, then publication date",
        "items":rows,
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Queue: {args.out}")
    print(f"Items: {len(rows)}")
    for r in rows[:10]:
        print(f"{r['priority']:02d} | {r['caption_status']:<22} | {r['minutes']:>5} min | {r['key']} | {r['published_at']}")
if __name__=="__main__":
    main()
