# Source of truth for data/tools.json. Every entry was checked on 2026-10-18 (entries with verified=V2 re-checked or added 2026-10-21; V3 = 2026-10-22; V4 = 2026-10-23; V5 = 2026-10-24; V6 = 2026-10-25; V7 = 2026-10-26; V8 = 2026-10-27; V9 = 2026-10-28; V10 = 2026-10-29; V11 = 2026-10-30; V12 = 2026-10-31):
# URL loaded (HTTP 200 or bot-check page on the real domain), pricing from the
# official pricing page unless "pricing_source" says otherwise.
import json, re
V = "2026-10-18"
V2 = "2026-10-21"  # entries added or re-checked in the 2026-10-21 daily ops pass
V3 = "2026-10-22"  # entries added or re-checked in the 2026-10-22 daily ops pass
V4 = "2026-10-23"  # entries added or re-checked in the 2026-10-23 daily ops pass
V5 = "2026-10-24"  # entries added or re-checked in the 2026-10-24 daily ops pass
V6 = "2026-10-25"  # entries re-checked in the 2026-10-25 daily ops pass
V7 = "2026-10-26"  # entries re-checked in the 2026-10-26 daily ops pass
V8 = "2026-10-27"  # entries added or re-checked in the 2026-10-27 daily ops pass
V9 = "2026-10-28"  # entries added or re-checked in the 2026-10-28 daily ops pass
V10 = "2026-10-29"  # entries re-checked in the 2026-10-29 daily ops pass
V11 = "2026-10-30"  # entries added or re-checked in the 2026-10-30 daily ops pass
V12 = "2026-10-31"  # entries added or re-checked in the 2026-10-31 daily ops pass
UPDATED = V12
def slug(n): return re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
T = []
def add(name,url,cat,pricing,best_for,verdict,aff=None,aff_url=None,substack_specific=False,pricing_source="official site",notes=None,free_plan=None,verified=None):
    T.append(dict(slug=slug(name),name=name,url=url,category=cat,pricing=pricing,free_plan=free_plan,
      pricing_source=pricing_source,best_for=best_for,verdict=verdict,
      affiliate_program=("yes" if aff else "not verified"),affiliate_url=aff_url,
      substack_specific=substack_specific,verified_on=verified or V,notes=notes))

# ---------- Growth & Notes ----------
add("SparkLoop","https://sparkloop.app/","growth",
 "Free to join the Partner Network and Upscribe recommendation widget (SparkLoop takes a share of paid-recommendation earnings). Paying other newsletters to recommend you is a separate paid program.",
 "Getting paid recommendations and buying cross-newsletter referrals",
 "The best-known newsletter recommendation network. Earning from recommendations is low-risk; paying for referrals only makes sense once you know what a subscriber is worth to you.",
 free_plan=True, pricing_source="official site (sparkloop.app/pricing: Paid Recommendations, Partner Programs and Free Recommendations all listed as included free; referral programs are a $2,000/yr add-on) + SparkLoop help center", verified=V5)
add("Supascribe","https://supascribe.com/","growth",
 "Free (2 basic embeds, first 1,000 views, first 100 new subscribers); Starter $9/mo, Growth $20/mo, Pro $249/mo (all billed yearly); paid plans add $2 per extra 10,000 views or 100 subscribers.",
 "Writers with their own website who want on-brand Substack signup forms, popups and landing pages",
 "Fills a real gap: Substack's native embed is fixed-width and unstyled. Independent (not affiliated with Substack), and only useful if you drive traffic from a site you control.",
 substack_specific=True, free_plan=True, verified=V5, pricing_source="official site (supascribe.com pricing section; yearly-billed prices shown)")
add("WriteStack","https://www.writestack.io/","growth",
 "Hobbyist $23.99/mo; Standard $32.99/mo; Enterprise $99.99/mo; every plan has a 7-day free trial. (Yearly prices aren't shown on its homepage.)",
 "Writers who live on Substack Notes and want batch scheduling, research and Notes-to-subscriber analytics",
 "The most complete Substack-only Notes suite: batch scheduling, voice-matched Note drafts, analytics on which Notes bring subscribers, a filtered notification inbox, and now an in-app writing coach (Quill) plus an MCP server so Claude or ChatGPT can draft and queue Notes. Pricey for a beginner, and publishing still runs through its browser extension acting in your logged-in session (you click Sync to send scheduled Notes).",
 aff=True, aff_url="https://www.writestack.io/affiliates", substack_specific=True, free_plan=False, verified=V11,
 pricing_source="official site (writestack.io homepage pricing section and writestack.io/llms.txt)",
 notes="Independent; not affiliated with Substack. Also offers free standalone tools (posting-time heatmap, Notes roast, Note generator).")
add("Narrareach","https://www.narrareach.com/","growth",
 "Audience Builder $19.99/mo ($199/yr); Revenue Writer $39/mo ($390/yr); Full Agentic Mode $89/mo ($890/yr). Every plan starts with a 7-day free trial, no card required.",
 "Turning long-form posts into Notes and cross-posting to LinkedIn, X, Bluesky, Threads and Medium",
 "Good if distribution beyond Substack is your bottleneck. Hands Notes to Substack's native scheduler rather than posting from a stored session.",
 substack_specific=True, free_plan=False, verified=V3)
