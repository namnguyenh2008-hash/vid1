# Build the Hyperframes composition for EP02 from src/words.json (ASR word timestamps).
import json, math, os, re, shutil, subprocess

EP = os.path.dirname(os.path.abspath(__file__))
SRC, COMP = f"{EP}/src", f"{EP}/comp"
ROOT = os.path.dirname(os.path.dirname(EP))
W = json.load(open(f"{SRC}/words.json"))
for w in W:
    w["u"] = w["w"].upper()
VO_DUR = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SRC}/vo.wav"]))
missing = []


def find(seq, after=0.0, before=1e9, default=None):
    toks = [t.split("|") for t in seq.upper().split()]
    for i, w in enumerate(W):
        if w["t"] < after - 1e-6 or w["t"] > before:
            continue
        if all(i + k < len(W) and W[i + k]["u"] in alts for k, alts in enumerate(toks)):
            return w["t"]
    missing.append(seq)
    return default if default is not None else after


T = {"S1": 0.0}
T["S1_prev"] = find("TẬP TRƯỚC")
T["S1_rat"] = find("CHUỘT TÍM")
T["S2"] = find("CÂU HỎI", T["S1_rat"])
T["S2_5"] = find("NĂM TUỔI", T["S2"])
T["S2_q"] = find("NHỚ RA KHÔNG", T["S2_5"])
T["S3"] = find("NGHE", T["S2_q"])
T["S3_tranh"] = find("BỨC TRANH", T["S3"])
T["S3_to"] = find("TÔ THÊM", T["S3_tranh"])
T["S3_do"] = find("MÀU ĐỎ", T["S3_to"])
T["S3_quen"] = find("QUÊN", T["S3_do"])
T["S4"] = find("NĂM MỘT NGHÌN", T["S3_quen"])
T["S4_nha"] = find("NHÀ TÂM LÝ HỌC", T["S4"])
T["S4_lof"] = find("ELIPAS|ELIZABETH", T["S4"], default=T["S4_nha"] + 0.6)
T["S4_pick"] = find("CỘNG SỰ", T["S4_lof"])
T["S5"] = find("HỌ HỎI", T["S4_pick"])
T["S5_24"] = find("HAI MƯƠI BỐN", T["S5"])
T["S5_3"] = find("BA TRUYỆN|CHUYỆN", T["S5_24"])
T["S5_len"] = find("LÉN", T["S5_3"])
T["S5_bia"] = find("TRUYỆN|CHUYỆN BỊA", T["S5_len"])
T["S5_ttm"] = find("TRUNG TÂM", T["S5_bia"])
T["S5_khoc"] = find("KHÓC", T["S5_ttm"])
T["S5_ba"] = find("BÀ CỤ", T["S5_khoc"])
T["S6"] = find("NGƯỜI THAM GIA ĐỌC", T["S5_ba"])
T["S6_hoi"] = find("HỎI ĐI HỎI", T["S6"])
T["S7"] = find("KẾT QUẢ", T["S6_hoi"])
T["S7_cu"] = find("CỨ", T["S7"])
T["S7_mot"] = find("MỘT NGƯỜI", T["S7_cu"])
T["S7_ke"] = find("TỰ KỂ", T["S7_mot"])
T["S8"] = find("CHUỘT TÍM", T["S7_ke"])
T["S8_lac"] = find("BỊ LẠC", T["S8"])
T["S9"] = find("VÌ SAO", T["S8_lac"])
T["S9_r1"] = find("HỢP LÝ", T["S9"])
T["S9_r2"] = find("XÁC NHẬN", T["S9_r1"])
T["S9_r3"] = find("NÃO KHÔNG", T["S9_r2"])
T["S9_pb"] = find("PHÂN BIỆT", T["S9_r3"])
T["S9_term"] = find("SHOWS|SOURCE", T["S9_pb"], default=T["S9_pb"] + 4)
T["S10"] = find("FORD|FOLLOW|FO", T["S9_term"], default=T["S9_term"] + 2.5)
T["S10_tap"] = find("TẬP SAU", T["S10"])
T["END"] = round(VO_DUR + 0.8, 3)
T["WORDS"] = [w["t"] for w in W]
T = {k: (round(v, 3) if isinstance(v, float) else v) for k, v in T.items()}

