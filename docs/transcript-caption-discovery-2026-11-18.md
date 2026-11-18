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

## Expanded inventory attempt

หลังจาก sample 9 หมวด ได้ลองตรวจ metadata ครบ 327 วิดีโอ YouTube โดยไม่ดาวน์โหลดข้อความคำบรรยาย

ระหว่างการตรวจ YouTube เริ่มตอบกลับด้วย `Sign in to confirm you’re not a bot` หลังตรวจไปจำนวนมาก จึงแยกสถานะดังกล่าวเป็น `blocked_by_youtube` และไม่นับเป็น “ไม่มีซับ”

เมื่อรวมผล Full scan กับหลักฐานจาก sample 9 หมวดที่ตรวจสำเร็จก่อนถูก throttle สถานะที่รู้จากการตรวจวันที่ 18 พฤศจิกายน 2569 คือ:

| สถานะ | จำนวน |
| --- | ---: |
| YouTube automatic captions (Thai) | 211 |
| Publisher subtitle (Thai) | 1 |
| ตรวจแล้วไม่พบ Thai captions | 2 |
| ยังไม่ทราบ เพราะถูก YouTube block | 113 |
| รวมวิดีโอ YouTube | 327 |

ดังนั้นมีอย่างน้อย 212 วิดีโอที่พบแหล่งซับไทยจริงจากการตรวจครั้งนี้ แต่ตัวเลขนี้ไม่ใช่ coverage สุดท้าย เพราะ 113 รายการยังตรวจไม่สำเร็จ

### สถานะตามหมวด

| หมวด | รวม | Auto | Publisher | ไม่พบ | Blocked |
| --- | ---: | ---: | ---: | ---: | ---: |
| อาสาหาธรรม | 30 | 30 | 0 | 0 | 0 |
| มามองพุทธ มุมมองพระ | 85 | 81 | 0 | 1 | 3 |
| คุยธรรมะสารพัน | 101 | 92 | 0 | 0 | 9 |
| งานต่างประเทศและสื่อสากล | 26 | 5 | 0 | 0 | 21 |
| ธรรมบรรยายและสื่อย้อนหลัง | 41 | 1 | 0 | 0 | 40 |
| เพื่อนกันวันติดโควิด | 7 | 1 | 0 | 0 | 6 |
| ทอล์ค ทู ธรรม | 2 | 1 | 0 | 0 | 1 |
| สวัสดีความสุข | 5 | 0 | 0 | 1 | 4 |
| หลวงพี่ช่วยด้วย · ซับไตเติล IBHAP | 30 | 0 | 1 | 0 | 29 |

### Recommended review order

1. **อาสาหาธรรม** — เริ่มก่อน เพราะ 30/30 คลิปมี Thai Auto-caption ที่ตรวจพบ และเป็นชุดที่ตรงกับงานคลังคำสอน/Quote โดยตรง
2. **มามองพุทธ มุมมองพระ** — มี Draft source ที่รู้สถานะแล้ว 81 คลิป
3. **คุยธรรมะสารพัน** — มี Draft source ที่รู้สถานะแล้ว 92 คลิป
4. หมวดที่มี `blocked_by_youtube` จำนวนมาก — retry metadata ในภายหลังโดยใช้โหมด `--resume` และความถี่ต่ำ ไม่ใช้ browser cookies เพื่อหลีกเลี่ยงข้อจำกัด

Auto-caption ทุกคลิปยังคงเป็น Draft จนกว่าจะมีการตรวจเทียบกับเสียง/วิดีโอต้นฉบับและบันทึก `--review-note`
