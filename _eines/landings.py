import html
import json
import os
import subprocess
from datetime import date, timedelta
from urllib.parse import quote

DOMINI = "https://mulhacen.cat"
WA = "34699088213"
INICI = {"ca": "/", "es": "/es/", "en": "/en/"}
MESOS = {
    "ca": ["de gener", "de febrer", "de març", "d'abril", "de maig", "de juny", "de juliol", "d'agost",
           "de setembre", "d'octubre", "de novembre", "de desembre"],
    "es": ["de enero", "de febrero", "de marzo", "de abril", "de mayo", "de junio", "de julio", "de agosto",
           "de septiembre", "de octubre", "de noviembre", "de diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
           "November", "December"],
}
DIES = {
    "ca": ["dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte", "diumenge"],
    "es": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
}

NADAL = {
    "ca": {
        "url": "/marisc-nadal-castelldefels/",
        "title": "Marisc per Nadal a Castelldefels · Peixateria Mulhacén",
        "desc": "Reserva el marisc i el peix de Nadal a Castelldefels i recull-lo sense cues el 24 i el 31 de desembre. Llagostins, gambes, escamarlans i més, des del 1954.",
        "h1": "Marisc per Nadal a Castelldefels",
        "intro": "A la Peixateria Mulhacén triem cada matí el millor de la llotja des del 1954. Per Nadal i Cap d'Any, reserva amb temps el marisc i el peix de les festes: t'ho preparem tal com ho vols i el reculls sense fer cua, o te'l portem a casa a Castelldefels.",
        "wa": "Hola, voldria fer un encàrrec de Nadal.",
        "waBtn": "Reservar per WhatsApp",
        "howTitle": "Com funciona",
        "deliveryTitle": "També a domicili",
        "deliveryMore": "Més sobre el lliurament a domicili →",
        "hoursTitle": "Horari de les festes",
        "closed": "Tancat",
        "visitTitle": "On som",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Telèfon de la botiga",
        "home": "Tornar a l'inici",
        "breadcrumb": "Inici",
        "deadline": "Encàrrecs fins al {d}.",
        "imgAlt": "Ostres, gambes i peix fresc al taulell de la Peixateria Mulhacén",
    },
    "es": {
        "url": "/es/marisco-navidad-castelldefels/",
        "title": "Marisco para Navidad en Castelldefels · Pescadería Mulhacén",
        "desc": "Reserva el marisco y el pescado de Navidad en Castelldefels y recógelo sin colas el 24 y el 31 de diciembre. Langostinos, gambas, cigalas y más, desde 1954.",
        "h1": "Marisco para Navidad en Castelldefels",
        "intro": "En la Pescadería Mulhacén elegimos cada mañana lo mejor de la lonja desde 1954. Para Navidad y Nochevieja, reserva con tiempo el marisco y el pescado de las fiestas: te lo preparamos como lo quieras y lo recoges sin hacer cola, o te lo llevamos a casa en Castelldefels.",
        "wa": "Hola, querría hacer un encargo de Navidad.",
        "waBtn": "Reservar por WhatsApp",
        "howTitle": "Cómo funciona",
        "deliveryTitle": "También a domicilio",
        "deliveryMore": "Más sobre la entrega a domicilio →",
        "hoursTitle": "Horario de las fiestas",
        "closed": "Cerrado",
        "visitTitle": "Dónde estamos",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Teléfono de la tienda",
        "home": "Volver al inicio",
        "breadcrumb": "Inicio",
        "deadline": "Encargos hasta el {d}.",
        "imgAlt": "Ostras, gambas y pescado fresco en el mostrador de la Pescadería Mulhacén",
    },
    "en": {
        "url": "/en/christmas-seafood-castelldefels/",
        "title": "Christmas seafood in Castelldefels · Mulhacén Fishmonger",
        "desc": "Reserve your Christmas seafood and fish in Castelldefels and pick it up with no queues on 24 and 31 December. Prawns, langoustines and more, since 1954.",
        "h1": "Christmas seafood in Castelldefels",
        "intro": "At Mulhacén Fishmonger we have picked the best of the fish market every morning since 1954. For Christmas and New Year's Eve, reserve your holiday seafood and fish in advance: we prepare it the way you like and you pick it up with no queue, or we deliver it to your home in Castelldefels.",
        "wa": "Hi, I'd like to place a Christmas order.",
        "waBtn": "Reserve on WhatsApp",
        "howTitle": "How it works",
        "deliveryTitle": "Home delivery too",
        "deliveryMore": "More about home delivery →",
        "hoursTitle": "Holiday opening hours",
        "closed": "Closed",
        "visitTitle": "Where we are",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Shop phone",
        "home": "Back to home",
        "breadcrumb": "Home",
        "deadline": "Orders until {d}.",
        "imgAlt": "Oysters, prawns and fresh fish on the counter at Mulhacén Fishmonger",
    },
}


