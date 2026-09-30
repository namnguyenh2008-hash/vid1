import cairosvg
DEF='''<defs>
<radialGradient id="fur" cx=".38" cy=".3" r=".8"><stop offset="0" stop-color="#A874EC"/><stop offset=".6" stop-color="#8447CF"/><stop offset="1" stop-color="#5E2A9E"/></radialGradient>
<radialGradient id="ear" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#FFD0DC"/><stop offset="1" stop-color="#EE8FAE"/></radialGradient>
<radialGradient id="eye" cx=".5" cy=".6" r=".6"><stop offset="0" stop-color="#7B3F8F"/><stop offset=".55" stop-color="#3A1650"/><stop offset="1" stop-color="#1A0826"/></radialGradient>
</defs>'''
PK="#F2A3BC"
def arm(s,a,L=62):
    x=178 if s=='L' else 322
    return f'<g transform="rotate({a} {x} 335)"><ellipse cx="{x}" cy="{335+L/2}" rx="24" ry="{L/2+14}" fill="url(#fur)"/><ellipse cx="{x}" cy="{335+L+6}" rx="17" ry="14" fill="{PK}"/><path d="M{x-8} {335+L+14} v6 M{x} {335+L+16} v6 M{x+8} {335+L+14} v6" stroke="#D97C9A" stroke-width="3" stroke-linecap="round"/></g>'
def mouth(m):
    t='<rect x="239" y="297" width="10" height="13" rx="3" fill="#fff"/><rect x="251" y="297" width="10" height="13" rx="3" fill="#fff"/>'
    return {'smile':t+'<path d="M226 292 Q238 302 250 293 Q262 302 274 292" stroke="#3A1650" stroke-width="4" fill="none" stroke-linecap="round"/>',
     'open':'<path d="M228 292 Q250 330 272 292 Z" fill="#3A1650"/><ellipse cx="250" cy="312" rx="11" ry="6" fill="#F07A9B"/>'+t,
     'o':'<ellipse cx="250" cy="306" rx="12" ry="15" fill="#3A1650"/>',
     'hmm':'<path d="M232 298 Q250 292 268 300" stroke="#3A1650" stroke-width="4" fill="none" stroke-linecap="round"/>'}[m]
def eyes(px,py,big=0):
    r=28+big
    o=''
    for x in (203,297):
        o+=f'<ellipse cx="{x}" cy="232" rx="{r-4}" ry="{r}" fill="url(#eye)"/><circle cx="{x-9+px}" cy="{220+py}" r="9" fill="#fff"/><circle cx="{x+9+px}" cy="{244+py}" r="4" fill="#fff" opacity=".9"/>'
    return o
def rat(la,ra,m='smile',px=0,py=0,big=0,brow=0,extra='',lL=62,rL=62):
    w=''.join(f'<line x1="{250+s*40}" y1="{275+d}" x2="{250+s*170}" y2="{250+d*3}" stroke="#fff" stroke-width="2" opacity=".75"/>' for s in (-1,1) for d in (-6,4,14))
    br=f'<path d="M180 {192-brow} Q203 {182-brow} 224 {190-brow}" stroke="#4A1D78" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M276 {190-brow} Q297 {182-brow} 320 {192-brow}" stroke="#4A1D78" stroke-width="5" fill="none" stroke-linecap="round"/>'
    return f'''<g>
<path d="M340 500 Q450 520 440 440 Q432 380 470 360" stroke="{PK}" stroke-width="13" fill="none" stroke-linecap="round"/>
<path d="M340 500 Q450 520 440 440 Q432 380 470 360" stroke="#D97C9A" stroke-width="13" fill="none" stroke-linecap="round" stroke-dasharray="2 14" opacity=".6"/>
<ellipse cx="195" cy="505" rx="38" ry="16" fill="{PK}"/><ellipse cx="305" cy="505" rx="38" ry="16" fill="{PK}"/>
<ellipse cx="250" cy="395" rx="128" ry="120" fill="url(#fur)"/>
<ellipse cx="250" cy="410" rx="78" ry="82" fill="#C9A6F2" opacity=".45"/>
<circle cx="148" cy="128" r="66" fill="url(#fur)"/><circle cx="148" cy="132" r="50" fill="url(#ear)"/>
<circle cx="352" cy="128" r="66" fill="url(#fur)"/><circle cx="352" cy="132" r="50" fill="url(#ear)"/>
<ellipse cx="250" cy="240" rx="118" ry="102" fill="url(#fur)"/>
<ellipse cx="250" cy="288" rx="52" ry="36" fill="#B58BEE" opacity=".6"/>
<ellipse cx="172" cy="282" rx="22" ry="13" fill="#FF8FB1" opacity=".45"/><ellipse cx="328" cy="282" rx="22" ry="13" fill="#FF8FB1" opacity=".45"/>
{br}{eyes(px,py,big)}
<path d="M238 268 Q250 262 262 268 Q258 282 250 284 Q242 282 238 268Z" fill="#F07A9B"/><ellipse cx="246" cy="269" rx="4" ry="2.5" fill="#fff" opacity=".7"/>
{mouth(m)}{w}
{arm('L',la,lL)}{arm('R',ra,rL)}{extra}</g>'''
MT="#3CE8B4";BL="#0077B6"
Q=f'<text x="385" y="95" font-family="Poppins" font-weight="bold" font-size="80" fill="{BL}">?</text>'
WV=f'<g stroke="{MT}" stroke-width="6" stroke-linecap="round" fill="none"><path d="M415 175 q14 -14 0 -28"/><path d="M435 185 q24 -26 0 -52"/></g>'
SP=f'<g stroke="{BL}" stroke-width="7" stroke-linecap="round"><line x1="120" y1="45" x2="105" y2="15"/><line x1="250" y1="20" x2="250" y2="-10"/><line x1="380" y1="45" x2="395" y2="15"/></g>'
AR=f'<path d="M440 330 L485 330 M470 315 L487 330 L470 345" stroke="{BL}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
ST=f'<g fill="{MT}"><path d="M150 380 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6z"/><path d="M350 380 l6 14 14 6 -14 6 -6 14 -6 -14 -14 -6 14 -6z"/></g>'
poses=[('idle','Idle',rat(35,-35,lL=48,rL=48)),
('wave','Wave',rat(35,-160,m='open',brow=4,extra=WV,lL=48)),
('point','Point',rat(35,-95,px=6,extra=AR,lL=48,rL=78)),
('think','Think',rat(150,-35,m='hmm',px=5,py=-6,brow=-3,extra=Q,lL=52,rL=48)),
('surprised','Surprised',rat(155,-155,m='o',big=4,brow=12,extra=SP)),
('happy','Happy',rat(55,-55,m='open',brow=3,extra=ST,lL=42,rL=42))]
for k,t,g in poses:
    open(f'rat2_{k}.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -20 520 560">{DEF}{g}</svg>')
cells=''.join(f'<g transform="translate({(i%3)*540+15},{(i//3)*640+20})"><rect width="520" height="620" rx="32" fill="#fff"/><g transform="translate(0,40)">{g}</g><text x="260" y="600" text-anchor="middle" font-family="Poppins" font-weight="bold" font-size="32" fill="#1A1A1A">{t}</text></g>' for i,(k,t,g) in enumerate(poses))
s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1650 1300">{DEF}<rect width="1650" height="1300" fill="#EAF4FB"/>{cells}</svg>'
cairosvg.svg2png(bytestring=s.encode(),write_to='rat2_sheet.png',output_width=1650)
