# Transcript Workflow — PMNapan Library

Updated: 18 November 2026

## Purpose

ระบบนี้ใช้สำหรับนำคำถอดเสียงหรือคำบรรยายที่มีต้นฉบับตรวจสอบได้เข้าสู่ PMNapan Library โดยไม่สร้างคำพูดแทนต้นฉบับที่ไม่มีอยู่

ไฟล์ที่รองรับ:
- `.txt`
- `.srt`
- `.vtt`

สคริปต์เตรียม Draft จาก YouTube:
- `scripts/fetch_youtube_caption_drafts.py`
- เก็บไฟล์ใน `.transcript-drafts/` ซึ่งไม่เผยแพร่และถูกกันออกจาก Git
- เลือก Publisher Thai subtitle ก่อน หากไม่มีจึงใช้ YouTube Thai automatic captions
- ดาวน์โหลดเป็น SRT เพื่อหลีกเลี่ยง rolling-caption duplication ที่พบใน VTT

สคริปต์นำเข้า:
- `scripts/import_transcript.py`

ทะเบียนปลายทาง:
- `data/transcripts.json`

## Editorial states

### draft

เป็นค่าเริ่มต้นของทุกการนำเข้า

- เก็บไว้เพื่อตรวจทาน
- เว็บไซต์ไม่นำข้อความไปค้นหา
- เว็บไซต์ไม่แสดงเป็น Transcript ที่ตรวจสอบแล้ว
- เหมาะกับไฟล์ที่เพิ่งได้รับหรือยังตรวจไม่ครบ

ตัวอย่าง:

```bash
python3 scripts/import_transcript.py \
  --key YouTube:bjy001UX7Mc \
  --file "/path/to/transcript.srt"
```

### verified

ใช้เมื่อผู้ดูแลตรวจคำถอดเสียงกับต้นฉบับแล้วเท่านั้น

ระบบบังคับให้ระบุ `--review-note` เพื่อให้มีร่องรอยว่าตรวจอย่างไร

หาก key เดิมมี Transcript อยู่แล้ว สคริปต์จะไม่เขียนทับอัตโนมัติ ต้องใช้ `--replace` หลังตรวจความเปลี่ยนแปลงก่อน

ตัวอย่าง:

```bash
python3 scripts/import_transcript.py \
  --key YouTube:bjy001UX7Mc \
  --file "/path/to/transcript.srt" \
  --verified \
  --review-note "ตรวจเทียบคำบรรยายกับวิดีโอต้นฉบับครบทั้งคลิป"
```

เมื่อสถานะเป็น `verified` เว็บไซต์จึงสามารถ:
- ค้นคำจาก Transcript ในหน้า Library
- แสดง Transcript ในหน้ารายละเอียดวิดีโอ
- เชื่อมแหล่งต้นฉบับกลับไปยังวิดีโอที่ตรวจสอบได้

## Source rules

1. `key` ต้องมีอยู่จริงใน `data/videos.json`
2. ค่าเริ่มต้นของแหล่งอ้างอิงจะใช้ URL วิดีโอต้นฉบับในทะเบียน
3. ถ้าใช้แหล่งอื่น ต้องระบุ HTTPS URL ที่ตรวจสอบได้ด้วย `--source-url`
4. ห้ามใช้ข้อความที่สร้างขึ้นจากการคาดเดา สรุป หรือแต่งเติมเป็น Transcript
5. ถ้าต้นฉบับฟังไม่ชัด ให้คงสถานะ draft จนกว่าจะตรวจสอบได้
6. การแก้คำผิดทำได้เฉพาะเมื่อเป็นการแก้จากการตรวจเทียบต้นฉบับ ไม่ใช่การปรับถ้อยคำให้สละสลวย

## Dry run

ใช้ตรวจไฟล์ก่อนแก้ทะเบียนจริง:

```bash
python3 scripts/import_transcript.py \
  --key YouTube:bjy001UX7Mc \
  --file "/path/to/transcript.vtt" \
  --dry-run
```

Dry run จะแสดง:
- video key
- ชื่อคลิป
- สถานะที่จะบันทึก
- จำนวนอักขระ
- รูปแบบไฟล์
- URL ต้นฉบับ
- SHA-256 ของไฟล์ต้นทาง

## Review queue และ Review Packet

สร้างคิวตรวจตามหมวด:

```bash
python3 scripts/build_transcript_review_queue.py \
  --category "อาสาหาธรรม" \
  --out .transcript-drafts/aasaha-review-queue.json
```

คิวจะเรียงตามความพร้อมของแหล่งซับ แล้วตามความยาวคลิปจากสั้นไปยาว เพื่อให้เริ่มตรวจชุดที่ใช้เวลาน้อยก่อน

สร้าง Private Review Packet จาก SRT Draft:

```bash
python3 scripts/build_transcript_review_packet.py \
  --key YouTube:bjy001UX7Mc \
  --file .transcript-drafts/captions/bjy001UX7Mc.th.srt
```

Review Packet:
- แสดง subtitle เป็น cue พร้อม timestamp
- timestamp คลิกกลับไปวิดีโอต้นฉบับได้
- ค้นคำใน Draft ได้
- ติ๊ก cue ที่ตรวจแล้วได้
- สถานะการติ๊กเก็บเฉพาะใน localStorage ของ browser
- ไฟล์ HTML อยู่ใต้ `.transcript-drafts/` และไม่เผยแพร่

การติ๊ก cue ใน Review Packet ไม่ได้เปลี่ยนสถานะ Transcript เป็น verified โดยอัตโนมัติ ผู้ดูแลยังต้องตรวจต้นฉบับครบและนำเข้าด้วย `--verified --review-note`

## Acceptance checks

หลังเพิ่ม Transcript จริงทุกครั้ง ให้ตรวจอย่างน้อย:

```bash
python3 -m py_compile scripts/import_transcript.py
python3 -m json.tool data/transcripts.json >/dev/null
node --check assets/site.js
```

จากนั้นเปิด:
- `library.html` และค้นคำที่มีอยู่จริงใน Transcript
- `video.html?id=<video-key>` และตรวจข้อความ/แหล่งอ้างอิง
- Mobile 390px เพื่อยืนยันว่า Transcript ไม่ทำให้หน้าล้นแนวนอน

## Important limitation

ณ วันที่ 18 พฤศจิกายน 2569 ยังไม่มี Transcript วิดีโอที่ผ่านสถานะ `verified` ในทะเบียน จึงยังไม่มีคำถอดเสียงใดถูกใช้ใน Public Search
