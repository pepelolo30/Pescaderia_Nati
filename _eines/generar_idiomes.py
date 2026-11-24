#!/usr/bin/env python3
import html
import json
import os
import re
import subprocess
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import landings  # noqa: E402

ARREL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMINI = "https://mulhacen.cat"
IDIOMES = {"es": {"locale": "es_ES"}, "en": {"locale": "en_GB"}}
BUITS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


def diccionari(font):
    ini = font.index("  var T = {")
    fi = font.index("['ca','es','en'].forEach(", ini)
    fi = font.index("\n", fi)
    codi = font[ini:fi] + "\nprocess.stdout.write(JSON.stringify(T));"
    r = subprocess.run(["node", "-e", codi], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


class Elements(HTMLParser):
    def __init__(self, font):
        super().__init__(convert_charrefs=False)
        self.linies = [0]
        for m in re.finditer("\n", font):
            self.linies.append(m.end())
        self.font = font
        self.pila = []
        self.elements = []

    def pos(self):
        l, c = self.getpos()
        return self.linies[l - 1] + c

    def handle_starttag(self, tag, attrs):
        ini = self.pos()
        text = self.get_starttag_text()
        el = {"tag": tag, "attrs": dict(attrs), "ini": ini, "fi_obre": ini + len(text), "tanca": None}
        self.elements.append(el)
        if tag not in BUITS:
            self.pila.append(el)

    def handle_startendtag(self, tag, attrs):
        ini = self.pos()
        text = self.get_starttag_text()
        self.elements.append({"tag": tag, "attrs": dict(attrs), "ini": ini, "fi_obre": ini + len(text), "tanca": None})

    def handle_endtag(self, tag):
        ini = self.pos()
        for i in range(len(self.pila) - 1, -1, -1):
            if self.pila[i]["tag"] == tag:
                self.pila[i]["tanca"] = ini
                del self.pila[i:]
                break


def posa_atribut(obre, nom, valor):
    v = html.escape(valor, quote=True)
    patro = re.compile(r'(\s' + re.escape(nom) + r'=)("[^"]*"|\'[^\']*\'|[^\s>]+)')
    if patro.search(obre):
        return patro.sub(lambda m: m.group(1) + '"' + v + '"', obre, count=1)
    return re.sub(r"(/?>)$", " " + nom + '="' + v + '"' + r"\1", obre, count=1)


def assignacions(font):
    ini = font.index("function applyLang(lang){")
    cos = font[ini:font.index("afterLang(lang, t);", ini)]
    return [(m.group(2), m.group(1) == "HTML", m.group(3))
            for m in re.finditer(r"set(Text|HTML)\('(\w+)',\s*t\.(\w+)\)", cos)]


def tradueix(font, t, lang):
    p = Elements(font)
    p.feed(font)
    canvis = []
    per_id = {e["attrs"].get("id"): e for e in p.elements if e["attrs"].get("id")}

    def interior(el, valor, es_html):
        if el["tanca"] is None:
            return
        canvis.append((el["fi_obre"], el["tanca"], valor if es_html else html.escape(valor, quote=False)))

    def atributs(el, parells):
        obre = font[el["ini"]:el["fi_obre"]]
        nou = obre
        for nom, valor in parells:
            nou = posa_atribut(nou, nom, valor)
        if nou != obre:
            canvis.append((el["ini"], el["fi_obre"], nou))

    for ident, es_html, clau in assignacions(font):
        if ident in per_id and isinstance(t.get(clau), str):
            interior(per_id[ident], t[clau], es_html)
    for ident in ("navOrderBtn", "heroOrderBtn"):
        if ident in per_id:
            interior(per_id[ident], t["orderCta"], False)
            atributs(per_id[ident], [("href", t["waLink"])])
    if "waCardBtn" in per_id:
        interior(per_id["waCardBtn"], t["waCardBtnLabel"], False)
        atributs(per_id["waCardBtn"], [("href", t["waLink"])])
    if "waFloatBtn" in per_id:
        atributs(per_id["waFloatBtn"], [("aria-label", t["waFloatLabel"]), ("href", t["waLink"])])
    if "nadalMore" in per_id and t.get("nadalMoreUrl"):
        atributs(per_id["nadalMore"], [("href", t["nadalMoreUrl"])])
    if "domiciliMore" in per_id and t.get("domiciliMoreUrl"):
        atributs(per_id["domiciliMore"], [("href", t["domiciliMoreUrl"])])
    if "radioBtn" in per_id:
        atributs(per_id["radioBtn"], [("aria-label", t["radioBtnLabel"]), ("title", t["radioBtnLabel"])])
    for ident, l in (("langCa", "ca"), ("langEs", "es"), ("langEn", "en")):
        if ident in per_id:
            atributs(per_id[ident], [("aria-pressed", "true" if l == lang else "false")])

    for el in p.elements:
        a = el["attrs"]
        if "data-t" in a and isinstance(t.get(a["data-t"]), str):
            interior(el, t[a["data-t"]], True)
        parells = []
        if a.get("data-t-ph") and t.get(a["data-t-ph"]):
            parells.append(("placeholder", t[a["data-t-ph"]]))
        if a.get("data-t-aria") and t.get(a["data-t-aria"]):
            parells += [("aria-label", t[a["data-t-aria"]]), ("title", t[a["data-t-aria"]])]
        if a.get("data-t-alt") and t.get(a["data-t-alt"]):
            parells.append(("alt", t[a["data-t-alt"]]))
        if parells:
            atributs(el, parells)

    canvis.sort(key=lambda c: (c[0], -c[1]))
    nets, fins = [], -1
    for c in canvis:
        if c[0] < fins and c[1] <= fins:
            continue
        nets.append(c)
        fins = max(fins, c[1])
    for ini, fi, nou in sorted(nets, key=lambda c: c[0], reverse=True):
        font = font[:ini] + nou + font[fi:]
    return font


def capcalera(font, t, lang):
    url = f"{DOMINI}/{lang}/"
    titol = html.escape(t["pageTitle"], quote=True)
    desc = html.escape(t["pageDesc"], quote=True)
    subs = [
        (r'<html lang="ca">', f'<html lang="{lang}">'),
        (r"<title>[^<]*</title>", f"<title>{titol}</title>"),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">'),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">'),
        (r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{IDIOMES[lang]["locale"]}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{titol}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
        (r'<base href="/">', f'<base href="/"><script>window.LANG_PAGINA="{lang}"</script>'),
    ]
    for patro, nou in subs:
        font, n = re.subn(patro, lambda m: nou, font, count=1)
        if n != 1:
            raise SystemExit(f"No trobo {patro} a index.html")
    return font


def sitemap(grups):
    urls = ""
    for grup in grups:
        alt = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{DOMINI}{u}"/>' for l, u in grup)
        alt += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{DOMINI}{grup[0][1]}"/>'
        urls += "".join(f"\n  <url>\n    <loc>{DOMINI}{u}</loc>{alt}\n  </url>" for _, u in grup)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
            f"{urls}\n</urlset>\n")


def escriu(ruta, contingut):
    ruta = os.path.join(ARREL, ruta)
    try:
        with open(ruta, encoding="utf-8") as f:
            if f.read() == contingut:
                return False
    except FileNotFoundError:
        pass
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contingut)
    return True


def main():
    with open(os.path.join(ARREL, "index.html"), encoding="utf-8") as f:
        font = f.read()
    T = diccionari(font)
    canviats = []
    for lang in IDIOMES:
        pagina = capcalera(tradueix(font, T[lang], lang), T[lang], lang)
        if escriu(f"{lang}/index.html", pagina):
            canviats.append(f"{lang}/index.html")
    pagines, grups_landings = landings.genera(ARREL, T)
    for ruta, html_pagina in pagines.items():
        if escriu(ruta, html_pagina):
            canviats.append(ruta)
    grups = [[("ca", "/"), ("es", "/es/"), ("en", "/en/")]] + grups_landings
    if escriu("sitemap.xml", sitemap(grups)):
        canviats.append("sitemap.xml")
    print("Generat: " + (", ".join(canviats) if canviats else "sense canvis"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
