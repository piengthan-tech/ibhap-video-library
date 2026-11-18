#!/usr/bin/env python3
"""Discover and stage Thai YouTube captions for editorial review.

This tool NEVER writes to data/transcripts.json and NEVER marks captions verified.
Draft files are staged outside the public data path and should remain git-ignored.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VIDEOS_PATH = ROOT / "data" / "videos.json"
DEFAULT_OUT = ROOT / ".transcript-drafts"


def run_json(cmd: list[str]) -> dict:
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout or "yt-dlp failed").strip().splitlines()[-1]
        raise RuntimeError(message)
    return json.loads(proc.stdout)


def load_catalog() -> list[dict]:
    with VIDEOS_PATH.open("r", encoding="utf-8") as fh:
        raw = json.load(fh)
    return [x for x in raw.get("items", []) if x.get("platform") == "YouTube" and x.get("key")]


def caption_kind(info: dict) -> str | None:
    if info.get("subtitles", {}).get("th"):
        return "publisher_subtitle"
    if info.get("automatic_captions", {}).get("th"):
        return "youtube_auto_caption"
    return None


def download_caption(yt_dlp: str, video: dict, kind: str, out_dir: Path) -> Path:
    video_id = video["video_id"]
    before = set(out_dir.glob(f"{video_id}*"))
    mode = "--write-subs" if kind == "publisher_subtitle" else "--write-auto-subs"
    cmd = [
        yt_dlp,
        mode,
        "--sub-langs", "th",
        "--sub-format", "srt",
        "--skip-download",
        "--no-warnings",
        "--paths", str(out_dir),
        "-o", "%(id)s.%(ext)s",
        video["url"],
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        message = (proc.stderr or proc.stdout or "caption download failed").strip().splitlines()[-1]
        raise RuntimeError(message)
    after = set(out_dir.glob(f"{video_id}*"))
    candidates = sorted(
        [p for p in (after | (after - before)) if p.suffix.lower() == ".srt"],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise RuntimeError("yt-dlp reported captions but no SRT file was created")
    return candidates[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="สำรวจ/ดึง Thai captions จาก YouTube มาเก็บเป็น Draft สำหรับตรวจทาน"
    )
    parser.add_argument(
        "--key",
        action="append",
        dest="keys",
        help="เลือก video key; ระบุซ้ำได้ ถ้าไม่ระบุจะใช้รายการ YouTube ตามลำดับทะเบียน",
    )
    parser.add_argument("--limit", type=int, default=10, help="จำนวนสูงสุดเมื่อไม่ได้ระบุ --key (default 10)")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="ตรวจว่ามีซับไทยหรือไม่ โดยไม่ดาวน์โหลดไฟล์",
    )
    args = parser.parse_args()

    yt_dlp = shutil.which("yt-dlp")
    if not yt_dlp:
        raise SystemExit("ไม่พบ yt-dlp ในเครื่อง")

    catalog = load_catalog()
    by_key = {x["key"]: x for x in catalog}
    if args.keys:
        missing = [k for k in args.keys if k not in by_key]
        if missing:
            raise SystemExit("ไม่พบ key ในทะเบียน: " + ", ".join(missing))
        selected = [by_key[k] for k in args.keys]
    else:
        if args.limit < 1 or args.limit > 100:
            raise SystemExit("--limit ต้องอยู่ระหว่าง 1 ถึง 100")
        selected = catalog[: args.limit]

    out_dir = args.out_dir.expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    counts = {"publisher_subtitle": 0, "youtube_auto_caption": 0, "none": 0, "error": 0}

    for index, video in enumerate(selected, 1):
        row = {
            "key": video["key"],
            "video_id": video["video_id"],
            "title": video["title"],
            "url": video["url"],
            "status": "draft_unreviewed",
        }
        try:
            info = run_json([
                yt_dlp,
                "--dump-single-json",
                "--skip-download",
                "--no-warnings",
                video["url"],
            ])
            kind = caption_kind(info)
            if not kind:
                row["caption_kind"] = "none"
                counts["none"] += 1
            else:
                row["caption_kind"] = kind
                counts[kind] += 1
                if not args.metadata_only:
                    caption_file = download_caption(yt_dlp, video, kind, out_dir)
                    row["local_file"] = caption_file.name
            row["language"] = "th"
        except Exception as exc:
            row["caption_kind"] = "error"
            row["error"] = str(exc)[:300]
            counts["error"] += 1
        results.append(row)
        print(
            f"[{index}/{len(selected)}] {video['key']} -> {row['caption_kind']}",
            flush=True,
        )

    manifest = {
        "schema": "pmnapan-transcript-draft-discovery-v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_search": False,
        "verification": "none",
        "items": results,
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print("\nSummary")
    print(json.dumps(counts, ensure_ascii=False, indent=2))
    print(f"Manifest: {manifest_path}")
    print("Draft captions are not verified and must not be published until manually reviewed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
