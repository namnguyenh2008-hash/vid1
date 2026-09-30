# EP02 Lost in a Mall: post-production brief (for Claude Code)

## Inputs
All files are already renamed; paths below are exact.

| File | What it is | Scene |
|---|---|---|
| `voice/audio_ep2.mp3` (77.3s) | AI voiceover, full episode | all |
| `script.md` | exact VO text | captions + sync |
| `mall.jpg` | crowded multi-floor mall | S1, S2, S5 |
| `child_cry.jpg` | cartoon child lost among adults | S5 |
| `vintage.jpg` | retro cartoon family (5 people) | S5, S9 |
| `hand_pencil.jpg` | pencil drawing of a hand holding a pencil | S3 |
| `tomau.jpg` | hand colouring flowers with a red pencil | S3 |
| `interview.jpg` | binder with notes (research file) | S6 |
| `brain_neurons.webp` | illustrated head full of memories | S9 |
| `1995_paper.png` | first page of Loftus & Pickrell (1995) "The Formation of False Memories" | S4 |
| `elizabeth_loftus.jpg` | portrait | S4 |
| `brand/logo.svg`, `logo_rat_avatar.png` | channel logo | S1 corner, S10 |
| `brand/mascot/rat_mascot.py` | purple rat generator | all |

## Global spec
- **Video:** 1440x2560, 30fps, H.264 + AAC 48kHz, ~18 Mbps. Scale all sizes for 1440 wide.
- **Audio:** voice only, no music, no SFX. Normalise from -22.6 to -14 LUFS, true peak -1 dB. Cut pauses longer than 0.3s down to 0.15s. The AI voice is already clean, so apply no de-noise.
- **Sync:** run Whisper word timestamps on the processed audio and trigger every cue on its **anchor word**. The times below are raw, approximate guides only.
- **Colour:** #0077B6 main, mint #3CE8B4 secondary, text #1A1A1A. Font: Be Vietnam Pro (must render all Vietnamese diacritics; verify "Ký ức", "lạc", "nguồn gốc").
- **Background:** never plain white. Soft gradient #EAF4FB → white (or mint tint), dot grid or blurred colour blobs at 8 to 15%, drifting slowly.
- **Fill the frame:** no large empty areas. Big headlines (100 to 140px), frosted-glass cards (white 72%, blur 24, radius 40, soft shadow), icons in the gaps.
- **Photos:** always moving (push-in 1.00 → 1.06, or a drift of 30px). Rounded 40px frames with a soft shadow, or full-bleed with a 25% white overlay behind text.
- **Captions:** word-synced, 5 to 7 words per line, max 2 lines, white on a #000 55% pill, bottom edge at y=1920, x 80 to 1240. Key terms in #0077B6.
- **Safe zone:** y 200 to 1920, x 80 to 1240.
- **Transitions:** hard cuts. A 6-frame whip only at S2→S3, S3→S4, S8→S9.
- **Visual beat:** something new every 3 to 5s.

