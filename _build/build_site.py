#!/usr/bin/env python3
"""Generate the krattus.com free-handbooks site: landing pages + Facebook/OG preview images."""
import html, os, subprocess

BASE = "https://krattus.github.io/books/"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP = os.path.join(ROOT, "_build", "tmp")
os.makedirs(TMP, exist_ok=True)

BOOKS = [
  dict(slug="safe-together", lang="en", alt="turvaliselt-koos", accent="#e8a23a", bg="#16243f",
       kicker="The Family Cybersecurity Handbook", title="Safe Together",
       subtitle="How to spot and stop phishing, scam calls, deepfakes and AI-powered tricks — for every age, from 8 to 88.",
       desc="A free, illustrated handbook that helps the whole family — kids to grandparents — spot and stop phishing, scam calls, AI voice clones and deepfakes.",
       intro="Criminals now use AI to write perfect emails, copy the voices of people you love and fake live video calls. This illustrated handbook shows the whole family the simple habits that beat them — written so an 8-year-old and an 88-year-old can both use it.",
       bullets=["The PAUSE method — five steps that beat almost every scam",
                "Phishing emails, scam texts and QR codes, with annotated examples",
                "AI voice clones, deepfake video calls and the family code word",
                "Romance, investment, crypto, shopping and job scams",
                "Passwords, passkeys and 2-step verification made simple",
                "Chapters for kids, teens and grandparents, plus a recovery plan",
                "Toolkit: family safety plan, quiz, wallet card and fridge poster"],
       pages=71, size="5.4 MB"),
  dict(slug="turvaliselt-koos", lang="et", alt="safe-together", accent="#e8a23a", bg="#16243f",
       kicker="Pere küberturvalisuse käsiraamat", title="Turvaliselt koos",
       subtitle="Kuidas ära tunda ja peatada õngitsust, petukõnesid, süvavõltsinguid ja tehisintellekti abil tehtud trikke – igas vanuses, 8–88.",
       desc="Tasuta illustreeritud käsiraamat kogu perele – lastest vanavanemateni. Õpi ära tundma õngitsust, petukõnesid, hääle kloonimist, süvavõltsinguid ja Smart-ID pettusi.",
       intro="Petised kasutavad nüüd tehisintellekti, et kirjutada veatuid e-kirju, kopeerida lähedaste hääli ja võltsida videokõnesid. See illustreeritud käsiraamat õpetab kogu perele lihtsad harjumused, mis neid trikke peatavad – kirjutatud nii, et sellest saavad aru nii 8- kui ka 88-aastased.",
       bullets=["PEATU-meetod – viis sammu, mis peatavad peaaegu iga pettuse",
                "Õngitsuskirjad, petu-SMS-id ja QR-koodid koos näidetega",
                "Hääle kloonimine, süvavõltsitud videokõned ja pere salasõna",
                "Smart-ID ja Mobiil-ID pettused – kuidas oma PIN-koode kaitsta",
                "Armastus-, investeerimis-, krüpto-, ostu- ja tööpakkumise pettused",
                "Peatükid lastele, noortele ja vanavanematele ning taastumisplaan",
                "Tööriistad: pere turvaplaan, viktoriin, rahakoti-kaart ja Eesti abinumbrid"],
       pages=73, size="5,4 MB"),
  dict(slug="after-the-algorithm", lang="en", alt="parast-algoritmi", accent="#f0a64a", bg="#1c2236",
       kicker="A Survival Handbook", title="After the Algorithm",
       subtitle="A Practical Handbook for Work, Money and Meaning in the Age of AI",
       desc="A free survival handbook for anyone whose work is being changed by AI: steady your finances, find your direction, win in the job market and build new income.",
       intro="For everyone who did good work and was told it was no longer needed. This calm, practical handbook walks you from the first shocked week after losing a job to a new direction — protecting your money and health, understanding how AI is reshaping work, and building income you control.",
       bullets=["“Lost your job this week? Read this first” — a calm seven-day plan",
                "Money triage, building your runway and handling the shock",
                "How AI is reshaping work, and the human skills that compound",
                "Skills inventory, choosing your path and reskilling smart",
                "The modern job search, networking, portfolios — and job scams",
                "Freelancing, a small business with AI as your team, multiple income streams",
                "The 90-day comeback plan, worksheets, scripts and a resource directory"],
       pages=404, size="20 MB"),
  dict(slug="parast-algoritmi", lang="et", alt="after-the-algorithm", accent="#f0a64a", bg="#1c2236",
       kicker="Ellujäämise käsiraamat", title="Pärast algoritmi",
       subtitle="Praktiline käsiraamat tööst, rahast ja elu mõttest tehisintellekti ajastul",
       desc="Tasuta käsiraamat kõigile, kelle tööd muudab tehisintellekt: kindlusta oma rahaasjad, leia uus suund, tule toime tööturul ja loo uusi sissetulekuallikaid.",
       intro="Kõigile, kes tegid head tööd ja kuulsid, et seda enam ei vajata. See rahulik ja praktiline käsiraamat juhatab sind esimesest raskest nädalast pärast töö kaotust uue suunani – kuidas kaitsta oma raha ja tervist, mõista, kuidas tehisintellekt tööd muudab, ning luua sissetulekut, mis on sinu enda kontrolli all.",
       bullets=["„Kaotasid sel nädalal töö? Loe kõigepealt seda“ – rahulik seitsme päeva plaan",
                "Rahaline esmaabi, varu loomine ja šokiga toimetulek",
                "Kuidas tehisintellekt tööd ümber kujundab ja millised oskused kasvavad väärtuses",
                "Sinu oskuste inventuur, oma tee valimine ja targalt ümberõppimine",
                "Tänapäevane tööotsing, võrgustumine, portfoolio – ja pettused",
                "Vabakutseline töö, väikeettevõte koos TI-ga ja mitu sissetulekuallikat",
                "90 päeva tagasitulekuplaan, töölehed, näidistekstid ja abiallikad"],
       pages=430, size="20 MB"),
  dict(slug="ai-visibility-handbook", lang="en", alt="ai-nahtavuse-kasiraamat", accent="#f2b33d", bg="#0d1a33",
       kicker="The Complete Business Guide · 2026 Edition", title="The AI Visibility Handbook",
       subtitle="How to get your business found, cited, recommended and chosen by AI search engines and autonomous AI agents.",
       desc="A free business guide to GEO, AEO and agent readiness: get your business found, cited and recommended by ChatGPT, Gemini, Perplexity and AI agents.",
       intro="Customers increasingly ask an AI instead of searching. This end-to-end guide shows businesses of every size how AI search engines and AI agents choose what to recommend — and exactly what to change on your site, your content and your reputation so they choose you.",
       bullets=["From ten blue links to one answer: how AI search really works",
                "How AI agents discover, evaluate and transact",
                "Technical foundations for a machine-readable business",
                "Structured data, entity optimisation and content AI wants to cite",
                "Brand authority, reviews, reputation and local AI visibility",
                "Agentic commerce and agent interfaces: APIs, MCP and actions",
                "A 90-day roadmap, a 120-point checklist and ready-made templates"],
       pages=83, size="4.3 MB"),
  dict(slug="ai-nahtavuse-kasiraamat", lang="et", alt="ai-visibility-handbook", accent="#f2b33d", bg="#0d1a33",
       kicker="Täielik juhend ettevõtetele · 2026. aasta väljaanne", title="AI-nähtavuse käsiraamat",
       subtitle="Kuidas tagada, et AI-otsingumootorid ja autonoomsed AI-agendid teie ettevõtte leiaksid, sellele viitaksid, seda soovitaksid ja selle valiksid.",
       desc="Tasuta juhend ettevõtetele: GEO, AEO ja agentvalmidus. Kuidas ChatGPT, Gemini, Perplexity ja AI-agendid teie ettevõtte leiavad ja seda soovitavad.",
       intro="Kliendid küsivad üha sagedamini AI-lt, mitte ei otsi ise. See terviklik juhend näitab igas suuruses ettevõttele, kuidas AI-otsingumootorid ja AI-agendid valivad, mida soovitada – ning mida täpselt muuta oma veebilehel, sisus ja mainel, et nad valiksid teid.",
       bullets=["Kümnest sinisest lingist ühe vastuseni: kuidas AI-otsing tegelikult töötab",
                "Kuidas AI-agendid leiavad, hindavad ja tehinguid teevad",
                "Tehnilised alused: masinloetav ettevõte",
                "Struktureeritud andmed, olemite optimeerimine ja sisu, millele AI viitab",
                "Brändi autoriteet, arvustused, maine ja kohalik AI-nähtavus",
                "Agentkaubandus ja agendiliidesed: API-d, MCP ja toimingud",
                "90 päeva tegevuskava, 120-punktiline kontrollnimekiri ja valmis mallid"],
       pages=89, size="4,4 MB"),
]

