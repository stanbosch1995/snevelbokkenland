import re, sys, base64, io
from PIL import Image

def remove_white_bg(img):
    img = img.convert('RGBA')
    try:
        import numpy as np
        data = np.array(img, dtype=np.uint8)
        mask = (data[:,:,0]>240)&(data[:,:,1]>240)&(data[:,:,2]>240)
        data[mask,3] = 0
        return Image.fromarray(data)
    except ImportError:
        px = img.load()
        for y in range(img.height):
            for x in range(img.width):
                r,g,b,a = px[x,y]
                if r>240 and g>240 and b>240: px[x,y]=(r,g,b,0)
        return img

def img_b64(path, max_w=1200, max_h=1200, quality=82, strip_white=False):
    img = Image.open(path)
    if strip_white or (path.lower().endswith('.png') and path.endswith('19_54_49.png')):
        img = remove_white_bg(img)
    img.thumbnail((max_w, max_h), Image.LANCZOS)
    buf = io.BytesIO()
    fmt = 'PNG' if (path.lower().endswith('.png') or strip_white) else 'JPEG'
    mime = 'image/png' if fmt == 'PNG' else 'image/jpeg'
    img.save(buf, format=fmt, quality=quality, optimize=True)
    return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()

# Read images directly from source files
LOGO           = img_b64("C:/Users/Systeembeheer/Downloads/ChatGPT Image 18 mei 2026, 19_54_49.png", max_w=300, max_h=300)
HERO_PRINCE    = img_b64("C:/Users/Systeembeheer/Pictures/Snevelbokkenland/Fotografierenekuijs_2025_-_kopie (1).jpg", max_w=700, max_h=900)
PRINCE_PORTRAIT= HERO_PRINCE
MERCH1         = img_b64("C:/Users/Systeembeheer/Downloads/1000097941.jpg", max_w=600, max_h=600)
MERCH2         = img_b64("C:/Users/Systeembeheer/Downloads/2026-embleem-snevelbokkenland.jpg", max_w=600, max_h=600)
MERCH3         = img_b64("C:/Users/Systeembeheer/Downloads/1000097966.jpg", max_w=600, max_h=600)

# Oud-prinsen foto mapping: (jaar_label, naam, bestand)
CACHE = 'C:/Users/Systeembeheer/prins_images/'
OUD_PRINSEN = [
    ('2025',            "Prins Rob d’n Twidde",      'prins-rob-de-backer.jpg'),
    ('2024',            "Prins Mike d’n Urste",      'prins-mike-dn-urste-site_kopie.jpg'),
    ('2022–2023',  "Prins Rob d’n Urste",       'IMG_20230831_194916.jpg'),
    ('2020–2021',  "Prinses Heidi d’n Urste",   '2B1C9620-E061-4DB4-AD73-5FA5C01E0FD9home_edit_1049819320968971.jpg'),
    ('2019',            "Prins Guido d’n Urste",     'Guido1.jpg'),
    ('2018',            "Prins Driekus d’n Urste",   'Driekus1.jpg'),
    ('2017',            "Prins Ton d’n Twidde",      'prins_ton_13x18_edit_197657115013588.jpg'),
    ('2016',            "Prins Sander d’n Urste",    'Sander1.jpg'),
    ('2015',            "Prins Joost d’n Urste",     'Joost.jpg'),
    ('2014',            "Prins Bart d’n Urste",      'Bart1.png'),
    ('2013',            "Prinses Marianne d’n Urste",'Marianne1.png'),
    ('2012',            "Prins Wilson d’n Urste",    'Wilson.png'),
    ('2011',            "Prins Dennis d’n Urste",    'Dennis1.png'),
    ('2010',            "Prins Bert d’n Urste",      'Bert1.png'),
    ('2009',            "Prins Henk d’n Urste",      'Henk1.png'),
    ('2008',            "Prins Len d’n Urste",       'Len1.png'),
    ('2007',            "Prins Hans d’n Urste",      'Hans1.png'),
    ('2006',            "Prins Corlix d’n Urste",    'Corlix1.png'),
    ('2005',            "Prins Ad d’n Urste",        'Ad1.png'),
    ('2004',            "Prins Erik d’n Urste",      'Erik1.png'),
    ('2003',            "Prins Wim d’n Urste",       'Wim1.png'),
    ('2002',            "Prins Ton d’n Urste",       'Ton1.png'),
    ('2001',            "Prins Fred d’n Urste",      'Fred1.png'),
    ('2000',            "Prins Leon d’n Urste",      'Leon1.png'),
    ('1999',            "Prins Rene d’n Urste",      'rene1.png'),
    ('1998',            "Prins Adrianus d’n Urste",  'Adrianus1.png'),
    ('1997',            "Prins Rien d’n Urste",      'rien1.png'),
    ('1996',            "Prins Marius d’n Urste",    'Marius1.png'),
    ('1995',            "Prins Jan d’n Vierde",      'Jan4.png'),
    ('1994',            "Prins Jan d’n Derde",       'Jan3.png'),
    ('1993',            "Prins Nico d’n Urste",      'Nico1.png'),
    ('1992',            "Prins Ber d’n Urste",       'Ber1.png'),
    ('1991',            "Prins Harrie d’n Urste",    'Harrie1.png'),
    ('1990',            "Prins Piet d’n Urste",      'Piet1.png'),
    ('1989',            "Prins Maricus d’n Urste",   'Maricus1.png'),
    ('1988',            "Prins Basilius d’n Urste",  'Basilius1.png'),
    ('1987',            "Prins Nilles d’n Twidde",   'Nilles2.png'),
    ('1986',            "Prins Gerrit d’n Urste",    'Gerrit1.png'),
    ('1985',            "Prins Jan d’n Twidde",      'Jan_dn_2.png'),
    ('1984',            "Prins Toon d’n Urste",      'Toon1.png'),
    ('1983',            "Prins Nilles d’n Urste",    'Nilles1.png'),
    ('1982',            "Prins Tien d’n Urste",      'Tien1.png'),
    ('1981',            "Prins Fons d’n Urste",      'Fons1.png'),
    ('1980',            "Prins Gerard d’n Urste",    'Gerard1.png'),
    ('1979',            "Prins Grad d’n Urste",      'Grad1.png'),
    ('1978',            "Prins Xaveer d’n Urste",    'Xaveer1.png'),
    ('1977',            "Prins Has d’n Urste",       'Has1.png'),
    ('1976',            "Prins Knilles d’n Urste",   'Knilles_1.png'),
    ('1975',            "Prins Jan d’n Urste",       'Jan1.png'),
    ('1972–1974',  "Prins Teun d’n Urste",      'teun1.png'),
    ('1971',            "Prins Tinus d’n Urste",     'Tinus_1.png'),
]

print('Encoding oud-prinsen photos...')
OUD_PRINSEN_B64 = []
import os
for jaar, naam, fname in OUD_PRINSEN:
    path = CACHE + fname
    if os.path.exists(path):
        b64 = img_b64(path, max_w=220, max_h=280, quality=78)
    else:
        b64 = ''
        print(f'  MISSING: {fname}')
    OUD_PRINSEN_B64.append((jaar, naam, b64))
print(f'  Done: {sum(1 for _,_,b in OUD_PRINSEN_B64 if b)} photos encoded')

# Build oud-prinsen HTML cards
def build_oud_prinsen_html():
    cards = ''
    for jaar, naam, b64 in OUD_PRINSEN_B64:
        img_tag = (f'<img src="{b64}" alt="{naam}" style="width:100%;height:200px;object-fit:cover;object-position:top">'
                   if b64 else
                   '<div style="height:200px;background:linear-gradient(135deg,#e8eeff,#c8d8ff);display:flex;align-items:center;justify-content:center;font-size:3rem">&#128081;</div>')
        cards += (
            f'<div class="op-card">'
            f'{img_tag}'
            f'<div class="op-card-body">'
            f'<div class="op-card-jaar">{jaar}</div>'
            f'<div class="op-card-naam">{naam}</div>'
            f'</div></div>'
        )
    return cards

OUD_PRINSEN_HTML = build_oud_prinsen_html()

# Read SB_JS from current index.html if possible, else use fallback
with open('C:/Users/Systeembeheer/index.html', 'r', encoding='utf-8') as f:
    old = f.read()

script_start = old.rfind('<script>')
script_end   = old.rfind('</script>')
js_block     = old[script_start+8:script_end]
sb_start = js_block.find('/* =========================================================\n   SIDE-BURST')
SB_JS = js_block[sb_start:]

print(f'Logo: {len(LOGO)}, HeroPrince: {len(HERO_PRINCE)}, Portrait: {len(PRINCE_PORTRAIT)}')
print(f'Merch1: {len(MERCH1)}, Merch2: {len(MERCH2)}, Merch3: {len(MERCH3)}')
print(f'SB_JS: {len(SB_JS)}')

# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Nunito',sans-serif;background:#FFF8E7;color:#1a1a2e;overflow-x:hidden}
img{max-width:100%;display:block}
a{text-decoration:none;color:inherit}

/* SIDE-BURST CONFETTI ONLY */
.sc-piece{position:fixed;left:0;top:0;pointer-events:none;z-index:9999;border-radius:2px;will-change:transform,opacity}

