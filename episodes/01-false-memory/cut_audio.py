# Cut pauses >0.25s to 0.12s (keep S2 word-list pauses), join, loudnorm.
import soundfile as sf, numpy as np, json
SR=48000; KEEP=0.12; fade=int(0.008*SR)
def segs(i, dur, protect):
    sil=[tuple(map(float,l.split())) for l in open(f'sil{i}.txt')]
    keep=[]; t=0.0
    for s,e in sil:
        if protect[0] <= s and e <= protect[1]: continue
        if s==0: s=max(0,e-0.10)          # lead-in: keep 0.10s
        mid_s = s+KEEP/2; mid_e = e-KEEP/2
        if mid_e>mid_s: keep.append((t,mid_s)); t=mid_e
    keep.append((t,dur)); return keep
out=[]; cmap=[]; T=0.0
for i,prot in [(1,(6.5,14.5)),(2,(-1,-1))]:
    a,_=sf.read(f'a{i}.wav',dtype='float32'); dur=len(a)/SR
    for s,e in segs(i,dur,prot):
        seg=a[int(s*SR):int(e*SR)].copy()
        n=min(fade,len(seg)//2); seg[:n]*=np.linspace(0,1,n); seg[-n:]*=np.linspace(1,0,n)
        cmap.append(dict(file=i,src_start=s,src_end=e,out_start=T)); out.append(seg); T+=len(seg)/SR
    if i==1: out.append(np.zeros(int(0.12*SR),'float32')); T+=0.12
sf.write('vo_cut.wav',np.concatenate(out),SR); json.dump(cmap,open('cutmap.json','w'),indent=0)
print('duration',T)