UI = {
  "en": dict(free="Free PDF handbook", download="Download the free PDF", pages="pages", inside="What's inside",
             other="Loe eesti keeles", other_lang="et", share="Share on Facebook", library="All free handbooks",
             note="Free to read, download and share with family, friends, schools and community groups.",
             ogtag="FREE PDF", locale="en_US"),
  "et": dict(free="Tasuta PDF-käsiraamat", download="Laadi alla tasuta PDF", pages="lk", inside="Mis raamatus on",
             other="Read in English", other_lang="en", share="Jaga Facebookis", library="Kõik tasuta käsiraamatud",
             note="Tasuta lugeda, alla laadida ja jagada pere, sõprade, koolide ja kogukondadega.",
             ogtag="TASUTA PDF", locale="et_EE"),
}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">')

CSS = """
:root{--bg:#0f1729;--ink:#eef2f8;--muted:#aab4c8;--card:#18233b;--line:rgba(255,255,255,.1)}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;overflow-x:hidden;overflow-wrap:break-word;background:var(--bg);color:var(--ink);font:16px/1.6 Inter,system-ui,-apple-system,sans-serif}
a{color:inherit}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header.top{display:flex;flex-wrap:wrap;gap:6px 16px;justify-content:space-between;align-items:center;padding:18px 0;font-size:14px;color:var(--muted)}
header.top a{text-decoration:none}
header.top b{color:var(--ink);letter-spacing:.06em}
.hero{display:grid;grid-template-columns:minmax(220px,340px) 1fr;gap:48px;align-items:center;padding:28px 0 48px}
.hero>div{min-width:0}
.hero img{width:100%;height:auto;border-radius:6px;box-shadow:0 24px 60px rgba(0,0,0,.5),0 0 0 1px var(--line)}
.kicker{font-size:12.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--accent)}
h1{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:clamp(34px,6vw,58px);line-height:1.04;margin:10px 0 14px}
.sub{font-size:19px;line-height:1.5;color:#d6deeb;margin:0 0 22px}
.btn{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:#141a2a;font-weight:700;text-decoration:none;padding:15px 24px;border-radius:10px;font-size:17px}
.btn:hover{filter:brightness(1.07)}
.meta{color:var(--muted);font-size:14px;margin-top:12px}
.row{display:flex;flex-wrap:wrap;gap:10px 18px;margin-top:18px;font-size:15px}
.row a{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);padding-bottom:2px}
.row a:hover{border-color:var(--accent)}
section.body{display:grid;grid-template-columns:1fr 1fr;gap:40px;padding:40px 0 56px;border-top:1px solid var(--line)}
section.body p{color:#d6deeb;font-size:17px;margin:0}
h2{font-family:Fraunces,Georgia,serif;font-size:26px;margin:0 0 14px}
ul.ins{list-style:none;padding:0;margin:0}
ul.ins li{padding:9px 0 9px 28px;position:relative;border-bottom:1px solid var(--line);color:#d6deeb}
ul.ins li:before{content:"";position:absolute;left:4px;top:17px;width:9px;height:9px;border-radius:50%;background:var(--accent)}
footer{border-top:1px solid var(--line);padding:24px 0 40px;color:var(--muted);font-size:14px;text-align:center}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;padding:10px 0 56px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;display:flex;flex-direction:column}
.card img{width:100%;height:auto;aspect-ratio:7/10;object-fit:cover;border-radius:6px;margin-bottom:14px}
.card h3{font-family:Fraunces,Georgia,serif;font-size:22px;line-height:1.15;margin:0 0 4px}
.card .et{color:var(--muted);font-size:14.5px;margin-bottom:10px}
.card p{color:#cfd7e5;font-size:14.5px;margin:0 0 16px;flex:1}
.card .langs{display:flex;gap:8px}
.card .langs a{flex:1;text-align:center;text-decoration:none;font-weight:600;font-size:14px;padding:10px;border-radius:8px;border:1px solid var(--line);background:rgba(255,255,255,.04)}
.card .langs a:hover{border-color:var(--c)}
.intro{padding:24px 0 30px;max-width:720px}
.intro h1{font-size:clamp(32px,5.5vw,52px)}
@media (max-width:760px){.hero{grid-template-columns:1fr;gap:26px}.hero img{max-width:260px;margin:0 auto;display:block}
 section.body{grid-template-columns:1fr;gap:28px}.grid{grid-template-columns:1fr}}
"""

