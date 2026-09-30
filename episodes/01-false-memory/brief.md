# EP01 False Memory v3 (with chuột tím): post-production brief

Full rebuild of EP01. The old edit is discarded. New AI voice, same content, plus the purple rat as the on-screen guide.

## Inputs
| File | What it is | Scene |
|---|---|---|
| `voice/audio_ep1.mp3` (88.1s, -22.2 LUFS) | new AI voiceover v2 | all |
| `script.md` | exact VO text (v3, with chuột tím) | captions + sync |
| `drm` | DRM image | S5 |
| `1995` | Roediger & McDermott (1995) paper | S5 |
| `1974` | Loftus & Palmer (1974) paper | S7 |
| `elizabeth_loftus` | portrait | S7 |
| `vid_5_5` | 5.5s clip, "memory is rebuilt" | S11 |
| `brand/logo.svg`, `logo_rat_avatar` | logos | corner, S12 |
| `brand/mascot/rat_mascot.py` | purple rat generator | all |

Match assets by basename, any extension. Rename anything with spaces to snake_case first. **Do not use `bed`**: it has been removed.

## Global spec
- **Video:** 1440x2560, 30fps, H.264 + AAC 48kHz, ~18 Mbps. Scale all sizes for 1440 wide.
- **Audio:** voice only. No music, no SFX. Loudness from -22.2 to -14 LUFS, true peak -1 dB. Cut pauses longer than 0.3s down to 0.15s, **except** the 10-word list (keep its natural rhythm) and the ~1s beat after "Không hề có từ 'ngủ'" (keep it for the reveal). Target final length ~80s.
- **Sync:** the raw times next to each scene come from pause detection on `audio_ep1.mp3` and are approximate (± 1s), especially S2 to S4. Run Whisper word timestamps first, then trigger every cue on the **anchor word** in quotes.
- **Font:** Be Vietnam Pro. It must render every Vietnamese diacritic; check "Ký ức", "ngủ", "đâm sầm", "lệch".
- **Colour:** #0077B6 main, mint #3CE8B4 secondary, text #1A1A1A.
- **Background:** never plain white. Soft gradient #EAF4FB → white (or mint tint), dot grid or blurred blobs at 8 to 15%, drifting slowly.
- **Fill the frame:** no big empty areas. Headlines 100 to 140px. Frosted cards (white 72%, blur 24, radius 40, soft shadow). Icons fill the gaps.
- **Photos:** always moving (push-in 1.00 → 1.06), rounded 40px frames.
- **Captions:** word-synced, 5 to 7 words per line, white on a #000 55% pill, bottom edge at y=1920, x 80 to 1240, key terms in #0077B6. **Hide captions during the word list (S2).**
- **Safe zone:** y 200 to 1920, x 80 to 1240.
- **Transitions:** hard cuts. A 6-frame whip only at S3→S4, S6→S7, S10→S11.

