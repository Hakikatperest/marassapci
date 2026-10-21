#!/usr/bin/env python3
"""Maraş Şapçı — marassapci.com statik site üreticisi.

Çalıştır:  python3 _src/build.py   (herhangi bir dizinden)
Girdi:     _src/ilceler.py (11 ilçe), mahalle listesi yanimdaevdesaglik verisinden (_src/data/mahalleler.json'a kopyalanır)
Çıktı:     index.html, /maras-sap-fiyatlari/, /sap-atmadan-once/, /<ilce>-sapci/ × 11, 404.html, sitemap.xml,
           robots.txt, assets/site.css, assets/site.js, images/k/*.webp (640 px türev), favicon seti
Denetim:   yasak ifade, kırık iç link, tekrar eden title/description, uzunluk → HATA, dosya yazılmaz.
İç yollar sayfa derinliğine göre GÖRELİ (Pages alt yol önizlemesi kırılmasın); canonical/sitemap mutlak.
"""
import html, json, os, re, sys, shutil

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, "_src"))
from ilceler import ILCELER, DUZELT

SITE = "https://marassapci.com/"
AD = "Maraş Şapçı"
TEL, TEL_G, WA = "+905345175046", "0534 517 50 46", "905345175046"
BUGUN = "2026-10-21"            # yayın tarihi SABİT
FIYAT_TARIH = "Ekim 2026"
ISCILIK = (70, 100)             # TL/m² — kullanıcı 2026-10-21
MALZEMELI = (300, 350)          # TL/m² malzemeli + faturalı
SURUM = "3"
YASAK = ["en ucuz", "garanti", "1 numara", "bir numaralı", "%100", "lider"]
VERI_KAYNAK = "/root/yanimdaevdesaglik_repo/_src/data/turkiye_ilce_mahalle.json"
VERI = os.path.join(KOK, "_src/data/mahalleler.json")

e = html.escape
ONEK = ""
def ic(y): return (ONEK + y) if y else (ONEK or "./")
def tr_lower(s): return s.replace("I", "ı").replace("İ", "i").lower()
def tl(n): return f"{n:,}".replace(",", ".")

# ------------------------------------------------------------------ veri
def mahalleler():
    if not os.path.exists(VERI):
        os.makedirs(os.path.dirname(VERI), exist_ok=True)
        d = json.load(open(VERI_KAYNAK, encoding="utf-8"))["KAHRAMANMARAŞ"]["ilceler"]
        json.dump(d, open(VERI, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    d = json.load(open(VERI, encoding="utf-8"))
    return {k: sorted(dict.fromkeys(DUZELT.get(m, m) for m in v), key=tr_lower) for k, v in d.items()}

MAH = mahalleler()
SLUG = {i["slug"]: i for i in ILCELER}

# görseller: (dosya, alt, en, boy) — en/boy CLS için
GORSEL = [
 ("maras-sapci", "Balkon zemininde mastarla çekilmiş, perdahı bitmiş makineli şap"),
 ("sap-ustasi", "Şap ustası boş betonarme katta mastarla şap çekiyor, arkada kum yığını"),
 ("sap-yapilmis-hali", "Perdah makinesiyle düzeltilmiş şap, büyük pencereli yeni bina katı"),
 ("sap-referans", "Pencere önüne kadar düz çekilmiş şap, arkada Kahramanmaraş'ta apartmanlar"),
 ("iyi-sap", "Kapı boşluklarına kadar tek seviyede atılmış şap zemin"),
 ("kaliteli-sap", "Yeni atılmış şapın yakından görünen düzgün yüzeyi"),
 ("maras-sap1", "Şap yüzeyine konmuş su terazisi, kabarcık ortada"),
 ("maras-sap3", "Odalar arasında aynı kotta biten makineli şap"),
 ("sap-isi", "Uzun koridorda kenarlara kadar düz şap"),
 ("sap-yapimi", "Merdiven sahanlığında kalıp profilleriyle şap yapımı"),
 ("sapci", "Dükkan önü açık alanda şap dökümü, pompa hortumu ve perdah makinesi"),
 ("sapci2", "Tuğla duvar dibine kadar perdahlanmış şap"),
 ("maras-sapci-sitesi", f"Maraş Şapçı: Kahramanmaraş'ın 11 ilçesinde makineli şap, telefon {TEL_G}"),
 ("maras-sap-ustasi", f"Maraş Şapçı şap ustası ıslak şapı mastarla düzeltiyor, telefon {TEL_G}"),
]
BANNER = ["maras-sapci-sitesi", "maras-sap-ustasi"]
OLCU = {}

def gorselleri_hazirla():
    from PIL import Image
    os.makedirs(os.path.join(KOK, "images/k"), exist_ok=True)
    for ad, _ in GORSEL:
        k = os.path.join(KOK, f"images/{ad}.webp"); t = os.path.join(KOK, f"images/k/{ad}-640.webp")
        im = Image.open(k); OLCU[ad] = im.size
        if not os.path.exists(t) or os.path.getmtime(t) < os.path.getmtime(k):
            im2 = im.convert("RGB"); im2.thumbnail((640, 2000)); im2.save(t, "WEBP", quality=74, method=5)
        if ad in BANNER:
            t2 = os.path.join(KOK, f"images/k/{ad}-1200.webp")
            if not os.path.exists(t2) or os.path.getmtime(t2) < os.path.getmtime(k):
                im3 = im.convert("RGB"); im3.thumbnail((1200, 2000)); im3.save(t2, "WEBP", quality=78, method=6)

FP = ' fetchpriority="high"'
AC = ' aria-current="page"'
def resim(ad, sinif="", yukle="lazy", sizes="(max-width: 700px) 100vw, 50vw"):
    alt = dict(GORSEL)[ad]; w, h = OLCU[ad]
    if ad in BANNER:
        return (f'<img class="{sinif}" src="{ic(f"images/k/{ad}-1200.webp")}" srcset="{ic(f"images/k/{ad}-640.webp")} 640w, '
                f'{ic(f"images/k/{ad}-1200.webp")} 1200w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" loading="{yukle}"'
                f'{FP if yukle == "eager" else ""} decoding="async">')
    return (f'<img class="{sinif}" src="{ic(f"images/k/{ad}-640.webp")}" srcset="{ic(f"images/k/{ad}-640.webp")} 640w, '
            f'{ic(f"images/{ad}.webp")} {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" loading="{yukle}"'
            f'{FP if yukle == "eager" else ""} decoding="async">')

def favicon():
    from PIL import Image, ImageDraw, ImageFont
    yol = os.path.join(KOK, "images/favicon-192.png")
    if os.path.exists(yol): return
    S = 768; im = Image.new("RGB", (S, S), "#23292C"); d = ImageDraw.Draw(im)
    d.rounded_rectangle([90, 330, 678, 438], 54, fill="#A6D22E")       # su terazisi gövdesi
    d.ellipse([318, 344, 450, 424], fill="#23292C")                      # kabarcık penceresi
    d.ellipse([346, 358, 422, 410], fill="#E9F5C9")
    d.rectangle([90, 520, 678, 560], fill="#8E979B")                      # şap çizgisi
    for s in (48, 96, 192):
        im.resize((s, s), Image.LANCZOS).save(os.path.join(KOK, f"images/favicon-{s}.png"))
    im.resize((180, 180), Image.LANCZOS).save(os.path.join(KOK, "apple-touch-icon.png"))
    im.resize((512, 512), Image.LANCZOS).save(os.path.join(KOK, "images/logo-512.png"))
    im.save(os.path.join(KOK, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])

# ------------------------------------------------------------------ ortak parçalar
def isletme():
    return {"@type": "HomeAndConstructionBusiness", "@id": SITE + "#isletme", "name": AD, "url": SITE,
            "telephone": TEL, "image": SITE + "images/maras-sapci.webp", "logo": SITE + "images/logo-512.png",
            "priceRange": f"{ISCILIK[0]}-{MALZEMELI[1]} TL/m²",
            "address": {"@type": "PostalAddress", "addressRegion": "Kahramanmaraş", "addressCountry": "TR"},
            "areaServed": [{"@type": "City", "name": "Kahramanmaraş"}] +
                          [{"@type": "AdministrativeArea", "name": f"{i['ad']}, Kahramanmaraş"} for i in ILCELER],
            "makesOffer": [
              {"@type": "Offer", "name": "Makineli şap işçiliği", "priceCurrency": "TRY",
               "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": ISCILIK[0], "maxPrice": ISCILIK[1],
                                      "priceCurrency": "TRY", "unitCode": "MTK", "unitText": "m²"}},
              {"@type": "Offer", "name": "Malzemeli ve faturalı şap", "priceCurrency": "TRY",
               "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": MALZEMELI[0], "maxPrice": MALZEMELI[1],
                                      "priceCurrency": "TRY", "unitCode": "MTK", "unitText": "m²"}}]}

