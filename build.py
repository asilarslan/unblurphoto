#!/usr/bin/env python3
"""Static site generator for unblurphoto.app (GitHub Pages).

    python3 build.py            # build from content/ and content/app.json
    python3 build.py --refresh  # also refresh rating/version from the App Store

Generated HTML is committed; GitHub Pages serves the repo root as-is.
"""
import datetime
import hashlib
import html
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content.home import HOME  # noqa: E402
from content.guides import GUIDES, TOOL_PAGE  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://unblurphoto.app"
APP_ID = "6751783489"
# App Store Connect → App Analytics → Campaigns shows this provider token.
# Campaign tokens (ct) are only attributed when it is set.
PROVIDER_TOKEN = ""
LANGS = ["en", "tr", "es", "pt", "de", "ja"]
TODAY = datetime.date.today().isoformat()
SUPPORT = "asilarslan93@gmail.com"

esc = html.escape


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def version(path):
    return hashlib.sha1(read(path).encode()).hexdigest()[:8]


def load_app(refresh):
    path = os.path.join(ROOT, "content", "app.json")
    if refresh or not os.path.exists(path):
        url = f"https://itunes.apple.com/lookup?id={APP_ID}&country=us"
        r = json.load(urllib.request.urlopen(url, timeout=20))["results"][0]
        data = {
            "rating": round(r["averageUserRating"], 1),
            "count": r["userRatingCount"],
            "min_os": r["minimumOsVersion"],
            "version": r["version"],
            "fetched": TODAY,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    with open(path) as f:
        return json.load(f)


def store_url(campaign):
    q = f"?ct={campaign}&mt=8"
    if PROVIDER_TOKEN:
        q = f"?pt={PROVIDER_TOKEN}&ct={campaign}&mt=8"
    return f"https://apps.apple.com/app/apple-store/id{APP_ID}{q}"


def home_path(lang):
    return "/" if lang == "en" else f"/{lang}/"


def badge(t, campaign, extra=""):
    return (f'<a class="badge" href="{store_url(campaign)}" rel="noopener"{extra}>'
            f'<img src="/assets/img/app-store-{t["badge"]}.svg" alt="Download on the App Store" width="162" height="54"></a>')


def header(t, lang, anchors_local):
    base = "" if anchors_local else home_path(lang)
    opts = "".join(
        f'<option value="{home_path(l)}"{" selected" if l == lang else ""}>{HOME[l]["name"]}</option>' for l in LANGS)
    n = t["nav"]
    return f"""<header class="top"><div class="wrap">
<a class="brand" href="{home_path(lang)}"><img src="/assets/img/icon-64.png" alt="" width="32" height="32">Unblur Image</a>
<nav>
<a class="hide-sm" href="{base}#free-tool">{n['tool']}</a>
<a class="hide-sm" href="{base}#how">{n['how']}</a>
<a class="hide-sm" href="{base}#faq">{n['faq']}</a>
<select class="lang" aria-label="Language">{opts}</select>
<a class="get" href="{store_url('web-nav-' + lang)}" rel="noopener">{n['get']}</a>
</nav></div></header>"""


def footer(t, lang):
    guides = "".join(f'<li><a href="/{g["slug"]}/">{esc(g["h1"])}</a></li>' for g in GUIDES)
    langs = "".join(f'<li><a href="{home_path(l)}" hreflang="{l}">{HOME[l]["name"]}</a></li>' for l in LANGS)
    return f"""<footer><div class="wrap cols">
<div><div class="h">{t['footer_app']}</div><ul>
<li><a href="{store_url('web-footer-' + lang)}" rel="noopener">App Store</a></li>
<li><a href="/free-unblur-tool/">{esc(HOME['en']['nav']['tool'] if lang == 'en' else t['nav']['tool'])}</a></li>
<li><a href="mailto:{SUPPORT}">{t['support']}</a></li></ul></div>
<div><div class="h">{t['footer_guides']}</div><ul>{guides}</ul></div>
<div><div class="h">Language</div><ul>{langs}</ul></div>
<div><div class="h">{t['footer_legal']}</div><ul>
<li><a href="/privacy-policy.html">{t['privacy']}</a></li>
<li><a href="/terms-of-use.html">{t['terms']}</a></li></ul>
<p style="margin-top:12px">© {datetime.date.today().year} {t['copyright']}</p></div>
</div></footer>"""


def sticky(t, lang):
    return (f'<div class="sticky-cta"><a class="btn btn-primary" href="{store_url("web-sticky-" + lang)}" '
            f'rel="noopener">{t["nav"]["get"]}</a></div>')


def tool_html(t, default_mode="focus"):
    tt = t["tool"]
    seg = "".join(
        f'<button type="button" data-mode="{m}" aria-pressed="{"true" if m == default_mode else "false"}">{tt[m]}</button>'
        for m in ("focus", "motion", "text"))
    strings = json.dumps({k: tt[k] for k in ("processing", "done", "error")}, ensure_ascii=False)
    return f"""<div class="tool" data-tool data-worker="/assets/deblur-worker.js?v={version('assets/deblur-worker.js')}" data-sample="/assets/img/sample-blurry.webp">
<script type="application/json" class="tool-i18n">{strings}</script>
<div class="drop" data-drop role="button" tabindex="0">
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#5b5bd6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg>
<div class="big">{tt['drop']}</div><div class="small">{tt['privacy']}</div>
<input type="file" accept="image/*" hidden></div>
<div class="tool-row" data-start><button type="button" class="btn btn-ghost" data-sample>{tt['sample']}</button></div>
<div class="tool-work" data-work hidden>
<div class="ba" data-result>
<img class="ba-after" alt="{t['after']}"><img class="ba-before" alt="{t['before']}">
<span class="ba-tag l">{t['before']}</span><span class="ba-tag r">{t['after']}</span>
<div class="ba-line"></div><div class="ba-knob" role="slider" tabindex="0" aria-label="{t['before']} / {t['after']}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">⇔</div>
</div>
<div>
<div class="seg" role="group">{seg}</div>
<div class="ctl"><label>{tt['strength']} <span data-strength-val>50</span></label><input type="range" min="0" max="100" value="50" data-strength aria-label="{tt['strength']}"></div>
<div class="ctl" data-angle-row{'' if default_mode == 'motion' else ' hidden'}><label>{tt['angle']} <span data-angle-val>0°</span></label><input type="range" min="0" max="175" step="5" value="0" data-angle aria-label="{tt['angle']}"></div>
<div class="status" data-status aria-live="polite"></div><div class="bar"><i></i></div>
<div class="actions"><a class="btn btn-primary" data-download download="unblurred-preview.jpg" href="#" aria-disabled="true">{tt['download']}</a>
<button type="button" class="btn btn-ghost" data-new>{tt['again']}</button></div>
<div class="upsell"><strong>{tt['upsell']}</strong>{badge(t, 'web-tool-' + t['badge'][:2])}</div>
<p class="note">{tt['note']}</p>
</div></div></div>"""


def slider_html(t):
    return f"""<div class="ba" data-hint>
<img class="ba-after" src="/assets/img/demo-after.webp" alt="Photo after AI blur removal" width="720" height="900" fetchpriority="high">
<img class="ba-before" src="/assets/img/demo-before.webp" alt="Blurry photo before" width="720" height="900">
<span class="ba-tag l">{t['before']}</span><span class="ba-tag r">{t['after']}</span>
<div class="ba-line"></div><div class="ba-knob" role="slider" tabindex="0" aria-label="{t['before']} / {t['after']}" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">⇔</div>
</div>"""


def faq_html(t_title, items):
    rows = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items)
    return f'<h2>{esc(t_title)}</h2><div class="faq">{rows}</div>'


def ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False)}</script>'


def page(lang, title, desc, path, body, *, alternates=None, jsonld=(), preload="", tool=False, og_type="website"):
    t = HOME[lang]
    url = SITE + path
    alt = ""
    if alternates:
        alt = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{home_path(l)}">' for l in alternates)
        alt += f'<link rel="alternate" hreflang="x-default" href="{SITE}/">'
    scripts = f'<script src="/assets/site.js?v={version("assets/site.js")}" defer></script>'
    if tool:
        scripts += f'<script src="/assets/tool.js?v={version("assets/tool.js")}" defer></script>'
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
{alt}
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta name="theme-color" content="#ffffff">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Unblur Image">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/assets/img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{t['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/assets/img/og.jpg">
<link rel="icon" href="/assets/img/icon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="manifest" href="/manifest.json">
{preload}
<style>{read('assets/site.css')}</style>
{''.join(ld(j) for j in jsonld)}
</head>
<body>
{body}
{scripts}
</body>
</html>
"""


def app_ld(app, lang):
    return {
        "@context": "https://schema.org",
        "@type": "MobileApplication",
        "name": "Unblur Image: AI Remove Blur",
        "operatingSystem": f"iOS {app['min_os']} or later",
        "applicationCategory": "MultimediaApplication",
        "url": SITE + home_path(lang),
        "downloadUrl": f"https://apps.apple.com/app/id{APP_ID}",
        "image": f"{SITE}/assets/img/icon-512.png",
        "screenshot": [f"{SITE}/assets/img/screen-{i}.webp" for i in (1, 2, 3)],
        "softwareVersion": app["version"],
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": str(app["rating"]),
                            "ratingCount": str(app["count"]), "bestRating": "5", "worstRating": "1"},
    }


def build_home(lang, app):
    t = HOME[lang]
    fmt = {"rating": f"{app['rating']:.1f}", "count": app["count"]}
    if lang in ("tr", "de", "es", "pt"):
        fmt["rating"] = fmt["rating"].replace(".", ",")
    uses = []
    for title, text, link in t["uses"]:
        if link:
            uses.append(f'<a class="card" href="{link}"><h3>{esc(title)}</h3><p>{esc(text)}</p><span class="more">{t["more"]}</span></a>')
        else:
            uses.append(f'<div class="card"><h3>{esc(title)}</h3><p>{esc(text)}</p></div>')
    steps = "".join(f'<div class="card"><div class="num">{i}</div><h3>{esc(a)}</h3><p>{esc(b)}</p></div>'
                    for i, (a, b) in enumerate(t["steps"], 1))
    shots = "".join(f'<img src="/assets/img/screen-{i}.webp" alt="{esc(a)}" width="430" height="934" loading="lazy">'
                    for i, a in enumerate(t["shots_alt"], 1))
    body = f"""{header(t, lang, True)}