def e(s): return html.escape(s, quote=True)

def head(lang, title, desc, url, img, locale, extra=""):
    return f"""<!doctype html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="krattus.com">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:locale" content="{locale}">
<meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(title)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{img}">
{extra}<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E%F0%9F%93%98%3C/text%3E%3C/svg%3E">
{FONTS}<style>{CSS}</style></head>"""

def book_page(b):
    u = UI[b["lang"]]; url = BASE + b["slug"] + "/"; img = BASE + "img/og-" + b["slug"] + ".jpg"
    alt_link = f'<link rel="alternate" hreflang="{u["other_lang"]}" href="{BASE}{b["alt"]}/">\n'
    pdf = f"../pdf/{b['slug']}.pdf"
    share = "https://www.facebook.com/sharer/sharer.php?u=" + url
    lis = "".join(f"<li>{e(x)}</li>" for x in b["bullets"])
    return head(b["lang"], f'{b["title"]} — {u["free"]}', b["desc"], url, img, u["locale"], alt_link) + f"""
<body style="--accent:{b['accent']}">
<div class="wrap">
<header class="top"><a href="../"><b>KRATTUS</b> · {e(u['library'])}</a><a href="../{b['alt']}/">{e(u['other'])}</a></header>
<div class="hero">
  <img src="../img/cover-{b['slug']}.jpg" alt="{e(b['title'])}" width="770" height="1100">
  <div>
    <div class="kicker">{e(b['kicker'])}</div>
    <h1>{e(b['title'])}</h1>
    <p class="sub">{e(b['subtitle'])}</p>
    <a class="btn" href="{pdf}" download>⬇ {e(u['download'])}</a>
    <div class="meta">PDF · {b['pages']} {u['pages']} · {b['size']}</div>
    <div class="row"><a href="{share}" target="_blank" rel="noopener">{e(u['share'])}</a><a href="../{b['alt']}/">{e(u['other'])}</a></div>
  </div>
</div>
<section class="body">
  <div><p>{e(b['intro'])}</p><p style="margin-top:16px;color:var(--muted);font-size:15px">{e(u['note'])}</p></div>
  <div><h2>{e(u['inside'])}</h2><ul class="ins">{lis}</ul></div>
</section>
<footer>© 2026 <a href="https://www.krattus.com">www.krattus.com</a></footer>
</div></body></html>"""