def config(arrel):
    codi = "var window={};" + open(os.path.join(arrel, "config.js"), encoding="utf-8").read() + \
           ";process.stdout.write(JSON.stringify(window.MULHACEN));"
    r = subprocess.run(["node", "-e", codi], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def data_llarga(iso, lang, amb_dia=False):
    d = date.fromisoformat(iso)
    if lang == "en":
        txt = f"{d.day} {MESOS['en'][d.month - 1]}"
    else:
        txt = f"{d.day} {MESOS[lang][d.month - 1]}"
    return f"{DIES[lang][d.weekday()]} {txt}" if amb_dia else txt


def e(t):
    return html.escape(t, quote=True)


def alternates(pagines):
    out = "".join(f'<link rel="alternate" hreflang="{l}" href="{DOMINI}{p["url"]}">' for l, p in pagines.items())
    return out + f'<link rel="alternate" hreflang="x-default" href="{DOMINI}{pagines["ca"]["url"]}">'


CSS = """
:root{--cream:#F2E8D8;--paper:#FBF6EC;--ink:#2B1A10;--ink-soft:#5E4936;--marine:#2C1D14;--gold:#8E6035;--gold-deep:#6E4824;--gold-light:#D9B98F;--line:rgba(43,26,16,.15)}
*{box-sizing:border-box}
body{margin:0;background:var(--cream);color:var(--ink);font:16px/1.65 "Libre Franklin",ui-sans-serif,system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}
img{display:block;max-width:100%;height:auto}
h1,h2,h3{font-family:"Playfair Display",Georgia,serif;font-weight:500;letter-spacing:-.01em;margin:0;text-wrap:balance}
.wrap{max-width:1040px;margin:0 auto;padding:0 clamp(16px,5vw,48px)}
header{border-bottom:1px solid var(--line);background:var(--cream)}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;padding-top:10px;padding-bottom:10px}
header img{width:84px;border-radius:4px}
.langs{display:flex;gap:4px;font-size:13px;font-weight:700}
.langs a{padding:6px 10px;border-radius:999px;text-decoration:none;color:var(--ink-soft)}
.langs a[aria-current]{background:var(--marine);color:#fff}
.crumbs{font-size:13px;color:var(--ink-soft);margin:18px 0 0}
.crumbs a{text-decoration:none;border-bottom:1px solid var(--line)}
.hero{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center;padding:28px 0 48px}
.eyebrow{font-size:12.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold-deep);margin:0 0 10px}
h1{font-size:clamp(32px,4.4vw,52px);line-height:1.08}
.lead{color:var(--ink-soft);font-size:17px;margin:18px 0 0;max-width:52ch}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:26px}
.btn{display:inline-block;padding:13px 22px;border-radius:999px;text-decoration:none;font-weight:700;font-size:15px}
.btn-gold{background:var(--gold);color:#fff}
.btn-line{border:1.5px solid var(--ink);color:var(--ink)}
.hero img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:6px;box-shadow:0 18px 40px rgba(43,26,16,.25)}
section{padding:40px 0;border-top:1px solid var(--line)}
section h2{font-size:clamp(24px,3vw,32px);margin-bottom:16px}
.chips{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:0}
.chips li{background:var(--paper);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-weight:600;font-size:15px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:36px}
ul.plain,ol.steps{margin:0;padding-left:20px}
ul.plain li,ol.steps li{margin:6px 0}
.note{color:var(--ink-soft);margin-top:12px}
.recipes{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}
.recipe{background:var(--paper);border:1px solid var(--line);border-radius:8px;padding:18px}
.recipe .tag{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--gold-deep)}
.recipe h3{font-size:21px;margin:6px 0 8px}
.recipe p{margin:0;color:var(--ink-soft);font-size:15px}
.dark{background:var(--marine);color:#F2E8D8;border-top:0}
.dark h2{color:#fff}
.dark a{color:var(--gold-light)}
.dark .btn-gold{color:#fff}
footer{background:var(--marine);color:var(--gold-light);font-size:13px;padding:18px 0 28px}
@media (max-width:760px){.hero,.grid2{grid-template-columns:1fr}.hero{gap:24px}.hero .img{order:-1}}
"""


def pagina_nadal(lang, T, cfg, pagines):
    p, t, n = pagines[lang], T[lang], cfg.get("nadal", {})
    inici = INICI[lang]
    wa = f"https://wa.me/{WA}?text={quote(p['wa'])}"
    productes = (n.get("productes") or {}).get(lang) or []
    recollida = n.get("recollida") or {}
    if recollida:
        rec = "".join(f"<li><strong>{e(data_llarga(d, lang, True).capitalize())}</strong>: {e(', '.join(h.replace('-', '–') for h in hs))}</li>"
                      for d, hs in sorted(recollida.items()))
        rec = f'<ul class="plain">{rec}</ul>'
    else:
        rec = f'<p>{e(t["pickupEmpty"])}</p>'
    limit = f'<p class="note">{e(p["deadline"].format(d=data_llarga(n["limitReserves"], lang)))}</p>' if n.get("limitReserves") else ""

    des, fins = n.get("mostrarDes", ""), n.get("mostrarFins", "")
    hores = {}
    for d in cfg.get("festius", []):
        if des <= d <= fins and date.fromisoformat(d).weekday() in (1, 2, 3, 4, 5):
            hores[d] = p["closed"]
    for d, hs in (cfg.get("horariEspecial") or {}).items():
        if des <= d <= fins:
            hores[d] = ", ".join(h.replace("-", "–") for h in hs)
    hores_html = "".join(f"<li><strong>{e(data_llarga(d, lang, True).capitalize())}</strong>: {e(v)}</li>"
                         for d, v in sorted(hores.items()))
    normal = (f'<p class="note">{e(t["hoursDay1"])}: {e(t["hoursTime1"])} · {e(t["hoursDay2"])}: {e(t["hoursTime2"])} · '
              f'{e(t["hoursDay3"])}: {e(t["hoursTime3"])}</p>')

    receptes = "".join(
        f'<div class="recipe"><span class="tag">{e(t[f"n{i}Tag"])}</span><h3>{e(t[f"n{i}Title"])}</h3><p>{e(t[f"n{i}Body"])}</p></div>'
        for i in range(1, 5))
    cos = f"""
    <div class="hero">
      <div>
        <p class="eyebrow">{e(t["nadalEyebrow"])}</p>
        <h1>{e(p["h1"])}</h1>
        <p class="lead">{e(p["intro"])}</p>
        <div class="ctas">
          <a class="btn btn-gold" href="{wa}" target="_blank" rel="noopener">{e(p["waBtn"])}</a>
          <a class="btn btn-line" href="{inici}#encarrec">{e(t["nadalBtn"])}</a>
        </div>
      </div>
      <div class="img"><img src="/img/taulell-sense-preus.webp" width="1067" height="800" alt="{e(p["imgAlt"])}" fetchpriority="high"></div>
    </div>
  </div>
  <section><div class="wrap">
    <h2>{e(t["chipsTitle"])}</h2>
    <ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in productes)}</ul>
    <p class="note">{e(t["nadalLead"])}</p>
  </div></section>
  <section><div class="wrap grid2">
    <div>
      <h2>{e(t["pickupTitle"])}</h2>
      {rec}
      {limit}
    </div>
    <div>
      <h2>{e(p["howTitle"])}</h2>
      <ol class="steps"><li>{e(t["nadalStep1"])}</li><li>{e(t["nadalStep2"])}</li><li>{e(t["nadalStep3"])}</li></ol>
      <h2 style="margin-top:26px">{e(p["deliveryTitle"])}</h2>
      <p>{t["valueReparto"]} <a href="{DOMICILI[lang]["url"]}">{e(p["deliveryMore"])}</a></p>
    </div>
  </div></section>
  <section><div class="wrap">
    <h2>{e(t["rnH2"])}</h2>
    <p class="note" style="margin:0 0 18px">{e(t["rnLead"].split(". ")[0].rstrip(".") + ".")}</p>
    <div class="recipes">{receptes}</div>
  </div></section>
  <section class="dark"><div class="wrap grid2">
    <div>
      <h2>{e(p["hoursTitle"])}</h2>
      <ul class="plain">{hores_html}</ul>
      {normal}
    </div>
    {on_som(p, wa)}
  </div></section>"""
    return marc(lang, p, pagines, t, cos)


def on_som(p, wa):
    return f"""<div>
      <h2>{e(p["visitTitle"])}</h2>
      <p><a href="https://www.google.com/maps/place/?q=place_id:ChIJHfs3fCyDpBIRCZyUIs1L600" target="_blank" rel="noopener">{e(p["address"])} ↗</a></p>
      <p>WhatsApp: <a href="tel:+34699088213">699 08 82 13</a><br>{e(p["shopPhone"])}: <a href="tel:+34936652322">936 65 23 22</a></p>
      <div class="ctas"><a class="btn btn-gold" href="{wa}" target="_blank" rel="noopener">{e(p["waBtn"])}</a></div>
    </div>"""


def marc(lang, p, pagines, t, cos):
    inici = INICI[lang]
    actual = ' aria-current="page"'
    langs = "".join(
        f'<a href="{pagines[l]["url"]}" hreflang="{l}" lang="{l}"{actual if l == lang else ""}>{"CAT" if l == "ca" else l.upper()}</a>'
        for l in ("ca", "es", "en"))
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebPage", "@id": DOMINI + p["url"], "url": DOMINI + p["url"], "name": p["title"],
             "description": p["desc"], "inLanguage": lang, "about": {"@id": DOMINI + "/#store"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": p["breadcrumb"], "item": DOMINI + inici},
                {"@type": "ListItem", "position": 2, "name": p["h1"], "item": DOMINI + p["url"]}]},
        ],
    }
    fonts = "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Libre+Franklin:wght@400;600;700&display=swap"
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p["title"])}</title>
<meta name="description" content="{e(p["desc"])}">
<link rel="canonical" href="{DOMINI}{p["url"]}">
{alternates(pagines)}
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
<meta name="theme-color" content="#2C1D14">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Peixateria Mulhacén">
<meta property="og:title" content="{e(p["title"])}">
<meta property="og:description" content="{e(p["desc"])}">
<meta property="og:url" content="{DOMINI}{p["url"]}">
<meta property="og:image" content="{DOMINI}/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
<script data-goatcounter="https://peixaterialadorada.goatcounter.com/count" async src="/js/count.js"></script>
</head>
<body>
<header><div class="wrap">
  <a href="{inici}"><img src="/img/mulhacen-logo.webp" width="900" height="595" alt="Mulhacén · Peixaters des del 1954"></a>
  <nav class="langs">{langs}</nav>
