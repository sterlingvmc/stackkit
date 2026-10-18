#!/usr/bin/env python3
"""StackKit static site generator. Usage: SITE_URL=https://yourdomain python3 build.py
Reads data/tools.json, writes the site to ./site (clean URLs: /tools/<slug>/index.html)."""
import json, os, shutil, html, datetime
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
# Used in canonical URLs, sitemap, robots, llms.txt and the GitHub Pages CNAME file.
SITE_URL = os.environ.get("SITE_URL", "https://stackkit.ink").rstrip("/")
BRAND = "StackKit"
TAGLINE = "The toolkit for writers growing a newsletter on Substack"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "hello@stackkit.ink")
# TODO: replace with real Stripe Payment Links.
STRIPE = {
  "featured_category": "TODO_STRIPE_LINK_FEATURED_CATEGORY",
  "featured_home": "TODO_STRIPE_LINK_FEATURED_HOMEPAGE",
  "newsletter_slot": "TODO_STRIPE_LINK_NEWSLETTER_SLOT",
  "fast_track": "TODO_STRIPE_LINK_FAST_TRACK",
}
GUIDE_SLUG = "best-tools-to-grow-your-substack-2026"
GUIDE_TOOLS = {"google-analytics","canva","grammarly","hemingway-editor","notion","unsplash","sparkloop","supascribe","buffer","writestack","narrareach","stacksweller","subshack","typefully","taplio","hypefury","repurpose-io","byline-os","bitly","plausible","descript","elevenlabs","riverside","opusclip","adobe-podcast","hecto","swapstack","paved","gumroad","ko-fi"}  # keep in sync with guide() sections

data = json.load(open(os.path.join(ROOT, "data", "tools.json")))
TOOLS = data["tools"]; CATS = data["categories"]
CAT = {c["slug"]: c for c in CATS}
BY = {t["slug"]: t for t in TOOLS}
BYCAT = defaultdict(list)
for t in sorted(TOOLS, key=lambda t: t["name"].lower()): BYCAT[t["category"]].append(t)
TODAY = datetime.date.today().isoformat()
e = lambda s: html.escape(str(s or ""), quote=True)
pages = []  # (path, priority) for sitemap

LOGO = '<svg viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="8" fill="#ff5a1f"/><rect x="7" y="8" width="18" height="4" rx="2" fill="#fff"/><rect x="7" y="14" width="18" height="4" rx="2" fill="#fff" opacity=".8"/><rect x="7" y="20" width="12" height="4" rx="2" fill="#fff" opacity=".6"/></svg>'