def breadcrumb(adimlar):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": a, "item": SITE + y} for n, (a, y) in enumerate(adimlar)]}

def sss_sema(sss):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": s,
            "acceptedAnswer": {"@type": "Answer", "text": c}} for s, c in sss]}

MENU = [("", "Anasayfa"), ("maras-sap-fiyatlari/", "Şap Fiyatları"), ("sap-turleri/", "Şap Türleri"),
        ("sap-atmadan-once/", "Şap Rehberi"), ("#ilceler", "İlçeler")]

def bas(yol, title, desc, sema, ogimg="maras-sapci", onyukle=""):
    url = SITE + yol
    pre = (f'\n<link rel="preload" as="image" href="{ic(onyukle)}" imagesrcset="{ic("images/k/hero-900.webp")} 900w, {ic(onyukle)} 1500w" imagesizes="100vw">' if onyukle else "")
    menu = "".join(f'<a href="{ic("") + h if h.startswith("#") else ic(h)}"{AC if h == yol else ""}>{a}</a>'
                   for h, a in MENU)
    return f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{AD}"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}images/{("k/" + ogimg + "-1200") if ogimg in BANNER else ogimg}.webp">
<meta property="og:image:width" content="{1200 if ogimg in BANNER else OLCU.get(ogimg, (1500, 630))[0]}"><meta property="og:image:height" content="{661 if ogimg in BANNER else OLCU.get(ogimg, (1500, 630))[1]}">
<meta property="og:image:alt" content="{e(dict(GORSEL).get(ogimg, title))}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="theme-color" content="#23292C">{pre}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/images/favicon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=Source+Sans+3:wght@400;600;700&display=swap">
<link rel="stylesheet" href="{ic('assets/site.css')}?v={SURUM}">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": sema}, ensure_ascii=False)}</script>
</head>
<body>
<header class="ust"><div class="ic">
 <a class="logo" href="{ic('')}"><span class="terazi" aria-hidden="true"><i></i></span><span>Maraş <b>Şapçı</b></span></a>
 <nav class="menu" id="menu" aria-label="Ana menü">{menu}</nav>
 <a class="ust-tel" href="tel:{TEL}">{TEL_G}</a>
 <button class="menu-btn" type="button" aria-controls="menu" aria-expanded="false" aria-label="Menüyü aç"><span></span></button>
</div></header>
<main>
"""

def cta_bant(baslik="Metrekareyi söyleyin, fiyatı hemen verelim"):
    return f"""<section class="cta"><div class="ic">
 <div><h2>{baslik}</h2><p>Arayın ya da WhatsApp'tan yazın: ilçe, metrekare ve şapın atılacağı kat yeterli.</p></div>
 <div class="dugmeler"><a class="btn btn-ana" href="tel:{TEL}">Ara: {TEL_G}</a>
 <a class="btn btn-wa" href="https://wa.me/{WA}?text={e('Merhaba, şap için fiyat almak istiyorum.')}" rel="noopener" target="_blank">WhatsApp'tan yaz</a></div>
</div></section>"""

def son():
    ilce_link = "".join(f'<li><a href="{ic(i["slug"] + "/")}">{i["ad"]} şapçı</a></li>' for i in ILCELER)
    return f"""</main>
<footer class="alt"><div class="ic">
 <div class="alt-kol"><p class="logo"><span class="terazi" aria-hidden="true"><i></i></span><span>Maraş <b>Şapçı</b></span></p>
  <p>Kahramanmaraş'ın 11 ilçesinde makineli şap atma. İşçilik {ISCILIK[0]}–{ISCILIK[1]} TL/m², malzemeli ve faturalı {MALZEMELI[0]}–{MALZEMELI[1]} TL/m² ({FIYAT_TARIH}).</p>
  <p><a href="tel:{TEL}">{TEL_G}</a></p></div>
 <div class="alt-kol"><p class="alt-bas">Hizmet verdiğimiz ilçeler</p><ul class="alt-ilce">{ilce_link}</ul></div>
 <div class="alt-kol"><p class="alt-bas">Sayfalar</p><ul><li><a href="{ic('maras-sap-fiyatlari/')}">Maraş şap fiyatları</a></li>
  <li><a href="{ic('sap-turleri/')}">Şap türleri ve şap yaptırma rehberi</a></li>
  <li><a href="{ic('sap-atmadan-once/')}">Şap atmadan önce bilinmesi gerekenler</a></li></ul></div>
</div>
<div class="w4"><div class="w4-bag"><span class="w4-etiket">Web Tasarım:</span> <a class="w4-ad" href="https://www.web4medya.com/" target="_blank" rel="noopener">Web<span class="w4-d">4</span>Medya</a></div></div>
</footer>
<div class="dock" id="dock"><a class="dock-tel" href="tel:{TEL}"><small>Şap ustası hattı</small><span>{TEL_G}</span></a>
<a class="dock-ik dock-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp'tan yaz"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.2-.2-.5-.3Z"/></svg></a>
<a class="dock-ik dock-ara" href="tel:{TEL}" aria-label="Hemen ara"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1Z"/></svg></a></div>
<script src="{ic('assets/site.js')}?v={SURUM}" defer></script>
</body>
</html>
"""

def iz(adimlar):  # görünür breadcrumb
    p = [f'<a href="{ic(y)}">{e(a)}</a>' for a, y in adimlar[:-1]] + [f'<span aria-current="page">{e(adimlar[-1][0])}</span>']
    return '<nav class="iz" aria-label="Konum">' + ' <span aria-hidden="true">›</span> '.join(p) + '</nav>'

def fiyat_kutu():
    return f"""<div class="fiyat-kutu">
 <div class="fk-satir"><p class="fk-ad">Şap işçiliği</p><p class="fk-tutar">{ISCILIK[0]}–{ISCILIK[1]} <small>TL/m²</small></p>
  <p class="fk-not">Kum ve çimento sizden, makine ve ekip bizden.</p></div>
 <div class="fk-satir"><p class="fk-ad">Malzemeli + faturalı</p><p class="fk-tutar">{MALZEMELI[0]}–{MALZEMELI[1]} <small>TL/m²</small></p>
  <p class="fk-not">Kum, çimento, işçilik ve fatura dahil anahtar teslim.</p></div>
 <p class="fk-tarih">Fiyatlar {FIYAT_TARIH} itibarıyla. Kesin rakam metrekare ve iş koşullarına göre verilir.</p>
