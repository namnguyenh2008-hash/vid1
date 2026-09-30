# 1 Minute Psychology: video editor

Kênh TikTok tiếng Việt, mỗi tập giải thích một thuật ngữ tâm lý học. Người dùng: hn (sinh viên tâm lý, USYD). Trả lời bằng tiếng Việt, ngắn gọn. Không dùng em dash.

## Vai trò
Claude Code là EDITOR. Không viết nội dung. Cowork viết script và brief hậu kỳ; Claude Code dựng đúng theo brief, khớp voice.
Script không khớp 100% với lời thu âm: dùng script cho nội dung chữ trên màn hình, còn phụ đề và timing lấy theo voice thật (ASR).

## Mỗi tập
`episodes/NN-slug/`: `brief.md`, `src/` (voice, ảnh, video), `out/` (mp4 + captions.srt).
1. `bash scripts/setup.sh` nếu môi trường chưa sẵn sàng (SessionStart hook tự chạy).
2. `episodes/NN/cut_audio.py`: highpass 80Hz, afftdn, cắt pause >0.25s còn 0.12s, loudnorm -14 LUFS.
3. `scripts/asr.py vo16.wav words.json`: timestamp từng từ (sherpa-onnx zipformer tiếng Việt; HuggingFace bị chặn nên không dùng Whisper chuẩn).
4. Dựng composition Hyperframes, trigger cue theo anchor word, không theo giây cứng.
5. Render, xuất 1080x1920 30fps H.264 10Mbps + AAC 48kHz.

## Spec cố định
- Safe zone TikTok: top 150px, bottom 480px, right 150px.
- Phụ đề: 5 đến 7 từ/dòng, tối đa 2 dòng, chữ trắng trên pill đen 55%, đáy ở y=1440.
- Audio first. Ảnh không bao giờ đứng yên. Điểm nhấn mới mỗi 3 đến 5s. Hook ở 0:00.
- Brand: nền trắng, accent #0077B6, text #1A1A1A, mint #3CE8B4. Font Be Vietnam Pro. Logo `brand/logo.svg`.

## Môi trường cloud
- CDN (jsdelivr) và HuggingFace bị chặn. Chỉ npm, PyPI, GitHub release downloads đi qua.
- GSAP và font bundle local (npm i gsap @fontsource/be-vietnam-pro).
- Model ASR: GitHub release k2-fsa/sherpa-onnx `asr-models/sherpa-onnx-zipformer-vi-2025-04-20`.