def layout(path, title, desc, body, jsonld=None, js=False, current=None):
    canon = SITE_URL + path
    nav = [("/", "Directory"), ("/guides/%s/" % GUIDE_SLUG, "2026 Guide"), ("/about/", "About"), ("/feature/", "Feature your tool")]
    navh = "".join('<a href="%s"%s%s>%s</a>' % (h, ' aria-current="page"' if h == current else "", ' class="hide-sm"' if h == "/about/" else "", l) for h, l in nav[:-1])
    ld = ('<script type="application/ld+json">%s</script>' % json.dumps(jsonld, ensure_ascii=False)) if jsonld else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(canon)}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(canon)}">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
{ld}
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap">
<a class="logo" href="/">{LOGO}{BRAND}</a>
<nav class="main" aria-label="Main">{navh}<a class="btn sm brand" href="/feature/">Feature your tool</a></nav>
</div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap cols">
<div><strong>{BRAND}</strong><br>{e(TAGLINE)}.<br>Independent. Not affiliated with, sponsored by, or endorsed by Substack Inc.</div>
<div><a href="/">Directory</a><br><a href="/guides/{GUIDE_SLUG}/">Best tools to grow your Substack in 2026</a><br><a href="/feature/">Feature your tool</a><br><a href="/about/">About &amp; disclosures</a></div>
<div>Some links may be affiliate links; it never changes our verdicts.<br>Data last verified {e(data['generated'])}.<br><a href="/llms.txt">llms.txt</a> · <a href="/sitemap.xml">sitemap</a></div>
</div></footer>
{'<script src="/assets/app.js" defer></script>' if js else '<script src="/assets/app.js" defer></script>'}
</body></html>"""

def write(path, content, priority="0.6"):
    fp = os.path.join(OUT, path.lstrip("/"), "index.html") if path.endswith("/") else os.path.join(OUT, path.lstrip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w").write(content)
    if path.endswith("/"): pages.append((path, priority))

def tags(t):
    out = ['<span class="tag">%s</span>' % e(CAT[t["category"]]["name"])]
    if t.get("free_plan"): out.append('<span class="tag free">Free plan</span>')
    if t.get("substack_specific"): out.append('<span class="tag ss">Built for Substack</span>')
    return "".join(out)

def card(t):
    hay = " ".join([t["name"], t["best_for"], t["verdict"], CAT[t["category"]]["name"], t["pricing"]]).lower()
    return (f'<article class="card" data-cat="{e(t["category"])}" data-free="{1 if t.get("free_plan") else 0}" data-ss="{1 if t.get("substack_specific") else 0}" data-search="{e(hay)}">'
            f'<h3><a href="/tools/{e(t["slug"])}/">{e(t["name"])}</a></h3><p>{e(t["best_for"])}</p><div class="meta">{tags(t)}</div></article>')

FEATURED_PLACEHOLDER = ('<aside class="card featured" aria-label="Featured placement available"><span class="tag">Featured · placeholder</span>'
    '<h3><a href="/feature/">Your tool here</a></h3><p>Reach writers actively looking for tools. Featured spots are clearly labeled as sponsored.</p></aside>')

SUBSTACK_URL = "https://stackkit.substack.com"
SIGNUP = f"""<section class="block" id="newsletter"><div class="wrap"><div class="signup">
<div><h2>One useful tool a week</h2><p>A short weekly email: one tool we've checked, what it costs, and who it's actually for. Free.</p></div>
<div class="embed">
<iframe src="{SUBSTACK_URL}/embed" title="Subscribe to the StackKit newsletter on Substack" width="480" height="150" loading="lazy" frameborder="0" scrolling="no"></iframe>
<p class="fallback">Form not loading? <a href="{SUBSTACK_URL}/subscribe" target="_blank" rel="noopener">Subscribe on Substack →</a></p>
</div></div></div></section>"""

# ---------------- Homepage ----------------
def home():
    chips = '<button class="chip" data-cat="all" aria-pressed="true">All</button>' + "".join(
        f'<button class="chip" data-cat="{c["slug"]}" aria-pressed="false">{e(c["name"])}</button>' for c in CATS)
    allcards = sorted(TOOLS, key=lambda t: (t["category"] != "growth", t["name"].lower()))
    grid = FEATURED_PLACEHOLDER + "".join(card(t) for t in allcards)
    cats = "".join(f'<a href="/category/{c["slug"]}/"><strong>{e(c["name"])}</strong> ({len(BYCAT[c["slug"]])})<span>{e(c["desc"])}</span></a>' for c in CATS)
    body = f"""<section class="hero"><div class="wrap">
<h1>Tools to grow your Substack,<br>checked by hand.</h1>
<p class="lead">{len(TOOLS)} verified tools for growth, Notes, analytics, design, editing, audio and sponsorships, each with real pricing and an honest one-line verdict.</p>
<form class="search" role="search" onsubmit="return false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
<label for="q" class="skip">Search tools</label><input id="q" type="search" placeholder="Try “Notes scheduler”, “analytics”, “free”, “podcast”…" autocomplete="off"></form>
<div class="chips" role="group" aria-label="Filter by use case">{chips}</div>
<div class="toggles"><label><input type="checkbox" id="f-free"> Has a free plan</label><label><input type="checkbox" id="f-ss"> Built specifically for Substack</label></div>
</div></section>
<div class="wrap"><p class="count" id="count" aria-live="polite">{len(TOOLS)} tools</p>
<div class="grid" id="grid">{grid}</div><p class="empty" id="empty">No tools match. Try a broader search.</p></div>
<section class="block"><div class="wrap"><h2>Browse by use case</h2><p class="sub">Every category page lists tools with pricing and verdicts.</p><div class="cats">{cats}</div></div></section>
<section class="block"><div class="wrap"><h2>New here? Start with the guide</h2><p class="sub">Our long-form guide picks the tools that matter at each stage, from $0 to a full paid-newsletter stack.</p>
<a class="btn" href="/guides/{GUIDE_SLUG}/">Read: Best tools to grow your Substack in 2026 →</a></div></section>
{SIGNUP}"""
    ld = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE_URL + "/", "description": TAGLINE,
          "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/?q={search_term_string}", "query-input": "required name=search_term_string"}}
    write("/", layout("/", f"{BRAND}: Tools to grow your Substack newsletter ({len(TOOLS)} verified)",
        f"A hand-checked directory of {len(TOOLS)} tools for Substack writers: growth, Notes scheduling, analytics, design, editing, audio and sponsorships, with real pricing and honest verdicts.",
        body, ld, current="/"), "1.0")

# ---------------- Category pages ----------------
def category(c):
    ts = BYCAT[c["slug"]]
    rows = "".join(f'<tr><td><a href="/tools/{t["slug"]}/"><strong>{e(t["name"])}</strong></a></td><td>{e(t["best_for"])}</td><td>{e(t["pricing"])}</td></tr>' for t in ts)
    others = " · ".join(f'<a href="/category/{o["slug"]}/">{e(o["name"])}</a>' for o in CATS if o["slug"] != c["slug"])
    body = f"""<div class="wrap page"><div class="crumbs"><a href="/">Directory</a> / {e(c['name'])}</div>
