# Word timestamps from sherpa-onnx Vietnamese zipformer (chunked at ~20s).
import sherpa_onnx as s, soundfile as sf, json, numpy as np, sys
M='/home/user/models/sherpa-onnx-zipformer-vi-2025-04-20/'
r=s.OfflineRecognizer.from_transducer(encoder=M+'encoder-epoch-12-avg-8.onnx',decoder=M+'decoder-epoch-12-avg-8.onnx',joiner=M+'joiner-epoch-12-avg-8.onnx',tokens=M+'tokens.txt',decoding_method='modified_beam_search')
a,sr=sf.read(sys.argv[1],dtype='float32')
# chunk at quiet points near every 20s
env=np.convolve(np.abs(a),np.ones(1600)/1600,'same'); cuts=[0]
while len(a)-cuts[-1]>25*sr:
    lo=cuts[-1]+15*sr; hi=cuts[-1]+22*sr; cuts.append(lo+int(np.argmin(env[lo:hi])))
cuts.append(len(a)); words=[]
for c0,c1 in zip(cuts,cuts[1:]):
    st=r.create_stream(); st.accept_waveform(sr,np.concatenate([a[c0:c1],np.zeros(int(.3*sr),'float32')])); r.decode_stream(st)
    res=st.result
    for tok,t in zip(res.tokens,res.timestamps):
        t=t+c0/sr
        if tok[:1] in ('▁',' ') or not words: words.append(dict(w=tok.replace('▁','').strip(),t=round(t,3)))
        else: words[-1]['w']+=tok
words=[w for w in words if w['w']]
for i,w in enumerate(words): w['end']=round(words[i+1]['t'] if i+1<len(words) else len(a)/sr,3)
json.dump(words,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(' '.join(f"{w['w']}@{w['t']}" for w in words))
