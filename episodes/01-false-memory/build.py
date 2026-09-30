# Build the EP01 v3 Hyperframes composition: align script.md to ASR word times, derive anchors, captions, assets.
import difflib, json, math, os, re, shutil, subprocess
import numpy as np, soundfile as sf

EP = os.path.dirname(os.path.abspath(__file__))
SRC, COMP = f"{EP}/src", f"{EP}/comp"
ROOT = os.path.dirname(os.path.dirname(EP))
ASR = json.load(open(f"{SRC}/words.json"))
VO_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SRC}/vo.wav"]))
missing = []

# ---------- voiced mask (10ms) from the final voice ----------
a, sr = sf.read(f"{SRC}/vo.wav", dtype="float32")
hop = sr // 100
rms = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
voiced = 20 * np.log10(rms) > -42


def snap(t):
    """ASR sometimes stamps a word inside a pause; move it to where the voice resumes."""
    i = int(round(t * 100))
    if i >= len(voiced) or voiced[i]:
        return t
    j = i
    while j < len(voiced) and not voiced[j]:
        j += 1
    return round(j / 100, 3) if (j - i) >= 12 else t


# ---------- align script words to ASR words ----------
norm = lambda s: re.sub(r"[^\wÀ-ỹ]", "", s.lower())
script = open(f"{EP}/script.md").read().split()
sn = [norm(w) for w in script]
an = [norm(w["w"]) for w in ASR]
tt = [None] * len(script)
for blk in difflib.SequenceMatcher(None, sn, an, autojunk=False).get_matching_blocks():
    for k in range(blk.size):
        tt[blk.a + k] = ASR[blk.b + k]["t"]
known = [i for i, t in enumerate(tt) if t is not None]
for i in range(len(tt)):
    if tt[i] is None:
        lo = max([k for k in known if k < i], default=None)
        hi = min([k for k in known if k > i], default=None)
        if lo is None:
            tt[i] = 0.0
        elif hi is None:
            tt[i] = tt[lo] + 0.25 * (i - lo)
        else:
            tt[i] = tt[lo] + (tt[hi] - tt[lo]) * (i - lo) / (hi - lo)
tt = [snap(round(t, 3)) for t in tt]
for i in range(1, len(tt)):
    tt[i] = max(tt[i], tt[i - 1])
WORDS = [(w, t) for w, t in zip(script, tt)]


def find(seq, after=0.0, default=None):
    toks = [norm(x) for x in seq.split()]
    for i in range(len(sn)):
        if tt[i] >= after - 1e-6 and sn[i:i + len(toks)] == toks:
            return tt[i]
    missing.append(seq)
    return default if default is not None else after


def voice_onsets(t0, t1, gap=0.12):
    out = []
    for i in range(int(t0 * 100), int(t1 * 100)):
        if voiced[i] and not voiced[max(0, i - int(gap * 100)):i].any():
            out.append(round(i / 100, 3))
    return out


# ---------- anchors ----------
T = {"S1": 0.0}
T["S1_tri"] = find("Trí nhớ")
T["S1_rat"] = find("Chuột tím")
T["S1_10"] = find("10 từ", T["S1_rat"])
T["S2"] = find("Giường.", T["S1_10"])
T["S3"] = find("Có từ", T["S2"])
on = voice_onsets(T["S2"] - 0.1, T["S3"] - 0.1)
if len(on) != 10:
    missing.append(f"list onsets ({len(on)}/10)")
    on = (on + [on[-1] + 0.7 * k for k in range(1, 11)])[:10]
T["list"] = on
T["S3_ngu"] = find("\"ngủ\"", T["S3"])
T["S4"] = find("Nếu bạn", T["S3"])
T["S4_chuc"] = find("chúc mừng", T["S4"])
T["S4_kyuc"] = find("ký ức giả.", T["S4"])
T["S4_khong"] = find("Không hề có", T["S4_kyuc"])
T["S4_lan"] = find("Lần đầu", T["S4_khong"])
T["S4_chuot"] = find("chuột tím cũng", T["S4_lan"])
T["S5"] = find("Đây là", T["S4_chuot"])
T["S5_drm"] = find("DRM", T["S5"])
T["S5_nha"] = find("nhà tâm lý học", T["S5"])
T["S5_n1"] = find("Deese,", T["S5_nha"])
T["S5_n2"] = find("Roediger", T["S5_n1"])
T["S5_n3"] = find("McDermott.", T["S5_n2"])
T["S6"] = find("Lý do:", T["S5_n3"])
T["S6_mang"] = find("mạng lưới.", T["S6"])
T["S6_kich"] = find("kích hoạt lan", T["S6_mang"])
T["S6_term"] = find("spreading activation.", T["S6_kich"])
T["S6_nghedu"] = find("Nghe đủ", T["S6_term"])
T["S6_sang"] = find("sáng đèn,", T["S6_nghedu"])
T["S6_tuong"] = find("tưởng mình vừa", T["S6_sang"])
T["S7"] = find("Nhà tâm lý học Elizabeth", T["S6_tuong"])
T["S7_name"] = find("Elizabeth", T["S7"])
T["S7_loi"] = find("lời khai", T["S7"])
T["S7_hai"] = find("hai nhóm", T["S7_loi"])
T["S7_video"] = find("video tai nạn", T["S7_hai"])
T["S8"] = find("Nhóm một", T["S7_video"])
T["S8_va"] = find("va nhau", T["S8"])
T["S8_hai"] = find("Nhóm hai:", T["S8_va"])
T["S8_dam"] = find("đâm sầm", T["S8_hai"])
T["S8_nhom"] = find("Nhóm \"đâm", T["S8_dam"])
T["S8_nhanh"] = find("nhanh hơn.", T["S8_nhom"])
T["S9"] = find("Một tuần sau,", T["S8_nhanh"])
T["S9_bay"] = find("câu hỏi bẫy", T["S9"])
T["S9_q"] = find("\"Bạn có thấy", T["S9_bay"])
T["S9_khong"] = find("không hề có kính", T["S9_q"])
T["S9_tuong"] = find("tưởng tượng", T["S9_khong"])
T["S9_vo"] = find("vỡ kính.", T["S9_tuong"])
T["S9_gap"] = find("gấp đôi", T["S9_vo"])
T["S10"] = find("Chỉ một chữ", T["S9_gap"])
T["S10_de"] = find("viết đè", T["S10"])
T["S10_hien"] = find("Hiện tượng này", T["S10_de"])
T["S10_mis"] = find("misinformation", T["S10_hien"])
T["S11"] = find("Ký ức không phải", T["S10_mis"])
T["S11_khong"] = find("không phải video", T["S11"])
T["S11_dung"] = find("dựng lại", T["S11_khong"])
T["S11_sai"] = find("dựng sai.", T["S11_dung"])
T["S12"] = find("Follow", T["S11_sai"])
T["S12_tap"] = find("tập sau", T["S12"])
T["S12_cai"] = find("cài được", T["S12_tap"])
T["VO_END"] = round(VO_DUR, 3)
T["END"] = round(VO_DUR + 0.8, 3)
T["WORDS"] = [t for _, t in WORDS]
T = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in T.items()}