<h1>{e(c['name'])} tools for Substack writers</h1><p class="sub">{e(c['desc'])}</p>
<div class="grid">{''.join(card(t) for t in ts)}{FEATURED_PLACEHOLDER}</div>
<h2>Pricing at a glance</h2><div class="table-wrap"><table class="cmp"><thead><tr><th>Tool</th><th>Best for</th><th>Pricing (checked {e(data['generated'])})</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Prices change. Always confirm on the vendor's site.</p>
<p class="small">Other categories: {others}</p></div>{SIGNUP}"""
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": c["name"] + " tools",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + f"/tools/{t['slug']}/", "name": t["name"]} for i, t in enumerate(ts)]}
    write(f"/category/{c['slug']}/", layout(f"/category/{c['slug']}/", f"Best {c['name']} tools for Substack writers (2026) | {BRAND}",
        f"{len(ts)} hand-checked {c['name'].lower()} tools for Substack writers, including " + ", ".join(t['name'] for t in ts[:4]) + ". Real pricing and honest verdicts.", body, ld), "0.8")

# ---------------- Tool pages ----------------
def tool(t):
    c = CAT[t["category"]]
    rel = [o for o in BYCAT[t["category"]] if o["slug"] != t["slug"]][:6]
    aff = t["affiliate_program"] == "yes"
    affnote = ("This vendor runs an affiliate program, so we may earn a commission if you sign up through StackKit in the future. It doesn't affect the verdict."
               if aff else "We have no affiliate relationship with this vendor.")
    # TODO: when an affiliate link is approved, swap t['url'] for the tracking link and use rel="sponsored noopener".
    body = f"""<div class="wrap page"><div class="crumbs"><a href="/">Directory</a> / <a href="/category/{c['slug']}/">{e(c['name'])}</a> / {e(t['name'])}</div>
<div class="tool-head"><div><h1>{e(t['name'])}</h1><div class="meta" style="display:flex;gap:6px;flex-wrap:wrap">{tags(t)}</div></div>
<a class="btn brand" href="{e(t['url'])}" target="_blank" rel="noopener">Visit {e(t['name'])} ↗</a></div>
<p class="verdict"><strong>Our verdict:</strong> {e(t['verdict'])}</p>
<div class="facts">
<div class="fact"><h2>Best for</h2><p>{e(t['best_for'])}</p></div>
<div class="fact"><h2>Pricing</h2><p>{e(t['pricing'])}</p><p class="small">Source: {e(t['pricing_source'])}</p></div>
<div class="fact"><h2>Website</h2><p><a href="{e(t['url'])}" target="_blank" rel="noopener">{e(t['url'].replace('https://','').rstrip('/'))}</a></p></div>
<div class="fact"><h2>Last checked</h2><p>{e(t['verified_on'])}</p></div>
</div>
{f'<p class="small">Note: {e(t["notes"])}</p>' if t.get("notes") and not t["notes"].startswith("Affiliate") else ''}
<p class="small">Disclosure: {affnote} {BRAND} is independent and not affiliated with Substack Inc. Spot an error? Email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<h2>Other {e(c['name'].lower())} tools</h2><div class="grid">{''.join(card(o) for o in rel)}</div>
{f'<p><a href="/guides/{GUIDE_SLUG}/">See where {e(t["name"])} fits in our 2026 growth guide →</a></p>' if t['slug'] in GUIDE_TOOLS else f'<p><a href="/guides/{GUIDE_SLUG}/">Read our 2026 growth guide →</a></p>'}</div>"""
    ld = {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": t["name"], "url": t["url"], "applicationCategory": "BusinessApplication",
          "description": t["best_for"], "review": {"@type": "Review", "author": {"@type": "Organization", "name": BRAND}, "reviewBody": t["verdict"]}}
    write(f"/tools/{t['slug']}/", layout(f"/tools/{t['slug']}/", f"{t['name']} for Substack writers: pricing & verdict | {BRAND}",
        f"{t['name']}: {t['best_for']}. Pricing: {t['pricing']}"[:300], body, ld), "0.7")

# ---------------- Feature page ----------------
def feature():
    def btn(key, label):
        return (f'<span class="todo-label">TODO: Stripe Payment Link</span>'
                f'<a class="btn brand" href="#{STRIPE[key]}" data-todo="Replace with Stripe Payment Link ({STRIPE[key]})">{label}</a>')
    body = f"""<div class="wrap page"><div class="crumbs"><a href="/">Directory</a> / Feature your tool</div>
