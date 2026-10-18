import re, urllib.request, urllib.parse, collections, sys
BASE="http://localhost:8765"
seen=set(); queue=["/"]; bad=[]; ext=set(); n=0
extra=["/sitemap.xml","/robots.txt","/llms.txt","/data/tools.json","/assets/style.css","/assets/app.js","/assets/favicon.svg"]
while queue:
    p=queue.pop()
    if p in seen: continue
    seen.add(p)
    try:
        r=urllib.request.urlopen(BASE+p); body=r.read().decode(); n+=1
    except Exception as ex:
        bad.append((p,str(ex))); continue
    if not p.endswith("/") and not p.endswith(".html"): continue
    if "<title>" not in body or 'name="description"' not in body: bad.append((p,"missing title/description"))
    for h in re.findall(r'(?:href|src)="([^"]+)"',body):
        if h.startswith("#") or h.startswith("mailto:"): continue
        if h.startswith("http"):
            if "stackkit.ink" not in h: ext.add(h)
            continue
        u=urllib.parse.urljoin(p,h).split("#")[0].split("?")[0]
        if u not in seen: queue.append(u)
for p in extra:
    try: urllib.request.urlopen(BASE+p)
    except Exception as ex: bad.append((p,str(ex)))
print("internal pages fetched:",n,"broken:",bad)
# sitemap urls all resolve locally
sm=urllib.request.urlopen(BASE+"/sitemap.xml").read().decode()
locs=[l.replace("https://stackkit.ink","") for l in re.findall(r"<loc>(.*?)</loc>",sm)]
miss=[l for l in locs if l not in seen]
print("sitemap urls:",len(locs),"not reached by crawl:",miss)
open("/tmp/ext.txt","w").write("\n".join(sorted(ext)))
print("external links:",len(ext))