<main>
<section class="hero" data-hero><div class="wrap">
<div>
<a class="eyebrow" href="{store_url('web-rating-' + lang)}" rel="noopener"><span class="stars">★★★★★</span> {t['rating'].format(**fmt)}</a>
<h1>{esc(t['h1'])}</h1>
<p class="sub">{esc(t['sub'])}</p>
<div class="ctas">{badge(t, 'web-hero-' + lang)}<a class="btn btn-ghost" href="#free-tool">{t['try']} ↓</a></div>
<p class="compat">{esc(t['compat'])}</p>
<div class="qr"><img src="/assets/img/qr-app-store.svg" alt="QR code" width="84" height="84"><span>{esc(t['qr'])}</span></div>
</div>
<div class="media">{slider_html(t)}<p class="caption">{esc(t['demo_caption'])}</p></div>
</div></section>

<section id="free-tool" class="alt"><div class="wrap">
<div class="center"><h2>{esc(t['tool_h2'])}</h2><p class="lead">{esc(t['tool_lead'])}</p></div>
{tool_html(t)}
</div></section>

<section><div class="wrap">
<h2>{esc(t['uses_h2'])}</h2><p class="lead">{esc(t['uses_lead'])}</p>
<div class="grid2">{''.join(uses)}</div>
</div></section>

<section id="how" class="alt"><div class="wrap">
<h2>{esc(t['how_h2'])}</h2>
<div class="grid3" style="margin-top:24px">{steps}</div>
<h2 style="margin-top:56px" class="center">{esc(t['shots_h2'])}</h2>
<div class="shots">{shots}</div>
</div></section>

<section id="faq"><div class="wrap narrow">{faq_html(t['faq_h2'], t['faq'])}</div></section>

<section><div class="wrap"><div class="cta-band">
<h2>{esc(t['cta_h2'])}</h2><p>{esc(t['cta_p'])}</p>
<div class="ctas">{badge(t, 'web-bottom-' + lang)}</div>
<p class="compat" style="color:#d1d5db">{esc(t['compat'])}</p>
</div></div></section>
</main>
{footer(t, lang)}
{sticky(t, lang)}"""
    desc = t["desc"].format(**fmt)
    jsonld = [app_ld(app, lang), {
        "@context": "https://schema.org", "@type": "WebSite", "name": "Unblur Image",
        "url": SITE + home_path(lang), "inLanguage": lang}]
    out = page(lang, t["title"], desc, home_path(lang), body, alternates=LANGS, jsonld=jsonld, tool=True,
               preload='<link rel="preload" as="image" href="/assets/img/demo-after.webp" fetchpriority="high">')
    write("index.html" if lang == "en" else f"{lang}/index.html", out)


def build_article(g, app, *, is_tool=False):
    t = HOME["en"]
    path = f"/{g['slug']}/"
    crumbs = f'<nav class="crumbs"><a href="/">Home</a> › {esc(g["h1"])}</nav>'
    related = ""
    if g.get("related"):
        by = {x["slug"]: x for x in GUIDES}
        cards = "".join(f'<a class="card" href="/{s}/"><h3>{esc(by[s]["h1"])}</h3><p>{esc(by[s]["desc"])}</p></a>'
                        for s in g["related"])
        related = f'<section class="alt"><div class="wrap"><h2>Related guides</h2><div class="grid2" style="margin-top:20px">{cards}</div></div></section>'
    inline = (f'<div class="inline-cta"><p>Need a sharper, full-resolution result? Unblur Image for iPhone '
              f'rebuilds lost detail with AI. Rated {app["rating"]:.1f}★ on the App Store.</p>'
              f'{badge(t, "web-" + g["slug"])}</div>')
    body = f"""{header(t, 'en', False)}