</div>"""

def sss_html(sss):
    return '<div class="sss">' + "".join(f"<details><summary>{e(s)}</summary><p>{e(c)}</p></details>" for s, c in sss) + "</div>"

def ilce_kartlari():
    return '<ul class="ilce-grid">' + "".join(
        f'<li><a href="{ic(i["slug"] + "/")}"><b>{i["ad"]}</b><span>{len(MAH[i["ad"]])} mahalle</span></a></li>'
        for i in ILCELER) + "</ul>"

def galeri(adlar):
    return '<div class="galeri">' + "".join(
        f'<figure><button type="button" class="gal-ac" data-tam="{ic(f"images/{a}.webp")}" aria-label="Büyüt: {e(dict(GORSEL)[a])}">'
        f'{resim(a, sizes="(max-width: 700px) 50vw, 25vw")}</button><figcaption>{e(dict(GORSEL)[a])}</figcaption></figure>'
        for a in adlar) + "</div>"

SUREC = [
 ("Keşif ve ölçü", "Metrekareyi, katı ve şapın üstüne gelecek kaplamayı öğreniyoruz. Gerekirse yerinde kot ölçüyoruz."),
 ("Kot ve mastar", "Dairenin en yüksek noktasından kotu alıp ıslak mastarları çekiyoruz; bütün odalar aynı seviyede biter."),
 ("Pompa ile döküm", "Kum ve çimento aşağıda karıştırılıp pompayla kata basılır. Malzeme taşınmaz, kat farkı oluşmaz."),
 ("Mastar ve perdah", "Şap mastarla çekilir, ardından perdah makinesiyle yüzeyi kapatılır; seramik ve parkeye hazır zemin."),
 ("Kür (bakım)", "İlk günlerde şap güneşten, rüzgârdan ve dondan korunur; sıcakta sulanır. Çatlağın çoğu bu adımda önlenir."),
]

GENEL_SSS = [
 ("Maraş'ta şap fiyatları ne kadar?",
  f"{FIYAT_TARIH} itibarıyla şap işçiliği metrekaresi {ISCILIK[0]}–{ISCILIK[1]} TL, malzemeli ve faturalı şap "
  f"{MALZEMELI[0]}–{MALZEMELI[1]} TL. Kesin fiyat metrekare, kalınlık ve iş koşullarına göre verilir."),
 ("Şap kaç günde kurur?",
  "Üzerinde dikkatli yürümek için genellikle 1–2 gün yeterli. Seramik ve parke için bekleme süresi kalınlığa, havaya "
  "ve havalandırmaya göre değişir; parke gibi neme hassas kaplamalarda nem ölçülmeden döşenmemelidir."),
 ("Şap kalınlığı kaç cm olmalı?",
  "Konutlarda yaygın uygulama 4–6 cm aralığıdır. Tesisat borusu, yalıtım ya da yerden ısıtma varsa kalınlık "
  "yerinde ölçülerek belirlenir."),
 ("Malzemeyi ben alırsam fiyat ne olur?",
  f"Kum ve çimentoyu siz alırsanız yalnız işçilik ödersiniz: metrekaresi {ISCILIK[0]}–{ISCILIK[1]} TL. "
  "Ne kadar malzeme gerektiğini metrekareye göre biz söylüyoruz."),
 ("Fatura kesiyor musunuz?",
  f"Malzemeli işlerde faturalı çalışıyoruz; malzemeli ve faturalı fiyatımız metrekaresi {MALZEMELI[0]}–{MALZEMELI[1]} TL."),
]

# ------------------------------------------------------------------ sayfalar
def capa(i, n=0):
    """İlçe bağlantısı için dönen çapa metni — aynı kalıp her yerde tekrar etmesin (örümcek ağı)."""
    k = [f"{i['ad']} şapçı", f"{i['ad']} şap ustası", f"{i['de']} şap yapan yer", f"{i['de']} şap yaptırma"]
    return k[n % len(k)]

def ag(haric=None, n0=0, sinif="ag"):
    """Bütün ilçelere bağlantı listesi (kendisi hariç)."""
    li = [f'<li><a href="{ic(i["slug"] + "/")}">{e(capa(i, n0 + j))}</a></li>'
          for j, i in enumerate(x for x in ILCELER if x is not haric)]
    return f'<ul class="{sinif}">' + "".join(li) + "</ul>"

def hero_resim():
    return (f'<img class="kb" src="{ic("images/k/hero-1500.webp")}" srcset="{ic("images/k/hero-900.webp")} 900w, '
            f'{ic("images/k/hero-1500.webp")} 1500w" sizes="100vw" width="1500" height="630" '
            f'alt="Islak şap mastarla çekilirken çizmeli şap ustası" fetchpriority="high" decoding="async">')


def anasayfa():
    t = f"Kahramanmaraş Şap Ustası - {TEL_G} | Maraş Şapçı"
    d = (f"Kahramanmaraş şap ustası ve Maraş şapçı: 11 ilçede makineli, helikopterli şap. Şap nereye yaptırılır diye "
         f"düşünmeyin, hemen arayın: {TEL_G}")
    sss = [
     ("Kahramanmaraş'ta şap nereye yaptırılır?",
      f"Kahramanmaraş'ın 11 ilçesinde şapı biz yapıyoruz. {TEL_G} numarasını arayın ya da WhatsApp'tan yazın; ilçe, "
      "metrekare ve kat bilgisini söyleyin, gün ve fiyatı hemen verelim."),
     ("Maraş'ta şap ustası numarası nedir?", f"Maraş Şapçı'ya {TEL_G} numarasından ulaşabilirsiniz. Aynı numara WhatsApp'ta da açık."),
    ] + GENEL_SSS
    sema = [isletme(), {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": AD, "inLanguage": "tr"},
            sss_sema(sss)]
    surec = "".join(f"<li><h3>{a}</h3><p>{p}</p></li>" for a, p in SUREC)
    return bas("", t, d, sema, "maras-sapci-sitesi", onyukle="images/k/hero-1500.webp") + f"""
<section class="hero"><div class="hero-fon" aria-hidden="true">{hero_resim()}</div><div class="ic hero-ic">
  <p class="ust-etiket">Maraş Şapçı · Kahramanmaraş'ın 11 ilçesi</p>
  <h1>Kahramanmaraş Şap Ustası</h1>
  <p class="giris">Maraş'ta şap yaptıracaksınız ve kime ulaşacağınızı bilmiyorsanız doğru yerdesiniz. Pompayla kata
  basıyor, mastarla çekip helikopterle (perdah makinesi) kapatıyoruz. Odalar aynı kotta, seramiğe ve parkeye hazır biter.</p>
  <a class="hero-tel" href="tel:{TEL}"><small>Şap ustası hattı</small>{TEL_G}</a>
  <div class="dugmeler"><a class="btn btn-ana" href="tel:{TEL}">Hemen Ara</a>
  <a class="btn btn-wa" href="https://wa.me/{WA}?text={e('Merhaba, şap yaptırmak istiyorum.')}" target="_blank" rel="noopener">WhatsApp'tan yaz</a></div>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>Maraş'ta en iyi şap ustası kim?</h2>
 <p>Bunu söylemek bize düşmez aslında :) Maraş'ta en iyi şap ustası kim diye soruyorsanız cevabı biz değil, yaptığımız
 zeminler versin. Aşağıdaki fotoğrafların hepsi kendi işlerimiz; kapı eşiğinden pencere dibine kadar tek kot, terazi
 nereye konsa ortada.</p>
 <p>Beğendiyseniz uzatmayalım: Kahramanmaraş'ta şap denince aklınıza gelecek numara <a href="tel:{TEL}"><strong>{TEL_G}</strong></a>.
 Onikişubat'tan Elbistan'a, Pazarcık'tan Göksun'a kadar 11 ilçenin hepsine geliyoruz.</p>
 {galeri(["maras-sapci", "sap-referans", "maras-sap1", "sap-yapilmis-hali"])}
</div></section>

<section class="blok acik"><div class="ic dar">
 <h2>Kahramanmaraş'ta şap nereye yaptırılır?</h2>
 <p>Şap işini çoğu kişi ömründe bir iki kere yaptırır, haliyle "şap yapan yer neresi, kime güveneyim" diye sormak çok
 normal. Bizim tavsiyemiz şu: şapı, işi makineyle yapan ve kotu baştan ölçen bir ekibe verin. Elle kova kova taşınan
 şapta karışım odadan odaya değişir, sonra seramikçi ya da parkeci bunun bedelini öder.</p>
 <p>Maraş Şapçı olarak yaptığımız iş tam olarak bu: keşif, kot, pompayla döküm, mastar, helikopter ve kür. Ne
 yapacağınızı bilmiyorsanız da sorun değil; arayın, birlikte bakalım.</p>
 <ol class="kisa-adim"><li><b>Arayın ya da yazın:</b> {TEL_G}</li><li><b>İlçe, metrekare ve katı söyleyin.</b></li>
 <li><b>Gün ve fiyatı birlikte netleştirelim.</b></li><li><b>Ekip ve makine adresinize gelsin.</b></li></ol>