def index_page():
    pairs = [(BOOKS[i], BOOKS[i + 1]) for i in range(0, len(BOOKS), 2)]
    cards = ""
    for en, et in pairs:
        cards += f"""<div class="card" style="--c:{en['accent']}"><a href="{en['slug']}/"><img src="img/cover-{en['slug']}.jpg" alt="{e(en['title'])}"></a>
<h3>{e(en['title'])}</h3><div class="et">{e(et['title'])}</div><p>{e(en['desc'])}</p>
<div class="langs"><a href="{en['slug']}/">English</a><a href="{et['slug']}/">Eesti keeles</a></div></div>"""
    title = "Free handbooks · Tasuta käsiraamatud — krattus.com"
    desc = "Free, illustrated PDF handbooks in English and Estonian: family cybersecurity, surviving work changes in the age of AI, and AI visibility for businesses."
    return head("en", title, desc, BASE, BASE + "img/og-index.jpg", "en_US") + f"""
<body style="--accent:#e8a23a"><div class="wrap">
<header class="top"><a href="https://www.krattus.com"><b>KRATTUS</b></a><span>English · Eesti</span></header>
<div class="intro"><div class="kicker">Free handbooks · Tasuta käsiraamatud</div>
<h1>Practical guides for life with AI</h1>
<p class="sub">Free, illustrated PDF handbooks — each in English and Estonian. Read, download and share.<br><span style="color:var(--muted)">Tasuta illustreeritud PDF-käsiraamatud inglise ja eesti keeles. Loe, laadi alla ja jaga.</span></p></div>
<div class="grid">{cards}</div>
<footer>© 2026 <a href="https://www.krattus.com">www.krattus.com</a></footer>
</div></body></html>"""