</div></header>
<main>
  <div class="wrap">
    <p class="crumbs"><a href="{inici}">{e(p["breadcrumb"])}</a> › {e(p["h1"])}</p>{cos}
</main>
<footer><div class="wrap">{e(t["footBrand"])} · <a href="{inici}" style="color:inherit">{e(p["home"])}</a></div></footer>
</body>
</html>
"""


def pagina_domicili(lang, T, cfg, pagines):
    p, t = pagines[lang], T[lang]
    inici = INICI[lang]
    wa = f"https://wa.me/{WA}?text={quote(p['wa'])}"
    preps = [t[f"prep_{k}"] for k in ("net", "filets", "rodanxes", "sencer", "forn", "planxa", "sal", "cru", "sopa")]
    normal = "".join(f"<li><strong>{e(t[f'hoursDay{i}'])}</strong>: {e(t[f'hoursTime{i}'])}</li>" for i in (1, 2, 3))
    hoy = date.today().isoformat()
    nadal = cfg.get("nadal", {})
    enllac_nadal = ""
    if nadal.get("mostrarFins", "") >= hoy:
        enllac_nadal = f'<p class="note"><a href="{NADAL[lang]["url"]}">{e(p["nadalLink"])}</a></p>'
    cos = f"""
    <div class="hero">
      <div>
        <p class="eyebrow">{e(p["eyebrow"])}</p>
        <h1>{e(p["h1"])}</h1>
        <p class="lead">{e(p["intro"])}</p>
        <div class="ctas">
          <a class="btn btn-gold" href="{wa}" target="_blank" rel="noopener">{e(p["waBtn"])}</a>
          <a class="btn btn-line" href="{inici}#encarrec">{e(p["formBtn"])}</a>
        </div>
      </div>
      <div class="img"><img src="/img/taulell-sense-preus.webp" width="1067" height="800" alt="{e(p["imgAlt"])}" fetchpriority="high"></div>
    </div>
  </div>
  <section><div class="wrap grid2">
    <div>
      <h2>{e(p["howTitle"])}</h2>
      <ol class="steps">{"".join(f"<li>{e(x)}</li>" for x in p["steps"])}</ol>
    </div>
    <div>
      <h2>{e(p["deliveryTitle"])}</h2>
      <p>{t["valueReparto"]}</p>
      {enllac_nadal}
    </div>
  </div></section>
  <section><div class="wrap">
    <h2>{e(p["prepTitle"])}</h2>
    <ul class="chips">{"".join(f"<li>{e(x)}</li>" for x in preps)}</ul>
    <p class="note">{e(t["perk1"])}</p>
  </div></section>
  <section><div class="wrap grid2">
    <div>
      <h2>{e(p["avuiTitle"])}</h2>
      <p>{e(p["avuiText"])}</p>
      <div class="ctas"><a class="btn btn-line" href="{inici}#avui">{e(p["avuiBtn"])}</a></div>
    </div>
    <div>
      <h2>{e(p["whyTitle"])}</h2>
      <p><strong>{e(t["feat1Title"])}.</strong> {e(t["feat1Body"])}</p>
      <p><strong>{e(t["feat3Title"])}.</strong> {html.unescape(t["feat3Body"])}</p>
    </div>
  </div></section>
  <section class="dark"><div class="wrap grid2">
    <div>
      <h2>{e(p["hoursTitle"])}</h2>
      <ul class="plain">{normal}</ul>
      <p class="note" style="color:inherit">{e(p["hoursNote"])}</p>
    </div>
    {on_som(p, wa)}
  </div></section>"""
    return marc(lang, p, pagines, t, cos)


DOMICILI = {
    "ca": {
        "url": "/peix-marisc-domicili-castelldefels/",
        "title": "Peix i marisc a domicili a Castelldefels · Peixateria Mulhacén",
        "desc": "Peix i marisc de llotja a domicili a Castelldefels, net i a punt per cuinar. Encarrega per WhatsApp: lliurament gratuït a partir de 50 €. Des del 1954.",
        "eyebrow": "A domicili a Castelldefels",
        "h1": "Peix i marisc a domicili a Castelldefels",
        "intro": "Triem cada matí el millor de la llotja i t'ho portem a casa, a Castelldefels, preparat tal com ho demanaries al taulell. Encarrega-ho per WhatsApp i acordem amb tu l'hora del lliurament. Gratuït a partir de 50 € de compra.",
        "wa": "Hola, voldria fer un encàrrec a domicili.",
        "waBtn": "Demanar per WhatsApp",
        "formBtn": "Fer l'encàrrec al web",
        "howTitle": "Com funciona",
        "steps": ["Digues-nos què vols i com t'ho preparem, per WhatsApp o amb el formulari del web.",
                  "Et confirmem el peix disponible i acordem l'hora del lliurament.",
                  "T'ho portem a casa, a punt per cuinar."],
        "deliveryTitle": "Lliurament a domicili",
        "nadalLink": "Per Nadal, reserva el marisc amb temps →",
        "prepTitle": "Com t'ho preparem",
        "avuiTitle": "Què ha arribat avui",
        "avuiText": "Cada matí publiquem al web la pissarra del dia, amb el que ha arribat de la llotja i les fotos del taulell.",
        "avuiBtn": "Veure la pissarra d'avui",
        "whyTitle": "Per què la Peixateria Mulhacén",
        "hoursTitle": "Horari de la botiga",
        "hoursNote": "L'hora del lliurament l'acordem amb tu per WhatsApp.",
        "visitTitle": "On som",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Telèfon de la botiga",
        "home": "Tornar a l'inici",
        "breadcrumb": "Inici",
        "imgAlt": "Ostres, gambes i peix fresc al taulell de la Peixateria Mulhacén",
    },
    "es": {
        "url": "/es/pescado-marisco-domicilio-castelldefels/",
        "title": "Pescado y marisco a domicilio en Castelldefels · Pescadería Mulhacén",
        "desc": "Pescado y marisco de lonja a domicilio en Castelldefels, limpio y listo para cocinar. Encarga por WhatsApp: entrega gratis a partir de 50 €. Desde 1954.",
        "eyebrow": "A domicilio en Castelldefels",
        "h1": "Pescado y marisco a domicilio en Castelldefels",
        "intro": "Elegimos cada mañana lo mejor de la lonja y te lo llevamos a casa, en Castelldefels, preparado como lo pedirías en el mostrador. Encárgalo por WhatsApp y acordamos contigo la hora de la entrega. Gratis a partir de 50 € de compra.",
        "wa": "Hola, querría hacer un pedido a domicilio.",
        "waBtn": "Pedir por WhatsApp",
        "formBtn": "Hacer el encargo en la web",
        "howTitle": "Cómo funciona",
        "steps": ["Dinos qué quieres y cómo te lo preparamos, por WhatsApp o con el formulario de la web.",
                  "Te confirmamos el pescado disponible y acordamos la hora de la entrega.",
                  "Te lo llevamos a casa, listo para cocinar."],
        "deliveryTitle": "Entrega a domicilio",
        "nadalLink": "Para Navidad, reserva el marisco con tiempo →",
        "prepTitle": "Cómo te lo preparamos",
        "avuiTitle": "Qué ha llegado hoy",
        "avuiText": "Cada mañana publicamos en la web la pizarra del día, con lo que ha llegado de la lonja y las fotos del mostrador.",
        "avuiBtn": "Ver la pizarra de hoy",
        "whyTitle": "Por qué la Pescadería Mulhacén",
        "hoursTitle": "Horario de la tienda",
        "hoursNote": "La hora de la entrega la acordamos contigo por WhatsApp.",
        "visitTitle": "Dónde estamos",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Teléfono de la tienda",
        "home": "Volver al inicio",
        "breadcrumb": "Inicio",
        "imgAlt": "Ostras, gambas y pescado fresco en el mostrador de la Pescadería Mulhacén",
    },
    "en": {
        "url": "/en/fish-seafood-delivery-castelldefels/",
        "title": "Fish and seafood delivery in Castelldefels · Mulhacén Fishmonger",
        "desc": "Fresh fish and seafood delivered to your home in Castelldefels, cleaned and ready to cook. Order on WhatsApp: free delivery over €50. Since 1954.",
        "eyebrow": "Home delivery in Castelldefels",
        "h1": "Fish and seafood delivery in Castelldefels",
        "intro": "Every morning we pick the best of the fish market and bring it to your home in Castelldefels, prepared just as you'd ask at the counter. Order on WhatsApp and we'll agree the delivery time with you. Free on orders over €50.",
        "wa": "Hi, I'd like to order a home delivery.",
        "waBtn": "Order on WhatsApp",
        "formBtn": "Order on the website",
        "howTitle": "How it works",
        "steps": ["Tell us what you want and how to prepare it, on WhatsApp or with the order form on the website.",
                  "We confirm what's available and agree the delivery time.",
                  "We bring it to your door, ready to cook."],
        "deliveryTitle": "Home delivery",
        "nadalLink": "For Christmas, reserve your seafood in advance →",
        "prepTitle": "How we prepare it",
        "avuiTitle": "What came in today",
        "avuiText": "Every morning we post the day's board on the website, with what came in from the fish market and photos of the counter.",
        "avuiBtn": "See today's board",
        "whyTitle": "Why Mulhacén Fishmonger",
        "hoursTitle": "Shop opening hours",
        "hoursNote": "We agree the delivery time with you on WhatsApp.",
        "visitTitle": "Where we are",
        "address": "Carrer de la Llibertat, 10 · 08860 Castelldefels",
        "shopPhone": "Shop phone",
        "home": "Back to home",
        "breadcrumb": "Home",
        "imgAlt": "Oysters, prawns and fresh fish on the counter at Mulhacén Fishmonger",
    },
}


def genera(arrel, T):
    cfg = config(arrel)
    sortida, grups = {}, []
    for pagines, fn in ((NADAL, pagina_nadal), (DOMICILI, pagina_domicili)):
        for lang, p in pagines.items():
            sortida[p["url"].strip("/") + "/index.html"] = fn(lang, T, cfg, pagines)
        grups.append([(l, p["url"]) for l, p in pagines.items()])
    return sortida, grups