</div></section>

<section class="blok koyu"><div class="ic">
 <h2>Şap işi nasıl yapılıyor?</h2>
 <ol class="surec">{surec}</ol>
</div></section>

<section class="blok" id="ilceler"><div class="ic">
 <h2>Maraş'ın bütün ilçelerinde şapçı ve şap ustası</h2>
 <p class="bolum-giris">Merkezde (Onikişubat, Dulkadiroğlu) ve 9 ilçede çalışıyoruz. İlçenize tıklayın; o ilçede şapta
 neye dikkat ettiğimizi ve hizmet verdiğimiz mahalleleri görün.</p>
 {ilce_kartlari()}
 <h3 class="ag-bas">İlçelere göre şap ustası</h3>
 {ag()}
</div></section>

<section class="blok acik" id="fiyat"><div class="ic dar">
 <h2>Maraş şap fiyatları</h2>
 <p>Fiyatı iki şekilde veriyoruz. Kum ve çimentoyu kendiniz alırsanız yalnız işçilik ödersiniz. Malzeme, işçilik ve
 faturanın tek elden olmasını isterseniz malzemeli fiyat geçerli.</p>
 {fiyat_kutu()}
 <p><a class="ok-link" href="{ic('maras-sap-fiyatlari/')}">Maraş şap fiyatları ve metrekare hesabı →</a></p>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>Hangi şap size uygun?</h2>
 <p>Çimento esaslı, kendiliğinden yayılan, anhidrit, hafif, elyaflı, kuru, endüstriyel… Şapın da türü var ve her biri
 her yere uygun değil. Hangisinin nerede kullanıldığını sade bir dille anlattık.</p>
 <p><a class="ok-link" href="{ic('sap-turleri/')}">Şap türleri ve şap yaptırma rehberi →</a></p>
 <h2>Sık sorulan sorular</h2>
 {sss_html(sss)}
 <p><a class="ok-link" href="{ic('sap-atmadan-once/')}">Şap atmadan önce yapılması gerekenler →</a></p>
</div></section>
""" + cta_bant("Kahramanmaraş'ta şap mı yaptıracaksınız?") + son()


TURLER = [
 ("Çimento esaslı şap", "En yaygın kullanılan şap türüdür. Çimento, kum ve su karışımından oluşur.",
  ["Daire, ofis ve iş yerlerinde kullanılır.", "Seramik, parke ve mermer altına uygulanabilir.",
   "İç ve dış mekânlarda uygun karışımla kullanılabilir."],
  "Maraş'ta her gün yaptığımız iş bu :) Makineyle, pompayla atıyor; helikopterle kapatıyoruz. Daire, kalıcı konut, "
  "dükkan fark etmez; şap yaptıracaksanız büyük ihtimalle ihtiyacınız olan da bu."),
 ("Kendiliğinden yayılan şap (self-leveling)", "Akışkan yapısı sayesinde zemine yayılarak düzgün bir yüzey oluşturur.",
  ["İnce tesviye işlemlerinde kullanılır.", "Vinil, PVC ve bazı parke uygulamalarına zemin hazırlar.",
   "Ürün türüne göre farklı kalınlıklarda uygulanır."],
  "Bunu kalın şapın yerine düşünmeyin; düzgün bir şapın üstüne ince son kat gibi düşünün. Vinil ya da PVC "
  "döşetecekseniz konuşalım."),
 ("Anhidrit (kalsiyum sülfat) şap", "Özel bağlayıcılarla hazırlanan, genellikle akışkan uygulanan bir şap türüdür.",
  ["Yerden ısıtma sistemlerinde tercih edilir.", "Geniş alanlarda düzgün yüzey sağlayabilir.",
   "Islak hacimlerde kullanılmadan önce ürünün uygunluğu kontrol edilmelidir."],
  "Banyo ve ıslak zeminde dikkat ister. Yerden ısıtmada çimento esaslı şap da kullanılır; hangisinin size uygun olduğunu "
  "projeye bakarak söyleriz."),
 ("Hafif şap", "Hafif agregalar veya özel hafif malzemeler kullanılarak hazırlanır.",
  ["Döşemeye gelen sabit yükü azaltmaya yardımcı olur.", "Kot yükseltme ve dolgu uygulamalarında kullanılabilir.",
   "Ürüne göre üzerine ayrıca dayanımlı tesviye katmanı gerekebilir."],
  "Kot farkı çok büyükse her şeyi normal şapla doldurmak döşemeye gereksiz yük bindirir. Böyle bir durum varsa keşifte "
  "söylüyoruz."),
 ("Elyaf takviyeli şap", "İçerisine uygun sentetik veya çelik lifler eklenerek hazırlanan şaptır.",
  ["Rötre çatlaklarının kontrolüne yardımcı olur.", "Endüstriyel ve konut zeminlerinde kullanılabilir.",
   "Tek başına her türlü donatı veya yapısal güçlendirme yerine geçmez."],
  "Dürüst olalım: lif çatlağı azaltır ama mucize değildir :) Kür (sulama, koruma) yapılmayan şap lifli de olsa çatlar."),
 ("Kuru şap", "Genellikle kuru yapı levhaları veya kuru dolgu sistemleriyle oluşturulan, ıslak harç kullanımını azaltan zemin sistemidir.",
  ["Hızlı ve temiz uygulama gereken renovasyonlarda kullanılır.", "Kuruma süresini bekleme ihtiyacını azaltabilir.",
   "Nem ve yük koşullarına uygun sistem seçilmelidir."],
  "İçinde oturulan evde hızlı tadilat gerekiyorsa akla gelir. Her zemine uygun değildir; nem ve yük durumuna bakılmalı."),
 ("Endüstriyel şap", "Fabrika, depo, atölye ve yoğun kullanımlı alanlar için tasarlanan yüksek dayanımlı zemin uygulamalarıdır.",
  ["Aşınma ve mekanik yüklere dayanım hedeflenir.",
   "Kullanıma göre özel çimento esaslı veya reçine esaslı sistemler seçilebilir.",
   "Ağır araç yükleri için zemin tasarımı ayrıca değerlendirilmelidir."],
  "Forklift dolaşacak bir depoya normal konut şapı atmak sonradan çok pahalıya patlar. Zemine ne gelecekse baştan söyleyin."),
 ("Epoksi esaslı zemin kaplaması", "Teknik olarak geleneksel çimento şapından farklıdır; ancak zemin tesviye ve bitiş sistemleriyle birlikte değerlendirilir.",
  ["Fabrika, garaj, hastane ve ticari alanlarda kullanılabilir.",
   "Kimyasal dayanım ve kolay temizlenebilirlik sağlayabilir.", "Alt zeminin nemi ve hazırlığı çok önemlidir."],
  "Epoksi ancak altındaki zemin kadar iyidir. Düzgün ve kurumuş bir şap olmadan epoksi kabarır."),
]
TUR_TABLO = [("Daire ve konut zeminleri", "Çimento esaslı şap"), ("Çok düzgün kaplama altı", "Kendiliğinden yayılan şap"),
             ("Yerden ısıtma", "Çimento esaslı veya anhidrit şap"), ("Kot yükseltme ve hafif dolgu", "Hafif şap"),
             ("Fabrika ve depo", "Endüstriyel, yüksek dayanımlı sistemler"), ("Hızlı renovasyon", "Kuru şap sistemi"),
             ("Garaj ve kimyasala maruz alanlar", "Uygun hazırlık üzerine epoksi sistem")]

def turler():
    yol = "sap-turleri/"
    t = "Şap Türleri ve Kahramanmaraş'ta Şap Yaptırma Rehberi"
    d = ("8 şap türü ve hangi şapın nerede kullanıldığı; Kahramanmaraş'ta şap yaptırma süreci adım adım. "
         f"Kahramanmaraş şap ustası: {TEL_G}")
    sss = [
     ("Evime hangi şap atılmalı?", "Daire ve konutlarda çoğunlukla çimento esaslı şap kullanılır. Yerden ısıtma, çok ince "
      "kaplama ya da ağır yük gibi özel bir durum varsa tür buna göre seçilir."),
     ("Kahramanmaraş'ta şap yaptırmak için kime ulaşmalıyım?",
      f"Maraş Şapçı'yı {TEL_G} numarasından arayabilir ya da WhatsApp'tan yazabilirsiniz. 11 ilçenin hepsine geliyoruz."),
     ("Şap seçerken neye bakılmalı?", "Kalınlık, zemin taşıma kapasitesi, nem, kuruma süresi, yerden ısıtma ve üstüne "
      "gelecek kaplama birlikte değerlendirilmelidir."),
    ]
    adim = [("Anasayfa", ""), ("Şap Türleri", yol)]
    sema = [isletme(), breadcrumb(adim), sss_sema(sss),
            {"@type": "Article", "headline": t, "datePublished": BUGUN, "dateModified": BUGUN, "inLanguage": "tr",
             "author": {"@id": SITE + "#isletme"}, "publisher": {"@id": SITE + "#isletme"},
             "image": SITE + "images/sap-yapilmis-hali.webp", "mainEntityOfPage": SITE + yol}]
    kart = "".join(
        f'<li class="tur" id="tur-{n + 1}"><p class="tur-no">{n + 1}</p><h3>{e(a)}</h3><p>{e(tanim)}</p>'
        f'<ul>{"".join(f"<li>{e(m)}</li>" for m in md)}</ul><p class="tur-yorum"><b>Bizden not:</b> {e(yorum)}</p></li>'
        for n, (a, tanim, md, yorum) in enumerate(TURLER))
    tablo = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in TUR_TABLO)
    adimlar = "".join(f"<li><h3>{a}</h3><p>{p}</p></li>" for a, p in SUREC)
    return bas(yol, t, d, sema, "maras-sap-ustasi") + f"""
