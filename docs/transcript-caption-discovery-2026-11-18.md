# YouTube Caption Discovery Sample — 18 November 2026

## Purpose

สำรวจความพร้อมของคำบรรยายภาษาไทยจากวิดีโอ YouTube ในทะเบียน PMNapan Library ก่อนเริ่มงาน Transcript แบบเป็นระบบ

การสำรวจนี้เป็นเพียงตัวอย่างข้ามหมวด ไม่ใช่ผลตรวจครบทั้ง 327 วิดีโอ YouTube และห้ามนำอัตราส่วนนี้ไปอนุมานเป็น coverage ของทั้งคลัง

## Sample

ตรวจตัวอย่าง 9 วิดีโอ โดยเลือกวิดีโอหนึ่งรายการจากแต่ละหมวด YouTube ที่มีอยู่ในทะเบียน

| หมวด | Video key | ผล |
| --- | --- | --- |
| อาสาหาธรรม | YouTube:bjy001UX7Mc | YouTube automatic captions (Thai) |
| มามองพุทธ มุมมองพระ | YouTube:GNkeMcv-T6o | YouTube automatic captions (Thai) |
| คุยธรรมะสารพัน | YouTube:LenQQkkePyU | YouTube automatic captions (Thai) |
| งานต่างประเทศและสื่อสากล | YouTube:uy4BzBiKH9Q | YouTube automatic captions (Thai) |
| ธรรมบรรยายและสื่อย้อนหลัง | YouTube:msX39bLJEbk | YouTube automatic captions (Thai) |
| เพื่อนกันวันติดโควิด | YouTube:M6LUV0AdULw | YouTube automatic captions (Thai) |
| ทอล์ค ทู ธรรม | YouTube:dYt2_tt2k2I | YouTube automatic captions (Thai) |
| สวัสดีความสุข | YouTube:NP3IrZzSRkw | ไม่พบ Thai captions ในการตรวจครั้งนี้ |
| หลวงพี่ช่วยด้วย · ซับไตเติล IBHAP | YouTube:1oOA5cn8NJ0 | Publisher subtitle (Thai) |

สรุปตัวอย่าง:
- Publisher subtitle: 1
- YouTube automatic captions: 7
- ไม่พบ Thai captions: 1
- Error: 0

## Editorial interpretation

1. Auto-caption ใช้เป็น “Draft source” ได้ แต่ไม่ถือเป็นคำถอดเสียงที่ตรวจสอบแล้ว เพราะอาจฟังชื่อบุคคล ภาษาบาลี ศัพท์เฉพาะ หรือประโยคต่อเนื่องผิด
2. Publisher subtitle มีน้ำหนักมากกว่า Auto-caption แต่ยังต้องตรวจว่าซับตรงกับคลิปและเป็นฉบับที่ต้องการอ้างอิงก่อนเปลี่ยนสถานะเป็น verified
3. รายการที่ไม่พบ captions ต้องใช้การถอดจากเสียงต้นฉบับหรือแหล่งข้อความอื่นที่ตรวจสอบได้
4. Draft captions ต้องเก็บนอก Public Search และนอก Git จนกว่าจะผ่านการตรวจ

## Technical finding

การทดลองกับ YouTube Auto-caption พบว่า VTT มีลักษณะ rolling caption และเกิดข้อความซ้ำข้าม cue ได้มาก จึงกำหนด staging script ให้ดาวน์โหลด SRT เป็นค่าเริ่มต้น ซึ่งสะอาดกว่าสำหรับการตรวจทาน

ตัวอย่างคลิป YouTube:bjy001UX7Mc:
- VTT ที่ยังไม่เหมาะกับ workflow ตรวจทาน: ประมาณ 120,097 ตัวอักษรหลัง parser รุ่นแรก
- SRT หลังการทำความสะอาดและตัด cue ซ้ำติดกัน: ประมาณ 39,618 ตัวอักษร
- ทั้งสองค่าคือ Draft เท่านั้น ไม่ใช่ transcript ที่ผ่านการรับรอง

## Tools

- `scripts/fetch_youtube_caption_drafts.py` — สำรวจและดาวน์โหลด Thai captions ไปยัง `.transcript-drafts/`
- `scripts/import_transcript.py` — นำไฟล์ที่ตรวจแล้วเข้าสู่ทะเบียน โดยค่าเริ่มต้นเป็น draft
- `docs/transcript-workflow.md` — ขั้นตอนและเกณฑ์ตรวจรับ