def og_html(b):
    u = UI[b["lang"]]
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:radial-gradient(circle at 78% 20%, {b['accent']}33, transparent 55%),{b['bg']};font-family:Inter,sans-serif;color:#fff;display:flex;align-items:center}}
img{{height:530px;margin:0 56px 0 64px;border-radius:6px;box-shadow:0 30px 70px rgba(0,0,0,.55)}}
.t{{flex:1;padding-right:64px}}
.tag{{display:inline-block;background:{b['accent']};color:#141a2a;font-weight:800;letter-spacing:.16em;font-size:20px;padding:8px 16px;border-radius:6px}}
h1{{font-family:Fraunces,serif;font-size:{68 if len(b['title'])<20 else 58}px;line-height:1.02;margin:22px 0 18px}}
p{{font-size:25px;line-height:1.38;color:#d9e1ee;margin:0}}
.f{{margin-top:30px;font-size:20px;color:#aab4c8;letter-spacing:.06em}}
</style></head><body><img src="../../img/cover-{b['slug']}.jpg"><div class="t">
<span class="tag">{u['ogtag']}</span><h1>{e(b['title'])}</h1><p>{e(b['subtitle'])}</p>
<div class="f">{b['pages']} {u['pages']} · www.krattus.com</div></div></body></html>"""

def og_index_html():
    imgs = "".join(f'<img src="../../img/cover-{b["slug"]}.jpg">' for b in BOOKS if b["lang"] == "en")
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}
body{{background:#0f1729;font-family:Inter,sans-serif;color:#fff;display:flex;align-items:center}}
.c{{display:flex;gap:18px;margin-left:56px}} img{{height:380px;border-radius:5px;box-shadow:0 24px 50px rgba(0,0,0,.6)}}
.c img:nth-child(2){{transform:translateY(-22px)}}
.t{{flex:1;padding:0 56px 0 48px}} .k{{color:#e8a23a;font-weight:800;letter-spacing:.16em;font-size:19px}}
h1{{font-family:Fraunces,serif;font-size:54px;line-height:1.05;margin:16px 0}} p{{font-size:23px;color:#cfd7e5;margin:0}}
</style></head><body><div class="c">{imgs}</div><div class="t"><div class="k">FREE PDF HANDBOOKS</div>
<h1>Practical guides for life with AI</h1><p>English &amp; Eesti · www.krattus.com</p></div></body></html>"""

def shoot(name, markup):
    path = os.path.join(TMP, name + ".html"); open(path, "w").write(markup)
    png = os.path.join(TMP, name + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                    "--virtual-time-budget=8000", "--allow-file-access-from-files", f"--screenshot={png}", "file://" + path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from PIL import Image
    Image.open(png).convert("RGB").save(os.path.join(ROOT, "img", f"og-{name}.jpg"), quality=88, optimize=True)

for b in BOOKS:
    os.makedirs(os.path.join(ROOT, b["slug"]), exist_ok=True)
    open(os.path.join(ROOT, b["slug"], "index.html"), "w").write(book_page(b))
    shoot(b["slug"], og_html(b))
open(os.path.join(ROOT, "index.html"), "w").write(index_page())
shoot("index", og_index_html())
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
print("built", len(BOOKS), "book pages + index")