## Mascot (purple rat, "chuột tím")
- Build the rig from `rat_mascot.py` with separate layers. Add props: round glasses (#1A1A1A thin frame) and a pointer stick (#0077B6 tip).
- Build these reusable action clips: idle (breathing bob, tail sway, blink every 3 to 4s), wave, point, teach (tap with pointer), scratch head, glasses on/off, think, surprised, happy, nod, enter/exit.
- Idle between actions. Light lip-flap while the VO plays.
- Default position: lower-left or lower-right, 30 to 40% of frame height, never over captions or key text. Centre stage only in S1 and S8.
- Motion: 200 to 400ms, ease-out with a small overshoot. No spinning or distortion.

## Scenes

### S1 Recap + handover | ~0.0 to 6.5
VO: "Tập trước bạn đã biết não có thể tự bịa ra ký ức. Từ giờ, chuột tím sẽ dẫn bạn đi tiếp."
- 0:00: title card, large: "Cài ký ức giả" with the pill "(Lost in a mall)". Small tagline above: "TẬP 2 · KÝ ỨC SAI LỆCH".
- "Tập trước": a mini thumbnail of EP01 (a word card reading "ngủ?") slides in from the top-left, tilted -4°, and fades after 1.5s.
- "chuột tím": the rat **enters** centre-bottom with a bounce, then **waves**. The logo sits small top-right (120px).

### S2 Question | ~6.5 to 12.5
VO: "Câu hỏi hôm nay: nếu mình nói hồi 5 tuổi bạn từng bị lạc trong siêu thị, bạn có nhớ ra không?"
- `mall` full-bleed, blurred 6px, push-in. Question card centre: "Hồi 5 tuổi, bạn từng bị lạc?", pill on "bị lạc".
- "5 tuổi": a counter badge counts 1 → 5.
- Rat: **scratch head**, then a "?" pops.

### S3 Pencil analogy | ~12.5 to 28
VO: "Nghe vô lý đúng không? ... Ký ức giống một bức tranh vẽ bằng bút chì ... tô thêm ... màu đỏ ... của người khác."
- Whip. `hand_pencil` in a rounded frame, top half (slow push-in).
- "bức tranh": the lower half draws a simple line drawing (a house + a child) stroke by stroke.
- "tô thêm": cross-fade to `tomau` (the red pencil colouring).
- "màu đỏ": a second hand icon enters from the right and adds a red patch; the label "người khác" pops beside it.
- "quên luôn": the "người khác" label fades out, and the red patch stays as if it were original.
- Rat: **teach** with the pointer, tapping the drawing on "màu đỏ".

### S4 Researchers | ~28 to 34.3
VO: "Năm 1995, nhà tâm lý học Elizabeth Loftus, người ở tập trước, cùng cộng sự Jacqueline Pickrell thử đúng điều đó."
- Whip. "1995": a big year chip "1995" pops, and `1995_paper` pushes in on a tilted paper card (-3°) with a #0077B6 marker sweep on the title.
- "Elizabeth Loftus": `elizabeth_loftus` in a round crop, with a name card "Elizabeth Loftus · nhà tâm lý học" and the chip "ở tập trước".
- "Jacqueline Pickrell": a second text-only name chip "Jacqueline Pickrell · cộng sự" slides in under it.
- Rat: **glasses on** at "nhà tâm lý học", then **point** at the name cards.

### S5 The method | ~34.3 to 46.3
VO: "Họ hỏi người thân của 24 người tham gia để lấy 3 chuyện tuổi thơ có thật. Rồi lén cài thêm 1 chuyện bịa: ... bị lạc trong trung tâm thương mại, khóc rất to, và được một bà cụ dẫn về."
- "24 người": a grid of 24 small person icons draws in (staggered 30ms), with a counter to 24.
- "3 chuyện ... có thật": 3 crops from `vintage` (retro family) appear as 3 stacked polaroid cards, each with a mint check "THẬT".
- "1 chuyện bịa": a 4th card slides in with a #0077B6 border and a "?" stamp, then the 4 cards shuffle once.
- "trung tâm thương mại": the 4th card flips to show `mall`.
- "khóc rất to": it cross-fades to `child_cry`.
- "bà cụ dẫn về": draw a simple flat elderly woman holding the child's hand, walking out of the crowd.
- Rat: **point** at the 4th card on "lén cài", then a small sneaky **nod**.

### S6 Repeated interviews | ~46.3 to 52.2
VO: "Người tham gia đọc cả 4 chuyện, rồi bị hỏi đi hỏi lại qua vài buổi: 'Bạn còn nhớ gì về chuyện này không?'"
- `interview` in a rounded frame.
- "hỏi đi hỏi lại": 3 speech bubbles stack in (staggered), each with the same question, plus a small calendar showing "Buổi 1 → 2 → 3".
- Rat: **think** (hand at chin).

### S7 Result | ~52.2 to 58.8
VO: "Kết quả, cứ 4 người thì có 1 người bắt đầu 'nhớ' ra lần bị lạc đó. Có người còn tự kể thêm chi tiết."
- The 24-person grid returns. On "cứ 4 người thì có 1", 6 icons turn #0077B6 one by one, and a big stat card reads "≈ 1/4" with the subline "6 trên 24 người".
- "tự kể thêm chi tiết": speech bubbles grow out of 2 of the highlighted icons with small doodles (a balloon, a shop sign).
- Rat: **surprised** on "1 người".

### S8 Rat joke | ~58.8 to 61.3
VO: "Chuột tím cũng suýt nhớ ra mình từng bị lạc."
- The rat takes centre stage, with a thought bubble showing a tiny rat lost among giant legs (a flat drawing). Then it shakes its head fast, the bubble pops, and it gives a sheepish smile.
- No card; the rat alone on the gradient.

### S9 Why + term | ~61.3 to 71.0
VO: "Vì sao? Chuyện nghe rất hợp lý. Người thân lại 'xác nhận' là có. Và lâu dần, não không còn phân biệt được đâu là chuyện mình nghe kể, đâu là chuyện mình tự trải qua. Hiện tượng này gọi là source confusion, nhầm lẫn nguồn gốc ký ức."
- Whip. Three reason cards stagger in (the "Người thân xác nhận" card can use a crop of `vintage`) as a vertical list, each with an icon: "Nghe hợp lý" (puzzle piece), "Người thân xác nhận" (two people), "Lẫn nguồn gốc" (brain).
- "không còn phân biệt": `brain_neurons` blurred as the background. Two bubbles, "Nghe kể" and "Tự trải qua", drift toward each other and merge into one.
- "source confusion": term card with the tagline "HIỆN TƯỢNG", headline "Source confusion", pill on "Source confusion", and the subline "nhầm lẫn nguồn gốc ký ức".
- Rat: **teach** (tap each reason card), then **glasses off** on the term card.

### S10 CTA | ~71.6 to end
VO: "Follow để tập sau chuột tím kể tiếp: vì sao những ký ức bạn tin là khắc sâu nhất lại có thể sai nhiều nhất."
- `logo_rat_avatar` scales in top-centre. Card: tagline "TẬP SAU", headline "Ký ức khắc sâu cũng sai?", pill on "khắc sâu". The small subline "Flashbulb memory" sits under it.
- "Follow": a #0077B6 Follow pill pulses once.
- Rat: **wave** goodbye, then exit. Hold the final frame 0.8s.

## Output
- `episodes/02-lost-in-a-mall/out/ep02_lost_in_a_mall.mp4` plus `captions.srt`.
- Export 6 still frames (S1, S3, S5, S7, S9, S10) for review.
- Report in 3 lines max: duration, missing anchors, changes.