add("StackBuddy","https://stackbuddy.io/","growth",
 "Free plan (scheduling and creator network free forever); Pro $12.50/mo billed yearly or $15/mo month-to-month. Every account starts with 14 days of Pro, no card.",
 "Batch-scheduling Notes into posting slots and finding other writers to cross-promote with",
 "A Notes scheduler with a free plan that keeps scheduling, and its Chrome extension hands each Note to Substack's own scheduler, so Notes publish from Substack's servers with your computer off. Pro adds voice-matching AI drafts, analytics and LinkedIn cross-posting. Small one-developer tool; the extension acts in your logged-in Substack session and syncs your existing Notes to StackBuddy's dashboard, so read its privacy page first.",
 substack_specific=True, free_plan=True, verified=V9,
 pricing_source="official site (stackbuddy.io FAQ and pricing section) + stackbuddy.io/terms and /privacy; Chrome Web Store listing (offered by Patrick God)",
 notes="Independent, not affiliated with Substack. Chrome needs to be open only while a Note syncs to Substack, not at publish time.")
add("StackSweller","https://stacksweller.com/","growth",
 "Pro $39/mo, or $25/mo billed yearly ($250/yr).",
 "A simple cloud queue for batch-scheduling Substack Notes",
 "Does one job (a Notes queue that runs with your laptop closed). Be aware it works by holding your Substack session, and Substack now schedules single Notes natively.",
 substack_specific=True, free_plan=False, verified=V3)

# ---------- Analytics ----------
add("SubflowAI","https://www.genaiunplugged.com/subflowai/","growth",
 "Pro Monthly $9.97/mo; Pro 5-Year $69.97 one-time; Premium $99.97 (5 years, includes Connect to Claude/ChatGPT). Connect is a $30 one-time add-on on Pro plans. 5-day free trial, no card; 14-day money-back guarantee.",
 "Batch-scheduling a week or month of Notes cheaply, with a visual calendar and AI Note drafts from your articles",
 "The cheapest serious batch Notes scheduler we've found (the 5-year plan works out to about $1.17/mo), and Notes are queued on Substack's own scheduler so they publish with your laptop closed. It's a one-person product that works through your logged-in Substack session (the Claude/ChatGPT Connect feature uses Substack's unofficial API), and the AI-in-your-voice features are optional: edit anything it drafts before it goes out.",
 substack_specific=True, free_plan=False, verified=V5,
 pricing_source="official site (genaiunplugged.com/subflowai pricing section and FAQ); Chrome Web Store listing v3.11.0, updated Oct 2, 2026, 5.0 from 10 ratings",
 notes="Made by Dheeraj Sharma (GenAI Unplugged); independent, not affiliated with Substack.")
add("Byline OS","https://bylineos.com/","analytics",
 "Starter free (CSV import, 30-day retention); Growth $19/mo; Scale $49/mo. 14-day trial. Currently in private beta.",
 "Paid-newsletter writers who want MRR, churn, cohort and revenue-per-post analytics",
 "Promising revenue-first analytics built specifically for Substack. It is a beta product; live sync uses your Substack session cookie and undocumented internal APIs, so the CSV-upload mode is the safer start.",
 substack_specific=True, free_plan=True, verified=V5)
add("Google Analytics","https://analytics.google.com/","analytics",
 "Free.",
 "Seeing where your Substack traffic comes from (Substack lets you add a GA measurement ID)",
 "Free and worth connecting on day one for referral sources. Overkill for most writers beyond the acquisition reports.",
 free_plan=True, verified=V10)
add("Google Search Console","https://search.google.com/search-console/about","analytics",
 "Free.",
 "Seeing which Google searches bring readers to your Substack and whether your posts are indexed",
 "The only way to see the actual search queries that find your posts. Free, but Substack says Search Console verification becomes available as your publication grows, so newer publications may not see the option in settings yet.",
 free_plan=True, verified=V4, pricing_source="official site (Google Search Console Help: \"a free service offered by Google\")",
 notes="Substack's SEO help article (updated Sep 14, 2026) says sitemaps and Google Search Console verification unlock as a publication grows.")
add("Subshack","https://www.subshack.pro/","analytics",
 "Free (Subshack 1.0), including a no-signup public profile audit.",
 "Finding out which Notes and posts actually bring subscribers, and auditing your profile",
 "A free, measurement-first browser extension (Chrome and Firefox) that never posts Notes or articles for you. Optional welcome-message sending is off unless you turn it on, with daily limits. New and small, so expect rough edges.",
 substack_specific=True, free_plan=True, verified=V5)
add("Bitly","https://bitly.com/","analytics",
 "Free (with ads; 5 links and 2 QR Codes a month); Core $10/mo (annual only, $120/yr); Growth $29/mo ($348/yr); Premium $199/mo ($2,388/yr).",
 "Tracking clicks on links you share to social, podcasts and print",
 "Handy for knowing which channel sends readers. The free tier is limited; many writers can get by with UTM tags plus Google Analytics.",
 free_plan=True, verified=V9, pricing_source="official site (bitly.com/pages/pricing)")
add("Plausible","https://plausible.io/","analytics",
 "From $9/mo (Starter, 10k monthly pageviews); Growth $14/mo; Business $19/mo. Free trial.",
 "Privacy-friendly analytics for your own website or landing page",
 "Excellent lightweight analytics, but you can't install it on a substack.com publication. Use it on a personal site that funnels readers to Substack.",
 free_plan=False, verified=V9, pricing_source="official site (plausible.io pricing section)")