<section class="sayfa-bas"><div class="ic dar">
 {iz(adim)}
 <h1>Şap Türleri ve Kahramanmaraş'ta Şap Yaptırma Rehberi</h1>
 <p class="giris">Şap deyip geçmeyin :) Hepsi aynı gri zemin gibi görünür ama altında ne kullanıldığı, üstüne gelecek
 seramiğin, parkenin, hatta kaloriferinizin ömrünü belirler. Bu sayfada şap türlerini, hangisinin nerede kullanıldığını
 ve Kahramanmaraş'ta şap yaptırırken süreç nasıl işliyor, hepsini sade bir dille anlattık.</p>
 <p class="tarih">Yayın: <time datetime="{BUGUN}">21 Ekim 2026</time> · Hazırlayan: Maraş Şapçı</p>
 <nav class="icindekiler" aria-label="İçindekiler"><p>Bu sayfada</p><ol>
  <li><a href="#turler">8 şap türü</a></li><li><a href="#tablo">Hangi şap nerede kullanılır?</a></li>
  <li><a href="#surec">Şap yaptırma süreci</a></li><li><a href="#kime">Maraş'ta şap için kime ulaşmalı?</a></li></ol></nav>
</div></section>

<section class="blok" id="turler"><div class="ic">
 <h2>Şap türleri</h2>
 <ol class="turler">{kart}</ol>
</div></section>

<section class="blok acik" id="tablo"><div class="ic dar">
 <h2>Hangi şap nerede kullanılır?</h2>
 <div class="tablo"><table><thead><tr><th>Uygulama alanı</th><th>Genellikle tercih edilen tür</th></tr></thead>
 <tbody>{tablo}</tbody></table></div>
 <p class="onemli"><b>Önemli:</b> Şap seçerken kalınlık, zemin taşıma kapasitesi, nem, kuruma süresi, yerden ısıtma ve
 üzerine uygulanacak kaplama birlikte değerlendirilmelidir.</p>
</div></section>

<section class="blok koyu" id="surec"><div class="ic">
 <h2>Kahramanmaraş'ta şap yaptırma süreci</h2>
 <p class="bolum-giris">Bizi aradığınızda iş şöyle ilerliyor. Aceleye gelen tek adım bile sonradan çatlak ya da kot farkı
 olarak geri döner, o yüzden hiçbirini atlamıyoruz.</p>
 <ol class="surec">{adimlar}</ol>
</div></section>

<section class="blok" id="kime"><div class="ic dar">
 <h2>Maraş'ta şap için kime ulaşmalı?</h2>
 <p>Şap ustası ararken şu üç soruyu sorun: makineyle mi atıyorsunuz, kotu nereden alıyorsunuz, döküldükten sonra kürü
 kim yapıyor? Bu sorulara net cevap veren ustayla çalışın.</p>
 <p>Biz bu soruların cevabını yukarıda zaten yazdık :) Kahramanmaraş'ta şap yaptırmak istiyorsanız bize
 <a href="tel:{TEL}"><strong>{TEL_G}</strong></a> numarasından ulaşabilirsiniz. Hangi şapın size uygun olduğunu
 bilmiyorsanız da arayın; projenize bakıp dürüstçe söyleyelim.</p>
 {galeri(["sap-ustasi", "sapci", "sap-yapimi", "iyi-sap"])}
 <h2>Sık sorulan sorular</h2>
 {sss_html(sss)}
 <h3 class="ag-bas">İlçenizde şap ustası</h3>
 {ag(n0=2)}
 <p><a class="ok-link" href="{ic('maras-sap-fiyatlari/')}">Maraş şap fiyatları →</a> &nbsp;
 <a class="ok-link" href="{ic('sap-atmadan-once/')}">Şap atmadan önce →</a></p>
</div></section>
""" + cta_bant("Hangi şap gerektiğini birlikte bulalım") + son()


def fiyat_sayfasi():
    yol = "maras-sap-fiyatlari/"
    t = f"Maraş Şap Fiyatları 2026 | Maraş Şapçı - {TEL_G}"
    d = (f"Kahramanmaraş şap fiyatları ({FIYAT_TARIH}): işçilik {ISCILIK[0]}–{ISCILIK[1]} TL/m², malzemeli ve faturalı "
         f"{MALZEMELI[0]}–{MALZEMELI[1]} TL/m². Metrekareye göre hesaplayın, fiyatı neyin değiştirdiğini görün.")
    sss = [
     ("100 m² daire şapı ne tutar?",
      f"İşçilik olarak {tl(100 * ISCILIK[0])}–{tl(100 * ISCILIK[1])} TL, malzemeli ve faturalı olarak "
      f"{tl(100 * MALZEMELI[0])}–{tl(100 * MALZEMELI[1])} TL aralığında. Kalınlık ve iş koşulları kesin rakamı belirler."),
     ("Şap fiyatına KDV dahil mi?",
      "Malzemeli ve faturalı fiyat faturalı iş içindir. Fatura ve vergi ayrıntısını teklif verirken açıkça yazıyoruz."),
     ("Fiyat ilçeye göre değişir mi?",
      "Metrekare fiyat aralığımız bütün ilçelerde aynı. Çok küçük işlerde ya da ulaşımı zor yerlerde bunu teklifte ayrıca söylüyoruz."),
     ("Kalın şap daha mı pahalı?",
      "Malzemeli işte evet; kalınlık arttıkça kum ve çimento miktarı artar. İşçilik fiyatında normal kalınlıkta fark olmaz."),
    ]
    adim = [("Anasayfa", ""), ("Maraş Şap Fiyatları", yol)]
    sema = [isletme(), breadcrumb(adim), sss_sema(sss)]
    etken = [
     ("Metrekare", "Toplam alan büyüdükçe makinenin kurulum süresi metrekareye bölünür. Çok küçük işlerde fiyat iş bazında konuşulur."),
     ("Kalınlık", "Döşemedeki kot farkı ve borular kalınlığı belirler. Malzemeli işte her ek santim malzeme demektir."),
     ("Malzeme kimden", "Kum ve çimento sizdense yalnız işçilik; bizdense malzemeli fiyat geçerli."),
     ("Fatura", "Faturalı iş malzemeli fiyatın içinde. Yalnız işçilik işlerinde bunu ayrıca konuşuyoruz."),
     ("Ulaşım ve erişim", "Pompanın binaya yaklaşabilmesi işi kolaylaştırır. Dar yol ya da uzun hortum gereken işleri önceden söylüyoruz."),
     ("Yerden ısıtma", "Boru üstünde yeterli kalınlık ve dikkatli döküm gerekir; teklifte ayrıca belirtiyoruz."),
    ]
    etk = "".join(f"<li><h3>{a}</h3><p>{p}</p></li>" for a, p in etken)
    ornek = "".join(f"<tr><td>{m} m²</td><td>{tl(m * ISCILIK[0])}–{tl(m * ISCILIK[1])} TL</td>"
                    f"<td>{tl(m * MALZEMELI[0])}–{tl(m * MALZEMELI[1])} TL</td></tr>" for m in (50, 90, 120, 150, 250))
    return bas(yol, t, d, sema, "maras-sapci-sitesi") + f"""