# ---------- captions ----------
FIX = [("NĂM MỘT NGHÌN CHÍN TRĂM CHÍN MƯƠI LĂM", "năm 1995"), ("HAI MƯƠI BỐN", "24"), ("NĂM TUỔI", "5 tuổi"),
       ("ELIPAS", "Elizabeth Loftus"), ("IM PICRO", "Jacqueline Pickrell"), ("SHOWS CONTUSION", "source confusion"),
       ("SHOWS CONTFUSION", "source confusion"), ("FORD", "Follow"), ("BÚT CHỈ", "bút chì"), ("BA TRUYỆN", "3 chuyện"),
       ("BỐN TRUYỆN", "4 chuyện"), ("MỘT TRUYỆN", "1 chuyện"), ("CỨ BỐN NGƯỜI THÌ CÓ MỘT NGƯỜI", "cứ 4 người thì có 1 người")]
disp, i = [], 0
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
SENT = ["TẬP TRƯỚC", "TỪ GIỜ", "CÂU HỎI", "BẠN CÓ NHỚ", "NGHE THÌ", "NHƯNG THỬ", "KÝ ỨC GIỐNG", "MỖI LẦN", "NẾU CÓ", "BẠN SẼ",
        "LÂU DẦN", "HỌ HỎI", "RỒI HỌ", "HỒI KHOẢNG", "NGƯỜI THAM GIA ĐỌC", "BẠN CÒN", "KẾT QUẢ", "CÓ NGƯỜI CÒN", "CHUỘT TÍM CŨNG",
        "VÌ SAO", "VÌ CHUYỆN", "VÌ NGƯỜI", "VÀ VÌ", "HIỆN TƯỢNG", "NHẦM LẪN", "FORD"]
starts = set()
for s in SENT:
    toks = s.split()
    for j in range(len(W)):
        if [x["u"] for x in W[j:j + len(toks)]] == toks:
            starts.add(W[j]["t"])
starts |= {T[k] for k in T if re.fullmatch(r"S\d+", k)} | {T["S4"]}
sentences, cur = [], []
for word, t in disp:
    if t in starts and cur:
        sentences.append(cur)
        cur = []
    cur.append([word, t])
sentences.append(cur)
groups = []
for s in sentences:
    s[0][0] = s[0][0][:1].upper() + s[0][0][1:]
    n = math.ceil(len(s) / 6)
    size = math.ceil(len(s) / n)
    groups += [s[k:k + size] for k in range(0, len(s), size)]
caps = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0][1] if gi + 1 < len(groups) else VO_DUR
    caps.append({"s": g[0][1], "e": round(min(nxt, g[-1][1] + 1.2), 3), "w": g})


def srt_t(x):
    ms = int(round(x * 1000))
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


os.makedirs(f"{EP}/out", exist_ok=True)
with open(f"{EP}/out/captions.srt", "w") as f:
    for k, c in enumerate(caps, 1):
        f.write(f"{k}\n{srt_t(c['s'])} --> {srt_t(c['e'])}\n{' '.join(w for w, _ in c['w'])}\n\n")

# ---------- assets ----------
os.makedirs(f"{COMP}/assets", exist_ok=True)
for f in os.listdir(f"{SRC}/assets"):
    dst = f"{COMP}/assets/{f}"
    if f.endswith(".webp"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SRC}/assets/{f}", "-q:v", "3", dst.replace(".webp", ".jpg")], check=True)
    else:
        shutil.copy(f"{SRC}/assets/{f}", dst)
shutil.copy(f"{SRC}/vo.wav", f"{COMP}/assets/vo.wav")
shutil.copy(f"{SRC}/brand/logo.svg", f"{COMP}/assets/logo.svg")
for d in ["vendor"]:
    if not os.path.exists(f"{COMP}/{d}"):
        os.makedirs(f"{COMP}/{d}/fonts")
        shutil.copy(f"{ROOT}/vendor/gsap.min.js", f"{COMP}/{d}/gsap.min.js")
        for fn in os.listdir(f"{ROOT}/vendor/fonts"):
            shutil.copy(f"{ROOT}/vendor/fonts/{fn}", f"{COMP}/{d}/fonts/{fn}")

html = open(f"{EP}/template.html").read()
html = (html.replace("__T__", json.dumps(T)).replace("__CAPS__", json.dumps(caps, ensure_ascii=False))
        .replace("__DUR__", str(T["END"])).replace("__VODUR__", f"{VO_DUR:.3f}"))
open(f"{COMP}/index.html", "w").write(html)
if not os.path.exists(f"{COMP}/package.json"):
    open(f"{COMP}/package.json", "w").write('{"name":"ep02","private":true}\n')
json.dump({k: v for k, v in T.items() if k != "WORDS"}, open(f"{EP}/anchors.json", "w"), indent=1)
print(f"duration {T['END']}s | captions {len(caps)}")
print("MISSING:", missing if missing else "none")