add("StackStats","https://stackstats.app/","analytics",
 "1-year license $39 (renew updates for $29/yr; the app keeps working if you don't); Lifetime $79 early-adopter price (listed down from $129). One-time payments, no subscription; 14-day refund.",
 "Writers who want churn risk, cohort retention, superfan and growth-source analysis from their own Substack exports",
 "Digs far deeper than Substack's dashboard and keeps your subscriber data on your own computer (Mac or Windows). It's a new one-developer app: installers aren't code-signed yet, and the optional Auto-Sync (beta) logs in to Substack for you, so manual CSV exports are the cautious route.",
 substack_specific=True, free_plan=False, verified=V11, pricing_source="official site (stackstats.app pricing section and FAQ)",
 notes="Independent; not affiliated with Substack. A read-only live demo is on its site.")
add("Orbit","https://seeyourorbit.com/","analytics",
 "$12/mo or $120/yr, included with a paid subscription to creator Rebecca Spitzer's Substack (What's Working Right Now on Substack). No free plan or trial.",
 "Writers growing through relationships who want to remember who they've talked to across Notes, comments and DMs",
 "A thoughtful relationship tracker for Substack that never writes or replies for you, and you can ask it questions from Claude or ChatGPT. It works through a Chrome extension running alongside your logged-in Substack session (DMs off by default), and there's no way to try it before paying.",
 substack_specific=True, free_plan=False, verified=V11, pricing_source="official site (seeyourorbit.com FAQ, \"As of October 2026\")",
 notes="Independent; not affiliated with Substack. Access comes via a paid subscription to the creator's Substack.")

add("Substack Insights","https://substackinsights.com/","analytics",
 "Free for publications under 1,000 subscribers; $9.99 one-time above that. The pricing card lists Notes analytics and conversion stats under the paid tier.",
 "Writers who want a cheap, private look at their best posts, best publishing times and Notes engagement",
 "A simple, inexpensive Chrome side panel that ranks your posts and Notes and exports a CSV with ready-made AI prompts. Analysis runs in your browser using your logged-in Substack session; it only reads, never posts. Small and new (v1.0 on the Chrome Web Store).",
 substack_specific=True, free_plan=True, verified=V12, pricing_source="official site (substackinsights.com pricing section and FAQ)",
 notes="Independent; its Chrome Web Store listing says it is not affiliated with Substack.")
add("PlotStack","https://chromewebstore.google.com/detail/plotstack-%E2%80%94-newsletter-an/odcgiilenioilmnaimbcaamocnmhhaib","analytics",
 "Free. No paid tier or in-app purchases listed; its maker says his newsletter tools are free and will stay free.",
 "Writers who want Substack's stats, growth, posts and Notes numbers in one local dashboard, with CSV and PNG exports",
 "A free, read-only Chrome dashboard that pulls together what Substack spreads across several screens (subscribers, open rate, acquisition sources, cohort retention, per-post and per-Note stats, attributed signups) and points out what stands out compared with your own past numbers. No account and no server: data stays in your browser, and paid and revenue figures are hidden by default. It reads Substack's undocumented internal endpoints through your logged-in session and syncs once a day in the background, it doesn't support custom domains yet, and it's a very new one-person project with no Chrome Web Store ratings yet, so expect breakage when Substack changes things.",
 substack_specific=True, free_plan=True, verified=V12,
 pricing_source="Chrome Web Store listing (v1.6.0, updated Oct 24, 2026; no in-app purchases listed) + privacy policy (sotoplatero.github.io/plotstack/privacy/) + public source at github.com/sotoplatero/plotstack + maker's Sept 18, 2026 post (sotoplatero.substack.com/p/sistema-operativo: 'Las cuatro son gratis y van a seguir siéndolo')",
 notes="Made by Damian Soto (Objeto Brillante); independent, not affiliated with Substack. Interface in English or Spanish; *.substack.com publications only. Source is public on GitHub (no license file at time of checking).")
add("NoteStack","https://notestack.stacktreelabs.com/","analytics",
 "Starter $8/mo or $60/yr (capped scheduler: 7 new Notes/mo); Pro $12/mo or $99/yr (no caps, adds AI Ghostwriter and Post Coach). 7-day free trial.",
 "Notes-first writers who want subscriber-conversion rankings, best-time heatmaps and a scheduler in one extension",
 "A lot of Notes analytics for the price, with data kept in your browser. Be aware the scheduler auto-publishes through your logged-in Substack session, and the AI features send your Notes text to its server and Anthropic. Skip the Ghostwriter if your voice is the product.",
 substack_specific=True, free_plan=False, verified=V3, pricing_source="official site (notestack.stacktreelabs.com FAQ and /pricing)",
 notes="Made by StackTree Labs; independent, not affiliated with Substack.")
add("NotesIQ","https://www.notesiq.app/","analytics",
 "$4.99 one-time for lifetime access (analytics, scheduler, competitor lookups); 7-day money-back guarantee.",
 "Writers who want a cheap, one-time-payment Notes dashboard with a best-time heatmap and a weekly queue",
 "The cheapest Notes analytics extension we've found, and it keeps data in your browser with no account. Very new (v1.0.3, launched Sept 2026, no Chrome Web Store ratings yet) from a solo developer, and its price has already changed since launch, so treat it as an inexpensive experiment. Scheduling publishes through Substack's own composer in your logged-in session.",
 substack_specific=True, free_plan=False, verified=V4, pricing_source="official site (notesiq.app pricing section and FAQ; matches its Chrome Web Store listing)",
 notes="Independent; its site says it is not affiliated with Substack. Launch listings in Sept 2026 quoted $19 lifetime plus a $9/mo AI add-on; the current site and store listing say $4.99 lifetime.")

