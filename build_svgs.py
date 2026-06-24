#!/usr/bin/env python3
"""
Generates the F1-broadcast SVG panels for the dbisina/dbisina profile README.

The trick: GitHub strips <script> and inline style= from README HTML, but it
renders <img>-embedded SVG. An SVG carries its OWN <style> block, gradients,
and CSS/SMIL animation, all rendered client-side by the browser. So the whole
"website" look (cards, borders, motion) survives the sanitizer as images.

Run:  python build_svgs.py     (re-emits everything into ./assets)
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT / "assets"

# ---- palette ----------------------------------------------------------------
RED   = "#E10600"; AMBER = "#FFC400"; GREEN = "#22D67A"
INK   = "#05081A"; CARD0 = "#0E1736"; CARD1 = "#090E26"
LINE  = "#27315e"; TXT   = "#E9EDFB"; TXT2  = "#C8D0EE"
MUT   = "#6B76A6"; DIM   = "#5C6790"
SANS  = "'Arial Narrow','Helvetica Neue',Arial,sans-serif"
MONO  = "'Cascadia Code','Consolas','SFMono-Regular',ui-monospace,monospace"

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def b64(name):
    return base64.b64encode((ASSETS / name).read_bytes()).decode()

def write(name, svg):
    (ASSETS / name).write_text(svg, encoding="utf-8")
    print(f"  wrote assets/{name}  ({len(svg)//1024 or 1}kb)")

# shared <defs> (card gradient + soft shadow) -------------------------------
def defs(extra=""):
    return f"""<defs>
  <linearGradient id="card" x1="0" y1="0" x2="0.5" y2="1">
    <stop offset="0" stop-color="{CARD0}"/><stop offset="1" stop-color="{CARD1}"/>
  </linearGradient>
  <linearGradient id="accent" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{AMBER}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{LINE}"/><stop offset="1" stop-color="{LINE}" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="redfade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </linearGradient>
  {extra}
</defs>"""

def card_rect(x,y,w,h,rx=12):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="url(#card)" stroke="{LINE}" stroke-width="1"/>')

def bg(w,h,rx=14):
    """Full-bleed dark panel background — makes each SVG self-contained and
    readable on both GitHub light and dark themes."""
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="{INK}"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#card)" stroke="{LINE}"/>')

def inset(x,y,w,h,rx=10):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#0a0f26" stroke="{LINE}"/>'

def section_head(sx, title, sub, w=1000):
    """A broadcast section header strip: [Sx] TITLE / sub  --------."""
    return f"""<rect x="0" y="14" width="34" height="26" rx="4" fill="{RED}"/>