<main>
<section class="article" data-hero><div class="wrap narrow">
{crumbs}
<h1>{esc(g['h1'])}</h1>
<p class="intro">{esc(g['intro'])}</p>
</div></section>
<section id="free-tool" class="alt" style="padding:32px 0"><div class="wrap">{tool_html(t, g.get('tool_mode', 'focus'))}</div></section>
<section style="padding-top:24px"><div class="wrap narrow prose">
{g['body']}
{inline}
<div id="faq">{faq_html('FAQ', g['faq'])}</div>
</div></section>
{related}
<section><div class="wrap"><div class="cta-band">
<h2>{esc(t['cta_h2'])}</h2><p>{esc(t['cta_p'])}</p>
<div class="ctas">{badge(t, 'web-bottom-' + g['slug'])}<a class="btn btn-ghost" href="/">Back to home</a></div>
</div></div></section>
</main>
{footer(t, 'en')}
{sticky(t, 'en')}"""
    jsonld = [{
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": g["h1"], "item": SITE + path}]}]
    if is_tool:
        jsonld.append({
            "@context": "https://schema.org", "@type": "WebApplication", "name": "Unblur Image – Free Online Unblur Tool",
            "url": SITE + path, "applicationCategory": "MultimediaApplication", "operatingSystem": "Any (web browser)",
            "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}})
    else:
        jsonld.append({
            "@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
            "dateModified": TODAY, "mainEntityOfPage": SITE + path, "image": f"{SITE}/assets/img/og.jpg",
            "author": {"@type": "Organization", "name": "Unblur Image", "url": SITE + "/"},
            "publisher": {"@type": "Organization", "name": "Unblur Image",
                          "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/icon-512.png"}}})
    write(f"{g['slug']}/index.html", page("en", g["title"], g["desc"], path, body, jsonld=jsonld, tool=True,
                                          og_type="website" if is_tool else "article"))


def build_404():
    t = HOME["en"]
    body = f"""{header(t, 'en', False)}
<main><section class="article"><div class="wrap narrow">
<h1>Page not found</h1>
<p class="intro">The page you're looking for doesn't exist. Try the free unblur tool or one of the guides below.</p>
<div class="ctas"><a class="btn btn-primary" href="/free-unblur-tool/">Open the free tool</a><a class="btn btn-ghost" href="/">Home</a></div>
</div></section></main>
{footer(t, 'en')}"""
    out = page("en", "Page not found | Unblur Image", "This page doesn't exist.", "/404.html", body)
    write("404.html", out.replace('<meta name="robots" content="index, follow, max-image-preview:large">',
                                  '<meta name="robots" content="noindex">'))


def build_meta():
    urls = [(home_path(l), "1.0" if l == "en" else "0.9", True) for l in LANGS]
    urls += [("/free-unblur-tool/", "0.9", False)] + [(f"/{g['slug']}/", "0.8", False) for g in GUIDES]
    urls += [("/privacy-policy.html", "0.3", False), ("/terms-of-use.html", "0.3", False)]
    rows = []
    for path, prio, is_home in urls:
        alts = ""
        if is_home:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{SITE}{home_path(l)}"/>' for l in LANGS)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/"/>'
        rows.append(f"  <url>\n    <loc>{SITE}{path}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <priority>{prio}</priority>{alts}\n  </url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(rows) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    write("manifest.json", json.dumps({
        "name": "Unblur Image", "short_name": "Unblur Image",
        "description": "Fix blurry photos free in your browser, or with AI on iPhone.",
        "start_url": "/", "display": "browser", "background_color": "#ffffff", "theme_color": "#ffffff",
        "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "related_applications": [{"platform": "itunes", "url": f"https://apps.apple.com/app/id{APP_ID}"}],
    }, indent=2) + "\n")


def main():
    app = load_app("--refresh" in sys.argv)
    for lang in LANGS:
        build_home(lang, app)
    tool = dict(TOOL_PAGE, related=["fix-motion-blur-photos", "unblur-text-in-image"], tool_mode="focus")
    build_article(tool, app, is_tool=True)
    for g in GUIDES:
        build_article(g, app)
    build_404()
    build_meta()
    print(f"Built {len(LANGS)} home pages, {len(GUIDES) + 1} English pages · rating {app['rating']} ({app['count']})")


if __name__ == "__main__":
    main()