# ---------- Cross-posting & social ----------
add("Typefully","https://typefully.com/","social",
 "Free (10 posts/mo, 1 social set; Substack Notes included); Creator $99/yr (annual billing only); Business $18 per social set/mo billed yearly.",
 "X-first writers who also want to post to LinkedIn, Threads, Bluesky and Substack Notes",
 "A polished writing-first scheduler that now publishes and schedules Substack Notes on every plan, including free. It handles Notes only (no long-form posts, no video in Notes), and its paid analytics are for X, so it suits writers who start on X or LinkedIn more than Notes-first writers.",
 pricing_source="official site (typefully.com/pricing, rendered page; Substack support per typefully.com/changelog/substack-notes and Typefully Help Center \"Publish and Cross-Post to Substack Notes\")", free_plan=True, verified=V7)
add("Buffer","https://buffer.com/","social",
 "Free (up to 3 channels, 10 scheduled posts per channel at a time); Essentials $5/channel/mo billed yearly ($6 monthly); Team $10/channel/mo billed yearly ($12 monthly).",
 "Scheduling Notes alongside every other social channel from one calendar",
 "Reliable and affordable, and its free plan includes Substack Notes scheduling. The best default if you post to several networks.",
 free_plan=True, verified=V7, pricing_source="official site (buffer.com/pricing and its machine-readable buffer.com/pricing.md; Substack Notes support per buffer.com/substack)")
add("Hypefury","https://hypefury.com/","social",
 "Flexible $6/mo for 1 channel (plus $6/mo per extra channel); Full $19/mo for all channels; 7-day free trial, no card. No free plan.",
 "Scheduling and cross-posting to Bluesky, Threads, LinkedIn, Instagram and TikTok",
 "Hypefury no longer supports X, so it's now a scheduler for Bluesky, Threads, LinkedIn, Instagram and TikTok, with auto first comments (Autoplugs) and an engagement builder. Substack Notes isn't on its channel list, so pair it with Substack's own scheduler.",
 aff=True, aff_url="https://hypefury.com/affiliate", free_plan=False, verified=V9, pricing_source="official site (hypefury.com/pricing, including FAQ: \"Hypefury no longer supports X\")")
add("Taplio","https://taplio.com/","social",
 "Starter $39/mo; Growth $69/mo; Pro $199/mo (billed monthly). Its plan-comparison table also lists lower rates ($32, $49 and $149/mo) without stating the billing term. 7-day free trial with full Pro access; 30-day money-back guarantee.",
 "Writers growing a professional audience on LinkedIn",
 "Effective for LinkedIn but expensive. Only worth it if LinkedIn is a primary acquisition channel. Its automation features (auto-DMs, bulk connection requests) are best left off if you want your LinkedIn presence to sound like you.",
 aff=True, aff_url="https://taplio.com/affiliates", free_plan=False, verified=V12, pricing_source="official site (taplio.com/pricing)")
add("Repurpose.io","https://repurpose.io/","social",
 "Starter $35/mo; Pro $79/mo ($790/yr); Agency $179/mo ($1,790/yr); free trial of 14 days or 10 published videos, whichever comes first.",
 "Automatically distributing video and podcast clips across platforms",
 "Saves real time if you make video or audio. Pure text writers don't need it.",
 aff=True, aff_url="https://repurpose.io/become-an-affiliate/", free_plan=False, verified=V5)

# ---------- Design ----------
add("Canva","https://www.canva.com/","design",
 "Free; Pro US$144/yr for one person (before tax).",
 "Header images, social graphics, Notes images and simple brand kits",
 "The default design tool for newsletter writers. The free plan covers most needs.",
 aff=True, aff_url="https://www.canva.com/affiliates/", free_plan=True, verified=V10,
 notes="Affiliate: Canva Help Center page 'Become a Canva affiliate through the Canvassador Program'.")
add("Figma","https://www.figma.com/","design",
 "Free Starter; Professional full seat $16/mo.",
 "Custom visual systems, templates and detailed design work",
 "More power than most writers need. Pick it if you already know it or want pixel-level control.",
 free_plan=True, verified=V6)
add("Kittl","https://www.kittl.com/","design",
 "Free plan (personal use only); Pro $15/mo or $144/yr; Expert $35/mo or $312/yr; Max $65/mo or $576/yr (USD).",
 "Typography-heavy graphics and AI-assisted illustrations",
 "A stylish Canva alternative with great type tools. The free plan is for personal use only; Pro adds a commercial license.",
 free_plan=True, verified=V7, pricing_source="official site (kittl.com/pricing plan data and FAQ)")