/* BUTTONS */
.btn-primary{display:inline-flex;align-items:center;gap:.4rem;background:#FFD700;color:#003DA5;font-weight:800;font-size:1rem;padding:.8rem 2.2rem;border-radius:999px;border:none;cursor:pointer;transition:background .2s,transform .15s,box-shadow .2s;box-shadow:0 4px 14px rgba(255,215,0,.4)}
.btn-primary:hover{background:#ffc800;transform:translateY(-2px);box-shadow:0 8px 22px rgba(255,215,0,.5)}
.btn-outline{display:inline-flex;align-items:center;gap:.4rem;background:transparent;color:#fff;font-weight:800;font-size:1rem;padding:.8rem 2.2rem;border-radius:999px;border:2.5px solid rgba(255,255,255,.7);cursor:pointer;transition:all .2s}
.btn-outline:hover{background:#fff;color:#003DA5;transform:translateY(-2px)}
.btn-blue{display:inline-flex;align-items:center;gap:.4rem;background:#003DA5;color:#fff;font-weight:800;font-size:1rem;padding:.8rem 2.2rem;border-radius:999px;border:none;cursor:pointer;transition:background .2s,transform .15s,box-shadow .2s;box-shadow:0 4px 14px rgba(0,61,165,.35)}
.btn-blue:hover{background:#0048c2;transform:translateY(-2px)}
.btn-sm{padding:.5rem 1.4rem;font-size:.9rem}

/* HEADER */
#site-header{position:sticky;top:0;z-index:1000}
.header-logo-bar{background:linear-gradient(130deg,#001240 0%,#002a80 40%,#003DA5 75%,#0050cc 100%);display:flex;align-items:center;justify-content:center;padding:10px 2rem;height:90px}
.header-logo-bar img{height:70px;width:auto;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))}
.header-logo-bar .site-title{color:#FFD700;font-size:1.3rem;font-weight:900;margin-left:1rem;text-shadow:0 2px 6px rgba(0,0,0,.4)}
.header-nav-bar{background:#001240;display:flex;align-items:center;justify-content:center;gap:0;padding:0 1rem;height:46px;border-top:1px solid rgba(255,215,0,.2)}
.nav-item{position:relative}
.nav-item>a,.nav-item>span{display:flex;align-items:center;gap:.3rem;color:rgba(255,255,255,.88);font-weight:700;font-size:.88rem;padding:0 .9rem;height:46px;cursor:pointer;transition:color .2s;white-space:nowrap;letter-spacing:.3px}
.nav-item>a:hover,.nav-item>span:hover,.nav-item>a.active,.nav-item>span.active{color:#FFD700}
.nav-dropdown{display:none;position:absolute;top:100%;left:0;background:#001f5c;border:1px solid rgba(255,215,0,.25);border-radius:0 0 8px 8px;min-width:200px;z-index:2000;padding:.4rem 0}
.nav-item:hover .nav-dropdown{display:block}
.nav-dropdown a{display:block;color:rgba(255,255,255,.85);font-weight:600;font-size:.85rem;padding:.55rem 1.1rem;transition:background .15s,color .15s}
.nav-dropdown a:hover,.nav-dropdown a.active{background:rgba(255,215,0,.12);color:#FFD700}

/* PAGES */
.page{display:none}
.page.active{display:block}

/* HERO */
.hero{position:relative;min-height:92vh;background:linear-gradient(130deg,#001240 0%,#002a80 40%,#003DA5 75%,#0050cc 100%);display:flex;align-items:center;justify-content:center;overflow:hidden;padding:4rem 2rem}
.hero-garlands{position:absolute;top:0;left:0;width:100%;pointer-events:none;z-index:2}
.hero-content{position:relative;z-index:3;display:flex;align-items:center;gap:4rem;max-width:1100px;width:100%}
.hero-text{flex:1;color:#fff}
.hero-text .kicker{color:#FFD700;font-weight:800;font-size:.95rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:.6rem}
.hero-text h1{font-size:clamp(2.2rem,5vw,3.8rem);font-weight:900;line-height:1.1;margin-bottom:1rem;text-shadow:0 3px 15px rgba(0,0,0,.4)}
.hero-text p{font-size:1.1rem;opacity:.9;max-width:500px;line-height:1.7;margin-bottom:2rem}
.hero-btns{display:flex;gap:1rem;flex-wrap:wrap}
.hero-photo{flex-shrink:0;width:340px;height:440px;object-fit:cover;border-radius:24px;border:4px solid rgba(255,215,0,.4);box-shadow:0 20px 60px rgba(0,0,0,.5)}

/* PAGE HEADER BANNER */
.page-banner{background:linear-gradient(130deg,#001240 0%,#002a80 40%,#003DA5 75%,#0050cc 100%);padding:3.5rem 2rem 3rem;text-align:center;color:#fff}
.page-banner h1{font-size:clamp(2rem,4vw,3rem);font-weight:900;text-shadow:0 3px 12px rgba(0,0,0,.3)}
.page-banner p{font-size:1.1rem;opacity:.85;max-width:600px;margin:.8rem auto 0}

/* SECTION */
.section{padding:5rem 2rem;max-width:1100px;margin:0 auto}
.section-title{font-size:2rem;font-weight:900;color:#003DA5;margin-bottom:.5rem}
.section-sub{color:#666;margin-bottom:2.5rem}
.divider{width:60px;height:4px;background:linear-gradient(90deg,#FFD700,#003DA5);border-radius:2px;margin:1rem 0 2rem}

/* PRINS PAGE */
.prins-layout{display:grid;grid-template-columns:1fr 1fr;gap:4rem;align-items:start;padding:4rem 2rem;max-width:1100px;margin:0 auto}
.prins-photo-wrap{position:relative}
.prins-photo{width:100%;border-radius:20px;box-shadow:0 20px 50px rgba(0,0,0,.2)}
.prins-badge{position:absolute;bottom:-16px;left:50%;transform:translateX(-50%);background:#FFD700;color:#003DA5;font-weight:900;font-size:.85rem;padding:.5rem 1.4rem;border-radius:999px;white-space:nowrap;box-shadow:0 4px 14px rgba(255,215,0,.5)}
.prins-info{padding-top:1rem}
.prins-info h1{font-size:2.4rem;font-weight:900;color:#003DA5;margin-bottom:.5rem}
.prins-info .jaar-badge{display:inline-block;background:#003DA5;color:#FFD700;font-weight:800;font-size:.9rem;padding:.35rem 1rem;border-radius:999px;margin-bottom:1.2rem}
.prins-info p{font-size:1.1rem;line-height:1.8;color:#333;margin-bottom:1.5rem}

/* EVENEMENTEN */
.events-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.5rem;padding:3rem 2rem;max-width:1100px;margin:0 auto}
.event-card{background:#fff;border-radius:16px;box-shadow:0 4px 20px rgba(0,0,0,.08);overflow:hidden;cursor:pointer;transition:transform .2s,box-shadow .2s}
.event-card:hover{transform:translateY(-4px);box-shadow:0 12px 35px rgba(0,0,0,.14)}
.event-card-header{background:linear-gradient(135deg,#003DA5,#0050cc);padding:1.5rem;color:#fff;display:flex;align-items:center;gap:1rem}
.event-card-icon{font-size:2rem}
.event-card-header h3{font-size:1.2rem;font-weight:800}
.event-card-body{padding:1.3rem 1.5rem}
.event-meta{display:flex;flex-direction:column;gap:.4rem;margin-bottom:.8rem}
.event-meta-item{display:flex;align-items:center;gap:.5rem;font-size:.9rem;color:#555}
.event-meta-item span:first-child{color:#003DA5;font-size:1rem}
.event-card-body p{font-size:.92rem;color:#666;line-height:1.6}

/* EVENT DETAIL */
.event-detail{max-width:800px;margin:0 auto;padding:3rem 2rem}
.event-detail-meta{display:flex;flex-wrap:wrap;gap:1rem;margin:1.5rem 0 2rem}
.event-meta-badge{display:flex;align-items:center;gap:.5rem;background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:.6rem 1.1rem;font-size:.92rem;font-weight:600;color:#333}
.event-meta-badge .icon{font-size:1.1rem}
.event-detail h2{font-size:1.6rem;font-weight:800;color:#003DA5;margin:2rem 0 .8rem}
.event-detail p{line-height:1.8;color:#444;margin-bottom:1rem}
.event-program{background:#fff;border-radius:16px;padding:1.5rem;box-shadow:0 4px 20px rgba(0,0,0,.07);margin-top:1.5rem}
.program-item{display:flex;gap:1rem;padding:.6rem 0;border-bottom:1px solid #f0f0f0}
.program-item:last-child{border-bottom:none}
.program-time{font-weight:800;color:#003DA5;min-width:60px;font-size:.9rem}
.program-act{font-size:.9rem;color:#444}

/* DANSMARIEKES */
.dansmarieken-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.5rem;padding:2rem 0}
.dansmarieken-card{background:#fff;border-radius:14px;padding:1.5rem;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.07)}
.dansmarieken-card .avatar{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#FFD700,#003DA5);display:flex;align-items:center;justify-content:center;font-size:2rem;margin:0 auto 1rem}
.dansmarieken-card h4{font-weight:800;color:#003DA5;margin-bottom:.3rem}
.dansmarieken-card p{font-size:.85rem;color:#666}

/* OUD PRINSEN */
.oud-prinsen-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:1.2rem;padding:2rem 0}
.op-card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 4px 16px rgba(0,0,0,.08);transition:transform .2s,box-shadow .2s}
.op-card:hover{transform:translateY(-4px);box-shadow:0 10px 28px rgba(0,0,0,.14)}
.op-card-body{padding:.8rem .9rem}
.op-card-jaar{font-size:.75rem;font-weight:800;color:#FFD700;background:#003DA5;padding:.2rem .6rem;border-radius:999px;width:fit-content;margin-bottom:.35rem}
.op-card-naam{font-weight:800;color:#003DA5;font-size:.85rem;line-height:1.3}

/* MERCH */
.merch-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:2rem;padding:2rem 0}
.merch-card{background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.08);transition:transform .2s,box-shadow .2s}
.merch-card:hover{transform:translateY(-4px);box-shadow:0 12px 35px rgba(0,0,0,.14)}
.merch-card img{width:100%;height:220px;object-fit:cover}
.merch-card-body{padding:1.2rem 1.4rem}
.merch-card-body h3{font-size:1.1rem;font-weight:800;color:#003DA5;margin-bottom:.3rem}
.merch-card-body p{font-size:.9rem;color:#666;margin-bottom:.8rem}
.merch-card-body .prijs{font-size:1.3rem;font-weight:900;color:#003DA5}

/* SPONSOREN */
.sponsors-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1.5rem;padding:2rem 0}
.sponsor-card{background:#fff;border-radius:14px;padding:1.5rem;text-align:center;box-shadow:0 4px 20px rgba(0,0,0,.07);display:flex;flex-direction:column;align-items:center;gap:.8rem}
.sponsor-card img{max-height:80px;width:auto;object-fit:contain}
.sponsor-logo-placeholder{width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,#e8eeff,#c8d8ff);display:flex;align-items:center;justify-content:center;font-size:1.8rem}
.sponsor-card h4{font-weight:800;color:#003DA5;font-size:.95rem}
.sponsor-card p{font-size:.82rem;color:#888}

/* AANMELDEN */
.form-wrap{max-width:600px;margin:0 auto;padding:2rem 0}
.form-group{margin-bottom:1.4rem}
.form-group label{display:block;font-weight:700;color:#333;margin-bottom:.5rem}
.form-group input,.form-group select,.form-group textarea{width:100%;padding:.75rem 1rem;border:2px solid #e0e0e0;border-radius:10px;font-family:'Nunito',sans-serif;font-size:1rem;transition:border-color .2s}
.form-group input:focus,.form-group select:focus,.form-group textarea:focus{outline:none;border-color:#003DA5}
.form-group textarea{resize:vertical;min-height:120px}

/* VRIENDENKRING */
.vk-grid{display:grid;grid-template-columns:1fr 1fr;gap:3rem;padding:2rem 0}
.vk-block{background:#fff;border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.07)}
.vk-block h3{font-size:1.2rem;font-weight:800;color:#003DA5;margin-bottom:.8rem}
.vk-block p{line-height:1.7;color:#444;font-size:.95rem}
.vk-block ul{padding-left:1.2rem;color:#444;font-size:.95rem;line-height:2}

/* ADMIN */
#page-admin{background:#f0f4ff;min-height:100vh}
.admin-wrap{max-width:900px;margin:0 auto;padding:2rem}
.admin-header{background:linear-gradient(135deg,#001240,#003DA5);color:#fff;border-radius:16px 16px 0 0;padding:2rem;display:flex;align-items:center;gap:1rem}
.admin-header h2{font-size:1.6rem;font-weight:900}
.admin-lock{background:#fff2;border:none;color:#FFD700;font-size:1.8rem;cursor:pointer;padding:.3rem;border-radius:8px}
#admin-login{background:#fff;border-radius:0 0 16px 16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.1)}
#admin-login p{color:#666;margin-bottom:1rem}
.admin-pw-row{display:flex;gap:.8rem}
.admin-pw-row input{flex:1;padding:.75rem 1rem;border:2px solid #e0e0e0;border-radius:10px;font-family:'Nunito',sans-serif;font-size:1rem}
#admin-panel-content{display:none;background:#fff;border-radius:0 0 16px 16px;box-shadow:0 4px 20px rgba(0,0,0,.1)}
.admin-tabs{display:flex;border-bottom:2px solid #e8eeff;overflow-x:auto}
.admin-tab{padding:1rem 1.5rem;font-weight:700;font-size:.9rem;cursor:pointer;color:#888;border-bottom:3px solid transparent;margin-bottom:-2px;white-space:nowrap;transition:color .2s,border-color .2s}
.admin-tab.active{color:#003DA5;border-bottom-color:#003DA5}
.admin-tab-content{display:none;padding:2rem}
.admin-tab-content.active{display:block}
.admin-field{margin-bottom:1.4rem}
.admin-field label{display:block;font-weight:700;color:#333;margin-bottom:.5rem;font-size:.9rem}
.admin-field input,.admin-field textarea,.admin-field select{width:100%;padding:.7rem .9rem;border:2px solid #e0e0e0;border-radius:8px;font-family:'Nunito',sans-serif;font-size:.95rem;transition:border-color .2s}
.admin-field input:focus,.admin-field textarea:focus{outline:none;border-color:#003DA5}
.admin-field textarea{min-height:100px;resize:vertical}
.admin-event-block{background:#f8f9ff;border:1px solid #e0e8ff;border-radius:12px;padding:1.4rem;margin-bottom:1.2rem}
.admin-event-block h4{font-weight:800;color:#003DA5;margin-bottom:1rem;font-size:1rem}
.admin-save-bar{padding:1.2rem 2rem;border-top:1px solid #e8eeff;display:flex;gap:.8rem;align-items:center}
.admin-msg{color:#2e7d32;font-weight:700;font-size:.9rem}
.admin-merch-items,.admin-sponsor-items{margin-bottom:1rem}
.admin-merch-item,.admin-sponsor-item{background:#f8f9ff;border:1px solid #e0e8ff;border-radius:10px;padding:1rem;margin-bottom:.8rem;display:grid;gap:.6rem}
.admin-merch-item{grid-template-columns:1fr 1fr}
.admin-sponsor-item{grid-template-columns:1fr auto}
.admin-item-full{grid-column:1/-1}
.admin-item-del{background:#fee;border:1px solid #fcc;color:#c00;border-radius:6px;padding:.3rem .7rem;cursor:pointer;font-size:.85rem;font-weight:700;height:fit-content}
.admin-add-btn{background:#eef2ff;border:2px dashed #003DA5;color:#003DA5;border-radius:8px;padding:.6rem 1.2rem;font-weight:700;cursor:pointer;width:100%;transition:background .2s}
.admin-add-btn:hover{background:#dde6ff}

/* FOOTER */
footer{background:linear-gradient(135deg,#001240,#002a80);color:#fff;padding:3rem 2rem;text-align:center}
.footer-logo{height:60px;width:auto;margin:0 auto 1rem;filter:drop-shadow(0 2px 8px rgba(0,0,0,.4))}
footer h3{font-size:1.3rem;font-weight:900;margin-bottom:.3rem}
footer p{opacity:.7;font-size:.9rem;margin:.3rem 0}
.footer-links{display:flex;justify-content:center;gap:1.5rem;margin:1.2rem 0;flex-wrap:wrap}
.footer-links a{opacity:.7;font-size:.9rem;transition:opacity .2s}
.footer-links a:hover{opacity:1;color:#FFD700}
.footer-copy{border-top:1px solid rgba(255,255,255,.15);margin-top:1.5rem;padding-top:1.2rem;opacity:.5;font-size:.82rem}

/* CONTACT CARDS */
.contact-card{display:flex;flex-direction:column;background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,80,.09);border:2px solid transparent;transition:border-color .2s,transform .2s,box-shadow .2s;overflow:hidden;text-decoration:none;color:inherit}
.contact-card:hover{border-color:#FFD700;transform:translateY(-4px);box-shadow:0 8px 32px rgba(0,0,80,.14)}
.contact-card-icon{background:linear-gradient(135deg,#003DA5,#001240);color:#FFD700;font-size:2.2rem;padding:1.4rem;text-align:center}
.contact-card-body{padding:1.4rem 1.4rem 1.6rem;display:flex;flex-direction:column;gap:.6rem;flex:1}
.contact-card-body h3{font-size:1.05rem;font-weight:800;color:#001240;margin:0}
.contact-card-body p{font-size:.9rem;color:#555;line-height:1.6;margin:0;flex:1}
.contact-card-email{display:inline-block;margin-top:.4rem;font-size:.85rem;font-weight:700;color:#003DA5;word-break:break-all}
.contact-card:hover .contact-card-email{color:#001240}

/* HAMBURGER */
.hamburger-btn{display:none;background:none;border:none;cursor:pointer;padding:.4rem .6rem;color:#FFD700;font-size:1.7rem;line-height:1}
.mobile-nav-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:1500}
.mobile-nav-overlay.open{display:block}
.mobile-nav{position:fixed;top:0;left:0;height:100%;width:280px;background:linear-gradient(180deg,#001240,#002a80);z-index:1600;transform:translateX(-100%);transition:transform .28s cubic-bezier(.4,0,.2,1);overflow-y:auto;padding-top:1rem}
.mobile-nav.open{transform:translateX(0)}
.mobile-nav-header{display:flex;align-items:center;justify-content:space-between;padding:.8rem 1.2rem 1rem;border-bottom:1px solid rgba(255,215,0,.2)}
.mobile-nav-logo{height:44px;width:auto;filter:drop-shadow(0 1px 4px rgba(0,0,0,.4))}
.mobile-nav-close{background:none;border:none;color:#FFD700;font-size:1.6rem;cursor:pointer;line-height:1}
.mobile-nav-links{padding:.5rem 0}
.mobile-nav-links a,.mobile-nav-links .mn-group-label{display:flex;align-items:center;gap:.6rem;color:rgba(255,255,255,.9);font-weight:700;font-size:.97rem;padding:.75rem 1.4rem;transition:background .15s,color .15s;text-decoration:none}
.mobile-nav-links a:hover{background:rgba(255,215,0,.1);color:#FFD700}
.mobile-nav-links .mn-group-label{color:rgba(255,215,0,.8);font-size:.78rem;letter-spacing:1.5px;text-transform:uppercase;padding-top:1rem;padding-bottom:.3rem;pointer-events:none}
.mobile-nav-links .mn-sub{padding-left:2.4rem;font-size:.9rem;color:rgba(255,255,255,.75)}
.mobile-nav-links .mn-sub:hover{color:#FFD700}
.mobile-nav-links .mn-divider{border:none;border-top:1px solid rgba(255,255,255,.1);margin:.5rem 1.2rem}

/* COOKIE / CONFETTI NOTICE */
#confetti-notice{position:fixed;bottom:0;left:0;right:0;z-index:8000;background:linear-gradient(135deg,#001240,#002a80);border-top:3px solid #FFD700;padding:1rem 1.5rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap;transform:translateY(100%);transition:transform .4s ease;box-shadow:0 -4px 20px rgba(0,0,0,.3)}
#confetti-notice.show{transform:translateY(0)}
.cn-text{flex:1;color:#fff;font-size:.9rem;line-height:1.5;min-width:200px}
.cn-text strong{color:#FFD700;font-size:1rem}
.cn-btns{display:flex;gap:.6rem;flex-wrap:wrap}
.cn-accept{background:#FFD700;color:#003DA5;font-weight:800;font-size:.88rem;padding:.45rem 1.2rem;border-radius:999px;border:none;cursor:pointer;transition:background .2s}
.cn-accept:hover{background:#ffc800}
.cn-decline{background:transparent;color:rgba(255,255,255,.7);font-weight:600;font-size:.85rem;padding:.45rem 1rem;border-radius:999px;border:1px solid rgba(255,255,255,.3);cursor:pointer;transition:all .2s}
.cn-decline:hover{border-color:#fff;color:#fff}

/* RESPONSIVE */
@media(max-width:768px){
  .hero-content{flex-direction:column;text-align:center}
  .hero-photo{width:260px;height:320px}
  .prins-layout{grid-template-columns:1fr;gap:2rem}
  .vk-grid{grid-template-columns:1fr}
  .header-nav-bar{display:none}
  .hamburger-btn{display:flex;align-items:center}
  .events-grid{grid-template-columns:1fr}
  .home-agenda-grid{grid-template-columns:repeat(2,1fr)}
  .oud-prinsen-grid{grid-template-columns:repeat(auto-fill,minmax(120px,1fr))}
}

/* HOME SECTIONS */
.home-section{padding:5rem 2rem;max-width:1100px;margin:0 auto}
.home-section-full{padding:5rem 2rem}
.home-section h2{font-size:1.9rem;font-weight:900;color:#003DA5;margin-bottom:.4rem}
.home-section-sub{color:#888;font-size:.95rem;margin-bottom:2rem}
.home-divider{width:50px;height:4px;background:linear-gradient(90deg,#FFD700,#003DA5);border-radius:2px;margin:.8rem 0 2rem}

/* PRINS PREVIEW */
.home-prins-wrap{display:grid;grid-template-columns:280px 1fr;gap:3rem;align-items:center;background:#fff;border-radius:20px;box-shadow:0 6px 30px rgba(0,0,0,.08);overflow:hidden}
.home-prins-img{width:280px;height:360px;object-fit:cover;display:block}
.home-prins-img-ph{width:280px;height:360px;background:linear-gradient(135deg,#e8eeff,#c8d8ff);display:flex;align-items:center;justify-content:center;font-size:5rem}
.home-prins-body{padding:2.5rem 2.5rem 2.5rem 0}
.home-prins-body .jaar{display:inline-block;background:#003DA5;color:#FFD700;font-weight:800;font-size:.85rem;padding:.3rem .9rem;border-radius:999px;margin-bottom:.8rem}
.home-prins-body h3{font-size:1.8rem;font-weight:900;color:#003DA5;margin-bottom:.8rem}
.home-prins-body p{color:#555;line-height:1.7;font-size:.97rem;margin-bottom:1.5rem}

/* AGENDA */
.home-agenda-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem}
.agenda-card{background:#fff;border-radius:16px;padding:1.2rem 1.4rem;box-shadow:0 3px 16px rgba(0,0,0,.07);cursor:pointer;transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column;gap:.5rem;border-top:4px solid #003DA5}
.agenda-card:hover{transform:translateY(-3px);box-shadow:0 8px 28px rgba(0,0,0,.13)}
.agenda-card .icon{font-size:1.5rem}
.agenda-card .datum{font-size:.8rem;font-weight:700;color:#FFD700;background:#003DA5;padding:.2rem .6rem;border-radius:999px;width:fit-content}
.agenda-card h4{font-weight:800;color:#1a1a2e;font-size:1rem;margin:0}
.agenda-card .loc{font-size:.82rem;color:#888;display:flex;align-items:center;gap:.3rem}

/* SPONSORS BAR */
.home-sponsors-section{background:#fff;border-top:1px solid #e8eeff;border-bottom:1px solid #e8eeff;padding:3rem 2rem}
.home-sponsors-inner{max-width:1100px;margin:0 auto}
.home-sponsors-inner h2{font-size:1.5rem;font-weight:900;color:#003DA5;text-align:center;margin-bottom:.4rem}
.home-sponsors-inner .sub{text-align:center;color:#888;font-size:.9rem;margin-bottom:2rem}
.sponsors-logos-row{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:1.5rem}
.sponsor-logo-item{background:#f8f9ff;border:1px solid #e0e8ff;border-radius:12px;padding:1rem 1.5rem;display:flex;align-items:center;justify-content:center;min-width:120px;min-height:70px;transition:box-shadow .2s}
.sponsor-logo-item:hover{box-shadow:0 4px 16px rgba(0,61,165,.12)}
.sponsor-logo-item img{max-height:50px;max-width:130px;width:auto;object-fit:contain}
.sponsor-logo-item .sp-name{font-weight:800;color:#003DA5;font-size:.9rem;text-align:center}

/* MERCH PREVIEW */
.home-merch-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.5rem}
.home-merch-section{background:linear-gradient(135deg,#f8f9ff,#eef2ff);padding:5rem 2rem}
.home-merch-inner{max-width:1100px;margin:0 auto}

/* VK TEASER */
.home-vk-section{background:linear-gradient(135deg,#003DA5,#001240);padding:4rem 2rem;text-align:center;color:#fff}
.home-vk-section h2{font-size:2rem;font-weight:900;margin-bottom:.8rem}
.home-vk-section p{opacity:.85;max-width:600px;margin:0 auto 2rem;line-height:1.7;font-size:1rem}
.home-vk-section .btns{display:flex;justify-content:center;gap:1rem;flex-wrap:wrap}

/* ADMIN IMAGE UPLOAD */
.admin-img-preview{max-height:130px;width:auto;border-radius:8px;margin-bottom:.6rem;display:none;border:2px solid #e0e8ff}
.btn-upload{display:inline-flex;align-items:center;gap:.4rem;background:#f0f4ff;border:2px solid #003DA5;color:#003DA5;font-weight:700;font-size:.85rem;padding:.45rem 1rem;border-radius:8px;cursor:pointer;transition:background .2s;white-space:nowrap}
.btn-upload:hover{background:#dde6ff}
.upload-row{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap}
.upload-row input[type=text]{flex:1;min-width:0}

@media(max-width:768px){
  .home-prins-wrap{grid-template-columns:1fr}
  .home-prins-img,.home-prins-img-ph{width:100%;height:240px}
  .home-prins-body{padding:1.5rem}
}
"""

# ── GARLANDS SVG ────────────────────────────────────────────────────────────────
GARLANDS_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" style="width:100%;height:120px">
<defs>
  <radialGradient id="g1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFD700"/><stop offset="100%" stop-color="#FFA500"/></radialGradient>
  <radialGradient id="g2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FF4444"/><stop offset="100%" stop-color="#cc0000"/></radialGradient>
  <radialGradient id="g3" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#4CAF50"/><stop offset="100%" stop-color="#2e7d32"/></radialGradient>
  <radialGradient id="g4" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#9C27B0"/><stop offset="100%" stop-color="#6a1b9a"/></radialGradient>
</defs>
<path d="M0,30 Q120,85 240,30 Q360,85 480,30 Q600,85 720,30 Q840,85 960,30 Q1080,85 1200,30 Q1320,85 1440,30" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>
<path d="M0,50 Q180,100 360,50 Q540,100 720,50 Q900,100 1080,50 Q1260,100 1440,50" fill="none" stroke="rgba(255,215,0,0.3)" stroke-width="2"/>
''' + ''.join([
    f'<ellipse cx="{30+i*60}" cy="{35 + 30*(0.5+0.5*__import__(\"math\").sin(i*1.1)):.0f}" rx="8" ry="12" fill="url(#g{(i%4)+1})" opacity=".9"/>'
    for i in range(24)
]) + '''
</svg>"""

# ── LOGO SVG (inline fallback) ───────────────────────────────────────────────
def logo_img(extra=''):
    return f'<img src="{LOGO}" alt="Snevelbokkenland" {extra}>'

# ── HTML ─────────────────────────────────────────────────────────────────────
def build_html():
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Snevelbokkenland – Carnavalsvereniging Heeswijk-Dinther</title>
<link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,400;0,600;0,700;0,800;0,900;1,800;1,900&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<!-- ═══════════════════════════ HEADER ═══════════════════════════ -->
<header id="site-header">
  <div class="header-logo-bar">
    {logo_img('style="height:70px;width:auto;filter:drop-shadow(0 2px 8px rgba(0,0,0,.5))"')}
    <span class="site-title">Snevelbokkenland</span>
    <button class="hamburger-btn" id="hamburger-btn" aria-label="Menu" onclick="toggleMobileNav()">&#9776;</button>
  </div>
  <nav class="header-nav-bar">
    <div class="nav-item"><a href="#home">Home</a></div>
    <div class="nav-item"><a href="#prins">Prins(es)</a></div>
    <div class="nav-item"><a href="#jeugdprins">Jeugdprins(es)</a></div>
    <div class="nav-item">
      <a href="#evenementen">Evenementen ▾</a>
      <div class="nav-dropdown">
        <a href="#pronkzitting">Pronkzitting</a>
        <a href="#optocht">Optocht</a>
        <a href="#ontbijtshow">Ontbijtshow</a>
        <a href="#boerenbruiloft">Boerenbruiloft</a>
        <a href="#snevelbokkenplusbal">SnevelbokkenplusBal</a>
      </div>
    </div>
    <div class="nav-item"><a href="#dansmariekes">Dansmariekes</a></div>
    <div class="nav-item"><a href="#vriendenkring">Vriendenkring</a></div>
    <div class="nav-item"><a href="#oud-prinsen">Oud-Prinsen</a></div>
    <div class="nav-item"><a href="#merchandise">Merchandise</a></div>
    <div class="nav-item"><a href="#sponsoren">Sponsoren</a></div>
    <div class="nav-item"><a href="#aanmelden">Contact</a></div>
  </nav>
</header>

<!-- ═══════════════════════════ MOBILE NAV ═══════════════════════════ -->
<div class="mobile-nav-overlay" id="mobile-nav-overlay" onclick="closeMobileNav()"></div>
<nav class="mobile-nav" id="mobile-nav">
  <div class="mobile-nav-header">
    {logo_img('class="mobile-nav-logo"')}
    <button class="mobile-nav-close" onclick="closeMobileNav()" aria-label="Sluiten">&#10005;</button>
  </div>
  <div class="mobile-nav-links">
    <a href="#home" onclick="closeMobileNav()">&#127968; Home</a>
    <a href="#prins" onclick="closeMobileNav()">&#128081; Prins(es)</a>
    <a href="#jeugdprins" onclick="closeMobileNav()">&#127775; Jeugdprins(es)</a>
    <span class="mn-group-label">Evenementen</span>
    <a href="#evenementen" onclick="closeMobileNav()">&#128197; Overzicht</a>
    <a href="#pronkzitting" class="mn-sub" onclick="closeMobileNav()">&#127903; Pronkzitting</a>
    <a href="#optocht" class="mn-sub" onclick="closeMobileNav()">&#127882; Optocht</a>
    <a href="#ontbijtshow" class="mn-sub" onclick="closeMobileNav()">&#9749; Ontbijtshow</a>
    <a href="#boerenbruiloft" class="mn-sub" onclick="closeMobileNav()">&#128092; Boerenbruiloft</a>
    <a href="#snevelbokkenplusbal" class="mn-sub" onclick="closeMobileNav()">&#127926; SnevelbokkenplusBal</a>
    <hr class="mn-divider">
    <a href="#dansmariekes" onclick="closeMobileNav()">&#128131; Dansmariekes</a>
    <a href="#vriendenkring" onclick="closeMobileNav()">&#129309; Vriendenkring</a>
    <a href="#oud-prinsen" onclick="closeMobileNav()">&#128443; Oud-Prinsen</a>
    <a href="#merchandise" onclick="closeMobileNav()">&#128722; Merchandise</a>
    <a href="#sponsoren" onclick="closeMobileNav()">&#11088; Sponsoren</a>
    <hr class="mn-divider">
    <a href="#aanmelden" onclick="closeMobileNav()">&#9993; Contact</a>
  </div>
</nav>

<!-- ═══════════════════════════ COOKIE / CONFETTI NOTICE ═══════════════════════════ -->
<div id="confetti-notice" role="dialog" aria-label="Cookie-melding">
  <div class="cn-text">
    <strong>&#127881; Confetti &amp; Cookies!</strong><br>
    We gebruiken cookies om jouw bezoek aan Snevelbokkenland zo feestelijk mogelijk te maken. Geen ellende, gewoon carnaval!
  </div>
  <div class="cn-btns">
    <button class="cn-accept" onclick="acceptCookies()">&#127882; Joepie, akkoord!</button>
    <button class="cn-decline" onclick="declineCookies()">Nee bedankt</button>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: HOME ═══════════════════════════ -->
<div class="page active" id="page-home">
  <section class="hero">
    <div class="hero-garlands">{GARLANDS_SVG}</div>
    <div class="hero-content">
      <div class="hero-text">
        <div class="kicker">&#127881; Carnaval 2026</div>
        <h1 id="home-title">Welkom in<br>Snevelbokkenland!</h1>
        <p id="home-subtitle">Dé carnavalsvereniging van Heeswijk-Dinther. Samen maken we er ieder jaar een onvergetelijk feest van!</p>
        <div class="hero-btns">
          <button class="btn-primary" onclick="navigate('evenementen')">&#127882; Evenementen</button>
          <button class="btn-outline" onclick="navigate('prins')">Onze Prins</button>
        </div>
      </div>
      <img id="home-prins-photo" src="{HERO_PRINCE}" alt="Prins" class="hero-photo">
    </div>
  </section>

  <!-- PRINS PREVIEW -->
  <div class="home-section">
    <h2>&#128081; Onze Prins van Snevelbokkenland</h2>
    <div class="home-divider"></div>
    <div class="home-prins-wrap" id="home-prins-wrap">
      <img id="home-prins-img" src="{HERO_PRINCE}" alt="Prins" class="home-prins-img">
      <div class="home-prins-body">
        <div class="jaar" id="home-prins-jaar">Prins 2026</div>
        <h3 id="home-prins-naam">Prins Frank I</h3>
        <p id="home-prins-desc">Op vrijdag 7 november barstte de spanning los in een bomvol Stanserhorn, waar niemand minder dan Frank van Aspert werd onthuld als Prins Frank I voor carnaval 2026. Zijn motto: <em>"HDL mé hil oew hart, knallen wij uit onze voeg!"</em></p>
        <button class="btn-blue btn-sm" onclick="navigate('prins')">Lees meer over de Prins &#10148;</button>
      </div>
    </div>
  </div>

  <!-- AGENDA -->
  <div style="background:#fff;border-top:1px solid #e8eeff;border-bottom:1px solid #e8eeff;padding:5rem 2rem">
    <div style="max-width:1100px;margin:0 auto">
      <h2 style="font-size:1.9rem;font-weight:900;color:#003DA5;margin-bottom:.4rem">&#128197; Evenementen 2026</h2>
      <p style="color:#888;font-size:.95rem;margin-bottom:.8rem">Zet deze data alvast in je agenda!</p>
      <div class="home-divider"></div>
      <div class="home-agenda-grid" id="home-agenda-grid"></div>
      <div style="text-align:center;margin-top:2rem">
        <button class="btn-blue btn-sm" onclick="navigate('evenementen')">Alle evenementen bekijken &#10148;</button>
      </div>
    </div>
  </div>

  <!-- SPONSOREN -->
  <div class="home-sponsors-section" id="home-sponsors-section">
    <div class="home-sponsors-inner">
      <h2>&#129309; Onze Sponsoren</h2>
      <p class="sub">Dankzij onze sponsors kunnen wij elk jaar een geweldig carnaval neerzetten</p>
      <div class="sponsors-logos-row" id="home-sponsors-logos"></div>
      <div style="text-align:center;margin-top:2rem">
        <button class="btn-blue btn-sm" onclick="navigate('sponsoren')">Alle sponsoren bekijken &#10148;</button>
      </div>
    </div>
  </div>

  <!-- MERCHANDISE -->
  <div class="home-merch-section">
    <div class="home-merch-inner">
      <h2 style="font-size:1.9rem;font-weight:900;color:#003DA5;margin-bottom:.4rem">&#127947; Merchandise</h2>
      <p style="color:#888;font-size:.95rem;margin-bottom:.8rem">Draag de kleuren van Snevelbokkenland!</p>
      <div class="home-divider"></div>
      <div class="home-merch-grid" id="home-merch-grid"></div>
      <div style="text-align:center;margin-top:2rem">
        <button class="btn-blue btn-sm" onclick="navigate('merchandise')">Bekijk alle merchandise &#10148;</button>
      </div>
    </div>
  </div>

  <!-- VRIENDENKRING TEASER -->
  <div class="home-vk-section">
    <h2>&#129309; Stichting Vriendenkring</h2>
    <p>Steun het carnaval in Heeswijk-Dinther en word vriend van Snevelbokkenland. Geniet van exclusieve voordelen zoals gratis entree bij de Pronkzitting en persoonlijk hoog bezoek. Slechts €35 per jaar!</p>
    <div class="btns">
      <button class="btn-primary" onclick="navigate('vriendenkring')">Meer over de Vriendenkring</button>
      <button class="btn-outline" onclick="navigate('aanmelden')">&#9993; Contact</button>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: PRINS ═══════════════════════════ -->
<div class="page" id="page-prins">
  <div class="page-banner">
    <h1>&#128081; Prins(es) van Snevelbokkenland</h1>
    <p>De hoogheid van ons carnavalsrijk</p>
  </div>
  <div class="prins-layout">
    <div class="prins-photo-wrap">
      <img id="prins-portrait-img" src="{PRINCE_PORTRAIT}" alt="Prins" class="prins-photo">
      <div class="prins-badge" id="prins-badge-jaar">Prins 2026</div>
    </div>
    <div class="prins-info">
      <h1 id="prins-naam">Frank d'n Eerste</h1>
      <div class="jaar-badge" id="prins-jaar-badge">Seizoen 2026</div>
      <p id="prins-desc">Met trots presenteren wij onze prins voor carnaval 2026. Onder zijn bezielende leiding gaan wij er dit seizoen een onvergetelijk feest van maken. Vivat de Prins!</p>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: JEUGDPRINS ═══════════════════════════ -->
<div class="page" id="page-jeugdprins">
  <div class="page-banner">
    <h1>&#11088; Jeugdprins(es) van Snevelbokkenland</h1>
    <p>De jonge hoogheid van ons carnavalsrijk</p>
  </div>
  <div class="prins-layout">
    <div class="prins-photo-wrap">
      <div id="jeugdprins-photo-ph" style="width:100%;aspect-ratio:3/4;background:linear-gradient(135deg,#e8eeff,#c8d8ff);border-radius:20px;display:flex;align-items:center;justify-content:center;font-size:5rem">&#11088;</div>
      <img id="jeugdprins-portrait-img" src="" alt="Jeugdprins" class="prins-photo" style="display:none">
      <div class="prins-badge" id="jeugdprins-badge-jaar">Jeugdprins 2026</div>
    </div>
    <div class="prins-info">
      <h1 id="jeugdprins-naam">Jeugdprins 2026</h1>
      <div class="jaar-badge" id="jeugdprins-jaar-badge">Seizoen 2026</div>
      <p id="jeugdprins-desc">De jeugdprins van Snevelbokkenland wordt elk jaar gekozen en vertegenwoordigt de jongere generatie van ons carnavalsrijk. Vivat de Jeugdprins!</p>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: EVENEMENTEN OVERVIEW ═══════════════════════════ -->
<div class="page" id="page-evenementen">
  <div class="page-banner">
    <h1>&#127882; Evenementen</h1>
    <p>Alle activiteiten van Snevelbokkenland op een rij</p>
  </div>
  <div class="events-grid" id="events-overview-grid"></div>
</div>

<!-- ═══════════════════════════ PAGE: PRONKZITTING ═══════════════════════════ -->
<div class="page" id="page-pronkzitting">
  <div class="page-banner">
    <h1>&#127881; Pronkzitting</h1>
    <p id="pronkzitting-banner-sub">De feestelijke opening van het carnavalsseizoen</p>
  </div>
  <div class="event-detail" id="event-detail-pronkzitting"></div>
</div>

<!-- ═══════════════════════════ PAGE: OPTOCHT ═══════════════════════════ -->
<div class="page" id="page-optocht">
  <div class="page-banner">
    <h1>&#127916; Optocht</h1>
    <p id="optocht-banner-sub">De grote carnavalsoptocht door Heeswijk-Dinther</p>
  </div>
  <div class="event-detail" id="event-detail-optocht"></div>
</div>

<!-- ═══════════════════════════ PAGE: ONTBIJTSHOW ═══════════════════════════ -->
<div class="page" id="page-ontbijtshow">
  <div class="page-banner">
    <h1>&#9749; Ontbijtshow</h1>
    <p id="ontbijtshow-banner-sub">Gezellig ontbijten met entertainment</p>
  </div>
  <div class="event-detail" id="event-detail-ontbijtshow"></div>
</div>

<!-- ═══════════════════════════ PAGE: BOERENBRUILOFT ═══════════════════════════ -->
<div class="page" id="page-boerenbruiloft">
  <div class="page-banner">
    <h1>&#128142; Boerenbruiloft</h1>
    <p id="boerenbruiloft-banner-sub">Het traditionele boerenbruiloft feest</p>
  </div>
  <div class="event-detail" id="event-detail-boerenbruiloft"></div>
</div>

<!-- ═══════════════════════════ PAGE: SNEVELBOKKENPLUSBAL ═══════════════════════════ -->
<div class="page" id="page-snevelbokkenplusbal">
  <div class="page-banner">
    <h1>&#127881; SnevelbokkenplusBal</h1>
    <p id="snevelbokkenplusbal-banner-sub">Het exclusieve bal voor 50-plussers</p>
  </div>
  <div class="event-detail" id="event-detail-snevelbokkenplusbal"></div>
</div>

<!-- ═══════════════════════════ PAGE: DANSMARIEKES ═══════════════════════════ -->
<div class="page" id="page-dansmariekes">
  <div class="page-banner">
    <h1>&#128131; Dansmariekes</h1>
    <p>De dansgroep van Snevelbokkenland</p>
  </div>
  <div class="section">
    <p style="font-size:1.1rem;line-height:1.8;color:#444;max-width:750px;margin-bottom:2rem">
      Je kunt ze niet missen, de dansmariekes van HDL! De dansmariekes bestaan uit een gezellige groep meiden, verdeeld over drie groepen: <strong>Future</strong>, <strong>D-Votion</strong> en <strong>Amazed</strong>.
    </p>
    <div class="divider"></div>
    <h3 class="section-title">Onze drie groepen</h3>
    <div class="dansmarieken-grid">
      <div class="dansmarieken-card"><div class="avatar" style="background:linear-gradient(135deg,#ffb6c1,#ff69b4)">&#128131;</div><h4>Future</h4><p>De jongste groep — herkenbaar aan de <strong>roze jurkjes</strong></p></div>
      <div class="dansmarieken-card"><div class="avatar" style="background:linear-gradient(135deg,#90ee90,#2e8b57)">&#128131;</div><h4>D-Votion</h4><p>De middelste groep — herkenbaar aan de <strong>groene jurkjes</strong></p></div>
      <div class="dansmarieken-card"><div class="avatar" style="background:linear-gradient(135deg,#90ee90,#2e8b57)">&#128131;</div><h4>Amazed</h4><p>De oudste groep — herkenbaar aan de <strong>groene jurkjes</strong></p></div>
    </div>

    <div style="background:#fff;border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.07);margin-top:2rem">
      <h3 style="font-weight:800;color:#003DA5;margin-bottom:.8rem">&#127775; Trainingen & optredens</h3>
      <p style="color:#444;line-height:1.8">De trainingen voor de <strong>gardedans</strong> starten elk jaar na de meivakantie. In november moet deze dans klaar zijn om te laten zien tijdens de ontmanteling, onthulling van het jeugdpaar en de prinsenrecepties. Daarna komt de <strong>showdans</strong> erbij — met elk jaar een mooi thema (o.a. Frozen, Vaiana, Creepy Circus, 90's en ABBA). Alle dames zien er altijd tiptop uit met mooie make-up en strakke kapsels.</p>
    </div>

    <div style="background:#fff;border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.07);margin-top:1.5rem">
      <h3 style="font-weight:800;color:#003DA5;margin-bottom:.8rem">&#9997; Op de wachtlijst?</h3>
      <p style="color:#444;line-height:1.8;margin-bottom:1rem">Afhankelijk van het aantal vrije plekken en groepen kunnen meiden op de wachtlijst worden uitgenodigd voor een kennismakings-/auditieavond. Stuur een mail met je naam, geboortedatum en telefoonnummer naar <a href="mailto:info@snevelbokkenland.nl" style="color:#003DA5;font-weight:700">info@snevelbokkenland.nl</a>.</p>
      <div style="display:flex;gap:1rem;flex-wrap:wrap">
        <a href="https://www.facebook.com/DansmarekesHDL" target="_blank" style="display:inline-flex;align-items:center;gap:.5rem;background:#1877f2;color:#fff;padding:.5rem 1.2rem;border-radius:999px;font-weight:700;font-size:.9rem">&#128081; Facebook: @Dansmariekes-HDL</a>
        <a href="https://www.instagram.com/dansmariekes_hdl" target="_blank" style="display:inline-flex;align-items:center;gap:.5rem;background:linear-gradient(135deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);color:#fff;padding:.5rem 1.2rem;border-radius:999px;font-weight:700;font-size:.9rem">&#128247; Instagram: @dansmariekes_hdl</a>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: VRIENDENKRING ═══════════════════════════ -->
<div class="page" id="page-vriendenkring">
  <div class="page-banner">
    <h1>&#129309; Stichting Vriendenkring</h1>
    <p>De steunpilaar van Snevelbokkenland</p>
  </div>
  <div class="section">
    <p style="font-size:1.1rem;line-height:1.8;color:#444;max-width:750px;margin-bottom:2rem">
      De Stichting Vriendenkring Snevelbokkenland is de officiële steunstichting van onze carnavalsvereniging. De stichting zorgt voor de financiële ondersteuning van activiteiten en investeringen die bijdragen aan het carnaval in Heeswijk-Dinther.
    </p>
    <div class="divider"></div>
    <div class="vk-grid">
      <div class="vk-block">
        <h3>&#128218; Ontstaan</h3>
        <p>In 1983, nadat Martien van Zutphen had geregeerd over Snevelbokkenland, was de Hoge Raad op volle sterkte. Martien en Cees de Been wilden toch betrokken blijven bij de activiteiten. Zo ontstond het idee om een "vriendenkring" op te richten — een club van oud-prinsen met als doel: financiële ondersteuning van het sociale carnavalsgebeuren in HDL.</p>
      </div>
      <div class="vk-block">
        <h3>&#127775; Wat doet de Vriendenkring?</h3>
        <ul>
          <li>Financiële steun aan carnavalsactiviteiten voor mensen die carnaval niet op de gebruikelijke manier kunnen beleven</li>
          <li>Jaarlijkse attenties voor ernstig en langdurig zieken van HDL</li>
          <li>Gebakje bij de koffie voor bewoners en personeel van Laverhof</li>
          <li>Medailles voor de jeugdoptocht bekostigen</li>
          <li>Bijdrage aan de Dansmariekes en het gehandicaptenbal</li>
          <li>Kraambezoekjes bij Snevelbokken-baby's</li>
          <li>Organisatie Boerenbruiloft 3.0 & "Aanschuiven bij de Prins" bij De Toren</li>
        </ul>
      </div>
      <div class="vk-block">
        <h3>&#9997; Word vriend! — slechts €35 per jaar</h3>
        <p style="margin-bottom:.8rem">Als lid ontvang je:</p>
        <ul>
          <li>Gratis entreekaart voor de Pronkzitting</li>
          <li>Met voorrang extra kaarten bestellen</li>
          <li>Korting op "Aanschuiven bij de Prins" (eten + tonproater + muziek)</li>
          <li>Elk jaar "Hoog Bezoek" van een ex-prins met de carnavalskrant</li>
        </ul>
        <br>
        <p>Lid worden? Neem contact op met secretaris <strong>Heidi Juyn</strong>:<br>
        <a href="mailto:vriendenkring@snevelbokkenland.nl" style="color:#003DA5;font-weight:700">vriendenkring@snevelbokkenland.nl</a></p>
      </div>
      <div class="vk-block">
        <h3>&#128101; Bestuur</h3>
        <ul>
          <li><strong>Voorzitter:</strong> Bart Hoezen</li>
          <li><strong>Secretaris:</strong> Heidi Juyn</li>
        </ul>
        <br>
        <h3 style="margin-top:1rem">&#128222; Contact</h3>
        <p>Stichting Vriendenkring Carnaval H.D.L.<br>
        Heeswijk-Dinther<br><br>
        <a href="mailto:vriendenkring@snevelbokkenland.nl" style="color:#003DA5;font-weight:700">vriendenkring@snevelbokkenland.nl</a></p>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: OUD-PRINSEN ═══════════════════════════ -->
<div class="page" id="page-oud-prinsen">
  <div class="page-banner">
    <h1>&#127941; Oud-Prinsen &amp; Prinsessen</h1>
    <p>De hoogwaardige hooghedens door de jaren heen</p>
  </div>
  <div class="section">
    <p style="color:#666;margin-bottom:2rem">Al sinds 1971 kroont Snevelbokkenland jaarlijks een prins of prinses. Hier vindt u een overzicht van al onze hoogwaardige hooghedens.</p>
    <div class="divider"></div>
    <div class="oud-prinsen-grid">{OUD_PRINSEN_HTML}</div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: MERCHANDISE ═══════════════════════════ -->
<div class="page" id="page-merchandise">
  <div class="page-banner">
    <h1>&#127947; Merchandise</h1>
    <p>Draag de kleuren van Snevelbokkenland</p>
  </div>
  <div class="section">
    <div class="merch-grid" id="merch-grid"></div>
    <div style="margin-top:2rem;background:#fff;border-radius:16px;padding:2rem;box-shadow:0 4px 20px rgba(0,0,0,.07)">
      <h3 style="font-weight:800;color:#003DA5;margin-bottom:1rem">&#128205; Verkooppunten</h3>
      <div style="display:flex;flex-direction:column;gap:.8rem">
        <div style="display:flex;align-items:flex-start;gap:.8rem;padding:.8rem;background:#f0f4ff;border-radius:10px">
          <span style="font-size:1.3rem">&#127978;</span>
          <div><strong>Cigo Paperpoint</strong><br><span style="color:#666;font-size:.9rem">Sint Servatiusstraat 52A, 5473 GB Heeswijk-Dinther</span></div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:.8rem;padding:.8rem;background:#f0f4ff;border-radius:10px">
          <span style="font-size:1.3rem">&#127807;</span>
          <div><strong>van Lieshout Dier &amp; Tuin</strong><br><span style="color:#666;font-size:.9rem">Meerstraat 32, 5473 VW Heeswijk-Dinther</span><br><span style="color:#003DA5;font-size:.85rem;font-weight:700">&#127381; Het embleem van Snevelbokkenland 2026 nu verkrijgbaar!</span></div>
        </div>
        <div style="display:flex;align-items:flex-start;gap:.8rem;padding:.8rem;background:#f0f4ff;border-radius:10px">
          <span style="font-size:1.3rem">&#127881;</span>
          <div><strong>Tijdens het pronkzittingweekend</strong><br><span style="color:#666;font-size:.9rem">In de Snevelbokkenstal (De Zaert), tijdens het evenement</span></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: SPONSOREN ═══════════════════════════ -->
<div class="page" id="page-sponsoren">
  <div class="page-banner">
    <h1>&#129309; Onze Sponsoren</h1>
    <p>Dankzij onze trouwe sponsors kunnen wij elk jaar een geweldig carnaval neerzetten</p>
  </div>
  <div class="section">
    <div class="sponsors-grid" id="sponsors-grid"></div>
    <div style="margin-top:2.5rem;background:linear-gradient(135deg,#003DA5,#001240);border-radius:16px;padding:2.5rem;text-align:center;color:#fff">
      <h3 style="font-size:1.4rem;font-weight:900;margin-bottom:.8rem">Word ook sponsor!</h3>
      <p style="opacity:.85;max-width:500px;margin:0 auto 1.5rem;line-height:1.7">Steun Snevelbokkenland en vergroot de zichtbaarheid van uw bedrijf in de regio. We bieden verschillende sponsorpakketten aan.</p>
      <button class="btn-primary" onclick="navigate('aanmelden')">&#9993; Neem contact op</button>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: CONTACT ═══════════════════════════ -->
<div class="page" id="page-aanmelden">
  <div class="page-banner">
    <h1>&#9993; Contact</h1>
    <p>Stuur ons een mailtje — we horen graag van je!</p>
  </div>
  <div class="section">
    <p style="text-align:center;max-width:600px;margin:0 auto 2.5rem;color:#555;line-height:1.8">
      Heb je een vraag, opmerking of wil je meedoen? Kies hieronder het juiste mailadres en we nemen zo snel mogelijk contact met je op.
    </p>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1.8rem;max-width:1000px;margin:0 auto">

      <a href="mailto:vrijwilligers@snevelbokkenland.nl" class="contact-card">
        <div class="contact-card-icon">&#128111;</div>
        <div class="contact-card-body">
          <h3>Aanmelden als vrijwilliger</h3>
          <p>Wil je meehelpen bij evenementen, opbouw, bar of iets anders? We zijn altijd op zoek naar enthousiaste mensen!</p>
          <span class="contact-card-email">vrijwilligers@snevelbokkenland.nl</span>
        </div>
      </a>

      <a href="mailto:evenementen@snevelbokkenland.nl" class="contact-card">
        <div class="contact-card-icon">&#127882;</div>
        <div class="contact-card-body">
          <h3>Vragen over evenementen</h3>
          <p>Vragen over de pronkzitting, optocht, ontbijtshow, boerenbruiloft of SnevelbokkenplusBal? Stuur ons een bericht!</p>
          <span class="contact-card-email">evenementen@snevelbokkenland.nl</span>
        </div>
      </a>

      <a href="mailto:info@snevelbokkenland.nl" class="contact-card">
        <div class="contact-card-icon">&#128172;</div>
        <div class="contact-card-body">
          <h3>Algemene vraag</h3>
          <p>Heb je een algemene vraag over Snevelbokkenland, het carnaval in Heeswijk-Dinther of iets anders? Neem gerust contact op!</p>
          <span class="contact-card-email">info@snevelbokkenland.nl</span>
        </div>
      </a>

      <a href="mailto:website@snevelbokkenland.nl" class="contact-card">
        <div class="contact-card-icon">&#128187;</div>
        <div class="contact-card-body">
          <h3>Vragen over de website</h3>
          <p>Fout gevonden, suggestie of vraag over de website? Onze webmaster helpt je verder!</p>
          <span class="contact-card-email">website@snevelbokkenland.nl</span>
        </div>
      </a>

    </div>
  </div>
</div>

<!-- ═══════════════════════════ PAGE: ADMIN ═══════════════════════════ -->
<div class="page" id="page-admin">
  <div class="admin-wrap">
    <div class="admin-header">
      <span style="font-size:2rem">&#9881;</span>
      <h2>Beheerpaneel Snevelbokkenland</h2>
    </div>
    <div id="admin-login">
      <p>Voer het beheerderswachtwoord in om verder te gaan.</p>
      <div class="admin-pw-row">
        <input type="password" id="admin-pw-input" placeholder="Wachtwoord..." onkeydown="if(event.key==='Enter')checkAdminPw()">
        <button class="btn-blue btn-sm" onclick="checkAdminPw()">Inloggen</button>
      </div>
      <p id="admin-pw-err" style="color:#c00;margin-top:.6rem;font-size:.9rem;display:none">Onjuist wachtwoord.</p>
    </div>
    <div id="admin-panel-content">
      <div class="admin-tabs">
        <div class="admin-tab active" onclick="switchAdminTab('prins',this)">&#128081; Prins</div>
        <div class="admin-tab" onclick="switchAdminTab('jeugdprins',this)">&#11088; Jeugdprins</div>
        <div class="admin-tab" onclick="switchAdminTab('evenementen',this)">&#127882; Evenementen</div>
        <div class="admin-tab" onclick="switchAdminTab('merch',this)">&#127947; Merchandise</div>
        <div class="admin-tab" onclick="switchAdminTab('sponsors',this)">&#129309; Sponsoren</div>
      </div>

      <!-- PRINS TAB -->
      <div class="admin-tab-content active" id="tab-prins">
        <div class="admin-field"><label>Naam prins/prinses</label><input id="ap-naam" placeholder="bijv. Frank I"></div>
        <div class="admin-field"><label>Jaar</label><input id="ap-jaar" placeholder="2026"></div>
        <div class="admin-field"><label>Beschrijving</label><textarea id="ap-desc" rows="5"></textarea></div>
        <div class="admin-field">
          <label>Foto</label>
          <img id="ap-foto-preview" class="admin-img-preview">
          <div class="upload-row">
            <label class="btn-upload">&#128193; Afbeelding uploaden<input type="file" accept="image/*" style="display:none" onchange="readImgFile(this,'ap-foto','ap-foto-preview')"></label>
            <input id="ap-foto" type="text" placeholder="of plak hier een URL...">
          </div>
        </div>
        <div class="admin-save-bar">
          <button class="btn-blue btn-sm" onclick="savePrins()">Opslaan</button>
          <span class="admin-msg" id="ap-msg" style="display:none">&#10003; Opgeslagen!</span>
        </div>
      </div>

      <!-- JEUGDPRINS TAB -->
      <div class="admin-tab-content" id="tab-jeugdprins">
        <div class="admin-field"><label>Naam jeugdprins/prinses</label><input id="ajp-naam" placeholder="bijv. Jobbe & Aniek"></div>
        <div class="admin-field"><label>Jaar</label><input id="ajp-jaar" placeholder="2026"></div>
        <div class="admin-field"><label>Beschrijving</label><textarea id="ajp-desc" rows="5"></textarea></div>
        <div class="admin-field">
          <label>Foto</label>
          <img id="ajp-foto-preview" class="admin-img-preview">
          <div class="upload-row">
            <label class="btn-upload">&#128193; Afbeelding uploaden<input type="file" accept="image/*" style="display:none" onchange="readImgFile(this,'ajp-foto','ajp-foto-preview')"></label>
            <input id="ajp-foto" type="text" placeholder="of plak hier een URL...">
          </div>
        </div>
        <div class="admin-save-bar">
          <button class="btn-blue btn-sm" onclick="saveJeugdprins()">Opslaan</button>
          <span class="admin-msg" id="ajp-msg" style="display:none">&#10003; Opgeslagen!</span>
        </div>
      </div>

      <!-- EVENEMENTEN TAB -->
      <div class="admin-tab-content" id="tab-evenementen">
        <div id="admin-events-blocks"></div>
        <div class="admin-save-bar">
          <button class="btn-blue btn-sm" onclick="saveEvenementen()">Alles opslaan</button>
          <span class="admin-msg" id="ae-msg" style="display:none">&#10003; Opgeslagen!</span>
        </div>
      </div>

      <!-- MERCH TAB -->
      <div class="admin-tab-content" id="tab-merch">
        <div class="admin-merch-items" id="admin-merch-items"></div>
        <button class="admin-add-btn" onclick="addMerchItem()">+ Artikel toevoegen</button>
        <div class="admin-save-bar">
          <button class="btn-blue btn-sm" onclick="saveMerch()">Opslaan</button>
          <span class="admin-msg" id="am-msg" style="display:none">&#10003; Opgeslagen!</span>
        </div>
      </div>

      <!-- SPONSORS TAB -->
      <div class="admin-tab-content" id="tab-sponsors">
        <div class="admin-sponsor-items" id="admin-sponsor-items"></div>
        <button class="admin-add-btn" onclick="addSponsorItem()">+ Sponsor toevoegen</button>
        <div class="admin-save-bar">
          <button class="btn-blue btn-sm" onclick="saveSponsors()">Opslaan</button>
          <span class="admin-msg" id="as-msg" style="display:none">&#10003; Opgeslagen!</span>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- ═══════════════════════════ FOOTER ═══════════════════════════ -->
<footer>
  {logo_img('class="footer-logo"')}
  <h3>Snevelbokkenland</h3>
  <p>Carnavalsvereniging Heeswijk-Dinther</p>
  <p>info@snevelbokkenland.nl</p>
  <div class="footer-links">
    <a href="#home">Home</a>
    <a href="#prins">Prins</a>
    <a href="#evenementen">Evenementen</a>
    <a href="#dansmariekes">Dansmariekes</a>
    <a href="#merchandise">Merchandise</a>
    <a href="#sponsoren">Sponsoren</a>
    <a href="#aanmelden">Contact</a>
  </div>
  <div class="footer-copy">&copy; <span id="footer-year"></span> Snevelbokkenland. Alle rechten voorbehouden.</div>
</footer>

<script>
/* ─── DEFAULTS ─── */
var DEFAULTS_PRINS = {{
  naam: "Prins Frank I",
  jaar: "2026",
  desc: "Op vrijdag 7 november barstte de spanning los in een bomvol Stanserhorn, waar niemand minder dan Frank van Aspert (44) werd onthuld als Prins Frank I. Frank is een trotse Heeswijker, zoon van Henry en Gerrie van Aspert, en in 2012 getrouwd met Brenda Lunenburg. Samen hebben ze twee jongens: Vinz (9) en Jiem (7). Overdag is hij de man achter van Aspert Tegelwerken. Hij voetbalt al jaren bij VV Heeswijk en is ook actief als parkeerwachter bij De Kersouwe. Zijn rechterhand dit seizoen is adjudant Selly Dobbelsteen, al jarenlang bevriend vanuit hun tienerjaren. Motto: \\"HDL mé hil oew hart, knallen wij uit onze voeg!\\"",
  foto: "{HERO_PRINCE}"
}};
var DEFAULTS_JEUGDPRINS = {{
  naam: "Jeugdprins Jobbe & Jeugdprinses Aniek",
  jaar: "2026",
  desc: "Dit jaar wordt het Jeugdcarnaval in Heeswijk-Dinther en Loosbroek aangevoerd door Jeugdprins Jobbe van Overbeek en Jeugdprinses Aniek Hanegraaf, samen met adjudanten Dex van Zoggel en Benthe van den Broek. Jeugdprins Jobbe (11) woont in Loosbroek en zit in groep 8 van de Bolderik. Zijn motto: \\"Job hob, gas der op!\\" Jeugdprinses Aniek (10) zit in groep 7 van basisschool \\'t Palet en is dol op turnen. Haar motto: \\"Jeugdprinses Aniek turnt deze carnaval alles om!\\"",
  foto: ""
}};
var DEFAULTS_EVENEMENTEN = [
  {{ id:"pronkzitting", naam:"Pronkzitting", icon:"&#127881;",
     datum:"6 & 7 februari 2026", tijdstip:"Avondprogramma", locatie:"De Snevelbokkenstal (De Zaert), Heeswijk-Dinther",
     beschrijving:"Show, humor, muziek, gezelligheid, vermaak en (ont)spanning. De ingrediënten voor een carnavalesk pronkzittingsweekend! De Zaert wordt omgebouwd tot de vertrouwde Snevelbokkenstal. Kaarten kosten € 17,50 per persoon per avond.",
     programma:[["Inloop","Ontvangst met drankje"],["Opening","Officiële opening door Prins Frank I"],["Optreden","Dansmariekes en artiesten"],["Muziek","Livemuziek & feest"],["Sluiting","Feest tot in de late uurtjes"]] }},
  {{ id:"optocht", naam:"Optocht", icon:"&#127916;",
     datum:"15 februari 2026", tijdstip:"13:11 uur", locatie:"Start: Plein 1969, Heeswijk-Dinther",
     beschrijving:"De carnavalsoptocht 3.0 trekt door Heeswijk-Dinther. Met prachtige wagens, groepen en muziek is het een spektakel voor jong en oud. Inschrijving sluit op 11 februari 2026 om 17:00 uur.",
     programma:[["13:11","Start optocht bij Plein 1969"],["Route","Hoofdstraat – Flerusstraat – Graaf Wernerstraat – Irenestraat – Bernardstraat – Julianastraat – Torenstraat"],["Finish","Parkeerplaats Sporthal De Zaert"],["17:00 - 18:00","Prijsuitreiking bij De Zaert"],["Aansluitend","Feestavond in De Zaert"]] }},
  {{ id:"ontbijtshow", naam:"Ontbijtshow", icon:"&#9749;",
     datum:"16 februari 2026", tijdstip:"10:00 uur", locatie:"De Zaert, Heeswijk-Dinther",
     beschrijving:"Begin de laatste carnavalsdag gezellig met een heerlijk ontbijt én entertainment. De ontbijtshow is een vaste traditie waar jong en oud samenkomen voor een heerlijke ochtend vol gezelligheid.",
     programma:[["09:30","Inloop"],["10:00","Ontbijt met livemuziek"],["11:30","Show & entertainment"],["13:00","Einde"]] }},
  {{ id:"boerenbruiloft", naam:"Boerenbruiloft", icon:"&#128142;",
     datum:"Maandag carnaval 2026", tijdstip:"Vanaf 12:00 uur", locatie:"Café/zaal Stanserhorn, Heeswijk-Dinther",
     beschrijving:"De Boerenbruiloft 3.0 is hét carnavalsfeest van HDL! Twee bekende HDL-ers geven hun nephuwelijk voor iedereen. Met receptie, kindervertier, hapje eten, dienstenveiling en een overdonderende feestavond. BABS: Rob de Backer. Haal de klompen maar uit het vet!",
     programma:[["12:00","Inloop & receptie"],["Hapje eten","Inclusief maaltijd voor alle gasten"],["Diensten veiling","Kort en ludiek programma"],["Feestavond","Liveband, DJ en feestzanger tot in de late uurtjes"]] }},
  {{ id:"snevelbokkenplusbal", naam:"SnevelbokkenplusBal", icon:"&#127881;",
     datum:"1 februari 2026", tijdstip:"12:00 – 16:00 uur", locatie:"CC Servaes, Dinther",
     beschrijving:"Voor iedereen met een verstandelijke beperking uit HDL en omstreken. Gratis entree, 2 consumptiemuntjes bij binnenkomst. Met optredens, schminkhoek en fotomogelijkheden. Klapper dit jaar: William Burg! Aanmelden via snevelbokkenplusbal@gmail.com.",
     programma:[["12:00","Deuren open, ontvangst met consumptiemuntjes"],["Optredens","Verschillende acts, headliner: William Burg"],["Schminkhoek","Leuke schminkhoek aanwezig"],["Foto","Laat een mooie foto van jezelf maken"],["16:00","Einde"]] }}
];
var DEFAULTS_MERCH = [
  {{ naam:"Carnavalssjaal", beschrijving:"Officiële sjaal in de kleuren van Snevelbokkenland", prijs:"€ 12,50", foto:"{MERCH1}" }},
  {{ naam:"Embleem", beschrijving:"Officieel embleem van Snevelbokkenland", prijs:"€ 5,00", foto:"{MERCH2}" }},
  {{ naam:"Muts", beschrijving:"Warme carnavalsmuts in de kleuren blauw en goud", prijs:"€ 8,00", foto:"{MERCH3}" }}
];
var DEFAULTS_SPONSORS = [
  {{ naam:"Word hoofdsponsor!", beschrijving:"Neem contact op", logo:"" }},
  {{ naam:"Uw bedrijf hier?", beschrijving:"Sponsorpakketten beschikbaar", logo:"" }}
];

/* ─── LOCALSTORAGE ─── */
function ld(k,d){{ try{{ var v=localStorage.getItem('snevel_'+k); return v?JSON.parse(v):d; }} catch(e){{ return d; }} }}
function sd(k,v){{ localStorage.setItem('snevel_'+k,JSON.stringify(v)); }}

/* ─── ROUTER ─── */
var ROUTES = {{
  '':'home','home':'home','prins':'prins','jeugdprins':'jeugdprins',
  'evenementen':'evenementen','pronkzitting':'pronkzitting','optocht':'optocht',
  'ontbijtshow':'ontbijtshow','boerenbruiloft':'boerenbruiloft',
  'snevelbokkenplusbal':'snevelbokkenplusbal','dansmariekes':'dansmariekes',
  'vriendenkring':'vriendenkring','oud-prinsen':'oud-prinsen',
  'merchandise':'merchandise','sponsoren':'sponsoren',
  'aanmelden':'aanmelden','contact':'aanmelden','admin':'admin'
}};
var TITLES = {{
  'home':'Snevelbokkenland – Welkom','prins':'Prins – Snevelbokkenland',
  'jeugdprins':'Jeugdprins – Snevelbokkenland','evenementen':'Evenementen – Snevelbokkenland',
  'pronkzitting':'Pronkzitting – Snevelbokkenland','optocht':'Optocht – Snevelbokkenland',
  'ontbijtshow':'Ontbijtshow – Snevelbokkenland','boerenbruiloft':'Boerenbruiloft – Snevelbokkenland',
  'snevelbokkenplusbal':'SnevelbokkenplusBal – Snevelbokkenland',
  'dansmariekes':'Dansmariekes – Snevelbokkenland','vriendenkring':'Vriendenkring – Snevelbokkenland',
  'oud-prinsen':'Oud-Prinsen – Snevelbokkenland','merchandise':'Merchandise – Snevelbokkenland',
  'sponsoren':'Sponsoren – Snevelbokkenland','aanmelden':'Contact – Snevelbokkenland',
  'admin':'Beheer – Snevelbokkenland'
}};

function navigate(hash) {{ window.location.hash = hash; }}
function getHash() {{ return (window.location.hash||'').replace('#','').toLowerCase(); }}

/* ─── MOBILE NAV ─── */
function toggleMobileNav() {{
  document.getElementById('mobile-nav').classList.toggle('open');
  document.getElementById('mobile-nav-overlay').classList.toggle('open');
  document.body.style.overflow = document.getElementById('mobile-nav').classList.contains('open') ? 'hidden' : '';
}}
function closeMobileNav() {{
  document.getElementById('mobile-nav').classList.remove('open');
  document.getElementById('mobile-nav-overlay').classList.remove('open');
  document.body.style.overflow = '';
}}

/* ─── COOKIE / CONFETTI NOTICE ─── */
(function() {{
  var key = 'snevel_cookies_accepted';
  if (!localStorage.getItem(key)) {{
    setTimeout(function() {{
      var el = document.getElementById('confetti-notice');
      if (el) el.classList.add('show');
    }}, 800);
  }}
}})();
function acceptCookies() {{
  localStorage.setItem('snevel_cookies_accepted', '1');
  var el = document.getElementById('confetti-notice');
  if (el) {{ el.classList.remove('show'); }}
}}
function declineCookies() {{
  localStorage.setItem('snevel_cookies_accepted', '0');
  var el = document.getElementById('confetti-notice');
  if (el) {{ el.classList.remove('show'); }}
}}

function showPage(hash) {{
  var page = ROUTES[hash] || 'home';
  document.querySelectorAll('.page').forEach(function(p){{ p.classList.remove('active'); }});
  var el = document.getElementById('page-'+page);
  if(el) el.classList.add('active');
  document.title = TITLES[page] || 'Snevelbokkenland';
  // Update nav active states
  document.querySelectorAll('.nav-item a, .nav-dropdown a').forEach(function(a){{
    a.classList.toggle('active', a.getAttribute('href')==='#'+hash);
  }});
  window.scrollTo(0,0);
  // Render page content
  if(page==='home') renderHome();
  else if(page==='prins') renderPrins();
  else if(page==='jeugdprins') renderJeugdprins();
  else if(page==='evenementen') renderEvenementenOverview();
  else if(['pronkzitting','optocht','ontbijtshow','boerenbruiloft','snevelbokkenplusbal'].indexOf(page)>=0) renderEventDetail(page);
  else if(page==='merchandise') renderMerch();
  else if(page==='sponsoren') renderSponsors();
  else if(page==='admin') initAdmin();
}}

window.addEventListener('hashchange', function() {{ closeMobileNav(); showPage(getHash()); }});

/* ─── RENDER HOME ─── */
function renderHome() {{
  // Prins preview
  var prins = ld('prins', DEFAULTS_PRINS);
  var pi = document.getElementById('home-prins-img');
  if(pi && prins.foto && prins.foto.length > 10) pi.src = prins.foto;
  setText('home-prins-naam', prins.naam);
  setText('home-prins-jaar', 'Prins '+prins.jaar);
  var descEl = document.getElementById('home-prins-desc');
  if(descEl) descEl.textContent = prins.desc.substring(0,220)+'...';

  // Agenda
  var evs = ld('evenementen', DEFAULTS_EVENEMENTEN);
  var evHtml = '';
  evs.forEach(function(ev) {{
    evHtml += '<div class="agenda-card" data-id="'+ev.id+'" onclick="navigate(this.dataset.id)">' +
      '<div class="icon">'+ev.icon+'</div>' +
      '<div class="datum">'+ev.datum+'</div>' +
      '<h4>'+ev.naam+'</h4>' +
      '<div class="loc"><span>&#128205;</span>'+ev.locatie.split(',')[0]+'</div>' +
    '</div>';
  }});
  var ag = document.getElementById('home-agenda-grid');
  if(ag) ag.innerHTML = evHtml;

  // Sponsoren
  var sponsors = ld('sponsors', DEFAULTS_SPONSORS);
  var spHtml = '';
  sponsors.forEach(function(sp) {{
    spHtml += '<div class="sponsor-logo-item">';
    if(sp.logo && sp.logo.length > 10) spHtml += '<img src="'+sp.logo+'" alt="'+sp.naam+'">';
    else spHtml += '<div class="sp-name">'+sp.naam+'</div>';
    spHtml += '</div>';
  }});
  var sl = document.getElementById('home-sponsors-logos');
  if(sl) sl.innerHTML = spHtml;

  // Merchandise preview
  var merch = ld('merch', DEFAULTS_MERCH);
  var mHtml = '';
  merch.slice(0,3).forEach(function(item) {{
    var imgH = item.foto && item.foto.length > 10
      ? '<img src="'+item.foto+'" alt="'+item.naam+'" style="width:100%;height:200px;object-fit:cover">'
      : '<div style="height:200px;background:linear-gradient(135deg,#e8eeff,#c8d8ff);display:flex;align-items:center;justify-content:center;font-size:3.5rem">&#127947;</div>';
    mHtml += '<div class="merch-card">'+imgH+
      '<div class="merch-card-body"><h3>'+item.naam+'</h3><p>'+item.beschrijving+'</p><div class="prijs">'+item.prijs+'</div></div></div>';
  }});
  var mg = document.getElementById('home-merch-grid');
  if(mg) mg.innerHTML = mHtml;
}}

/* ─── RENDER PRINS ─── */
function renderPrins() {{
  var d = ld('prins', DEFAULTS_PRINS);
  setText('prins-naam', d.naam);
  setText('prins-badge-jaar', 'Prins '+d.jaar);
  setText('prins-jaar-badge', 'Seizoen '+d.jaar);
  setText('prins-desc', d.desc);
  var img = document.getElementById('prins-portrait-img');
  if(img && d.foto && d.foto.length > 10) img.src = d.foto;
}}

/* ─── RENDER JEUGDPRINS ─── */
function renderJeugdprins() {{
  var d = ld('jeugdprins', DEFAULTS_JEUGDPRINS);
  setText('jeugdprins-naam', d.naam);
  setText('jeugdprins-badge-jaar', 'Jeugdprins '+d.jaar);
  setText('jeugdprins-jaar-badge', 'Seizoen '+d.jaar);
  setText('jeugdprins-desc', d.desc);
  var img = document.getElementById('jeugdprins-portrait-img');
  var ph  = document.getElementById('jeugdprins-photo-ph');
  if(d.foto && d.foto.length > 10) {{
    img.src = d.foto; img.style.display='block'; if(ph) ph.style.display='none';
  }} else {{
    img.style.display='none'; if(ph) ph.style.display='flex';
  }}
}}

/* ─── RENDER EVENEMENTEN OVERVIEW ─── */
function renderEvenementenOverview() {{
  var evs = ld('evenementen', DEFAULTS_EVENEMENTEN);
  var html = '';
  evs.forEach(function(ev) {{
    html += '<div class="event-card" data-id="'+ev.id+'" onclick="navigate(this.dataset.id)">' +
      '<div class="event-card-header"><div class="event-card-icon">'+ev.icon+'</div><div><h3>'+ev.naam+'</h3></div></div>' +
      '<div class="event-card-body">' +
        '<div class="event-meta">' +
          '<div class="event-meta-item"><span>&#128197;</span>'+ev.datum+'</div>' +
          '<div class="event-meta-item"><span>&#128336;</span>'+ev.tijdstip+'</div>' +
          '<div class="event-meta-item"><span>&#128205;</span>'+ev.locatie+'</div>' +
        '</div>' +
        '<p>'+ev.beschrijving.substring(0,120)+'...</p>' +
      '</div></div>';
  }});
  document.getElementById('events-overview-grid').innerHTML = html;
}}

/* ─── RENDER EVENT DETAIL ─── */
function renderEventDetail(id) {{
  var evs = ld('evenementen', DEFAULTS_EVENEMENTEN);
  var ev = null;
  for(var i=0;i<evs.length;i++) {{ if(evs[i].id===id) {{ ev=evs[i]; break; }} }}
  if(!ev) return;
  var el = document.getElementById('event-detail-'+id);
  if(!el) return;
  var progHtml = '';
  if(ev.programma && ev.programma.length) {{
    progHtml = '<div class="event-program"><h2>Programma</h2>';
    ev.programma.forEach(function(p){{
      progHtml += '<div class="program-item"><div class="program-time">'+p[0]+'</div><div class="program-act">'+p[1]+'</div></div>';
    }});
    progHtml += '</div>';
  }}
  el.innerHTML =
    '<div class="event-detail-meta">' +
    '<div class="event-meta-badge"><span class="icon">&#128197;</span>'+ev.datum+'</div>' +
    '<div class="event-meta-badge"><span class="icon">&#128336;</span>'+ev.tijdstip+'</div>' +
    '<div class="event-meta-badge"><span class="icon">&#128205;</span>'+ev.locatie+'</div>' +
    '</div>' +
    '<h2>Over het evenement</h2><p>'+ev.beschrijving+'</p>' +
    progHtml +
    '<div style="margin-top:2rem"><button class="btn-blue btn-sm" data-nav="evenementen" onclick="navigate(this.dataset.nav)">&#8592; Alle evenementen</button></div>';
}}

/* ─── RENDER MERCH ─── */
function renderMerch() {{
  var items = ld('merch', DEFAULTS_MERCH);
  var html = '';
  items.forEach(function(item) {{
    var imgHtml = item.foto && item.foto.length > 10
      ? '<img src="'+item.foto+'" alt="'+item.naam+'" style="width:100%;height:220px;object-fit:cover">'
      : '<div style="height:220px;background:linear-gradient(135deg,#e8eeff,#c8d8ff);display:flex;align-items:center;justify-content:center;font-size:4rem">&#127947;</div>';
    html += '<div class="merch-card">'+imgHtml+
      '<div class="merch-card-body"><h3>'+item.naam+'</h3><p>'+item.beschrijving+'</p><div class="prijs">'+item.prijs+'</div></div></div>';
  }});
  document.getElementById('merch-grid').innerHTML = html;
}}

/* ─── RENDER SPONSORS ─── */
function renderSponsors() {{
  var items = ld('sponsors', DEFAULTS_SPONSORS);
  var html = '';
  items.forEach(function(sp) {{
    var logoHtml = sp.logo && sp.logo.length > 10
      ? '<img src="'+sp.logo+'" alt="'+sp.naam+'">'
      : '<div class="sponsor-logo-placeholder">&#129309;</div>';
    html += '<div class="sponsor-card">'+logoHtml+'<h4>'+sp.naam+'</h4>';
    if(sp.beschrijving) html += '<p>'+sp.beschrijving+'</p>';
    html += '</div>';
  }});
  document.getElementById('sponsors-grid').innerHTML = html;
}}

/* ─── UTILS ─── */
function setText(id, val) {{ var el=document.getElementById(id); if(el) el.textContent=val; }}

/* ─── VRIJWILLIGER FORM ─── */
function submitVrijwilliger() {{
  var naam=document.getElementById('vr-naam').value.trim();
  var email=document.getElementById('vr-email').value.trim();
  if(!naam||!email){{ alert('Vul tenminste naam en e-mail in.'); return; }}
  document.getElementById('vr-msg').style.display='block';
  ['vr-naam','vr-email','vr-tel','vr-opmerking'].forEach(function(id){{ var el=document.getElementById(id); if(el) el.value=''; }});
}}

/* ─── ADMIN ─── */
function checkAdminPw() {{
  var pw = document.getElementById('admin-pw-input').value;
  if(pw==='snevelbokken2026') {{
    document.getElementById('admin-login').style.display='none';
    document.getElementById('admin-panel-content').style.display='block';
    loadAdminForms();
  }} else {{
    document.getElementById('admin-pw-err').style.display='block';
  }}
}}
function switchAdminTab(name,btn) {{
  document.querySelectorAll('.admin-tab-content').forEach(function(el){{ el.classList.remove('active'); }});
  document.querySelectorAll('.admin-tab').forEach(function(el){{ el.classList.remove('active'); }});
  document.getElementById('tab-'+name).classList.add('active');
  btn.classList.add('active');
}}
function readImgFile(input, destId, previewId) {{
  var file = input.files[0];
  if(!file) return;
  var reader = new FileReader();
  reader.onload = function(e) {{
    var dest = document.getElementById(destId);
    if(dest) dest.value = e.target.result;
    var prev = document.getElementById(previewId);
    if(prev) {{ prev.src = e.target.result; prev.style.display = 'block'; }}
  }};
  reader.readAsDataURL(file);
}}
function setAdminImgPreview(inputId, previewId) {{
  var val = (document.getElementById(inputId)||{{}}).value||'';
  var prev = document.getElementById(previewId);
  if(prev && val && val.length > 10) {{ prev.src=val; prev.style.display='block'; }}
}}
function loadAdminForms() {{
  var p=ld('prins',DEFAULTS_PRINS);
  document.getElementById('ap-naam').value=p.naam;
  document.getElementById('ap-jaar').value=p.jaar;
  document.getElementById('ap-desc').value=p.desc;
  document.getElementById('ap-foto').value=p.foto||'';
  setAdminImgPreview('ap-foto','ap-foto-preview');
  var jp=ld('jeugdprins',DEFAULTS_JEUGDPRINS);
  document.getElementById('ajp-naam').value=jp.naam;
  document.getElementById('ajp-jaar').value=jp.jaar;
  document.getElementById('ajp-desc').value=jp.desc;
  document.getElementById('ajp-foto').value=jp.foto||'';
  setAdminImgPreview('ajp-foto','ajp-foto-preview');
  loadAdminEvents();
  loadAdminMerch();
  loadAdminSponsors();
}}
function savePrins() {{
  sd('prins',{{ naam:document.getElementById('ap-naam').value, jaar:document.getElementById('ap-jaar').value, desc:document.getElementById('ap-desc').value, foto:document.getElementById('ap-foto').value }});
  flash('ap-msg');
}}
function saveJeugdprins() {{
  sd('jeugdprins',{{ naam:document.getElementById('ajp-naam').value, jaar:document.getElementById('ajp-jaar').value, desc:document.getElementById('ajp-desc').value, foto:document.getElementById('ajp-foto').value }});
  flash('ajp-msg');
}}
function loadAdminEvents() {{
  var evs=ld('evenementen',DEFAULTS_EVENEMENTEN);
  var html='';
  evs.forEach(function(ev,i) {{
    html+='<div class="admin-event-block"><h4>'+ev.icon+' '+ev.naam+'</h4>'+
      '<div class="admin-field"><label>Datum</label><input id="aev-datum-'+i+'" value="'+ev.datum+'"></div>'+
      '<div class="admin-field"><label>Tijdstip</label><input id="aev-tijd-'+i+'" value="'+ev.tijdstip+'"></div>'+
      '<div class="admin-field"><label>Locatie</label><input id="aev-loc-'+i+'" value="'+ev.locatie+'"></div>'+
      '<div class="admin-field"><label>Beschrijving</label><textarea id="aev-desc-'+i+'">'+ev.beschrijving+'</textarea></div>'+
    '</div>';
  }});
  document.getElementById('admin-events-blocks').innerHTML=html;
}}
function saveEvenementen() {{
  var evs=ld('evenementen',DEFAULTS_EVENEMENTEN);
  evs.forEach(function(ev,i) {{
    var d=document.getElementById('aev-datum-'+i);
    var t=document.getElementById('aev-tijd-'+i);
    var l=document.getElementById('aev-loc-'+i);
    var b=document.getElementById('aev-desc-'+i);
    if(d) ev.datum=d.value;
    if(t) ev.tijdstip=t.value;
    if(l) ev.locatie=l.value;
    if(b) ev.beschrijving=b.value;
  }});
  sd('evenementen',evs); flash('ae-msg');
}}
function loadAdminMerch() {{
  var items=ld('merch',DEFAULTS_MERCH);
  renderAdminMerch(items);
}}
function renderAdminMerch(items) {{
  var html='';
  items.forEach(function(item,i) {{
    var hasFoto = item.foto && item.foto.length > 10;
    html+='<div class="admin-merch-item" id="am-row-'+i+'">'+
      '<div class="admin-field" style="grid-column:1/-1"><label>Naam</label><input id="am-naam-'+i+'" value="'+escHtml(item.naam)+'"></div>'+
      '<div class="admin-field"><label>Prijs</label><input id="am-prijs-'+i+'" value="'+escHtml(item.prijs)+'"></div>'+
      '<div class="admin-field"><label>Beschrijving</label><input id="am-desc-'+i+'" value="'+escHtml(item.beschrijving)+'"></div>'+
      '<div class="admin-field admin-item-full"><label>Foto</label>'+
        '<img id="am-foto-prev-'+i+'" class="admin-img-preview" src="'+(hasFoto?escHtml(item.foto):'')+'" style="'+(hasFoto?'display:block':'display:none')+'">'+
        '<div class="upload-row">'+
          '<label class="btn-upload">&#128193; Upload<input type="file" accept="image/*" style="display:none" data-dest="am-foto-'+i+'" data-prev="am-foto-prev-'+i+'" onchange="readImgFile(this,this.dataset.dest,this.dataset.prev)"></label>'+
          '<input id="am-foto-'+i+'" type="text" placeholder="of URL..." value="'+escHtml(item.foto||'')+'">'+
        '</div>'+
      '</div>'+
      '<button class="admin-item-del admin-item-full" onclick="delMerchItem('+i+')">&#10005; Verwijderen</button>'+
    '</div>';
  }});
  document.getElementById('admin-merch-items').innerHTML=html;
}}
function addMerchItem() {{
  var items=collectMerchItems();
  items.push({{ naam:'Nieuw artikel', prijs:'€ 0,00', beschrijving:'', foto:'' }});
  renderAdminMerch(items);
}}
function delMerchItem(idx) {{
  var items=collectMerchItems();
  items.splice(idx,1);
  renderAdminMerch(items);
}}
function collectMerchItems() {{
  var items=[];
  document.querySelectorAll('[id^="am-naam-"]').forEach(function(el) {{
    var i=el.id.split('-').pop();
    items.push({{ naam:el.value, prijs:(document.getElementById('am-prijs-'+i)||{{}}).value||'', beschrijving:(document.getElementById('am-desc-'+i)||{{}}).value||'', foto:(document.getElementById('am-foto-'+i)||{{}}).value||'' }});
  }});
  return items;
}}
function saveMerch() {{ sd('merch',collectMerchItems()); flash('am-msg'); }}

function loadAdminSponsors() {{
  var items=ld('sponsors',DEFAULTS_SPONSORS);
  renderAdminSponsors(items);
}}
function renderAdminSponsors(items) {{
  var html='';
  items.forEach(function(sp,i) {{
    var hasLogo = sp.logo && sp.logo.length > 10;
    html+='<div class="admin-sponsor-item">'+
      '<div class="admin-field"><label>Naam</label><input id="as-naam-'+i+'" value="'+escHtml(sp.naam)+'"></div>'+
      '<button class="admin-item-del" style="margin-top:1.8rem" onclick="delSponsorItem('+i+')">&#10005;</button>'+
      '<div class="admin-field admin-item-full"><label>Beschrijving</label><input id="as-desc-'+i+'" value="'+escHtml(sp.beschrijving||'')+'"></div>'+
      '<div class="admin-field admin-item-full"><label>Logo</label>'+
        '<img id="as-logo-prev-'+i+'" class="admin-img-preview" src="'+(hasLogo?escHtml(sp.logo):'')+'" style="'+(hasLogo?'display:block':'display:none')+'">'+
        '<div class="upload-row">'+
          '<label class="btn-upload">&#128193; Upload<input type="file" accept="image/*" style="display:none" data-dest="as-logo-'+i+'" data-prev="as-logo-prev-'+i+'" onchange="readImgFile(this,this.dataset.dest,this.dataset.prev)"></label>'+
          '<input id="as-logo-'+i+'" type="text" placeholder="of URL..." value="'+escHtml(sp.logo||'')+'">'+
        '</div>'+
      '</div>'+
    '</div>';
  }});
  document.getElementById('admin-sponsor-items').innerHTML=html;
}}
function addSponsorItem() {{
  var items=collectSponsorItems();
  items.push({{ naam:'Nieuwe sponsor', beschrijving:'', logo:'' }});
  renderAdminSponsors(items);
}}
function delSponsorItem(idx) {{
  var items=collectSponsorItems();
  items.splice(idx,1);
  renderAdminSponsors(items);
}}
function collectSponsorItems() {{
  var items=[];
  document.querySelectorAll('[id^="as-naam-"]').forEach(function(el) {{
    var i=el.id.split('-').pop();
    items.push({{ naam:el.value, beschrijving:(document.getElementById('as-desc-'+i)||{{}}).value||'', logo:(document.getElementById('as-logo-'+i)||{{}}).value||'' }});
  }});
  return items;
}}
function saveSponsors() {{ sd('sponsors',collectSponsorItems()); flash('as-msg'); }}
function initAdmin() {{
  var panel=document.getElementById('admin-panel-content');
  if(panel && panel.style.display==='block') loadAdminForms();
}}
function flash(id) {{
  var el=document.getElementById(id);
  if(!el) return;
  el.style.display='inline';
  setTimeout(function(){{ el.style.display='none'; }},2500);
}}
function escHtml(s) {{
  if(!s) return '';
  return s.replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

{SB_JS}

/* ─── INIT ─── */
document.addEventListener('DOMContentLoaded', function() {{
  document.getElementById('footer-year').textContent = new Date().getFullYear();
  showPage(getHash());
}});
</script>
</body>
</html>"""

# Build garlands properly (avoid f-string with math inside f-string)
import math
flags = ''
for i in range(24):
    y = int(35 + 30*(0.5+0.5*math.sin(i*1.1)))
    grad = f'g{(i%4)+1}'
    flags += f'<ellipse cx="{30+i*60}" cy="{y}" rx="8" ry="12" fill="url(#{grad})" opacity=".9"/>'

GARLANDS_SVG_FINAL = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" style="width:100%;height:120px">'
    '<defs>'
    '<radialGradient id="gg1" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FFD700"/><stop offset="100%" stop-color="#FFA500"/></radialGradient>'
    '<radialGradient id="gg2" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#FF4444"/><stop offset="100%" stop-color="#cc0000"/></radialGradient>'
    '<radialGradient id="gg3" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#4CAF50"/><stop offset="100%" stop-color="#2e7d32"/></radialGradient>'
    '<radialGradient id="gg4" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#9C27B0"/><stop offset="100%" stop-color="#6a1b9a"/></radialGradient>'
    '</defs>'
    '<path d="M0,30 Q120,85 240,30 Q360,85 480,30 Q600,85 720,30 Q840,85 960,30 Q1080,85 1200,30 Q1320,85 1440,30" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="2"/>'
    '<path d="M0,50 Q180,100 360,50 Q540,100 720,50 Q900,100 1080,50 Q1260,100 1440,50" fill="none" stroke="rgba(255,215,0,0.3)" stroke-width="2"/>'
    + flags +
    '</svg>'
)

# Replace the GARLANDS_SVG placeholder that build_html uses
html_out = build_html().replace(GARLANDS_SVG, GARLANDS_SVG_FINAL)

with open('C:/Users/Systeembeheer/index.html', 'w', encoding='utf-8') as f:
    f.write(html_out)

print('Done! index.html written:', len(html_out), 'bytes')
