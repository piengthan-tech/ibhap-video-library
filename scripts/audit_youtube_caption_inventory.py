#!/usr/bin/env python3
"""Audit Thai-caption availability for YouTube videos in the catalog.

Metadata only: does not download caption text and does not change public data.
The output is stored under .transcript-drafts/ (git-ignored).
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS_PATH = ROOT / "data" / "videos.json"
DEFAULT_OUT = ROOT / ".transcript-drafts" / "caption-inventory.json"
STATUSES = (
    "publisher_subtitle",
    "youtube_auto_caption",
    "none",
    "blocked_by_youtube",
    "error",
)
RETRYABLE = {"blocked_by_youtube", "error"}


def classify_error(message: str) -> str:
    lowered = message.lower()
    if "sign in to confirm" in lowered and "not a bot" in lowered:
        return "blocked_by_youtube"
    return "error"


def inspect(yt_dlp: str, item: dict) -> dict:
    row = {
        "key": item["key"],
        "video_id": item["video_id"],
        "category": item.get("category", ""),
        "title": item.get("title", ""),
        "url": item.get("url", ""),
        "published_at": item.get("published_at", ""),
    }
    try:
        proc = subprocess.run(
            [
                yt_dlp,
                "--dump-single-json",
                "--skip-download",
                "--no-warnings",
                item["url"],
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        if proc.returncode != 0:
            msg = (proc.stderr or proc.stdout or "yt-dlp failed").strip().splitlines()[-1]
            raise RuntimeError(msg)
        info = json.loads(proc.stdout)
        if info.get("subtitles", {}).get("th"):
            row["caption_kind"] = "publisher_subtitle"
        elif info.get("automatic_captions", {}).get("th"):
            row["caption_kind"] = "youtube_auto_caption"
        else:
            row["caption_kind"] = "none"
    except Exception as exc:
        message = str(exc)[:500]
        row["caption_kind"] = classify_error(message)
        row["error"] = message
    return row


def counts_for(rows: list[dict]) -> dict[str, int]:
    counts = {key: 0 for key in STATUSES}
    for row in rows:
        kind = row.get("caption_kind", "error")
        counts[kind if kind in counts else "error"] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ตรวจสถานะ Thai captions ของวิดีโอ YouTube ใน PMNapan Library"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=2,
        help="จำนวนงานพร้อมกัน (1-6); ค่าเริ่มต้นต่ำเพื่อลดความเสี่ยงถูก YouTube rate-limit",
    )
    parser.add_argument("--limit", type=int, default=0, help="0 = ตรวจทั้งหมด")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--resume",
        action="store_true",
        help="เก็บผลสำเร็จเดิมและ retry เฉพาะ blocked_by_youtube/error",
    )
    args = parser.parse_args()

    if not 1 <= args.workers <= 6:
        raise SystemExit("--workers ต้องอยู่ระหว่าง 1 ถึง 6")

    yt_dlp = shutil.which("yt-dlp")
    if not yt_dlp:
        raise SystemExit("ไม่พบ yt-dlp ในเครื่อง")

    with VIDEOS_PATH.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    videos = [
        x
        for x in raw.get("items", [])
        if x.get("platform") == "YouTube" and x.get("key") and x.get("url")
    ]
    if args.limit:
        if args.limit < 1:
            raise SystemExit("--limit ต้องเป็นจำนวนเต็มบวกหรือ 0")
        videos = videos[: args.limit]

    out = args.out.expanduser().resolve()
    order = {item["key"]: i for i, item in enumerate(videos)}
    selected_keys = set(order)
    rows: list[dict] = []
    previous_by_key: dict[str, dict] = {}

    if args.resume and out.is_file():
        try:
            previous = json.loads(out.read_text("utf-8"))
            previous_by_key = {
                row["key"]: row
                for row in previous.get("items", [])
                if row.get("key") in selected_keys
            }
        except Exception as exc:
            raise SystemExit(f"อ่าน inventory เดิมไม่ได้: {exc}") from exc

    todo = []
    for video in videos:
        previous = previous_by_key.get(video["key"])
        if previous and previous.get("caption_kind") not in RETRYABLE:
            rows.append(previous)
        else:
            todo.append(video)

    if args.resume:
        print(
            f"Resume: preserved={len(rows)} retry/new={len(todo)} total={len(videos)}",
            flush=True,
        )

    done = 0
    if todo:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(inspect, yt_dlp, item): item["key"] for item in todo}
            for future in as_completed(futures):
                rows.append(future.result())
                done += 1
                if done == 1 or done % 20 == 0 or done == len(todo):
                    print(
                        f"[{done}/{len(todo)} retry/new] {counts_for(rows)}",
                        flush=True,
                    )

    rows.sort(key=lambda x: order[x["key"]])
    summary = counts_for(rows)
    categories: dict[str, dict[str, int]] = {}
    for row in rows:
        cat = categories.setdefault(
            row["category"],
            {"total": 0, **{key: 0 for key in STATUSES}},
        )
        cat["total"] += 1
        kind = row.get("caption_kind", "error")
        cat[kind if kind in STATUSES else "error"] += 1

    result = {
        "schema": "pmnapan-youtube-caption-inventory-v2",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "scope": "metadata_only_no_caption_text_downloaded",
        "total_youtube_videos": len(videos),
        "summary": summary,
        "retryable_statuses": sorted(RETRYABLE),
        "by_category": categories,
        "items": rows,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("\nFINAL")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Inventory: {out}")
    if summary["blocked_by_youtube"]:
        print(
            "blocked_by_youtube means YouTube refused metadata access; it does NOT mean captions are absent."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