<text x="17" y="32" font-family="{MONO}" font-size="14" font-weight="700" fill="{INK}" text-anchor="middle">{sx}</text>
<text x="48" y="33" font-family="{SANS}" font-size="22" font-weight="800" letter-spacing="1.5" fill="{TXT}">{esc(title)}</text>
<text x="{52+len(title)*13}" y="33" font-family="{SANS}" font-size="15" font-weight="600" fill="{DIM}">/ {esc(sub)}</text>
<rect x="{72+len(title)*13+len(sub)*8}" y="26" width="{max(40, w-(80+len(title)*13+len(sub)*8))}" height="1.5" fill="url(#fade)"/>"""


# =============================================================================
# 1. BANNER  — animated broadcast hero
# =============================================================================
def car(x, y, s=1.0):
    """Stylised red F1 car (facing right), local box ~220x80, ground y~62."""
    return f"""<g transform="translate({x},{y}) scale({s})">
  <!-- speed lines -->
  <g class="trail" stroke="{AMBER}" stroke-width="2" stroke-linecap="round" opacity="0.7">
    <line x1="-60" y1="34" x2="6"  y2="34"/><line x1="-90" y1="46" x2="-14" y2="46"/>
    <line x1="-50" y1="58" x2="20" y2="58"/>
  </g>
  <!-- floor -->
  <polygon points="40,60 192,60 188,67 44,67" fill="#0c1124"/>
  <!-- rear wing -->
  <rect x="40" y="22" width="9" height="30" rx="2" fill="#14182f"/>
  <polygon points="32,18 60,18 60,25 32,25" fill="#14182f"/>
  <rect x="32" y="18" width="28" height="2.5" fill="{AMBER}"/>
  <!-- body -->
  <polygon points="50,60 60,38 86,31 108,41 150,42 198,55 172,60"
           fill="url(#carbody)" stroke="#7a0c06" stroke-width="1"/>
  <!-- sidepod shadow + intake -->
  <polygon points="92,46 130,46 126,58 96,58" fill="#a40d04"/>
  <!-- halo + cockpit -->
  <path d="M104,42 Q122,24 140,42" fill="none" stroke="#0b0e1c" stroke-width="4"/>
  <ellipse cx="112" cy="42" rx="8" ry="5" fill="#0b0e1c"/>
  <!-- nose tip + front wing -->
  <polygon points="198,55 214,57 214,61 184,61 184,57" fill="#14182f"/>
  <rect x="184" y="56" width="30" height="2.5" fill="{AMBER}"/>
  <!-- number roundel -->
  <circle cx="78" cy="48" r="9" fill="#fff"/>
  <text x="78" y="52" font-family="{SANS}" font-size="12" font-weight="900" fill="{RED}" text-anchor="middle">1</text>
  <!-- wheels -->
  <g class="wheel" style="transform-box:fill-box;transform-origin:center" transform="translate(60,60)">
    <circle r="16" fill="#101422" stroke="#5b6aa6" stroke-width="2.5"/>
    <circle r="6.5" fill="#1a1f38" stroke="{AMBER}" stroke-width="1.4"/>
    <g stroke="{AMBER}" stroke-width="1.5" opacity="0.85"><line x1="-12" y1="0" x2="12" y2="0"/><line x1="0" y1="-12" x2="0" y2="12"/></g>
  </g>
  <g class="wheel" style="transform-box:fill-box;transform-origin:center" transform="translate(166,60)">
    <circle r="16" fill="#101422" stroke="#5b6aa6" stroke-width="2.5"/>
    <circle r="6.5" fill="#1a1f38" stroke="{AMBER}" stroke-width="1.4"/>
    <g stroke="{AMBER}" stroke-width="1.5" opacity="0.85"><line x1="-12" y1="0" x2="12" y2="0"/><line x1="0" y1="-12" x2="0" y2="12"/></g>
  </g>
</g>"""

def hud_seg(x, w, label, val, vcolor=TXT, fill=CARD1, lab=DIM):
    return f"""<rect x="{x}" y="0" width="{w}" height="30" fill="{fill}"/>
