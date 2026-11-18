#!/usr/bin/env python3
"""Import a source-backed transcript into PMNapan Library.

Safety rule:
- Draft is the default and is NOT searchable on the public site.
- Publishing as verified requires --verified and --review-note.
- The script never generates, summarizes, or repairs missing speech.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
VIDEOS_PATH = ROOT / "data" / "videos.json"
TRANSCRIPTS_PATH = ROOT / "data" / "transcripts.json"
SUPPORTED = {".txt", ".srt", ".vtt"}

TIMING_RE = re.compile(
    r"^\s*(?:\d{1,2}:)?\d{1,2}:\d{2}[,.]\d{3}\s*-->\s*"
    r"(?:\d{1,2}:)?\d{1,2}:\d{2}[,.]\d{3}(?:\s+.*)?$"
)
TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"[ \t]+")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def clean_caption_line(line: str) -> str:
    value = html.unescape(TAG_RE.sub("", line))
    value = value.replace("\ufeff", "").replace("\u200b", "")
    return SPACE_RE.sub(" ", value).strip()


def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED:
        raise ValueError(f"รองรับเฉพาะไฟล์ {', '.join(sorted(SUPPORTED))}")
    raw = path.read_text("utf-8-sig")
    if "\ufffd" in raw:
        raise ValueError("พบอักขระทดแทน (�) ในไฟล์ กรุณาตรวจ encoding ก่อนนำเข้า")

    if suffix == ".txt":
        lines = [clean_caption_line(line) for line in raw.splitlines()]
    else:
        lines = []
        skip_block = False
        for original in raw.splitlines():
            stripped = original.strip()
            upper = stripped.upper()
            if upper.startswith(("NOTE", "STYLE", "REGION")):
                skip_block = True
                continue
            if skip_block:
                if not stripped:
                    skip_block = False
                continue
            if upper == "WEBVTT" or stripped.isdigit() or TIMING_RE.match(stripped):
                continue
            lines.append(clean_caption_line(original))

    paragraphs: list[str] = []
    current: list[str] = []
    previous = None
    for line in lines:
        if not line:
            if current:
                paragraphs.append(" ".join(current).strip())
                current = []
                previous = None
            continue
        # Many subtitle files repeat the same caption across adjacent cues.
        if line == previous:
            continue
        current.append(line)
        previous = line
    if current:
        paragraphs.append(" ".join(current).strip())

    deduped: list[str] = []
    for paragraph in paragraphs:
        if paragraph and (not deduped or paragraph != deduped[-1]):
            deduped.append(paragraph)
    text = "\n".join(deduped).strip()
    if len(text) < 10:
        raise ValueError("ข้อความหลังทำความสะอาดสั้นเกินไป กรุณาตรวจไฟล์ต้นฉบับ")
    return text


def https_url(value: str) -> bool:
    try:
        parsed = urlparse(value)
        return parsed.scheme == "https" and bool(parsed.netloc)
    except Exception:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="นำเข้า Transcript ที่มีต้นฉบับตรวจสอบได้เข้าสู่ PMNapan Library"
    )
    parser.add_argument("--key", required=True, help="video key เช่น YouTube:bjy001UX7Mc")
    parser.add_argument("--file", required=True, type=Path, help="ไฟล์ .txt, .srt หรือ .vtt")
    parser.add_argument("--source-url", help="URL แหล่งต้นฉบับ; ค่าเริ่มต้นใช้ URL ของวิดีโอในทะเบียน")
    parser.add_argument("--source-label", default="วิดีโอต้นฉบับ", help="ชื่อแหล่งสำหรับแสดงผล")
    parser.add_argument(
        "--verified",
        action="store_true",
        help="ยืนยันว่าได้ตรวจเทียบกับต้นฉบับแล้ว จึงอนุญาตให้เข้าสู่การค้นหาสาธารณะ",
    )
    parser.add_argument(
        "--review-note",
        help="บันทึกวิธีตรวจ เช่น 'ตรวจเทียบคำบรรยายกับวิดีโอต้นฉบับครบทั้งคลิป'",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="อนุญาตให้แทนที่รายการ key เดิมอย่างชัดเจน; ป้องกันการเขียนทับโดยไม่ตั้งใจ",
    )
    parser.add_argument("--dry-run", action="store_true", help="ตรวจและแสดงผลโดยไม่แก้ไฟล์")
    args = parser.parse_args()

    source_file = args.file.expanduser().resolve()
    if not source_file.is_file():
        raise SystemExit(f"ไม่พบไฟล์: {source_file}")

    catalog = load_json(VIDEOS_PATH)
    videos = {item["key"]: item for item in catalog.get("items", []) if item.get("key")}
    video = videos.get(args.key)
    if not video:
        raise SystemExit(f"ไม่พบ key ใน data/videos.json: {args.key}")

    source_url = args.source_url or video.get("url", "")
    if not https_url(source_url):
        raise SystemExit("source URL ต้องเป็น https URL ที่ตรวจสอบได้")

    if args.verified and not (args.review_note or "").strip():
        raise SystemExit("--verified ต้องระบุ --review-note เพื่อบันทึกว่าตรวจต้นฉบับอย่างไร")

    try:
        text = extract_text(source_file)
    except (UnicodeDecodeError, ValueError) as exc:
        raise SystemExit(f"นำเข้าไม่ได้: {exc}") from exc

    status = "verified" if args.verified else "draft"
    item = {
        "key": args.key,
        "status": status,
        "text": text,
        "source_url": source_url,
        "source_label": args.source_label.strip() or "วิดีโอต้นฉบับ",
        "source_format": source_file.suffix.lower().lstrip("."),
        "sha256": hashlib.sha256(source_file.read_bytes()).hexdigest(),
        "review_note": (args.review_note or "").strip(),
        "updated_at": date.today().isoformat(),
    }

    word_like = len(re.findall(r"\S+", text))
    report = {
        "key": args.key,
        "title": video.get("title", ""),
        "status": status,
        "characters": len(text),
        "tokens_by_whitespace": word_like,
        "source_url": source_url,
        "source_format": item["source_format"],
        "sha256": item["sha256"],
    }

    data = load_json(TRANSCRIPTS_PATH)
    existing = next((x for x in data.get("items", []) if x.get("key") == args.key), None)
    if existing:
        report["existing_status"] = existing.get("status", "unknown")
        if not args.replace and not args.dry_run:
            raise SystemExit(
                f"มี Transcript สำหรับ {args.key} อยู่แล้ว (status={existing.get('status','unknown')}); "
                "ใช้ --replace หลังตรวจความเปลี่ยนแปลงแล้ว"
            )

    if args.dry_run:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    entries = [x for x in data.get("items", []) if x.get("key") != args.key]
    entries.append(item)
    entries.sort(key=lambda x: x.get("key", ""))
    data["items"] = entries
    data["updated_at"] = date.today().isoformat()
    TRANSCRIPTS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"บันทึกแล้ว: {TRANSCRIPTS_PATH.relative_to(ROOT)}")
    if status == "draft":
        print("สถานะ draft: เว็บไซต์จะยังไม่นำข้อความนี้ไปค้นหาหรือแสดงเป็น Transcript")
    else:
        print("สถานะ verified: เว็บไซต์สามารถนำข้อความนี้ไปค้นหาและแสดงได้")
    return 0


if __name__ == "__main__":
    sys.exit(main())
