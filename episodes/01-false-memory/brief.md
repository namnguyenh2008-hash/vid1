# EP01 False Memory: post-production brief v2 (for Claude Code)

## Inputs (match by filename, any extension)
| File | What it is | Scene |
|---|---|---|
| `voice/audio1.m4a` (46.0s) | VO part 1: hook, test, DRM, spreading activation | S1 to S6 |
| `voice/audio2.m4a` (60.2s) | VO part 2: Loftus, misinformation effect, ending | S7 to S12 |
| `bed` | photo of a bed | S1 opening |
| `drm` | DRM image | S5 |
| `1995` | Roediger & McDermott (1995) paper | S5 |
| `elizabeth loftus` | portrait of Loftus | S7 |
| `1974` | Loftus & Palmer (1974) paper | S7 |
| `vid 5.5` | 5.5s video clip for the "memory is rebuilt" moment | S11 |
| `brand/logo.svg` | channel logo | S12 |
| `script.md` | exact VO text | captions |

No faces of Deese, Roediger or McDermott. The channel is faceless: no person on camera, only images, animation and cards.

## Global spec
- TikTok 1080x1920, 30fps, H.264 + AAC 48kHz, 10 Mbps.
- **Audio:** voice only. No music, no SFX. -14 LUFS, high-pass at 80Hz, light de-noise.
- **Edit:** join audio1 then audio2. Cut every pause over 0.25s down to 0.12s, and remove breaths. Keep the pauses inside the word list (S2) at their natural length, because the rhythm matters there.
- **Sync rule:** timestamps below come from the RAW files (pause detection). First run Whisper word timestamps on the joined, cut audio. Then trigger every cue on its **anchor word** (in quotes). Never trigger by seconds alone.
- **Colour:** white #FFFFFF base. Accent #0077B6, used sparingly. Text #1A1A1A. Mint #3CE8B4 for tiny details only.
- **Font:** Be Vietnam Pro. Headlines ExtraBold, body SemiBold.
- **Card:** frosted glass (white 72%, blur 20, radius 32, shadow 0 12 40 rgba(0,0,0,.12)). Small caps tagline (28px, #0077B6) above a big headline (80 to 96px). One key word in a #0077B6 pill with white text.
- **Photos:** never static. Slow push-in 1.00 to 1.06 across the shot, or a slight drift of 20px.
- **Paper images:** show on a white "paper" card rotated -3°, with a soft shadow. Highlight the title line with a #0077B6 marker sweep (left to right, 300ms).
- **Motion:** ease-out, 200 to 300ms. Staggered reveals 80ms apart. A new visual beat every 3 to 5s.
- **Characters:** flat white figure, thin #1A1A1A outline, dot eyes. One consistent style.
- **Captions:** word-synced, 5 to 7 words per line, max 2 lines, white on a #000 55% pill. Bottom edge at y=1440, x between 60 and 930. The current key term is coloured #0077B6. Hide captions during S2.
- **Transitions:** hard cuts. A 6-frame whip only at S1→S2, S6→S7 and S10→S11.

## Scene list

### S1 Opening | audio1 0.86 to 6.5
VO: "Trí nhớ của bạn có tốt không? Nghe kỹ 10 từ này nhé."
- 0:00: `bed` full-screen, soft 20% white overlay, slow push-in. It sets the sleep theme without giving the answer away.
- "Trí nhớ": card slides up from the bottom, tagline "TEST TRÍ NHỚ", headline "10 từ", pill on "10".
- "Nghe kỹ": a small #0077B6 ear icon pulses once beside the card.

### S2 Word list | audio1 6.77 to ~14.4
VO: the 10 words. Onsets approx.: Giường 6.77, Nghỉ ngơi 7.86, Mệt 8.75, Mơ 9.54, Chợp mắt 10.20, Chăn 11.09, Ngáy 11.75, Gối 12.69, Ngáp 13.41, Đêm 14.09.
- Whip cut to a full-screen white background. `bed` stays behind at 8% opacity, blurred.
- Each word pops into the centre on its onset (120px, #1A1A1A), holds, then shrinks and slides into a 2-column list (5 + 5) on the next onset.
- A thin #0077B6 progress bar across the top fills 1/10 per word.

### S3 Question | audio1 ~14.4 to 17.46
VO: "Có từ 'ngủ' không?"
- The list blurs to 30%. "ngủ?" pops in the centre (160px, #0077B6).
- Two pill buttons below: "CÓ" / "KHÔNG". A hand cursor drifts toward "CÓ" and stops just before it. It is a tease, so it never clicks.

### S4 Reveal | audio1 18.13 to ~26.9
VO: "Nếu bạn nói có, chúc mừng, bạn vừa tạo ra một ký ức giả. Không hề có từ 'ngủ'."
- "chúc mừng": the cursor clicks "CÓ". A tiny mint confetti burst (sarcastic), and the white character does a slow clap.
- "ký ức giả": card with tagline "BẠN VỪA TẠO RA", headline "ký ức giả", pill on "giả".
- "Không hề có": the list comes back sharp. A #0077B6 scan line sweeps top to bottom over the 10 words. An empty dashed slot labelled "ngủ" appears below the list, then a #0077B6 line strikes through it.

### S5 DRM | audio1 27.26 to 30.16
VO: "Đây là bài test DRM của các nhà tâm lý học Deese, Roediger và McDermott."
- "DRM": `drm` image full-width in a rounded frame (radius 32), push-in. A pill "DRM" above it.
- "Deese / Roediger / McDermott": three text-only name chips stagger in under the image, one on each name. No faces.
- Last 1.2s ("McDermott"): the `1995` paper card slides in from the right on top, the title gets the marker sweep, and a chip reads "Roediger & McDermott, 1995".

### S6 Spreading activation | audio1 30.48 to 46.0
VO: "Lý do: trong não, các từ liên quan nối với nhau như mạng lưới. Mỗi từ bạn nghe lại kích hoạt lan sang những từ bên cạnh, gọi là spreading activation. Nghe đủ nhiều từ về giấc ngủ, chữ 'ngủ' tự sáng đèn, và não tưởng mình vừa nghe thấy nó."
- "mạng lưới": full-screen white. The 10 words become grey nodes in a ring, linked by thin lines, and draw in quickly (600ms). The centre node is empty.
- "kích hoạt lan": nodes light up #0077B6 one after another, and ripple pulses travel along the lines toward the centre.
- "spreading activation": term card slides in at the top, pill on "spreading activation". Hold until "Nghe đủ".
- "sáng đèn": the centre node fills #0077B6 with a white "ngủ" label, a glow pulses twice, and all lines flash once.
- "não tưởng": a simple brain icon pops next to the node with a speech bubble "nghe rồi mà!", then a small smug nod.

### S7 Loftus | audio2 0.49 to 10.49
VO: "Nhà tâm lý học Elizabeth Loftus, người cả đời nghiên cứu lời khai nhân chứng, cho hai nhóm xem cùng một video tai nạn xe."
- Whip cut. "Elizabeth Loftus": `elizabeth loftus` photo in a large round crop, upper half, push-in. Card below: tagline "NHÀ TÂM LÝ HỌC", headline "Elizabeth Loftus".
- "lời khai nhân chứng": a subline appears on the card, "chuyên gia về lời khai nhân chứng", with a small #0077B6 scale-of-justice icon.
- "hai nhóm": the photo shrinks to a small circle top-left. `1974` paper card pops in lower-right, small, with a chip "Loftus & Palmer, 1974". Two groups of 3 white characters appear facing one TV.
- "video tai nạn xe": the TV plays a flat animation of two simple cars bumping gently, with a clearly clean result: no glass, no debris.

### S8 Two questions | audio2 10.79 to ~26
VO: Group 1 "va nhau" question, Group 2 "đâm sầm" question, "Nhóm đâm sầm đoán nhanh hơn."
- "Nhóm một": split screen. Left column "NHÓM 1", speech bubble "Hai xe **va** nhau chạy nhanh cỡ nào?".
- "Nhóm hai": right column "NHÓM 2", bubble with "**ĐÂM SẦM**" in the pill. That word alone shakes (3 frames, 6px).
- "đoán nhanh hơn": a speedometer under each column. The needle sweeps: left to a medium level, right to a noticeably higher one. No numbers on screen.

### S9 Broken glass | audio2 ~26 to 45.7
VO: "Một tuần sau, bà gài một câu hỏi bẫy... Bạn có thấy kính vỡ không? Trong video không hề có kính vỡ. Nhưng chữ 'đâm sầm' khiến não tưởng tượng ra một vụ va chạm mạnh, mà va mạnh thì phải vỡ kính. Thế là nhóm này trả lời 'có' nhiều gấp đôi nhóm kia."
- "Một tuần sau": a calendar flips 7 pages (500ms), label "+7 ngày".
- "câu hỏi bẫy": card with tagline "CÂU HỎI BẪY", headline "Bạn có thấy kính vỡ không?", pill on "kính vỡ".
- "không hề có kính vỡ": a mini replay of the clean crash in a small frame, with a mint check "0 mảnh kính".
- "tưởng tượng": a Group 2 character gets a thought bubble. Inside it, the same crash replays faster and more dramatic.
- "phải vỡ kính": cracked-glass shards appear only inside the bubble. The real frame beside it stays clean. The contrast is the point.
- "gấp đôi": 2 bars grow, NHÓM 1 = 1 unit and NHÓM 2 = 2 units. A "x2" pill counts up 1 to 2.

### S10 Misinformation effect | audio2 45.99 to 51.16
VO: "Chỉ một chữ nghe sau sự việc đã viết đè lên ký ức. Hiện tượng này gọi là misinformation effect."
- "viết đè": a film-frame "memory card" shows the clean crash. The word "đâm sầm" flies in, and a #0077B6 pen scribbles glass onto the frame (a write-over animation, 600ms).
- "misinformation effect": term card with tagline "HIỆN TƯỢNG", headline "misinformation effect", pill on "misinformation". Hold until the scene ends.

### S11 Memory is rebuilt | audio2 51.53 to 57.24 (about 5.5s after cuts)
VO: "Ký ức không phải video được lưu sẵn. Mỗi lần nhớ, não dựng lại từ đầu, và đôi khi dựng sai."
- Whip cut. `vid 5.5` full-screen for the whole scene. Start it on "Ký ức". If the clip is 5.5s and the VO is longer, slow the clip to fit (max 0.9x). If shorter, hold the last frame.
- "không phải video": a small #0077B6 "▶ REC" badge top-left gets a strike-through.
- "dựng lại": a frosted card at the bottom, headline "Não dựng lại", pill on "dựng lại".
- "dựng sai": the card text glitches once (2 frames of RGB split) and swaps to "đôi khi dựng sai". This is the only glitch in the video.

### S12 CTA | audio2 57.52 to end
VO: "Follow mình để phần sau cùng tìm hiểu: làm sao các nhà khoa học cài được cả một ký ức tuổi thơ chưa từng xảy ra."
- White background. The logo scales in at the centre-top (spring, 300ms).
- "phần sau": card with tagline "TẬP SAU", headline "Cài ký ức giả", pill on "ký ức giả".
- "Follow": a #0077B6 "Follow" pill pulses once under the card.
- Hold the final frame 0.8s after the VO ends.

## Output
- `episodes/01-false-memory/out/ep01_false_memory.mp4` plus `captions.srt`.
- Report back in 3 lines max: final duration, any anchor word you could not find, anything you changed from this brief.