<h1>Put your tool in front of Substack writers</h1>
<p class="sub" style="max-width:720px">{BRAND} readers are newsletter writers actively looking for tools to grow free and paid subscribers. Sponsored placements are always labeled, and sponsorship never buys a better verdict.</p>
<div class="tiers">
<div class="tier"><h2>Fast-track listing</h2><div class="price">$49 <small>one-time</small></div>
<p>Skip the free-submission queue. We review and publish within 5 business days if your tool qualifies.</p>
<ul><li>Priority review</li><li>Standard listing with an honest verdict</li><li>No guarantee of inclusion: refunded if rejected</li></ul>{btn('fast_track','Get fast-tracked')}</div>
<div class="tier"><h2>Featured in a category</h2><div class="price">$59 <small>/ month</small></div>
<p>Pinned "Featured" card at the top of one category page.</p>
<ul><li>One category of your choice</li><li>Clearly labeled sponsored</li><li>Cancel anytime</li></ul>{btn('featured_category','Feature in a category')}</div>
<div class="tier pop"><h2>Featured on the homepage</h2><div class="price">$129 <small>/ month</small></div>
<p>The featured card in the main directory grid, seen by every visitor.</p>
<ul><li>Homepage + one category</li><li>Limited to 2 sponsors at a time</li><li>Clearly labeled sponsored</li></ul>{btn('featured_home','Feature on the homepage')}</div>
<div class="tier"><h2>Newsletter sponsor slot</h2><div class="price">$79 <small>/ issue</small></div>
<p>The single sponsor block in our weekly "one useful tool" email.</p>
<ul><li>~60 words + link</li><li>One sponsor per issue</li><li>Launch pricing while the list grows</li></ul>{btn('newsletter_slot','Book a newsletter slot')}</div>
</div>
<div class="prose"><h2>Free submissions</h2><p>Listing is free. Email <a href="mailto:{CONTACT_EMAIL}?subject=Tool%20submission">{CONTACT_EMAIL}</a> with your tool's name, URL, pricing page and why Substack writers should care. Free submissions are reviewed in batches.</p>
<h2>Our rules</h2><ul><li>We only list tools we can verify exist and are usable today.</li><li>Paid placement buys visibility, never a better verdict.</li><li>Sponsored and affiliate links are labeled.</li><li>We may decline sponsors that aren't relevant or trustworthy for writers.</li></ul></div>
<p class="small">Prices are launch placeholders. TODO: confirm final pricing and connect Stripe Payment Links.</p></div>"""
    write("/feature/", layout("/feature/", f"Feature your tool to Substack writers | {BRAND} sponsorships",
        "Reach newsletter writers growing on Substack: featured listings, newsletter sponsor slots and fast-track submissions on StackKit.", body, current="/feature/"), "0.6")

# ---------------- About page ----------------
def about():
    body = f"""<div class="wrap page prose"><div class="crumbs"><a href="/">Directory</a> / About</div>
