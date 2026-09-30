# Build the Hyperframes composition for EP01 from words.json (ASR word timestamps).
import json, math, os, re, shutil, subprocess, sys

EP = os.path.dirname(os.path.abspath(__file__))
SRC, COMP = f"{EP}/src", f"{EP}/comp"
ROOT = os.path.dirname(os.path.dirname(EP))
W = json.load(open(f"{SRC}/words.json"))
for w in W:
    w["u"] = w["w"].upper()
VO_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SRC}/vo.wav"]))
missing = []


def find(seq, after=0.0, before=1e9, default=None):
    """Time of the first word of `seq` (tokens may hold A|B alternatives) at or after `after`."""
    toks = [t.split("|") for t in seq.upper().split()]
    for i, w in enumerate(W):
        if w["t"] < after - 1e-6 or w["t"] > before:
            continue
        if all(i + k < len(W) and W[i + k]["u"] in alts for k, alts in enumerate(toks)):
            return w["t"]
    missing.append(seq)
    return default if default is not None else after


def idx_at(t):
    return min(range(len(W)), key=lambda i: abs(W[i]["t"] - t))


def after_word(t):
    """Start time of the word following the word at t."""
    i = idx_at(t)
    return W[i + 1]["t"] if i + 1 < len(W) else VO_DUR


# ---------- anchors ----------
T = {}
T["S1"] = 0.0
T["S1_tri"] = find("TRÍ NHỚ")
T["S1_nghe"] = find("NGHE KỸ", T["S1_tri"])
LIST = [("Giường", "GIƯỜNG"), ("Nghỉ ngơi", "NGHỈ NGƠI"), ("Mệt", "MỆT"), ("Mơ", "MƠ"), ("Chợp mắt", "CHỢP|TRƯỢP|CHỚP MẮT"),
        ("Chăn", "CHĂN"), ("Ngáy", "NGÁY"), ("Gối", "GỐI"), ("Ngáp", "NGÁP"), ("Đêm", "ĐÊM")]
T["S2"] = find("GIƯỜNG", T["S1_nghe"])
on, prev = [], T["S2"]
for disp, key in LIST:
    t = find(key, prev, prev + 3.0, default=-1)
    if t < 0:
        missing.pop()
        on.append(None)
    else:
        on.append(t)
        prev = t + 0.05
# a word not heard in the VO (e.g. "Chăn") pops halfway between its neighbours
for i, t in enumerate(on):
    if t is None:
        a = on[i - 1]
        b = next(x for x in on[i + 1:] if x is not None)
        on[i] = round((a + b) / 2, 3)
        missing.append(f"{LIST[i][0]} (không có trong voice, chèn giữa hai từ bên cạnh)")