add("Unsplash","https://unsplash.com/","design",
 "Free to use under the Unsplash License (commercial use allowed, no attribution required). Optional paid Unsplash+ subscription for exclusive images under a separate license.",
 "Free, high-quality photos for post headers",
 "The go-to free photo library. Popular images show up everywhere, so crop or edit them to stand out. Credit the photographer anyway: it's appreciated, though not required.",
 free_plan=True, verified=V11, pricing_source="official site (unsplash.com/license and unsplash.com/plus/license)",
 notes="The license doesn't allow selling images without significant modification. Unsplash+ images have their own license (for example, no use in AI or machine-learning training).")
add("Excalidraw","https://excalidraw.com/","design",
 "Free and open source (MIT license); optional Excalidraw+ at $6/user/mo with a 14-day free trial.",
 "Quick hand-drawn-style diagrams and process sketches to drop into posts",
 "The fastest way to turn a paragraph of explanation into a simple diagram: draw boxes and arrows, export a PNG, and add it to your post like any image. The free web app saves drawings in your browser's storage, which can be cleared, so save a file of anything you'll want to edit later.",
 free_plan=True, verified=V8, pricing_source="official site (plus.excalidraw.com/pricing) + github.com/excalidraw/excalidraw README",
 notes="Exports PNG, SVG and an open .excalidraw file. For Substack, add the exported PNG to your post as an image.")
add("remove.bg","https://www.remove.bg/","design",
 "Free preview-size downloads (up to 0.25 megapixels) on remove.bg; full-resolution cutouts cost 1 credit each. Subscriptions from $9/mo for 40 credits ($8.10/mo billed yearly), or pay-as-you-go credits.",
 "One-click background removal for headshots and product images",
 "Fast and accurate, and the free preview size is often enough for a small inline image. Now a Canva brand, and Canva Pro includes a background remover, so you may not need both.",
 free_plan=True, verified=V7, pricing_source="official site (remove.bg/pricing plan data and FAQ)")

# ---------- Editing ----------
add("Grammarly","https://www.grammarly.com/","editing",
 "Free (includes 100 AI prompts/mo); Pro from $12/mo with a free trial (2,000 AI prompts/mo, full-sentence rewrites, tone adjustments, plagiarism and AI-text detection).",
 "Catching typos and clarity issues everywhere you write, including the Substack editor",
 "The free browser extension is worth installing. Pro's rewrites can flatten your voice, so accept suggestions selectively.",
 aff=True, aff_url="https://www.grammarly.com/affiliates", free_plan=True, verified=V9, pricing_source="official site (grammarly.com/plans) + grammarly.com/browser")
add("Hemingway Editor","https://hemingwayapp.com/","editing",
 "Free web editor; Editor Plus (AI rewrites) Individual 5K $8.33/mo billed annually ($100/yr) or Individual 10K $12.50/mo billed annually ($150/yr); desktop app $19.99 one-time (no AI features).",
 "Making dense posts easier to read",
 "The free web version does the core job (highlighting long and passive sentences). Most writers don't need Plus.",
 free_plan=True, verified=V4, pricing_source="official site (hemingwayapp.com/hemingway-editor-plus and /desktop; the old /pricing page now returns 404)")
add("ProWritingAid","https://prowritingaid.com/","editing",
 "Free (500 words at a time, 2 runs per report a day, 10 Rephrases a day); Premium $10/mo billed yearly ($120) or $30/mo monthly; Premium Pro $12/mo billed yearly ($144) or $36/mo monthly. Lifetime options and a 3-day money-back guarantee on yearly and lifetime plans.",
 "Deep style reports for long-form and fiction writers",
 "More thorough reports than Grammarly. Worth trying if you write long essays or serialized fiction.",
 aff=True, aff_url="https://prowritingaid.com/affiliates", free_plan=True, verified=V9, pricing_source="official site (prowritingaid.com/pricing) + prowritingaid.com/integrations")
add("LanguageTool","https://languagetool.org/","editing",
 "Free (up to 2,000 characters per text field); Premium $24.90/mo monthly, $49.90/quarter, $69.90/yr or $119.80 for 2 years.",
 "Multilingual writers and anyone who wants a Grammarly alternative",
 "Strong grammar checking across many languages, and much cheaper per year than monthly billing.",
 pricing_source="official site (languagetool.org/premium, rendered page, USD incl. VAT)", free_plan=True, verified=V7)
add("QuillBot","https://quillbot.com/","editing",
 "Free (paraphrase up to 125 words at a time, 2 modes); Premium $19.95 monthly, $39.95 every 3 months, or $99.95/yr ($8.33/mo). Prices may vary by region.",
 "Paraphrasing, summarizing and quick rewrites",
 "Useful for tightening a stubborn paragraph. Don't lean on it for whole posts, because readers subscribe for your voice.",
 pricing_source="official site (quillbot.com Premium page and QuillBot FAQ \"How much is QuillBot Premium?\") + QuillBot help center (prices vary by region)", free_plan=True, verified=V11)

# ---------- Planning, research & automation ----------
add("Notion","https://www.notion.com/","planning",
 "Free; Plus $10/seat/mo.",
 "Editorial calendars, idea banks and sponsor CRMs",
 "The most flexible planning hub for newsletter writers. The free plan covers solo use.",
 aff=True, aff_url="https://www.notion.com/affiliates", free_plan=True, verified=V12)
add("Trello","https://trello.com/","planning",
 "Free (up to 10 collaborators); Standard $5/user/mo billed annually.",
 "A simple kanban for drafts moving from idea to published",
 "Simpler than Notion if you only need a board. Free is plenty for one writer.",
 free_plan=True, verified=V7, pricing_source="official site (trello.com/pricing; Standard is $6/user/mo billed monthly)")