<h1>About {BRAND}</h1>
<p>{BRAND} is a directory of tools for writers growing a newsletter on Substack, whether you want more free subscribers, more paid conversions, or simply less busywork.</p>
<h2>How we pick and check tools</h2>
<ul><li>Every tool listed was checked on the vendor's own website on {e(data['generated'])}: the site loads, the product exists, and it's usable today.</li>
<li>Pricing comes from the official pricing page where it's readable. When a page couldn't be read directly, we say where the figure came from.</li>
<li>Verdicts are short and honest, including caveats such as browser extensions that act in your logged-in Substack session.</li>
<li>We don't list tools we couldn't verify, and we remove tools that shut down or stop accepting customers.</li></ul>
<h2>How {BRAND} makes money</h2>
<p>Clearly labeled sponsored placements (featured listings and newsletter sponsor slots), paid fast-track review for submissions, and affiliate links for some tools. None of these change a tool's verdict. Tools with a verified affiliate program are noted on their page.</p>
<h2>Not affiliated with Substack</h2><p>{BRAND} is independent and not affiliated with, sponsored by, or endorsed by Substack Inc. "Substack" is a trademark of its owner and is used here only to describe compatibility.</p>
<h2>Contact</h2><p>Corrections, submissions and sponsorships: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p></div>{SIGNUP}"""
    write("/about/", layout("/about/", f"About {BRAND}: how we verify tools for Substack writers",
        "How StackKit verifies tools, makes money, and stays independent. Not affiliated with Substack Inc.", body, current="/about/"), "0.5")

# ---------------- Guide ----------------
def L(slug):
    t = BY[slug]; return f'<a href="/tools/{slug}/">{e(t["name"])}</a>'
def P(slug): return e(BY[slug]["pricing"])
def guide():
    sections = [
      ("1. Start with the free basics", "Before paying for anything, set up the free foundations. They cover most of what a new publication needs.",
       ["google-analytics", "canva", "grammarly", "hemingway-editor", "notion", "unsplash"]),
      ("2. Get subscribers from other newsletters", "Recommendations are one of the most reliable growth channels for newsletters. If you also have a personal site, make the signup form there worth using.",
       ["sparkloop", "supascribe"]),
      ("3. Win on Substack Notes", "Notes is where Substack readers discover new writers. Substack now schedules single Notes natively; the tools below add batch queues, cross-posting and, most importantly, attribution: which Notes actually bring subscribers.",
       ["buffer", "writestack", "narrareach", "stacksweller", "subshack"]),
      ("4. Cross-post where your readers already are", "Pick one or two networks where your audience lives and repurpose each post there, rather than spreading yourself across all of them.",
       ["typefully", "taplio", "hypefury", "repurpose-io"]),
      ("5. Measure what converts to paid", "Opens and likes aren't revenue. Once you have paid subscribers, track which posts drive upgrades and where churn comes from.",
       ["byline-os", "subshack", "bitly", "plausible"]),
      ("6. Add audio and video", "Substack supports podcasts and video. Audio versions and short clips can reach people who won't read a 2,000-word post.",
       ["descript", "elevenlabs", "riverside", "opusclip", "adobe-podcast"]),
      ("7. Earn beyond subscriptions", "Sponsorships, digital products and tips can out-earn paid subscriptions for some niches, and they don't put your writing behind a paywall.",
       ["hecto", "swapstack", "paved", "gumroad", "ko-fi"]),
    ]
    assert {x for _,_,sl in sections for x in sl} == GUIDE_TOOLS, 'GUIDE_TOOLS out of sync'
    secs = ""
    for h, intro, slugs in sections:
        items = "".join(f"<li><strong>{L(s)}</strong>: {e(BY[s]['verdict'])} <em>Pricing: {P(s)}</em></li>" for s in slugs)
        secs += f"<h2>{h}</h2><p>{intro}</p><ul>{items}</ul>"
    stacks = [
      ("The $0 stack", "Brand-new publication, under ~500 subscribers.", ["google-analytics", "canva", "grammarly", "notion", "buffer", "subshack", "sparkloop"]),
      ("The ~$25/month stack", "Posting Notes daily and starting to convert paid readers.", ["writestack", "canva", "hemingway-editor", "google-analytics", "sparkloop"]),
      ("The paid-newsletter operator stack", "Hundreds of paid subscribers; growth and churn are now business metrics.", ["byline-os", "writestack", "typefully", "descript", "hecto", "notion"]),
    ]
    st = "".join(f"<h3>{n}</h3><p>{d}</p><ul>" + "".join(f"<li>{L(s)}: {P(s)}</li>" for s in sl) + "</ul>" for n, d, sl in stacks)
    allslugs = []
    for _, _, sl in sections:
        for s in sl:
            if s not in allslugs: allslugs.append(s)
    rows = "".join(f'<tr><td>{L(s)}</td><td>{e(CAT[BY[s]["category"]]["name"])}</td><td>{e(BY[s]["best_for"])}</td><td>{P(s)}</td></tr>' for s in allslugs)
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / Guides</div>
<h1>Best tools to grow your Substack in 2026</h1>
<p class="small">Updated {e(data['generated'])} · Every tool and price below was checked on the vendor's site · {len(allslugs)} tools</p>
<p>Substack gives you a lot out of the box: hosting, email, payments, recommendations and Notes. So the question isn't "what do I need?" but "what fills the gaps that limit my growth?" This guide walks through those gaps in the order most writers hit them, recommends specific tools for each, and is upfront about the trade-offs.</p>
<p><strong>The short version:</strong> start free (Google Analytics, Canva, Grammarly, Notion). Join a recommendation network early ({L('sparkloop')}). Treat Notes as your main discovery channel and measure which Notes convert ({L('subshack')} is free, {L('writestack')} is the full suite). Add revenue analytics ({L('byline-os')}) once paid subscribers matter.</p>
{secs}
<h2>Starter stacks by budget</h2>{st}
<h2>A word on browser extensions and your Substack login</h2>
<p>Substack has no official public API for most of this, so many Substack-specific tools work through a browser extension or by holding your logged-in Substack session. That's how tools like WriteStack, StackSweller, Subshack and Byline OS's live sync function. It's common and often fine, but read each tool's privacy page, prefer read-only or CSV modes when they exist, and be wary of anything that auto-follows, auto-likes or messages people for you.</p>
</div>
<h2>All tools in this guide</h2><div class="table-wrap"><table class="cmp"><thead><tr><th>Tool</th><th>Category</th><th>Best for</th><th>Pricing</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Prices change; confirm on each vendor's site. Some vendors run affiliate programs; that never affects inclusion or verdicts. See <a href="/about/">disclosures</a>.</p>
<p><a class="btn" href="/">Browse all {len(TOOLS)} tools →</a></p></div>{SIGNUP}"""
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": "Best tools to grow your Substack in 2026", "dateModified": data["generated"],
          "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE_URL + f"/guides/{GUIDE_SLUG}/"}
    write(f"/guides/{GUIDE_SLUG}/", layout(f"/guides/{GUIDE_SLUG}/", f"Best tools to grow your Substack in 2026 (verified picks) | {BRAND}",
        "The tools that actually help Substack writers grow free and paid subscribers in 2026: recommendations, Notes, analytics, cross-posting, audio and sponsorships, with real pricing.", body, ld, current=f"/guides/{GUIDE_SLUG}/"), "0.9")