T["list"] = on
T["S3"] = after_word(on[-1])
T["S3_ngu"] = find("NGỦ", T["S3"])
T["S4"] = find("NẾU BẠN", T["S3_ngu"])
T["S4_chuc"] = find("CHÚC MỪNG", T["S4"])
T["S4_kyuc"] = find("KÝ ỨC GIẢ", T["S4"])
T["S4_khong"] = find("KHÔNG HỀ CÓ", T["S4_kyuc"])
T["S5"] = find("ĐÂY LÀ", T["S4_khong"])
T["S5_drm"] = find("D|DRM|STED|TEST", T["S5"])
T["S5_n1"] = find("DIS|ĐI|DI|DEESE", T["S5_drm"])
T["S5_n2"] = find("GOOGLE|RODIGER|ROEDIGER", T["S5_n1"], default=T["S5_n1"] + 0.6)
T["S5_n3"] = find("MARKYMOD|MCDERMOTT|MẮC", T["S5_n2"], default=T["S5_n2"] + 0.6)
T["S6"] = find("LÝ DO", T["S5_n3"])
T["S5_paper"] = min(T["S5_n3"], T["S6"] - 1.2)
T["S6_mang"] = find("MẠNG LƯỚI", T["S6"])
T["S6_kich"] = find("KÍCH HOẠT", T["S6_mang"])
T["S6_term"] = find("SREING|SPREADING|SPRE", T["S6_kich"], default=T["S6_kich"] + 2.5)
T["S6_nghedu"] = find("NGHE ĐỦ", T["S6_term"])
T["S6_sang"] = find("SÁNG ĐÈN", T["S6_nghedu"])
T["S6_tuong"] = find("TƯỞNG", T["S6_sang"])
T["S7"] = find("NHÀ TÂM LÝ HỌC", T["S6_tuong"])
T["S7_name"] = after_word(find("HỌC", T["S7"]))
T["S7_loi"] = find("LỜI KHAI", T["S7"])
T["S7_hai"] = find("HAI NHÓM", T["S7_loi"])
T["S7_video"] = find("VIDEO TAI NẠN", T["S7_hai"])
T["S8"] = find("NHÓM MỘT", T["S7_video"])
T["S8_hai"] = find("NHÓM HAI", T["S8"])
T["S8_dam"] = find("ĐÂM", T["S8_hai"], default=T["S8_hai"] + 1.2)
T["S8_doan"] = find("ĐOÁN NHANH", T["S8_hai"])
T["S9"] = find("MỘT TUẦN SAU", T["S8_doan"])
T["S9_bay"] = find("CÂU HỎI BẪY", T["S9"])
T["S9_khong"] = find("KHÔNG HỀ CÓ KÍNH", T["S9_bay"])
T["S9_tuong"] = find("TƯỞNG", T["S9_khong"])
T["S9_vo"] = find("VỠ KÍNH", T["S9_tuong"])
T["S9_gap"] = find("GẤP ĐÔI", T["S9_vo"])
T["S10"] = find("VẬY ĐẤY", T["S9_gap"])
T["S10_de"] = find("ĐÈ", T["S10"])
T["S10_mis"] = find("MIXION|MISINFORMATION|MIS", T["S10_de"], default=T["S10_de"] + 2.5)
T["S11"] = find("KÝ ỨC KHÔNG PHẢI", T["S10_mis"])
T["S11"] = find("THẬT RA", T["S11"] - 1.2, T["S11"], default=T["S11"])
T["S11_khong"] = find("KHÔNG PHẢI", T["S11"])
T["S11_dung"] = find("DỰNG LẠI", T["S11_khong"])
T["S11_sai"] = find("DỰNG SAI", T["S11_dung"])
T["S12"] = find("HÃY CÙNG", T["S11_sai"])
T["S12_follow"] = find("FOU|FOLLOW|FO", T["S12"], default=T["S12"] + 0.4)
T["S12_phan"] = find("PHẦN SAU", T["S12"])
T["END"] = round(VO_DUR + 0.8, 3)
T = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in T.items()}

# ---------- captions ----------
FIX = [("STED D M", "test DRM"), ("TEST D M", "test DRM"), ("D M", "DRM"), ("DIS GOOGLE VÀ MARKYMOD", "Deese, Roediger và McDermott"),
       ("SREING ATI VEION", "spreading activation"), ("ELIPAS", "Elizabeth Loftus"), ("ĐÂM SÂU", "đâm sầm"), ("BÀ DÀI", "bà gài"),
       ("MIXION EF", "misinformation effect"), ("FOU", "follow"), ("LISHEN", "list"), ("TRƯỢP", "chợp"), ("VIDEO", "video")]