add("Obsidian","https://obsidian.md/","planning",
 "Free, no sign-up required; optional Sync $4/user/mo and Publish $8/site/mo (billed annually).",
 "Building a personal knowledge base of notes, quotes and ideas",
 "Great for writers who think in linked notes. Your files stay local in Markdown.",
 free_plan=True, verified=V12)
add("Persistwise","https://persistwise.com/","planning",
 "Keep plan: 30 days free (no card), then $40/yr.",
 "Keeping an independent backup of every post you publish on Substack",
 "Set-and-forget insurance for your archive: give it your Substack RSS feed and every new post gets a public Wayback Machine snapshot, a pinned IPFS copy and a private copy it stores. Brand new (launched Oct 26, 2026) and honest about its limits: each post is captured once, so later edits aren't saved, copies are HTML without images, and there's no export button yet. Keep using Substack's own export for a full backup.",
 free_plan=False, verified=V9,
 pricing_source="official site (persistwise.com) + maker's launch post (blog.ninepointlabs.com/2026/10/persistwise-launch/, Oct 26, 2026)",
 notes="Made by Nine Point Labs; independent, not affiliated with Substack. Wayback and IPFS copies are public, so only add feeds for writing you're happy to keep public.")
add("newsletterapi","https://www.newsletterapi.io/","planning",
 "Free (1 publication, recent posts from your public feed, limited API/MCP calls); Writer $9/mo (full archive from your export, MCP archive search, automatic backups); Pro $29/mo; Agency/Developer $79/mo. Priced per publication.",
 "Letting Claude or ChatGPT search your whole Substack archive, and backing up every post with images to your own storage",
 "A read-only API and MCP server built from your public RSS feed and the export you download yourself: no password, session cookie or browser extension. The Writer plan adds full-archive search for AI assistants and automatic Markdown/HTML backups (with images) to GitHub, Google Drive, Dropbox or S3. It's new and run by an unnamed independent team, and access is set up by email invite rather than instant signup, so try the free tier first.",
 substack_specific=True, free_plan=True, verified=V11,
 pricing_source="official site (newsletterapi.io and newsletterapi.io/pricing; \"You are never charged without confirming by email first\")",
 notes="Independent; not affiliated with Substack. Read-only by design: it can't publish posts or Notes.")
add("Readwise","https://readwise.io/","planning",
 "Full Readwise (Reader + Highlights) $9.99/mo billed yearly; Highlights only or Reader only $7.99/mo; Highlights Lite $5.59/mo billed yearly. Free for the first 30 days.",
 "Collecting highlights from books and articles to feed your writing",
 "A strong research engine for essayists and curators. Its Reader app is included with Full.",
 free_plan=False, verified=V4)
add("Google Trends","https://trends.google.com/","planning",
 "Free.",
 "Checking whether a topic is rising before you write about it",
 "A quick, free sanity check for timely topics and post titles.",
 free_plan=True, verified=V10)
add("Zapier","https://zapier.com/","planning",
 "Free (100 tasks/mo, two-step Zaps); Professional from $19.99/mo; Team from $69/mo.",
 "Automating busywork such as logging new posts to a spreadsheet or sending sponsor reminders",
 "Powerful glue between apps. Substack has no official public API, so automations usually start from its RSS feed or email.",
 free_plan=True, verified=V6, pricing_source="official site (zapier.com/pricing, USD)")

# ---------- AI writing & research ----------
add("ChatGPT","https://chatgpt.com/","ai",
 "Free; Go $8/mo (may include ads); Plus $20/mo; Pro from $100/mo. Monthly billing only for individual plans.",
 "Brainstorming angles, outlines, headlines and research summaries",
 "A versatile thinking partner. Use it for ideas and edits rather than finished prose your readers will recognize as generic.",
 pricing_source="chatgpt.com/pricing (plans and features; individual plans billed monthly) + OpenAI Help Center (Plus $20/mo) + OpenAI Go launch post (US $8/mo)", free_plan=True, verified=V10)
add("Claude","https://claude.ai/","ai",
 "Free; Pro $20/mo or $17/mo billed annually.",
 "Long-document feedback, structural edits and drafting help",
 "Particularly good at critiquing long drafts. The same caution about voice applies.",
 pricing_source="claude.com/pricing (Pro: $17/mo with annual billing, $200 billed up front; $20 billed monthly; Max from $100/mo)", free_plan=True, verified=V8)
add("Perplexity","https://www.perplexity.ai/","ai",
 "Free; Pro $20/mo, or $17/mo billed annually ($200/yr); Max $200/mo or $167/mo billed annually.",
 "Quick research with cited sources",
 "Faster than a search engine for background research. Always click through and verify the citations.",
 pricing_source="perplexity.ai/hub/pricing and /pro (annual prices) + Perplexity Help Center (monthly and yearly prices)", free_plan=True, verified=V10)
add("Sudowrite","https://sudowrite.com/","ai",
 "Hobby & Student $10/mo; Professional $22/mo; Max $44/mo (credit-based; yearly billing advertised as up to 50% off). Free trial, no credit card.",
 "Fiction writers publishing serialized stories",
 "Purpose-built for fiction, with tools for matching your style and keeping continuity across a series. Not the right tool for essays or news-style newsletters.",
 free_plan=False, verified=V8, pricing_source="official site (sudowrite.com/pricing; Max plan lists unused credits rolling over for 12 months)")