# ---------------- Extras ----------------
def extras():
    write("/404.html", layout("/404.html", f"Page not found | {BRAND}", "Page not found.",
        '<div class="wrap page"><h1>Page not found</h1><p>That page doesn\'t exist. <a href="/">Back to the directory</a>.</p></div>'))
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in pages:
        sm.append(f"  <url><loc>{SITE_URL}{p}</loc><lastmod>{data['generated']}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    lines = [f"# {BRAND}", "", f"> {BRAND} is an independent, hand-checked directory of {len(TOOLS)} tools for writers growing a newsletter on Substack (free and paid subscribers). Each tool has its real URL, pricing checked on {data['generated']}, who it's best for, and a short honest verdict. Not affiliated with Substack Inc.", "",
             "Monetization: labeled sponsored placements, paid fast-track review, and affiliate links for some tools. Verdicts are not for sale.", "",
             "## Key pages", f"- [Directory]({SITE_URL}/): searchable list of all tools", f"- [Best tools to grow your Substack in 2026]({SITE_URL}/guides/{GUIDE_SLUG}/): long-form guide with starter stacks by budget",
             f"- [About & disclosures]({SITE_URL}/about/)", f"- [Feature your tool]({SITE_URL}/feature/): sponsorship options", f"- [Raw data (JSON)]({SITE_URL}/data/tools.json)", ""]
    for c in CATS:
        lines.append(f"## {c['name']}")
        lines.append(c["desc"])
        for t in BYCAT[c["slug"]]:
            lines.append(f"- [{t['name']}]({SITE_URL}/tools/{t['slug']}/) ({t['url']}): {t['best_for']}. Pricing: {t['pricing']} Verdict: {t['verdict']}")
        lines.append("")
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(lines))
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)
    shutil.copy(os.path.join(ROOT, "data", "tools.json"), os.path.join(OUT, "data", "tools.json"))

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "src", "assets"), os.path.join(OUT, "assets"))
    open(os.path.join(OUT, "assets", "favicon.svg"), "w").write(LOGO.replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))
    home()
    for c in CATS: category(c)
    for t in TOOLS: tool(t)
    feature(); about(); guide(); extras()
    open(os.path.join(OUT, "CNAME"), "w").write(SITE_URL.split("://", 1)[1] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"Built {len(pages)} pages into {OUT} (SITE_URL={SITE_URL})")

if __name__ == "__main__": main()