disp = []  # (text, t)
i = 0
while i < len(W):
    for src, dst in FIX:
        s = src.split()
        if [x["u"] for x in W[i:i + len(s)]] == s:
            d = dst.split()
            for k, word in enumerate(d):
                disp.append([word, W[i + min(k * len(s) // len(d), len(s) - 1)]["t"]])
            i += len(s)
            break
    else:
        disp.append([W[i]["w"].lower(), W[i]["t"]])
        i += 1
SENT = ["BẠN CÓ BAO GIỜ", "HÃY CÙNG MÌNH", "Ở TRONG", "NẾU BẠN", "CHÚC MỪNG", "THẬT RA KHÔNG", "ĐÂY LÀ", "LÝ DO", "MỖI LẦN BẠN",
        "HIỆN TƯỢNG NÀY", "NGHE ĐỦ", "NHÀ TÂM LÝ HỌC", "BÀ ĐÃ", "NHÓM MỘT", "NHÓM HAI", "NHÓM ĐÂM", "MỘT TUẦN", "BẠN CÓ THẤY",
        "TRONG VIDEO", "NHƯNG NHÓM", "THẾ LÀ", "VẬY ĐẤY", "CHỈ MỘT", "THẬT RA KÝ", "MỖI LẦN NHỚ", "HÃY CÙNG FOU", "HÃY CÙNG FOLLOW"]
starts = set()
for s in SENT:
    toks = s.split()
    for j in range(len(W)):
        if [x["u"] for x in W[j:j + len(toks)]] == toks:
            starts.add(W[j]["t"])
starts |= {T[k] for k in T if re.fullmatch(r"S\d+", k)}
s2_lo, s2_hi = T["S2"] - 0.05, T["S3"] - 0.05
sentences, cur = [], []
for word, t in disp:
    if s2_lo <= t < s2_hi:
        continue
    if t in starts and cur:
        sentences.append(cur)
        cur = []
    cur.append([word, t])
if cur:
    sentences.append(cur)
groups = []
for s in sentences:
    s[0][0] = s[0][0][:1].upper() + s[0][0][1:]
    n = math.ceil(len(s) / 6)
    size = math.ceil(len(s) / n)
    for k in range(0, len(s), size):
        groups.append(s[k:k + size])
caps = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else VO_DUR
    end = min(nxt, g[-1][1] + 1.2)
    if s2_lo <= nxt <= s2_hi + 0.1:
        end = min(end, s2_lo)
    caps.append({"s": g[0][1], "e": round(end, 3), "w": g})


def srt_t(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


os.makedirs(f"{EP}/out", exist_ok=True)
with open(f"{EP}/out/captions.srt", "w") as f:
    for k, c in enumerate(caps, 1):
        f.write(f"{k}\n{srt_t(c['s'])} --> {srt_t(c['e'])}\n{' '.join(w for w, _ in c['w'])}\n\n")

# ---------- assets ----------
os.makedirs(f"{COMP}/assets", exist_ok=True)
for f in ["bed.jpg", "drm.png", "paper1995.png", "paper1974.png", "loftus.jpg", "vo.wav"]:
    shutil.copy(f"{SRC}/{f}", f"{COMP}/assets/{f}")
shutil.copy(f"{ROOT}/brand/logo.svg", f"{COMP}/assets/logo.svg")
# S11 clip: crop to 9:16, slow to fit (max 0.9x), then hold last frame
s11_len = T["S12"] - T["S11"]
clip_len = 5.52
rate = max(0.9, clip_len / s11_len) if s11_len > clip_len else 1.0
pad = max(0.0, s11_len - clip_len / rate) + 0.2
vf = f"crop=ih*9/16:ih,scale=1080:1920,setpts=PTS/{rate},fps=30,tpad=stop_mode=clone:stop_duration={pad:.3f}"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/vid55.mp4", "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16",
                "-pix_fmt", "yuv420p", f"{COMP}/assets/vid55.mp4"], check=True)

html = open(f"{EP}/template.html").read()
html = (html.replace("__T__", json.dumps(T)).replace("__CAPS__", json.dumps(caps, ensure_ascii=False))
        .replace("__DUR__", str(T["END"])).replace("__VODUR__", f"{VO_DUR:.3f}")
        .replace("__S11__", str(T["S11"])).replace("__S11LEN__", f"{s11_len:.3f}"))
open(f"{COMP}/index.html", "w").write(html)
json.dump(T, open(f"{EP}/anchors.json", "w"), indent=1)
print(f"duration {T['END']}s | S11 clip rate {rate:.2f} | captions {len(caps)}")
print("MISSING:", missing if missing else "none")