# ---------- Audio, podcast & video ----------
add("Descript","https://www.descript.com/","audio",
 "Free; Hobbyist $16/mo billed annually ($24 monthly); Creator $24/mo annually ($35 monthly); Business $50/mo annually ($65 monthly).",
 "Editing podcast and video by editing the transcript",
 "The easiest way for writers to edit audio and video. A natural fit for Substack podcasts.",
 aff=True, aff_url="https://www.descript.com/affiliate", free_plan=True, verified=V11, pricing_source="official site (descript.com/pricing)")
add("ElevenLabs","https://elevenlabs.io/","audio",
 "Free (10k credits/mo); Starter $6/mo; Creator $22/mo; higher tiers available.",
 "Producing audio versions of posts with natural-sounding AI voices",
 "Best-in-class AI voice. Tell listeners when a voice is synthetic.",
 aff=True, aff_url="https://elevenlabs.io/affiliates", free_plan=True, verified=V4)
add("Riverside","https://riverside.com/","audio",
 "Free (720p, Riverside watermark, 2 one-off hours of separate-track recording); Pro $24/mo billed annually ($288/yr) or $29 monthly; Grow $34/mo billed annually.",
 "Recording remote interviews in high quality",
 "Records each guest locally, so remote interviews sound studio-grade. Ideal for interview-driven newsletters.",
 aff=True, aff_url="https://riverside.com/affiliate-program", free_plan=True, verified=V4)
add("Audacity","https://www.audacityteam.org/","audio",
 "Free and open source.",
 "Recording and cleaning up voiceovers on a zero budget",
 "Dated interface but free and capable for simple narration edits.",
 free_plan=True, verified=V10)
add("Adobe Podcast","https://podcast.adobe.com/","audio",
 "Free (Enhance Speech: audio only, one file at a time, up to 30 minutes and 500 MB per file, 1 hour a day; Studio: 2 project downloads a day). Since Aug 30, 2026 Adobe no longer sells Podcast Premium on its own: new customers get the premium features through Adobe's Firefly Pro plan (see Adobe for the current price).",
 "Making laptop-mic recordings sound clean (Enhance Speech), for example a voiceover on a Substack post",
 "Enhance Speech is impressive on the free tier and enough for reading a weekly post aloud. Premium features (video, bulk uploads, adjustable strength, 4 hours a day) now come bundled in Adobe's broader Firefly Pro plan, so most writers should stick with the free plan.",
 pricing_source="official site (podcast.adobe.com/en/features) + Adobe Podcast Premium plan change FAQ (helpx.adobe.com, updated Jul 30, 2026)", free_plan=True, verified=V11)
add("OpusClip","https://www.opus.pro/","audio",
 "Free (60 credits/mo); Starter $15/mo (monthly only, 150 credits); Pro $29/mo or $14.50/mo billed annually.",
 "Turning long videos or podcast episodes into short social clips",
 "Fast way to get shorts from long recordings. Review the AI's clip choices before posting.",
 aff=True, aff_url="https://www.opus.pro/affiliate", free_plan=True, verified=V7, pricing_source="official site (opus.pro/pricing, US prices)")

# ---------- Embeds & interactive ----------
add("Tally","https://tally.so/","embeds",
 "Free (unlimited forms and submissions, within fair use); Pro $29/mo or $290/yr; Business $89/mo or $890/yr (USD; Tally shows euro prices to EU visitors).",
 "Reader surveys, sponsor inquiry forms and feedback forms",
 "The most generous free form builder. Substack posts can't host forms directly, so link to it from your post or About page.",
 free_plan=True, verified=V5, pricing_source="official site (tally.so/pricing; USD amounts from the page's plan data, the visible price depends on your location and monthly/yearly toggle)")
add("Datawrapper","https://www.datawrapper.de/","embeds",
 "Free (unlimited charts, maps and tables, with a \"Created with Datawrapper\" credit); Pro $21/user/mo excl. VAT (removes the credit); Business $39/user/mo excl. VAT.",
 "Clean, accurate charts, maps and tables for data-driven posts",
 "Newsroom-quality charts for free, and the one chart tool Substack embeds natively: paste the chart's share link into your draft. Interactive on the web and in the app; static in the email version.",
 free_plan=True, verified=V12, notes="Substack's help center documents native Datawrapper embeds (paste the share link into a draft).")
add("Flourish","https://flourish.studio/","embeds",
 "Free (public publishing with attribution); paid Presenter (via Canva Business) and Publisher/Enterprise plans on contract.",
 "Animated and interactive charts and scrollytelling",
 "More dramatic visuals than Datawrapper, but Substack doesn't list Flourish among its supported embeds and pasted embed code doesn't work, so plan on a static image linked to the interactive version.",
 free_plan=True, verified=V12)
add("Linktree","https://linktr.ee/","embeds",
 "Free (unlimited links, basic analytics); Starter $7/mo billed annually ($9 monthly); Pro $14/mo billed annually ($17 monthly); Premium $30/mo billed annually ($35 monthly). US prices; Linktree shows local prices by region.",
 "A link-in-bio page that points social followers to your Substack",
 "Fine for bios, but your Substack's /subscribe link can often serve as the link on its own. Only pay if you need the analytics.",
 free_plan=True, verified=V12, pricing_source="official site (linktr.ee/s/pricing, US prices)")