<section class="sayfa-bas"><div class="ic dar">
 {iz(adim)}
 <h1>Maraş Şap Fiyatları ({FIYAT_TARIH})</h1>
 <p class="giris">Kahramanmaraş'ta şap fiyatını metrekare üzerinden veriyoruz. Aşağıda iki fiyatımızı, metrekareye göre
 hesap aracını ve fiyatı neyin değiştirdiğini bulacaksınız.</p>
 {fiyat_kutu()}
</div></section>

<section class="blok"><div class="ic dar">
 <h2>Metrekareye göre şap fiyatı hesapla</h2>
 <div class="hesap" id="hesap" data-i0="{ISCILIK[0]}" data-i1="{ISCILIK[1]}" data-m0="{MALZEMELI[0]}" data-m1="{MALZEMELI[1]}">
  <label for="m2">Şap atılacak alan</label>
  <div class="hesap-giris"><input id="m2" type="number" inputmode="numeric" min="1" max="100000" value="100"><span>m²</span></div>
  <div class="hesap-sonuc">
   <div><p>Yalnız işçilik</p><output id="h-isc">{tl(100 * ISCILIK[0])}–{tl(100 * ISCILIK[1])} TL</output></div>
   <div><p>Malzemeli + faturalı</p><output id="h-mal">{tl(100 * MALZEMELI[0])}–{tl(100 * MALZEMELI[1])} TL</output></div>
  </div>
  <p class="hesap-not">Bu hesap fiyat aralığını gösterir. Kesin rakam için arayın ya da WhatsApp'tan metrekareyi yazın.</p>
 </div>
 <h3>Örnek hesaplar</h3>
 <div class="tablo"><table><thead><tr><th>Alan</th><th>İşçilik</th><th>Malzemeli + faturalı</th></tr></thead>
 <tbody>{ornek}</tbody></table></div>
</div></section>

<section class="blok acik"><div class="ic">
 <h2>Şap fiyatını ne değiştirir?</h2>
 <ul class="etken">{etk}</ul>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>İşçilik mi, malzemeli mi?</h2>
 <p>Kum ve çimentoyu kendiniz alabiliyorsanız yalnız işçilik daha düşük tutar. Bu durumda ne kadar malzeme gerektiğini
 metrekareye göre biz söylüyoruz; malzemenin iş günü sahada olması yeterli.</p>
 <p>Malzeme, nakliye ve faturayla uğraşmak istemiyorsanız malzemeli fiyat daha rahat. Fatura gereken müteahhit ve
 şirket işlerinde de malzemeli ve faturalı çalışıyoruz.</p>
 <h2>Sık sorulan sorular</h2>
 {sss_html(sss)}
 <h3 class="ag-bas">İlçelere göre şap fiyatları</h3>
 <ul class="ag">{"".join(f'<li><a href="{ic(i["slug"] + "/")}">{i["ad"]} şap fiyatları</a></li>' for i in ILCELER)}</ul>
 <p><a class="ok-link" href="{ic('sap-turleri/')}">Şap türleri ve şap yaptırma rehberi →</a></p>
</div></section>
""" + cta_bant() + son()


def rehber():
    yol = "sap-atmadan-once/"
    t = "Şap Atmadan Önce: Kalınlık, Kuruma Süresi ve Hazırlık"
    d = ("Şap atılmadan önce binada neler bitmiş olmalı, şap kaç cm olmalı, kaç günde kurur, kışın ve yazın neye dikkat "
         "edilir? Kahramanmaraş'ta şap yapan ekibin hazırlık listesi.")
    sss = [
     ("Şap atıldıktan sonra ne zaman üstüne basılır?",
      "Genellikle 1–2 gün sonra dikkatli yürünebilir. Ağır malzeme taşımak ve yük koymak için birkaç gün daha beklenmelidir."),
     ("Şap neden çatlar?",
      "En sık sebepler hızlı kuruma (güneş, rüzgâr, ısıtıcı), dona maruz kalma, geniş alanda derz bırakılmaması ve "
      "fazla su ile hazırlanmış karışımdır."),
     ("Şapın üstüne hemen seramik döşenir mi?",
      "Seramik için şapın yeterince sertleşmesi beklenir. Parke ve laminat gibi neme hassas kaplamalarda bekleme daha uzundur "
      "ve nem ölçümü yapılmalıdır."),
    ]
    adim = [("Anasayfa", ""), ("Şap Atmadan Önce", yol)]
    sema = [isletme(), breadcrumb(adim), sss_sema(sss),
            {"@type": "Article", "headline": t, "datePublished": BUGUN, "dateModified": BUGUN, "inLanguage": "tr",
             "author": {"@id": SITE + "#isletme"}, "publisher": {"@id": SITE + "#isletme"},
             "image": SITE + "images/maras-sap1.webp", "mainEntityOfPage": SITE + yol}]
    liste = [
     "Pencere ve kapı kasaları takılmış, bina dışarıya kapalı olmalı (rüzgâr, yağmur ve don şapı bozar).",
     "Sıva bitmiş olmalı; sıva şaptan sonra yapılırsa düşen harç zemini kirletir.",
     "Su, gider, kalorifer ve elektrik boruları yerine oturmuş ve sabitlenmiş olmalı.",
     "Yerden ısıtma varsa borular döşenmiş, basınç testi yapılmış olmalı.",
     "Kapı eşiği ve son kat zemin kotu belli olmalı (seramik mi, parke mi gelecek?).",
     "Pompanın kurulacağı yer ve kum-çimento için boş alan ayarlanmış olmalı.",
     "Elektrik ve su sahada hazır olmalı.",
    ]
    lst = "".join(f'<li><span class="kutu" aria-hidden="true"></span>{x}</li>' for x in liste)
    return bas(yol, t, d, sema, "maras-sap-ustasi") + f"""
<section class="sayfa-bas"><div class="ic dar">
 {iz(adim)}
 <h1>Şap Atmadan Önce Bilinmesi Gerekenler</h1>
 <p class="giris">Şapın düzgün çıkması iş gününden önce başlar. Bu sayfada sahada en sık karşılaştığımız eksikleri,
 kalınlığı, kuruma süresini ve Kahramanmaraş'ın iklimine göre dikkat edilmesi gerekenleri topladık.</p>
 <p class="tarih">Yayın: <time datetime="{BUGUN}">21 Ekim 2026</time></p>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>İş gününden önce kontrol listesi</h2>
 <ul class="kontrol">{lst}</ul>
 <figure class="tek-gorsel">{resim("sap-ustasi", sizes="(max-width: 760px) 100vw, 720px")}<figcaption>Sıvası bitmiş, boruları yerine oturmuş bir katta şap çekimi.</figcaption></figure>
</div></section>

