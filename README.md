# StackKit (v1)

Static directory of tools for Substack writers. No dependencies beyond Python 3.

```
python3 data/make_tools.py          # regenerate data/tools.json (source of truth for tool data)
SITE_URL=https://stackkit.ink CONTACT_EMAIL=hello@stackkit.ink python3 build.py   # build into ./site
cd site && python3 -m http.server 8765         # preview at http://localhost:8765
python3 check_links.py              # crawl the local server for broken internal links
```

## Layout
- `data/make_tools.py` → `data/tools.json`: 56 verified tools (checked 2026-10-18; new and re-checked entries 2026-10-21, 2026-10-22 and 2026-10-23, see `verified_on`)
- `build.py`: generator (home, 10 category pages, tool pages, comparison pages from `COMPARISONS`, free-tools hub (/free-substack-tools/), feature, about, guide, 404, sitemap.xml, robots.txt, llms.txt)
- `src/assets/`: style.css, app.js (client-side search/filter)
- `site/`: build output; deploy this folder

## TODO before launch
- [x] `SITE_URL=https://stackkit.ink`, `CONTACT_EMAIL=hello@stackkit.ink` (env vars, defaults in build.py)
- [ ] Create Stripe Payment Links and fill `STRIPE` in build.py (buttons currently show a TODO alert)
- [ ] Confirm sponsor prices ($49 fast-track, $59/mo category, $129/mo homepage, $79/issue newsletter)
- [x] Substack embed (https://stackkit.substack.com/embed) in `SIGNUP` in build.py
- [ ] Apply to affiliate programs (tools marked `affiliate_program: "yes"`), then swap URLs for tracking links and use rel="sponsored"
- [x] Hosting: GitHub Pages via `.github/workflows/pages.yml` (runs build.py on push to main)
- [ ] Namecheap DNS for stackkit.ink, then enable "Enforce HTTPS" in Pages settings
- [ ] Re-verify pricing periodically (prices change often)