# ---------- Sponsorships & monetization ----------
add("Paved","https://www.paved.com/","monetization",
 "Free publisher account, no subscription. Flat-fee scheduled ads need at least 50k subscribers; pay-per-click native ads need at least 1M monthly impressions.",
 "Established newsletters looking for sponsor demand",
 "A large newsletter ad network (3,000+ newsletters, per Paved). Its stated minimums of 50k subscribers or 1M monthly impressions rule out most smaller Substacks; start with Hecto or Swapstack until you're there.",
 free_plan=True, verified=V6, pricing_source="official site (paved.com/publishers)")
add("Hecto","https://app.hecto.io/","monetization",
 "Free for newsletter creators (no monthly fee); Hecto takes 5% of successful sponsorship sales, plus Stripe's payment fees (as of its pricing page on 2026-10-25; that page was offline on 2026-10-31).",
 "Selling sponsorship slots with transparent, upfront prices",
 "A straightforward sponsorship marketplace: you publish ad packages with upfront prices and a checkout link. Listing is free, but demand varies by niche. Caution: on Oct 31, 2026 Hecto's main website (hecto.io) was offline with a hosting error, though the app itself still loaded. Check that it's back before relying on it.",
 free_plan=True, verified=V6, pricing_source="official site (hecto.io/pricing on 2026-10-25; fee shown as 5%, monthly fee shown as £0)",
 notes="2026-10-31: www.hecto.io and hecto.io/pricing returned HTTP 402 (Vercel DEPLOYMENT_DISABLED); app.hecto.io returned 200. Listing URL switched to the app until the main site returns. Re-check and remove the listing if the app goes down too.")
add("Swapstack","https://www.swapstack.co/","monetization",
 "Free for publishers (Swapstack takes 10% on invite-only campaigns from its managed service). Paid publisher plans (Professional $30/mo, Enterprise $200/mo) are listed as coming soon.",
 "Finding sponsors and affiliate deals for small and mid-sized newsletters",
 "One of the original newsletter sponsorship marketplaces, with flat-rate sponsorships, pay-per-click and affiliate deals in one place. Worth a free signup to see what matches your niche.",
 free_plan=True, verified=V6, pricing_source="official site (swapstack.co/pricing)")
add("Gumroad","https://gumroad.com/","monetization",
 "No monthly fee; 10% + $0.50 per transaction on direct sales (profile or direct links); 30% on sales through Gumroad Discover.",
 "Selling ebooks, templates and guides alongside your newsletter",
 "The simplest way to sell a digital product to your readers. Fees are high per sale but there's no fixed cost, and Gumroad acts as merchant of record, collecting and remitting sales tax for you.",
 free_plan=True, verified=V12, pricing_source="official site (gumroad.com/pricing)")
add("Ko-fi","https://ko-fi.com/","monetization",
 "Free to join, no monthly cost. Ko-fi Free: 0% on one-off tips and Goals, 5% on monthly tips, memberships, shop and commissions. Standard: 5% on everything, plus extras like supporter-only content and scheduled posts. PayPal/Stripe fees (usually around 3% + $0.30) apply on top. Ko-fi Gold (0% on everything for a fixed monthly fee) is still offered; price not listed on its page.",
 "One-off tips from readers who won't commit to a paid subscription",
 "A low-friction tip jar that complements paid subscriptions. One-off tips are fee-free on Ko-fi Free, but new accounts start in Standard mode (5% on tips), so switch it off in Settings > Payment if tips are all you need.",
 free_plan=True, verified=V9, pricing_source="official site (help.ko-fi.com: Does Ko-fi take a fee? + ko-fi.com/gold)")

CATS = [
 dict(slug="growth",name="Growth & Notes",desc="Referral networks, recommendation swaps, signup embeds and Substack Notes tools that bring in new subscribers."),
 dict(slug="analytics",name="Analytics",desc="See which posts, Notes and channels actually turn readers into free and paid subscribers."),
 dict(slug="social",name="Cross-posting & Social",desc="Schedule and repurpose your writing for X, LinkedIn, Threads, Bluesky and Notes."),
 dict(slug="design",name="Design",desc="Header images, social cards and brand visuals without hiring a designer."),
 dict(slug="editing",name="Editing & Proofreading",desc="Catch typos, tighten sentences and keep your voice."),
 dict(slug="planning",name="Planning, Research & Automation",desc="Editorial calendars, idea capture, research and automations."),
 dict(slug="ai",name="AI Writing & Research",desc="AI assistants for brainstorming, outlining, critique and research. Use with care."),
 dict(slug="audio",name="Audio, Podcast & Video",desc="Record, edit and repurpose audio and video for Substack podcasts and social clips."),
 dict(slug="embeds",name="Embeds & Interactive",desc="Forms, charts and link pages that add interactivity around your newsletter."),
 dict(slug="monetization",name="Sponsorships & Monetization",desc="Sponsor marketplaces, digital product sales and tips beyond paid subscriptions."),
]
slugs=[t['slug'] for t in T]; assert len(slugs)==len(set(slugs))
json.dump(dict(generated=UPDATED,categories=CATS,tools=T),open('data/tools.json','w'),indent=2,ensure_ascii=False)
from collections import Counter; print(len(T),Counter(t['category'] for t in T))
