# แผนตรวจ Transcript — อาสาหาธรรม

วันที่จัดคิว: 18 พฤศจิกายน 2569

## สถานะรวม

- วิดีโอ YouTube ในหมวด: 30 คลิป
- ตรวจพบ Thai Auto-caption: 30/30 คลิป จาก inventory ก่อน YouTube เริ่ม rate-limit
- Verified Transcript ใน Public Registry: 0
- หลักการ: Auto-caption เป็น Draft เท่านั้น ต้องตรวจเทียบต้นฉบับก่อนเป็น verified
- ขณะจัดทำเอกสาร YouTube ปิดกั้นคำขอ metadata/caption เพิ่มเติมจาก IP ด้วยหน้า “Sign in to confirm you’re not a bot”; ไม่ใช้ cookies หรือข้อมูลล็อกอินเพื่อเลี่ยงข้อจำกัด

## ลำดับตรวจ

| Priority | วันที่ | นาที | Video key | Caption source | สถานะ |
| ---: | --- | ---: | --- | --- | --- |
| 1 | 2026-06-04 | 30.2 | `YouTube:vtF9iGz1cGQ` | Thai Auto-caption | รอตรวจ |
| 2 | 2026-09-02 | 35.6 | `YouTube:Z7dY9DRsbyg` | Thai Auto-caption | รอตรวจ |
| 3 | 2026-08-27 | 35.8 | `YouTube:l2v59uJLzgw` | Thai Auto-caption | รอตรวจ |
| 4 | 2026-09-24 | 36.2 | `YouTube:PDLdpx3H1vo` | Thai Auto-caption | รอตรวจ |
| 5 | 2026-07-09 | 36.5 | `YouTube:CFa2uM71FQU` | Thai Auto-caption | รอตรวจ |
| 6 | 2026-05-27 | 37.2 | `YouTube:NtLusy2HvN8` | Thai Auto-caption | รอตรวจ |
| 7 | 2026-03-15 | 37.3 | `YouTube:07s2wPy6UgA` | Thai Auto-caption | รอตรวจ |
| 8 | 2026-08-20 | 37.4 | `YouTube:3TaDpmsXLSI` | Thai Auto-caption | รอตรวจ |
| 9 | 2026-06-17 | 37.9 | `YouTube:v3QIctEt9Uc` | Thai Auto-caption | รอตรวจ |
| 10 | 2026-09-17 | 38.2 | `YouTube:hzJU9LO9i00` | Thai Auto-caption | รอตรวจ |
| 11 | 2026-02-05 | 38.4 | `YouTube:k5PVpS3rObo` | Thai Auto-caption | รอตรวจ |
| 12 | 2026-02-12 | 40.3 | `YouTube:-1PnaZ_MQko` | Thai Auto-caption | รอตรวจ |
| 13 | 2026-06-25 | 41.7 | `YouTube:L8rAwnZtVHw` | Thai Auto-caption | รอตรวจ |
| 14 | 2026-06-11 | 42.9 | `YouTube:k3LajBPEIwk` | Thai Auto-caption | รอตรวจ |
| 15 | 2026-04-17 | 44.8 | `YouTube:SKQbrrqFeJM` | Thai Auto-caption | รอตรวจ |
| 16 | 2026-10-08 | 49.8 | `YouTube:KCFGtoXDb54` | Thai Auto-caption | รอตรวจ |
| 17 | 2025-09-22 | 51.1 | `YouTube:0cnyryN54_4` | Thai Auto-caption | รอตรวจ |
| 18 | 2025-10-02 | 54.6 | `YouTube:DNrjE4jkkvQ` | Thai Auto-caption | รอตรวจ |
| 19 | 2025-08-31 | 55.1 | `YouTube:4Zkv2r7cmSE` | Thai Auto-caption | รอตรวจ |
| 20 | 2025-12-22 | 56.6 | `YouTube:k4uggPCmWTg` | Thai Auto-caption | รอตรวจ |
| 21 | 2026-01-09 | 57.4 | `YouTube:Tj6guWX5oPk` | Thai Auto-caption | รอตรวจ |
| 22 | 2026-01-28 | 57.8 | `YouTube:vSh-D841efA` | Thai Auto-caption | รอตรวจ |
| 23 | 2025-08-05 | 59.8 | `YouTube:xtuaTXS9mdE` | Thai Auto-caption | รอตรวจ |
| 24 | 2025-11-27 | 60.3 | `YouTube:m2GAxeZf_pY` | Thai Auto-caption | รอตรวจ |
| 25 | 2025-12-18 | 60.3 | `YouTube:CWhq588-r0g` | Thai Auto-caption | รอตรวจ |
| 26 | 2025-11-04 | 62.2 | `YouTube:RkTp_tlyrh0` | Thai Auto-caption | รอตรวจ |
| 27 | 2025-07-04 | 62.8 | `YouTube:bjy001UX7Mc` | Thai Auto-caption | รอตรวจ |
| 28 | 2025-07-23 | 66.3 | `YouTube:7pLcLNaW1m0` | Thai Auto-caption | รอตรวจ |
| 29 | 2025-11-10 | 69.4 | `YouTube:UVd1PIf7YzQ` | Thai Auto-caption | รอตรวจ |
| 30 | 2025-07-13 | 71.7 | `YouTube:hkgZjlWVqgk` | Thai Auto-caption | รอตรวจ |

## วิธีดำเนินงานต่อ

1. เมื่อ YouTube เปิดให้ดึง caption อีกครั้ง ให้ stage SRT ของคลิปตาม Priority โดยใช้ `scripts/fetch_youtube_caption_drafts.py`
2. สร้าง Review Packet ด้วย `scripts/build_transcript_review_packet.py` แล้วตรวจ cue กับวิดีโอต้นฉบับ
3. หากยังตรวจไม่ครบ ให้เก็บเป็น Draft ใน `.transcript-drafts/` เท่านั้น
4. เมื่อเทียบต้นฉบับครบแล้วจึงใช้ `scripts/import_transcript.py --verified --review-note ...`
5. ทดสอบ Search และหน้ารายละเอียดวิดีโอบน Desktop/Mobile ก่อน Deploy

## Pilot ที่เตรียมไว้แล้ว

- มี Draft SRT สำหรับ `YouTube:bjy001UX7Mc` จากการดาวน์โหลดก่อน YouTube เริ่ม block
- สร้าง Private Review Packet แล้ว 1,106 cues
- Review Packet ผ่านการทดสอบที่หน้าจอ 390px และเก็บสถานะ cue ใน browser-local storage
- Pilot นี้ยังไม่ใช่ verified transcript และไม่ได้ถูกนำเข้า `data/transcripts.json`