## Mascot (chuột tím)
- Build the layered rig from `rat_mascot.py`. Props: round glasses (#1A1A1A thin frame), pointer stick (#0077B6 tip).
- Build the action clips: idle (breathing bob, tail sway, blink every 3 to 4s), wave, point, teach (pointer tap), scratch head, glasses on/off, think, surprised, happy, nod, head shake, enter/exit.
- Idle between actions. Light lip-flap while the VO plays.
- Default position: lower-left or lower-right, 30 to 40% of frame height, never over captions or key text. Centre stage only in S1 and S4.
- Motion: 200 to 400ms, ease-out with a small overshoot.

## Scenes

### S1 Opening | raw 0.0 to 7.4s
VO: "Trí nhớ của bạn có tốt không? Chuột tím có một bài test nhỏ. Nghe kỹ 10 từ này nhé."
- 0:00: title card, large: "Kí ức sai lệch", with the pill "(False memory)". Tagline: "TEST TRÍ NHỚ".
- "Trí nhớ": a "Độ tự tin vào trí nhớ" bar (mint border) fills 0 → 100% with a counter, then wiggles at 100%.
- "Chuột tím": the rat **enters** centre-bottom with a bounce and **waves**.
- "10 từ": 10 face-down cards (2 rows × 5, backs #0077B6 with a white "?") fly in staggered 80ms apart. The confidence bar shrinks to the top corner. The rat moves to the lower-right and goes idle.

### S2 Word list (no captions) | raw 7.9 to ~22.8s
VO: the 10 words.
- On each word's onset, flip the matching card (250ms). The front is white with the word in #1A1A1A, 90px. Flipped cards stay in place.
- A thin #0077B6 progress bar at the top fills 1/10 per word.
- Rat: listens with a slight head tilt; its pupils follow each flipping card.

### S3 Question | raw ~22.8 to ~26.0s
VO: "Có từ 'ngủ' không?"
- All 10 cards: **Gaussian blur 24px, opacity 35%, plus a 40% white overlay**, so no word is readable.
- "ngủ?" pops in the centre (180px, #0077B6), sharp, with 2 sharp buttons below: "CÓ" / "KHÔNG". A cursor drifts toward "CÓ" and stops just short of it.
- Rat: **think** (hand at chin), with a "?" popping.

### S4 Reveal + rat joke | raw ~26.3 to 37.4s
VO: "Nếu bạn nói có, chúc mừng, bạn vừa tạo ra một ký ức giả. Không hề có từ 'ngủ'. Lần đầu làm bài này, chuột tím cũng trượt."
- "chúc mừng": the cursor clicks "CÓ", with a small sarcastic mint confetti burst.
- "ký ức giả": card with tagline "BẠN VỪA TẠO RA", headline "ký ức giả", pill on "giả".
- "Không hề có": the cards unblur. A #0077B6 scan line sweeps them. An empty dashed card "ngủ" appears, then gets struck through.
- "chuột tím cũng trượt": the rat moves to centre, puts a hand over its face and **shakes its head**, then gives a sheepish smile (1.5s).

### S5 DRM | raw 37.6 to 43.3s
VO: "Đây là bài test DRM của các nhà tâm lý học Deese, Roediger và McDermott."
- "DRM": `drm` in a rounded frame, push-in, with a pill "DRM" above it.
- On each name: a text-only name chip staggers in ("James Deese", "Henry Roediger", "Kathleen McDermott"). No faces.
- "McDermott": the `1995` paper card slides in, tilted -3°, with a #0077B6 marker sweep on the title.
- Rat: **glasses on** at "nhà tâm lý học", then **point** at the chips.

### S6 Spreading activation | raw 43.7 to ~54.2s
VO: "Lý do: trong não, các từ liên quan nối với nhau như mạng lưới ... spreading activation ... chữ 'ngủ' tự sáng đèn, và não tưởng mình vừa nghe thấy nó."
- "mạng lưới": full-frame network; the 10 words are nodes in a ring with lines, and the centre node is empty.
- "kích hoạt lan": nodes light up #0077B6 in sequence, with pulses flowing toward the centre.
- "spreading activation": a term card at the top, pill on "spreading activation".
- "sáng đèn": the centre node fills #0077B6 with "ngủ", glows twice, and all lines flash.
- Rat: **teach**, tapping nodes with the pointer; on "tưởng mình vừa nghe thấy" it does a proud **nod**, as if fooled.

### S7 Loftus | raw ~54.5 to ~59.5s
VO: "Nhà tâm lý học Elizabeth Loftus, người cả đời nghiên cứu lời khai nhân chứng, cho hai nhóm xem cùng một video tai nạn xe."
- "Elizabeth Loftus": `elizabeth_loftus` in a large round crop, with the name card "Elizabeth Loftus · nhà tâm lý học" and the subline "chuyên gia lời khai nhân chứng".
- "hai nhóm": the photo shrinks top-left. The `1974` paper card pops lower-right (chip "Loftus & Palmer, 1974"). Two groups of 3 flat characters face a TV.
- "video tai nạn xe": the TV shows 2 flat cars bumping gently, clearly with no glass.
- Rat: **point** at the TV.

### S8 Two questions | raw ~59.9 to ~64.3s
VO: Group 1 "va nhau", Group 2 "đâm sầm", "Nhóm 'đâm sầm' đoán nhanh hơn."
- Split screen. Left: "NHÓM 1" with the bubble "va nhau". Right: "NHÓM 2" with "ĐÂM SẦM" in the pill; that word alone shakes.
- "nhanh hơn": a speedometer under each side; the right needle goes higher. No numbers.
- Rat: **surprised** on "đâm sầm".

### S9 Broken glass trap | raw ~64.8 to ~76.1s
VO: "Một tuần sau, bà gài một câu hỏi bẫy ... Bạn có thấy kính vỡ không? ... va mạnh thì phải vỡ kính ... nhiều gấp đôi nhóm kia."
- "Một tuần sau": a calendar flips 7 pages, "+7 ngày".
- "câu hỏi bẫy": card "CÂU HỎI BẪY" with the headline "Bạn có thấy kính vỡ không?", pill on "kính vỡ".
- "không hề có kính vỡ": a mini replay of the clean crash with a mint check "0 mảnh kính".
- "tưởng tượng": a Group 2 character's thought bubble replays the crash dramatically, with glass shards **only inside the bubble**.
- "gấp đôi": 2 bars, 1 unit vs 2 units, and a pill counting "x1 → x2".
- Rat: **scratch head** on "câu hỏi bẫy", then **teach** tapping the x2 bar.

### S10 Misinformation effect | raw ~76.4 to 79.0s
VO: "Chỉ một chữ nghe sau sự việc đã viết đè lên ký ức. Hiện tượng này gọi là misinformation effect."
- "viết đè": a film-frame memory card of the clean crash; "đâm sầm" flies in and a #0077B6 pen scribbles glass onto it.
- "misinformation effect": term card with the tagline "HIỆN TƯỢNG", pill on "misinformation".
- Rat: **glasses off** on the term card.

### S11 Memory is rebuilt | raw 79.4 to 83.7s
VO: "Ký ức không phải video được lưu sẵn. Mỗi lần nhớ, não dựng lại từ đầu, và đôi khi dựng sai."
- `vid_5_5` full-frame for the whole scene (slow it to 0.9x if needed).
- "không phải video": a "▶ REC" badge gets struck through.
- "dựng lại": frosted card at the bottom, "Não dựng lại".
- "dựng sai": one 2-frame RGB glitch; the card changes to "đôi khi dựng sai".
- Rat: small, lower-right, **think**.

### S12 CTA | raw 84.1 to 88.1 (end)s
VO: "Follow để tập sau chuột tím kể tiếp: làm sao các nhà khoa học cài được cả một ký ức tuổi thơ chưa từng xảy ra."
- `logo_rat_avatar` scales in top-centre. Card: tagline "TẬP SAU", headline "Cài ký ức giả", pill on "ký ức giả", subline "Lost in a mall".
- "Follow": a #0077B6 Follow pill pulses once.
- Rat: **wave**, then exit. Hold the last frame 0.8s.

## Output
- `episodes/01-false-memory/out/ep01_false_memory_v3.mp4` plus `captions.srt`.
- Export 6 stills (S1, S3, S4, S6, S9, S12).
- Report in 3 lines max: duration, missing anchors, changes.