<section class="blok acik"><div class="ic dar">
 <h2>Şap kaç cm olmalı?</h2>
 <p>Konutlarda şap çoğunlukla <strong>4–6 cm</strong> arasında atılır. Kalınlığı üç şey belirler: betonarme döşemedeki kot
 farkı, döşemenin üstünden geçen borular ve şapın altına yalıtım konup konmadığı. Borunun üstünde yeterli şap kalmazsa
 o çizgi boyunca çatlak açılır.</p>
 <p>Isı ya da ses yalıtımı üstüne atılan (yüzer) şapta ve yerden ısıtma borusunun üstünde kalınlık daha dikkatli seçilir.
 Kalınlığı keşifte, dairenin birkaç noktasından kot alarak söylüyoruz.</p>
 <h2>Şap kaç günde kurur?</h2>
 <p>Makineyle atılan şapın üstünde genellikle <strong>1–2 gün</strong> sonra dikkatli yürünebilir. Seramik ve parke için
 bekleme süresi kalınlığa, havaya ve havalandırmaya göre değişir. Kalın ve soğukta atılmış şap daha geç kurur.</p>
 <p>Parke ve laminat neme hassastır. Üretici şartnameleri döşemeden önce şap neminin ölçülmesini ister; "kurumuştur"
 tahminiyle döşenen parke kabarabilir.</p>
 <figure class="tek-gorsel">{resim("maras-sap1", sizes="(max-width: 760px) 100vw, 720px")}<figcaption>Perdahı biten şapta su terazisiyle düzgünlük kontrolü.</figcaption></figure>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>Kahramanmaraş'ta mevsime göre şap</h2>
 <p><strong>Yaz (merkez, Türkoğlu, Pazarcık):</strong> Sıcak ve kuru havada şapın yüzeyi içinden önce kurur ve kılcal
 çatlaklar açılır. İlk günlerde şapı sulamak, açık pencereleri gölgelemek ve cereyanı kesmek gerekir.</p>
 <p><strong>Kış (Elbistan, Afşin, Göksun, Ekinözü, Nurhak):</strong> Donan şap yüzeyden dağılır ve sonradan düzelmez.
 Gece donu beklenen günlerde, camı takılmamış binaya şap dökmüyoruz.</p>
 <p><strong>Isıtma:</strong> Kaloriferi ya da yerden ısıtmayı şap kuruyana kadar yüksek açmayın. Ani kuruma şapı çatlatır;
 ısıtma kademeli açılmalıdır.</p>
 <h2>Sık sorulan sorular</h2>
 {sss_html(sss)}
 <p><a class="ok-link" href="{ic('maras-sap-fiyatlari/')}">Maraş şap fiyatları →</a></p>
</div></section>
""" + cta_bant("Hazırlık tamamsa gün planlayalım") + son()


IKLIM = {
 "merkez": "Merkezde yazlar sıcak geçiyor; şapın ilk günlerde sulanması ve gölgelenmesi gerekiyor. Kışın camı takılı, kapalı binalarda çalışıyoruz.",
 "ova": "Ovada yaz sıcağı şapı hızlı kurutur. İlk üç gün sulama ve gölgeleme çatlak riskini düşürür.",
 "yayla": "Yüksek ve soğuk bir ilçe olduğu için don, şapın en büyük düşmanı. Döküm gününü gece sıcaklığına göre seçiyoruz.",
 "dag": "Dağlık ve yağışlı bir bölge; yol, hava ve kuruma süresi iş planını belirliyor.",
}

def ilce_sayfasi(i):
    yol = i["slug"] + "/"
    ad, de, mah = i["ad"], i["de"], MAH[i["ad"]]
    t = f"{ad} Şapçı ve Şap Ustası - {TEL_G}"
    d = (f"{de} şap yaptırmak için {ad} şapçı ve şap ustası: {len(mah)} mahallede makineli şap. Şap nereye yaptırılır "
         f"diye düşünmeyin, arayın: {TEL_G}")
    sss = i["sss"] + [
     (f"{de} şap yapan yer neresi?",
      f"{de} şapı Maraş Şapçı olarak biz yapıyoruz; ekip ve makine adresinize geliyor. Ulaşmak için: {TEL_G}."),
     (f"{ad} şap ustası numarası nedir?", f"{ad} ve bütün mahalleleri için şap ustası hattımız {TEL_G}. WhatsApp'ta da açık."),
     (f"{de} şap fiyatı ne kadar?",
      f"{FIYAT_TARIH} itibarıyla işçilik {ISCILIK[0]}–{ISCILIK[1]} TL/m², malzemeli ve faturalı {MALZEMELI[0]}–{MALZEMELI[1]} TL/m²."),
    ]
    adim = [("Anasayfa", ""), (f"{ad} Şapçı", yol)]
    sema = [isletme(), breadcrumb(adim), sss_sema(sss),
            {"@type": "Service", "name": f"{ad} şapçı ve şap ustası", "serviceType": "Şap",
             "provider": {"@id": SITE + "#isletme"}, "areaServed": {"@type": "AdministrativeArea", "name": f"{ad}, Kahramanmaraş"},
             "url": SITE + yol}]
    giris = "".join(f"<p>{p}</p>" for p in i["giris"])
    dk = "".join(f"<li>{x}</li>" for x in i["dikkat"])
    mh = "".join(f"<li>{e(m)}</li>" for m in mah)
    n = ILCELER.index(i)
    komsu = "".join(f'<li><a href="{ic(k + "/")}">{e(capa(SLUG[k], n + j))}</a></li>' for j, k in enumerate(i["komsu"]))
    sira = [g[0] for g in GORSEL if g[0] not in BANNER]
    foto = [sira[(n * 3 + j) % len(sira)] for j in range(4)]
    iz_html = iz(adim).replace('<span aria-hidden="true">›</span>',
        f'<span aria-hidden="true">›</span> <a href="{ic("")}#ilceler">İlçeler</a> <span aria-hidden="true">›</span>', 1)
    return bas(yol, t, d, sema, BANNER[n % 2]) + f"""
<section class="sayfa-bas"><div class="ic dar">
 {iz_html}
 <h1>{ad} Şapçı ve Şap Ustası</h1>
 <p class="giris">{de} şap yaptıracaksanız aradığınız numara <a href="tel:{TEL}"><strong>{TEL_G}</strong></a>.
 {ad} merkezinde ve {len(mah)} mahallesinde makineli şap atıyoruz; pompa ile basıp mastarla çekiyor, helikopterle kapatıyoruz.</p>
 <div class="dugmeler"><a class="btn btn-ana" href="tel:{TEL}">Hemen Ara</a>
 <a class="btn btn-wa btn-wa-acik" href="https://wa.me/{WA}?text={e(f'Merhaba, {de} şap yaptırmak istiyorum.')}" target="_blank" rel="noopener">WhatsApp'tan yaz</a></div>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>{de} şap işleri</h2>
 {giris}
 <figure class="tek-gorsel">{resim(foto[0], sizes="(max-width: 760px) 100vw, 720px")}<figcaption>{e(dict(GORSEL)[foto[0]])}</figcaption></figure>
</div></section>

<section class="blok acik"><div class="ic dar">
 <h2>{de} şap nereye yaptırılır?</h2>
 <p>{de} "şap yapan yer neresi, hangi ustaya vereyim" diye soruyorsanız cevabımız kısa: bize. {ad} şap ustası olarak
 ekip ve makineyle adresinize geliyoruz; sizin bir yere gitmeniz gerekmiyor.</p>
 <ol class="kisa-adim"><li><b>Arayın:</b> {TEL_G}</li><li><b>Mahalle, metrekare ve katı söyleyin.</b></li>
 <li><b>Gün ve fiyatı netleştirelim.</b></li><li><b>Şapı atalım, kürünü anlatalım.</b></li></ol>
 <h2>{ad} şap ustası olarak dikkat ettiklerimiz</h2>
 <p>{IKLIM[i["tip"]]}</p>
 <ul class="madde">{dk}</ul>
</div></section>

<section class="blok"><div class="ic dar">
 <h2>{ad} şap fiyatları</h2>
 <p>Fiyat aralığımız {de} de diğer ilçelerle aynı. Kesin rakamı metrekare ve iş koşullarını öğrenince veriyoruz.</p>
 {fiyat_kutu()}
 <p><a class="ok-link" href="{ic('maras-sap-fiyatlari/')}">Maraş şap fiyatları ve metrekare hesabı →</a></p>
</div></section>

<section class="blok acik"><div class="ic">
 <h2>{ad} mahallelerinde şapçı</h2>
 <p class="bolum-giris">{ad} ilçesinde aşağıdaki {len(mah)} mahallenin hepsine geliyoruz. Mahallenizi yazmanız yeterli.</p>
 <ul class="mahalle">{mh}</ul>