# ---------- captions: script text, voice timing; none during the word list ----------
starts = {T[k] for k in T if re.fullmatch(r"S\d+", k)}
sentences, cur = [], []
for w, t in WORDS:
    if T["S2"] - 0.05 <= t < T["S3"] - 0.05:
        continue
    if cur and (t in starts and cur[-1][1] < t):
        sentences.append(cur)
        cur = []
    cur.append([w, t])
    if re.search(r"[.?!:]\"?$", w):
        sentences.append(cur)
        cur = []
if cur:
    sentences.append(cur)
groups = []
for s in sentences:
    n = math.ceil(len(s) / 7)
    size = math.ceil(len(s) / n)
    groups += [s[k:k + size] for k in range(0, len(s), size)]
caps = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else VO_DUR + 0.5
    end = min(nxt, g[-1][1] + 1.0)
    if g[-1][1] < T["S2"] <= nxt:
        end = min(end, T["S2"])
    caps.append({"s": g[0][1], "e": round(end, 3), "w": g})


def srt_t(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


os.makedirs(f"{EP}/out", exist_ok=True)
with open(f"{EP}/out/captions.srt", "w") as f:
    for k, c in enumerate(caps, 1):
        f.write(f"{k}\n{srt_t(c['s'])} --> {srt_t(c['e'])}\n{' '.join(w for w, _ in c['w'])}\n\n")

# ---------- assets ----------
if os.path.exists(f"{COMP}/assets"):
    shutil.rmtree(f"{COMP}/assets")
os.makedirs(f"{COMP}/assets")
for fn in ["drm.png", "1995.png", "1974.png", "elizabeth_loftus.jpg", "logo_rat_avatar.png"]:
    shutil.copy(f"{SRC}/assets/{fn}", f"{COMP}/assets/{fn}")
shutil.copy(f"{SRC}/vo.wav", f"{COMP}/assets/vo.wav")
shutil.copy(f"{ROOT}/brand/logo.svg", f"{COMP}/assets/logo.svg")
if os.path.exists(f"{COMP}/fonts"):
    shutil.rmtree(f"{COMP}/fonts")
os.makedirs(f"{COMP}/vendor/fonts", exist_ok=True)
shutil.copy(f"{ROOT}/vendor/gsap.min.js", f"{COMP}/vendor/gsap.min.js")
for fn in os.listdir(f"{ROOT}/vendor/fonts"):
    shutil.copy(f"{ROOT}/vendor/fonts/{fn}", f"{COMP}/vendor/fonts/{fn}")
# S11 clip: centre-crop to 9:16, slow to at most 0.9x only if the scene is longer than the clip, hold the last frame
s11_len = round(T["S12"] - T["S11"], 3)
clip_len = 5.52
rate = max(0.9, clip_len / s11_len) if s11_len > clip_len else 1.0
pad = max(0.0, s11_len - clip_len / rate) + 0.3
vf = f"crop=ih*9/16:ih,scale=1440:2560:flags=lanczos,setpts=PTS/{rate},fps=30,tpad=stop_mode=clone:stop_duration={pad:.3f}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/assets/vid_5_5.mp4", "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", f"{COMP}/assets/vid_5_5.mp4"], check=True)

html = open(f"{EP}/template.html").read()
html = (html.replace("__T__", json.dumps(T)).replace("__CAPS__", json.dumps(caps, ensure_ascii=False))
        .replace("__DUR__", str(T["END"])).replace("__VODUR__", f"{VO_DUR:.3f}")
        .replace("__S11__", str(T["S11"])).replace("__S11LEN__", f"{s11_len:.3f}"))
open(f"{COMP}/index.html", "w").write(html)
if not os.path.exists(f"{COMP}/package.json"):
    open(f"{COMP}/package.json", "w").write('{"name":"ep01","private":true}\n')
json.dump({k: v for k, v in T.items() if k != "WORDS"}, open(f"{EP}/anchors.json", "w"), indent=1)
print(f"duration {T['END']}s | S11 {s11_len}s clip rate {rate:.2f} | captions {len(caps)}")
print("MISSING:", missing if missing else "none")
