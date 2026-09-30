# EP01 v3 audio: highpass 80Hz + afftdn, cut pauses >0.3s to 0.15s (keep the word list and the beat
# after "Không hề có từ ngủ"), then two-pass loudnorm to -14 LUFS / -1 dBTP at 48 kHz.
import json, os, re, subprocess, sys
import numpy as np, soundfile as sf

EP = os.path.dirname(os.path.abspath(__file__))
SRC = f"{EP}/src"
IN = f"{SRC}/voice/audio_ep1.mp3"
SR, MAXP, KEEP, BEAT = 48000, 0.30, 0.15, 0.80
# protected windows in raw seconds: the 10-word list; the pause after "ngủ" (S4) is stretched to BEAT
LIST = (4.30, 12.40)
NGU_BEAT = (18.20, 18.70)

subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", IN, "-af", "highpass=f=80,afftdn=nf=-30", "-ac", "1", "-ar", str(SR),
                "-c:a", "pcm_f32le", f"{SRC}/clean.wav"], check=True)
a, _ = sf.read(f"{SRC}/clean.wav", dtype="float32")
# silence map: 10ms RMS below -45 dB relative to the file's loud level (95th percentile)
hop = SR // 100
rms = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
db = 20 * np.log10(rms) - 20 * np.log10(np.percentile(rms, 95))
quiet = db < -38
sil, i = [], 0
while i < len(quiet):
    if quiet[i]:
        j = i
        while j < len(quiet) and quiet[j]:
            j += 1
        sil.append((i / 100, j / 100))
        i = j
    else:
        i += 1
dur = len(a) / SR
keep, t, beat_done = [], 0.0, False
for s, e in sil:
    if s <= 0.01:  # lead-in: keep 0.05s
        t = max(0.0, e - 0.05)
        continue
    if e >= dur - 0.01:  # tail: keep 0.3s
        keep.append((t, min(dur, s + 0.3)))
        t = dur
        break
    if NGU_BEAT[0] <= s <= NGU_BEAT[1] and not beat_done:
        keep.append((t, s))
        keep.append(("pad", BEAT - (e - s)))  # stretch the natural pause to BEAT seconds
        t = s
        beat_done = True
        continue
    if LIST[0] <= s and e <= LIST[1]:
        continue
    if e - s > MAXP:
        keep.append((t, s + KEEP / 2))
        t = e - KEEP / 2
if t < dur:
    keep.append((t, dur))
fade = int(0.006 * SR)
out, cmap, T = [], [], 0.0
for k in keep:
    if k[0] == "pad":
        n = int(max(0, k[1]) * SR)
        out.append(np.zeros(n, "float32"))
        cmap.append(dict(pad=round(n / SR, 3), out_start=round(T, 3)))
        T += n / SR
        continue
    s, e = k
    seg = a[int(s * SR):int(e * SR)].copy()
    n = min(fade, len(seg) // 2)
    seg[:n] *= np.linspace(0, 1, n)
    seg[-n:] *= np.linspace(1, 0, n)
    cmap.append(dict(src_start=round(s, 3), src_end=round(e, 3), out_start=round(T, 3)))
    out.append(seg)
    T += len(seg) / SR
sf.write(f"{SRC}/vo_cut.wav", np.concatenate(out), SR)
json.dump(cmap, open(f"{SRC}/cutmap.json", "w"), indent=0)

# loudness: measure, apply static gain to -14 LUFS, then a true-peak-safe limiter at -1 dBTP; iterate once
def measure(f):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
gain = -14 - measure(f"{SRC}/vo_cut.wav")
for _ in range(3):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/vo_cut.wav", "-af",
                    f"volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.87:attack=2:release=60:level=false,aresample={SR}",
                    "-c:a", "pcm_s16le", f"{SRC}/vo.wav"], check=True)
    err = -14 - measure(f"{SRC}/vo.wav")
    if abs(err) < 0.15:
        break
    gain += err
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/vo.wav", "-ac", "1", "-ar", "16000", f"{SRC}/vo16.wav"], check=True)
os.remove(f"{SRC}/clean.wav")
print(f"raw {dur:.2f}s -> cut {T:.2f}s | pauses cut {sum(1 for c in cmap if 'src_start' in c) - 1}")