</div></section>

<section class="blok"><div class="ic">
 <h2>Şap işlerimizden fotoğraflar</h2>
 {galeri(foto[1:] + [sira[(n * 3 + 4) % len(sira)]])}
</div></section>

<section class="blok acik"><div class="ic dar">
 <h2>Sık sorulan sorular</h2>
 {sss_html(sss)}
 <h2>Yakın ilçeler</h2>
 <ul class="komsu">{komsu}</ul>
 <h3 class="ag-bas">Kahramanmaraş'ın diğer ilçelerinde şap ustası</h3>
 {ag(i, n0=n + 1)}
 <p><a class="ok-link" href="{ic('sap-turleri/')}">Şap türleri ve şap yaptırma rehberi →</a> &nbsp;
 <a class="ok-link" href="{ic('sap-atmadan-once/')}">Şap atmadan önce →</a></p>
</div></section>
""" + cta_bant(f"{de} şap için hemen arayın") + son()


def sayfa_404():
    global ONEK
    ONEK = "/"
    s = bas("404", "Sayfa bulunamadı | Maraş Şapçı", "Aradığınız sayfa bulunamadı.", [isletme()]).replace(
        '<link rel="canonical" href="https://marassapci.com/404">', '<meta name="robots" content="noindex">')
    s += f"""<section class="sayfa-bas"><div class="ic dar"><h1>Sayfa bulunamadı</h1>
<p class="giris">Aradığınız sayfa taşınmış ya da hiç olmamış olabilir.</p>
<p><a class="ok-link" href="/">Anasayfaya dönün →</a></p>{ilce_kartlari()}</div></section>""" + son()
    return s

# ------------------------------------------------------------------ denetim + yazım
def denetle(sayfalar):
    h, tt, dd = [], {}, {}
    for yol, s in sayfalar.items():
        t = re.search(r"<title>(.*?)</title>", s).group(1); d = re.search(r'name="description" content="(.*?)"', s).group(1)
        if yol != "404.html":
            if t in tt: h.append(f"tekrar title: {yol} = {tt[t]}")
            if d in dd: h.append(f"tekrar description: {yol} = {dd[d]}")
            tt[t] = yol; dd[d] = yol
            if len(html.unescape(t)) > 65: h.append(f"title uzun ({len(html.unescape(t))}): {yol}")
            if len(html.unescape(d)) > 170: h.append(f"description uzun ({len(html.unescape(d))}): {yol}")
        if s.count("<h1") != 1: h.append(f"h1 sayısı {s.count('<h1')}: {yol}")
        metin = tr_lower(re.sub(r"<[^>]+>", " ", s))
        h += [f"yasak '{y}': {yol}" for y in YASAK if y in metin]
        derin = yol.count("/")
        for href in re.findall(r'(?:href|src|data-tam)="([^"]+)"', s):
            href = re.split(r"[?#]", href)[0]
            if yol == "404.html" or href.startswith("/") or ":" in href or not href: continue
            hedef = os.path.normpath(os.path.join(os.path.dirname(yol) or ".", href))
            ok = (hedef in {os.path.normpath(p) for p in sayfalar} or
                  os.path.normpath(os.path.join(hedef, "index.html")) in {os.path.normpath(p) for p in sayfalar} or
                  os.path.exists(os.path.join(KOK, hedef)) or hedef.startswith("assets"))
            if not ok: h.append(f"kırık iç link {href} ({yol})")
    return h

INDEXNOW = "5f3c8e2a9b7d4c61a0e4f2b8d93c7a15"

def sayfa_bas_gorsel(s, yol):
    """İç sayfa başlık alanına markalı afiş (ilçe sayfalarında iki afiş sırayla)."""
    a = '<section class="sayfa-bas"><div class="ic dar">'
    if a not in s: return s
    n = next((k for k, i in enumerate(ILCELER) if i["slug"] + "/" == yol), {"maras-sap-fiyatlari/": 0, "sap-turleri/": 1, "sap-atmadan-once/": 1}.get(yol, 0))
    i0 = s.index(a); i1 = s.index("</div></section>", i0)
    fig = (f'</div><figure class="sb-gorsel">{resim(BANNER[n % 2], "sb-img", "eager", "(max-width: 900px) 100vw, 46vw")}</figure>')
    return s[:i0] + '<section class="sayfa-bas"><div class="ic sb-izgara"><div class="sb-metin">' + s[i0 + len(a):i1] + fig + s[i1:]

def sema_ekle(s, yol):
    """WebPage + birincil görsel (ImageObject) şemasını @graph'a ekler."""
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s)
    g = json.loads(m.group(1)); og = re.search(r'property="og:image" content="([^"]+)"', s).group(1)
    ad = re.sub(r"-1200$", "", og.rsplit("/", 1)[1][:-5])
    g["@graph"].append({"@type": "WebPage", "@id": SITE + yol + "#sayfa", "url": SITE + yol, "inLanguage": "tr",
        "name": html.unescape(re.search(r"<title>(.*?)</title>", s).group(1)),
        "description": html.unescape(re.search(r'name="description" content="(.*?)"', s).group(1)),
        "isPartOf": {"@id": SITE + "#site"}, "about": {"@id": SITE + "#isletme"}, "datePublished": BUGUN, "dateModified": BUGUN,
        "primaryImageOfPage": {"@type": "ImageObject", "url": og, "caption": dict(GORSEL).get(ad, AD),
                               "width": 1200 if ad in BANNER else OLCU.get(ad, (1500, 630))[0], "height": 661 if ad in BANNER else OLCU.get(ad, (1500, 630))[1]}})
    if not any(x.get("@type") == "WebSite" for x in g["@graph"]):
        g["@graph"].append({"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": AD, "inLanguage": "tr"})
    return s[:m.start(1)] + json.dumps(g, ensure_ascii=False) + s[m.end(1):]

def main():
    global ONEK
    gorselleri_hazirla(); favicon()
    S = {}
    def yaz(yol, fn, *a):
        global ONEK
        ONEK = "../" * yol.count("/") if yol else ""
        s = sayfa_bas_gorsel(fn(*a), yol)
        S[(yol + "index.html") if yol else "index.html"] = sema_ekle(s, yol)
    yaz("", anasayfa); yaz("maras-sap-fiyatlari/", fiyat_sayfasi); yaz("sap-atmadan-once/", rehber); yaz("sap-turleri/", turler)
    for i in ILCELER: yaz(i["slug"] + "/", ilce_sayfasi, i)
    S["404.html"] = sayfa_404()
    h = denetle(S)
    if h: print("\n".join(h)); sys.exit(1)
    for yol, s in S.items():
        p = os.path.join(KOK, yol); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(s)
    os.makedirs(os.path.join(KOK, "assets"), exist_ok=True)
    for f in ("site.css", "site.js"): shutil.copy(os.path.join(KOK, "_src", f), os.path.join(KOK, "assets", f))
    url = [y.replace("index.html", "") for y in S if y != "404.html"]
    def gorsel_xml(y):
        adlar = list(dict.fromkeys(re.findall(r'images/(?:k/)?([a-z0-9-]+?)(?:-640|-1200|-1500|-900)?\.webp', S[y])))
        adlar = list(dict.fromkeys("maras-sapci-hero" if a.startswith("hero") else a for a in adlar))
        return "".join(f"<image:image><image:loc>{SITE}images/{a}.webp</image:loc></image:image>"
                       for a in adlar if a in OLCU or a == "maras-sapci-hero")
    open(os.path.join(KOK, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' +
        "".join(f"<url><loc>{SITE}{y.replace('index.html', '')}</loc><lastmod>{BUGUN}</lastmod>{gorsel_xml(y)}</url>\n"
                for y in S if y != "404.html") + "</urlset>\n")
    open(os.path.join(KOK, INDEXNOW + ".txt"), "w").write(INDEXNOW)
    open(os.path.join(KOK, "robots.txt"), "w").write(f"User-agent: *\nDisallow: /_src/\n\nSitemap: {SITE}sitemap.xml\n")
    print(f"tamam: {len(S)} sayfa, sitemap {len(url)} URL")

if __name__ == "__main__":
    main()