<text x="{x+12}" y="19" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{lab}">{label}</text>
<text x="{x+18+len(label)*6.6:.0f}" y="19" font-family="{MONO}" font-size="11" font-weight="700" fill="{vcolor}">{val}</text>"""

def banner():
    extra = f"""<linearGradient id="carbody" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF2418"/><stop offset="1" stop-color="#C8102E"/></linearGradient>
    <linearGradient id="title" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#AEB8E0"/></linearGradient>
    <clipPath id="bclip"><rect width="1000" height="320" rx="14"/></clipPath>"""
    css = f""".live{{animation:pulse 1.6s ease-in-out infinite;transform-origin:center}}
    @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
    .cur{{animation:blink 1.1s step-end infinite}}
    @keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
    .car{{animation:drive 7s cubic-bezier(.45,0,.55,1) infinite}}
    @keyframes drive{{0%{{transform:translateX(-260px)}}55%,100%{{transform:translateX(1120px)}}}}
    .wheel{{animation:spin .45s linear infinite}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .streak{{animation:slide 6s linear infinite}}
    @keyframes slide{{to{{transform:translateX(-322px)}}}}
    .tl{{opacity:0;animation:cycle 9s infinite}}
    .tl2{{animation-delay:3s}} .tl3{{animation-delay:6s}}
    @keyframes cycle{{0%{{opacity:0}}4%,29%{{opacity:1}}33%,100%{{opacity:0}}}}"""
    spd = "".join(
        f'<rect class="streak" x="{i*322-322}" y="0" width="2" height="320" fill="{AMBER}" opacity="0.05"/>'
        f'<rect class="streak" x="{i*322-322+150}" y="0" width="2" height="320" fill="{RED}" opacity="0.06"/>'
        for i in range(5))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 320" width="1000" height="320" font-family="{SANS}">
{defs(extra)}
<style>{css}</style>
<g clip-path="url(#bclip)">
  <rect width="1000" height="320" fill="{INK}"/>
  <rect width="1000" height="320" fill="url(#card)" opacity="0.6"/>
  <g transform="skewX(-20)" opacity="0.9">{spd}</g>

  <!-- HUD bar -->
  <rect x="0" y="0" width="1000" height="30" fill="{CARD1}"/>
  <rect x="0" y="0" width="42" height="30" fill="{RED}"/>
  <text x="21" y="20" font-family="{MONO}" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">P1</text>
  <circle class="live" cx="62" cy="15" r="4" fill="{GREEN}"/>
  <text x="76" y="19" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="2" fill="{TXT}">DBISINA</text>
  {hud_seg(170, 92, 'LAP', '27/58')}
  {hud_seg(262, 70, 'DRS', 'ON', AMBER)}
  {hud_seg(332, 118, 'SPD', '318 KM/H', GREEN)}
  {hud_seg(820, 180, 'GEAR', '6  ·  ERS 88%', AMBER)}

  <!-- kicker -->
  <rect x="40" y="62" width="34" height="3" rx="1.5" fill="{RED}"/>
  <text x="84" y="68" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="4" fill="{AMBER}">REDLINE GARAGE</text>

  <!-- name -->
  <text x="38" y="150" font-family="{SANS}" font-size="92" font-weight="900" letter-spacing="-1" fill="url(#title)">DBISINA</text>
  <text x="42" y="184" font-family="{SANS}" font-size="20" font-weight="700" letter-spacing="2" fill="{TXT}">AI &amp; SYSTEMS ENGINEER</text>
  <rect class="cur" x="324" y="170" width="9" height="18" fill="{AMBER}"/>

  <!-- cycling tagline -->
  <g font-family="{MONO}" font-size="14">
    <text x="42" y="214" fill="{MUT}"><tspan fill="{GREEN}">&gt; </tspan><tspan class="tl">AI Systems &amp; Kernel Optimization</tspan></text>
    <text x="42" y="214" fill="{MUT}"><tspan fill="{GREEN}">&gt; </tspan><tspan class="tl tl2">High-Performance Computing</tspan></text>
    <text x="42" y="214" fill="{MUT}"><tspan fill="{GREEN}">&gt; </tspan><tspan class="tl tl3">Building the future, one commit at a time</tspan></text>
  </g>
  <text x="42" y="246" font-family="{SANS}" font-size="14" font-style="italic" fill="{TXT2}">"Building foundational technology that moves humanity forward."</text>
  <rect x="38" y="232" width="3" height="20" fill="{RED}"/>

  <!-- animated car drives along the lower lane -->
  <g class="car"><g transform="translate(0,244)">{car(0,0,1.0)}</g></g>

  <!-- driver dossier -->
  <g transform="translate(726,52)">
    <rect width="246" height="240" rx="10" fill="#0c1330" stroke="{LINE}"/>
    <rect width="246" height="240" rx="10" fill="none" stroke="{RED}" stroke-opacity="0.25"/>
    <text x="16" y="28" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUT}">DRIVER CARD</text>
    <circle cx="214" cy="24" r="4" class="live" fill="{AMBER}"/>
    <text x="200" y="28" font-family="{MONO}" font-size="10" fill="{AMBER}" text-anchor="end">ACTIVE</text>
    <text x="14" y="118" font-family="{SANS}" font-size="92" font-weight="900" fill="{RED}">01</text>
    <text x="150" y="118" font-family="{SANS}" font-size="30" font-weight="900" letter-spacing="6" fill="#fff">BIS</text>
    <rect x="16" y="132" width="214" height="1.5" fill="url(#redfade)"/>
    <g font-family="{MONO}">
      <text x="16" y="158" font-size="9" letter-spacing="1.5" fill="{DIM}">TEAM</text>
      <text x="16" y="174" font-size="13" fill="{TXT}">Redline</text>
      <text x="130" y="158" font-size="9" letter-spacing="1.5" fill="{DIM}">POWER UNIT</text>
      <text x="130" y="174" font-size="13" fill="{TXT}">AI / HPC</text>
      <text x="16" y="206" font-size="9" letter-spacing="1.5" fill="{DIM}">TYRES</text>
      <text x="16" y="222" font-size="13" fill="{AMBER}">SOFT ◉</text>
      <text x="130" y="206" font-size="9" letter-spacing="1.5" fill="{DIM}">STATUS</text>
      <text x="130" y="222" font-size="13" fill="{GREEN}">SHIPPING</text>
    </g>
  </g>
  <rect x="0" y="0" width="1000" height="320" rx="14" fill="none" stroke="{LINE}"/>
</g>
</svg>"""


# =============================================================================
# 2. ABOUT  — card with embedded Red Bull car photo + text
# =============================================================================
def about():
    img = b64("car-action.jpg")
    extra = '<clipPath id="ph"><rect x="16" y="16" width="250" height="248" rx="9"/></clipPath>'
    para = [
        ('I’m an ', '#fff','AI & Systems Engineer',' working at the seam'),
        ('between hardware and software. My focus is',None,None,None),
        ('','#FFC400','AI kernel optimization',', scalable architecture,'),
        ('and high-performance computing.',None,None,None),
    ]
    txt = f"""<text x="300" y="62" font-family="{SANS}" font-size="17" fill="{TXT2}">
  <tspan x="300" dy="0">I’m an <tspan font-weight="800" fill="#fff">AI &amp; Systems Engineer</tspan> working at the</tspan>
  <tspan x="300" dy="26">seam between hardware and software. My focus</tspan>
  <tspan x="300" dy="26">is <tspan font-weight="800" fill="{AMBER}">AI kernel optimization</tspan>, scalable</tspan>
  <tspan x="300" dy="26">architecture, and high-performance computing.</tspan>
  <tspan x="300" dy="34" fill="{TXT}">I don’t just write code — I engineer solutions</tspan>
  <tspan x="300" dy="26">that are <tspan font-weight="800" fill="#fff">robust, secure, and blazingly fast.</tspan></tspan>
</text>
<rect x="300" y="232" width="3" height="40" fill="{RED}"/>
<text x="316" y="250" font-family="{SANS}" font-size="14" font-style="italic" fill="{MUT}">"Building foundational technology that</text>
<text x="316" y="270" font-family="{SANS}" font-size="14" font-style="italic" fill="{MUT}">moves humanity forward."</text>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 296" width="1000" height="296">
{defs(extra)}
{bg(1000,296)}
<rect x="0" y="14" width="4" height="282" rx="2" fill="url(#accent)"/>
{section_head('S1','ABOUT','Driver Profile')}
<image x="16" y="58" width="250" height="248" href="data:image/jpeg;base64,{img}"
       preserveAspectRatio="xMidYMid slice" clip-path="url(#phb)"/>
<defs><clipPath id="phb"><rect x="16" y="58" width="250" height="222" rx="9"/></clipPath></defs>
<rect x="16" y="58" width="250" height="222" rx="9" fill="none" stroke="{LINE}"/>
{txt}
</svg>"""


# =============================================================================
# 3. SECTORS
# =============================================================================
def sectors():
    cols = [
        ("FOCUS", RED, ["AI systems & kernels","Low-level optimization"]),
        ("EXPLORING", AMBER, ["Quantum computing & FPGA","Neuromorphic engineering"]),
        ("COLLABORATE", GREEN, ["Open source & infra","Hackathons & events"]),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 230" width="1000" height="230">',
           defs(), bg(1000,230), section_head('S2','SECTORS','Where I Race')]
    cw, gap, x0, y0 = 318, 23, 14, 58
    for i,(name,clr,items) in enumerate(cols):
        x = x0 + i*(cw+gap)
        out.append(inset(x, y0, cw, 150))
        out.append(f'<rect x="{x}" y="{y0}" width="{cw}" height="34" rx="0" fill="{clr}" fill-opacity="0.12"/>')
        out.append(f'<rect x="{x}" y="{y0}" width="4" height="34" fill="{clr}"/>')
        out.append(f'<text x="{x+18}" y="{y0+23}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2" fill="#fff">{esc(name)}</text>')
        for j,it in enumerate(items):
            out.append(f'<text x="{x+18}" y="{y0+66+j*30}" font-family="{SANS}" font-size="16" font-weight="600" fill="{TXT}">{esc(it)}</text>')
            if j < len(items)-1:
                out.append(f'<rect x="{x+18}" y="{y0+78}" width="{cw-36}" height="1" fill="{LINE}"/>')
    out.append("</svg>")
    return "\n".join(out)


# =============================================================================
# 4. ARSENAL  — tech chips
# =============================================================================
def chip(x, y, label, color):
    w = 22 + len(label)*8.4 + 14
    return (f'<g transform="translate({x},{y})">'
            f'<rect width="{w:.0f}" height="30" rx="6" fill="#0B1330" stroke="{LINE}"/>'
            f'<rect x="12" y="11" width="8" height="8" rx="2" fill="{color}"/>'
            f'<text x="28" y="20" font-family="{MONO}" font-size="13" fill="{TXT2}">{esc(label)}</text></g>'), w+10

def chip_row(x0, y, items):
    out, x = [], x0
    for label,color in items:
        s,w = chip(x,y,label,color); out.append(s); x += w
    return "\n".join(out)

def arsenal():
    groups = [
        ("LANGUAGES", [("Python","#FFD43B"),("C / C++","#659AD2"),("Rust","#DEA584"),
                       ("CUDA","#76B900"),("TypeScript","#3178C6")]),
        ("AI & SYSTEMS", [("PyTorch","#EE4C2C"),("Triton","#8A6BF2"),
                          ("TensorFlow","#FF6F00"),("ONNX","#C0C7E0")]),
        ("INFRA & WEB", [("Linux","#FCC624"),("Docker","#2496ED"),("Kubernetes","#326CE5"),
                         ("AWS","#FF9900"),("React","#61DAFB"),("Redis","#DC382D"),("PostgreSQL","#336791")]),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 300" width="1000" height="300">',
           defs(), bg(1000,300), section_head('S3','ARSENAL','Tech Stack')]
    y = 78
    for name,items in groups:
        out.append(f'<text x="20" y="{y+14}" font-family="{MONO}" font-size="10" letter-spacing="2.5" fill="{MUT}">{esc(name)}</text>')
        out.append(chip_row(20, y+24, items))
        y += 74
    out.append("</svg>")
    return "\n".join(out)


# =============================================================================
# 5. PIT WALL  — objectives + quote
# =============================================================================
def pitwall():
    rows = [
        ("01","AI kernel generation & optimization","(U-HOP vision)"),
        ("02","Scalable backend & infrastructure systems",""),
        ("03","Full-stack platforms with real-world impact",""),
        ("04","Bridging hardware and software intelligence",""),
        ("05","Performance optimization & security hardening",""),
    ]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 360" width="1000" height="360">',
           defs(), bg(1000,360), section_head('S5','PIT WALL','Objectives This Season')]
    out.append(f'<rect x="1" y="44" width="998" height="28" fill="{RED}" fill-opacity="0.06"/>')
    out.append(f'<text x="20" y="62" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUT}">PIT WALL  //  RACE STRATEGY</text>')
    for i,(n,t,sub) in enumerate(rows):
        y = 96 + i*36
        out.append(f'<text x="22" y="{y}" font-family="{MONO}" font-size="13" font-weight="700" fill="{RED}">{n}</text>')
        out.append(f'<text x="60" y="{y}" font-family="{SANS}" font-size="16" fill="{TXT}">{esc(t)}'
                   + (f' <tspan fill="{MUT}" font-size="13">{esc(sub)}</tspan>' if sub else '') + '</text>')
        if i < len(rows)-1:
            out.append(f'<rect x="22" y="{y+12}" width="956" height="1" fill="{LINE}" fill-opacity="0.5"/>')
    # quote band
    out.append(inset(14,300,972,48))
    out.append(f'<rect x="14" y="300" width="4" height="48" rx="2" fill="url(#accent)"/>')
    out.append(f'<text x="500" y="326" font-family="{SANS}" font-size="18" font-style="italic" font-weight="700" fill="#fff" text-anchor="middle">"The best way to predict the future is to invent it."</text>')
    out.append(f'<text x="500" y="346" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{AMBER}" text-anchor="middle">— ALAN KAY</text>')
    out.append("</svg>")
    return "\n".join(out)


# =============================================================================
# 6. SECTION HEADERS for the live-widget / badge rows
# =============================================================================
def head(sx,title,sub):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 50" width="1000" height="50">'
            f'{defs()}{bg(1000,50,10)}{section_head(sx,title,sub)}</svg>')

def checkered():
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="18" viewBox="0 0 1600 18" preserveAspectRatio="none">
  <defs><pattern id="c" width="18" height="18" patternUnits="userSpaceOnUse">
    <rect width="18" height="18" fill="#0A0E28"/>
    <rect width="9" height="9" fill="#E9EDFB"/><rect x="9" y="9" width="9" height="9" fill="#E9EDFB"/>
  </pattern></defs>
  <rect width="1600" height="18" fill="url(#c)"/><rect width="1600" height="3" fill="{RED}"/>
</svg>"""


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    write("banner.svg",  banner())
    write("about.svg",   about())
    write("sectors.svg", sectors())
    write("arsenal.svg", arsenal())
    write("pitwall.svg", pitwall())
    write("head_telemetry.svg", head('S4','TELEMETRY','Live GitHub Data'))
    write("head_radio.svg",     head('S7','RADIO','Connect'))
    write("checkered.svg",      checkered())
    print("done.")
