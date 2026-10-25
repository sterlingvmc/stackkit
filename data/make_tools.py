# Source of truth for data/tools.json. Every entry was checked on 2026-10-18 (entries with verified=V2 re-checked or added 2026-10-21; V3 = 2026-10-22; V4 = 2026-10-23; V5 = 2026-10-24; V6 = 2026-10-25):
# URL loaded (HTTP 200 or bot-check page on the real domain), pricing from the
# official pricing page unless "pricing_source" says otherwise.
import json, re
V = "2026-10-18"
V2 = "2026-10-21"  # entries added or re-checked in the 2026-10-21 daily ops pass
V3 = "2026-10-22"  # entries added or re-checked in the 2026-10-22 daily ops pass
V4 = "2026-10-23"  # entries added or re-checked in the 2026-10-23 daily ops pass
V5 = "2026-10-24"  # entries added or re-checked in the 2026-10-24 daily ops pass
V6 = "2026-10-25"  # entries re-checked in the 2026-10-25 daily ops pass
UPDATED = V6
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
 "Hobbyist $23.99/mo ($239.88/yr); Standard $32.99/mo ($299.88/yr); Enterprise $99.99/mo ($959.88/yr); 7-day free trial.",
 "Writers who live on Substack Notes and want batch scheduling, research and Notes-to-subscriber analytics",
 "The most complete Substack-only Notes suite. Pricey for a beginner, and publishing runs through a Chromium browser extension acting in your logged-in session.",
 aff=True, aff_url="https://www.writestack.io/affiliates", substack_specific=True, free_plan=False, verified=V2)
add("Narrareach","https://www.narrareach.com/","growth",
 "Audience Builder $19.99/mo ($199/yr); Revenue Writer $39/mo ($390/yr); Full Agentic Mode $89/mo ($890/yr). Every plan starts with a 7-day free trial, no card required.",
 "Turning long-form posts into Notes and cross-posting to LinkedIn, X, Bluesky, Threads and Medium",
 "Good if distribution beyond Substack is your bottleneck. Hands Notes to Substack's native scheduler rather than posting from a stored session.",
 substack_specific=True, free_plan=False, verified=V3)
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
 free_plan=True)
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
 "Free (with ads); Core $10/mo (annual only); Growth $29/mo; Premium $199/mo (annual pricing).",
 "Tracking clicks on links you share to social, podcasts and print",
 "Handy for knowing which channel sends readers. The free tier is limited; many writers can get by with UTM tags plus Google Analytics.",
 free_plan=True, verified=V2)
add("Plausible","https://plausible.io/","analytics",
 "From $9/mo (Starter, 10k monthly pageviews); Growth $14/mo; Business $19/mo. Free trial.",
 "Privacy-friendly analytics for your own website or landing page",
 "Excellent lightweight analytics, but you can't install it on a substack.com publication. Use it on a personal site that funnels readers to Substack.",
 free_plan=False, verified=V2)

add("StackStats","https://stackstats.app/","analytics",
 "1-year license $39 (renew updates for $29/yr; the app keeps working if you don't); Lifetime $79 early-adopter price (listed down from $129). One-time payments, no subscription; 14-day refund.",
 "Writers who want churn risk, cohort retention, superfan and growth-source analysis from their own Substack exports",
 "Digs far deeper than Substack's dashboard and keeps your subscriber data on your own computer (Mac or Windows). It's a new one-developer app: installers aren't code-signed yet, and the optional Auto-Sync (beta) logs in to Substack for you, so manual CSV exports are the cautious route.",
 substack_specific=True, free_plan=False, verified=V2, pricing_source="official site (stackstats.app pricing section and FAQ)",
 notes="Independent; not affiliated with Substack. A read-only live demo is on its site.")
add("Orbit","https://seeyourorbit.com/","analytics",
 "$12/mo or $120/yr, included with a paid subscription to creator Rebecca Spitzer's Substack. No free plan or trial.",
 "Writers growing through relationships who want to remember who they've talked to across Notes, comments and DMs",
 "A thoughtful relationship tracker for Substack that never writes or replies for you, and it connects to Claude. It works through a Chrome extension running alongside your logged-in Substack session (DMs off by default), and there's no way to try it before paying.",
 substack_specific=True, free_plan=False, verified=V2, pricing_source="official site (seeyourorbit.com FAQ)",
 notes="Independent; not affiliated with Substack. Access comes via a paid subscription to the creator's Substack.")

add("Substack Insights","https://substackinsights.com/","analytics",
 "Free for publications under 1,000 subscribers; $9.99 one-time above that. The pricing card lists Notes analytics and conversion stats under the paid tier.",
 "Writers who want a cheap, private look at their best posts, best publishing times and Notes engagement",
 "A simple, inexpensive Chrome side panel that ranks your posts and Notes and exports a CSV with ready-made AI prompts. Analysis runs in your browser using your logged-in Substack session; it only reads, never posts. Small and new (v1.0 on the Chrome Web Store).",
 substack_specific=True, free_plan=True, verified=V3, pricing_source="official site (substackinsights.com pricing section and FAQ)",
 notes="Independent; its Chrome Web Store listing says it is not affiliated with Substack.")
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
 "Free (10 posts/mo); Creator $99/yr; Business $20 per social set/mo.",
 "X-first writers who also want to post to LinkedIn, Threads, Bluesky and Substack Notes",
 "A polished writing-first scheduler with Substack Notes support. The free plan is enough to test it.",
 pricing_source="official pricing page is JS-rendered; amounts from third-party pricing trackers checked Oct 2026", free_plan=True)
add("Buffer","https://buffer.com/","social",
 "Free (up to 3 channels, 10 scheduled posts per channel at a time); Essentials $5/channel/mo billed yearly ($6 monthly); Team $10/channel/mo billed yearly.",
 "Scheduling Notes alongside every other social channel from one calendar",
 "Reliable and affordable, and its free plan includes Substack Notes scheduling. The best default if you post to several networks.",
 free_plan=True, verified=V2)
add("Hypefury","https://hypefury.com/","social",
 "From $6/mo (1 channel) to $19/mo (all channels); 7-day free trial.",
 "Automating evergreen reposts and growth on X",
 "Strong automation for X-heavy writers. Less relevant if X isn't where your readers are.",
 aff=True, aff_url="https://hypefury.com/affiliate", free_plan=False, verified=V2)
add("Taplio","https://taplio.com/","social",
 "Starter $39/mo; Growth $69/mo; Pro $199/mo; 7-day free trial.",
 "Writers growing a professional audience on LinkedIn",
 "Effective for LinkedIn but expensive. Only worth it if LinkedIn is a primary acquisition channel.",
 aff=True, aff_url="https://taplio.com/affiliates", free_plan=False, verified=V3)
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
 aff=True, aff_url="https://www.canva.com/affiliates/", free_plan=True,
 notes="Affiliate: Canva Help Center page 'Become a Canva affiliate through the Canvassador Program'.")
add("Figma","https://www.figma.com/","design",
 "Free Starter; Professional full seat $16/mo.",
 "Custom visual systems, templates and detailed design work",
 "More power than most writers need. Pick it if you already know it or want pixel-level control.",
 free_plan=True, verified=V6)
add("Kittl","https://www.kittl.com/","design",
 "Free plan; paid Pro, Expert and Max plans (see pricing page).",
 "Typography-heavy graphics and AI-assisted illustrations",
 "A stylish Canva alternative with great type tools. The free plan is for personal use only.",
 free_plan=True)
add("Unsplash","https://unsplash.com/","design",
 "Free to use under the Unsplash License.",
 "Free, high-quality photos for post headers",
 "The go-to free photo library. Popular images show up everywhere, so crop or edit them to stand out.",
 free_plan=True)
add("remove.bg","https://www.remove.bg/","design",
 "Free to try; paid plans for full-resolution output (see pricing page).",
 "One-click background removal for headshots and product images",
 "Fast and accurate. Now a Canva brand, and Canva Pro includes a background remover, so you may not need both.",
 free_plan=True)

# ---------- Editing ----------
add("Grammarly","https://www.grammarly.com/","editing",
 "Free; Pro from $12/mo.",
 "Catching typos and clarity issues everywhere you write, including the Substack editor",
 "The free browser extension is worth installing. Pro's rewrites can flatten your voice, so accept suggestions selectively.",
 aff=True, aff_url="https://www.grammarly.com/affiliates", free_plan=True, verified=V2)
add("Hemingway Editor","https://hemingwayapp.com/","editing",
 "Free web editor; Editor Plus (AI rewrites) Individual 5K $8.33/mo billed annually ($100/yr) or Individual 10K $12.50/mo billed annually ($150/yr); desktop app $19.99 one-time (no AI features).",
 "Making dense posts easier to read",
 "The free web version does the core job (highlighting long and passive sentences). Most writers don't need Plus.",
 free_plan=True, verified=V4, pricing_source="official site (hemingwayapp.com/hemingway-editor-plus and /desktop; the old /pricing page now returns 404)")
add("ProWritingAid","https://prowritingaid.com/","editing",
 "Free; Premium $10/mo billed yearly ($120) or $30/mo monthly.",
 "Deep style reports for long-form and fiction writers",
 "More thorough reports than Grammarly. Worth trying if you write long essays or serialized fiction.",
 aff=True, aff_url="https://prowritingaid.com/affiliates", free_plan=True, verified=V4)
add("LanguageTool","https://languagetool.org/","editing",
 "Free; Premium $24.90/mo monthly or $69.90/yr.",
 "Multilingual writers and anyone who wants a Grammarly alternative",
 "Strong grammar checking across many languages, and much cheaper per year than monthly billing.",
 pricing_source="LanguageTool help center + third-party price tracker", free_plan=True)
add("QuillBot","https://quillbot.com/","editing",
 "Free; Premium $19.95/mo or $99.95/yr.",
 "Paraphrasing, summarizing and quick rewrites",
 "Useful for tightening a stubborn paragraph. Don't lean on it for whole posts, because readers subscribe for your voice.",
 pricing_source="QuillBot help center", free_plan=True)

# ---------- Planning, research & automation ----------
add("Notion","https://www.notion.com/","planning",
 "Free; Plus $10/seat/mo.",
 "Editorial calendars, idea banks and sponsor CRMs",
 "The most flexible planning hub for newsletter writers. The free plan covers solo use.",
 aff=True, aff_url="https://www.notion.com/affiliates", free_plan=True, verified=V3)
add("Trello","https://trello.com/","planning",
 "Free (up to 10 collaborators); Standard $5/user/mo billed annually.",
 "A simple kanban for drafts moving from idea to published",
 "Simpler than Notion if you only need a board. Free is plenty for one writer.",
 free_plan=True)
add("Obsidian","https://obsidian.md/","planning",
 "Free; optional Sync $4/mo and Publish $8/mo (billed annually).",
 "Building a personal knowledge base of notes, quotes and ideas",
 "Great for writers who think in linked notes. Your files stay local in Markdown.",
 free_plan=True, verified=V3)
add("Readwise","https://readwise.io/","planning",
 "Full Readwise (Reader + Highlights) $9.99/mo billed yearly; Highlights only or Reader only $7.99/mo; Highlights Lite $5.59/mo billed yearly. Free for the first 30 days.",
 "Collecting highlights from books and articles to feed your writing",
 "A strong research engine for essayists and curators. Its Reader app is included with Full.",
 free_plan=False, verified=V4)
add("Google Trends","https://trends.google.com/","planning",
 "Free.",
 "Checking whether a topic is rising before you write about it",
 "A quick, free sanity check for timely topics and post titles.",
 free_plan=True)
add("Zapier","https://zapier.com/","planning",
 "Free (100 tasks/mo, two-step Zaps); Professional from $19.99/mo; Team from $69/mo.",
 "Automating busywork such as logging new posts to a spreadsheet or sending sponsor reminders",
 "Powerful glue between apps. Substack has no official public API, so automations usually start from its RSS feed or email.",
 free_plan=True, verified=V6, pricing_source="official site (zapier.com/pricing, USD)")

# ---------- AI writing & research ----------
add("ChatGPT","https://chatgpt.com/","ai",
 "Free; Plus $20/mo.",
 "Brainstorming angles, outlines, headlines and research summaries",
 "A versatile thinking partner. Use it for ideas and edits rather than finished prose your readers will recognize as generic.",
 pricing_source="OpenAI help docs", free_plan=True)
add("Claude","https://claude.ai/","ai",
 "Free; Pro $20/mo or $17/mo billed annually.",
 "Long-document feedback, structural edits and drafting help",
 "Particularly good at critiquing long drafts. The same caution about voice applies.",
 pricing_source="claude.com/pricing", free_plan=True)
add("Perplexity","https://www.perplexity.ai/","ai",
 "Free; Pro $20/mo.",
 "Quick research with cited sources",
 "Faster than a search engine for background research. Always click through and verify the citations.",
 pricing_source="Perplexity pricing hub + third-party price tracker", free_plan=True)
add("Sudowrite","https://sudowrite.com/","ai",
 "Hobby & Student $10/mo; Professional $22/mo; Max $44/mo; free trial.",
 "Fiction writers publishing serialized stories",
 "Purpose-built for fiction. Not the right tool for essays or news-style newsletters.",
 free_plan=False)

# ---------- Audio, podcast & video ----------
add("Descript","https://www.descript.com/","audio",
 "Free; Hobbyist $16/mo billed annually ($24 monthly); Creator $24/mo annually ($35 monthly).",
 "Editing podcast and video by editing the transcript",
 "The easiest way for writers to edit audio and video. A natural fit for Substack podcasts.",
 aff=True, aff_url="https://www.descript.com/affiliate", free_plan=True, verified=V2)
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
 free_plan=True)
add("Adobe Podcast","https://podcast.adobe.com/","audio",
 "Free tier; premium features require a paid Adobe plan (check site for current offer).",
 "Making laptop-mic recordings sound clean (Enhance Speech)",
 "Enhance Speech is impressive on the free tier. Check Adobe's current plans before relying on premium features.",
 pricing_source="official site; premium-plan details from third-party reports", free_plan=True)
add("OpusClip","https://www.opus.pro/","audio",
 "Free (60 credits/mo); Starter $15/mo; Pro $14.50/mo billed annually.",
 "Turning long videos or podcast episodes into short social clips",
 "Fast way to get shorts from long recordings. Review the AI's clip choices before posting.",
 aff=True, aff_url="https://www.opus.pro/affiliate", free_plan=True)

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
 free_plan=True, verified=V2, notes="Substack's help center documents native Datawrapper embeds (paste the share link into a draft).")
add("Flourish","https://flourish.studio/","embeds",
 "Free (public publishing with attribution); paid Presenter (via Canva Business) and Publisher/Enterprise plans on contract.",
 "Animated and interactive charts and scrollytelling",
 "More dramatic visuals than Datawrapper, but Substack doesn't list Flourish among its supported embeds and pasted embed code doesn't work, so plan on a static image linked to the interactive version.",
 free_plan=True, verified=V2)
add("Linktree","https://linktr.ee/","embeds",
 "Free; Starter $6/mo billed annually ($8 monthly); Pro $12/mo billed annually ($15 monthly); Premium $30/mo billed annually ($35 monthly).",
 "A link-in-bio page that points social followers to your Substack",
 "Fine for bios, but your Substack homepage can often serve as the link. Only pay if you need the analytics.",
 free_plan=True, verified=V2)

# ---------- Sponsorships & monetization ----------
add("Paved","https://www.paved.com/","monetization",
 "Free publisher account, no subscription. Flat-fee scheduled ads need at least 50k subscribers; pay-per-click native ads need at least 1M monthly impressions.",
 "Established newsletters looking for sponsor demand",
 "A large newsletter ad network (3,000+ newsletters, per Paved). Its stated minimums of 50k subscribers or 1M monthly impressions rule out most smaller Substacks; start with Hecto or Swapstack until you're there.",
 free_plan=True, verified=V6, pricing_source="official site (paved.com/publishers)")
add("Hecto","https://www.hecto.io/","monetization",
 "Free for newsletter creators (no monthly fee); Hecto takes 5% of successful sponsorship sales, plus Stripe's payment fees.",
 "Selling sponsorship slots with transparent, upfront prices",
 "A straightforward sponsorship marketplace: you publish ad packages with upfront prices and a checkout link. Listing is free, but demand varies by niche.",
 free_plan=True, verified=V6, pricing_source="official site (hecto.io/pricing; fee shown as 5%, monthly fee shown as £0)")
add("Swapstack","https://www.swapstack.co/","monetization",
 "Free for publishers (Swapstack takes 10% on invite-only campaigns from its managed service). Paid publisher plans (Professional $30/mo, Enterprise $200/mo) are listed as coming soon.",
 "Finding sponsors and affiliate deals for small and mid-sized newsletters",
 "One of the original newsletter sponsorship marketplaces, with flat-rate sponsorships, pay-per-click and affiliate deals in one place. Worth a free signup to see what matches your niche.",
 free_plan=True, verified=V6, pricing_source="official site (swapstack.co/pricing)")
add("Gumroad","https://gumroad.com/","monetization",
 "No monthly fee; 10% + $0.50 per transaction on direct sales (profile or direct links); 30% on sales through Gumroad Discover.",
 "Selling ebooks, templates and guides alongside your newsletter",
 "The simplest way to sell a digital product to your readers. Fees are high per sale but there's no fixed cost.",
 free_plan=True, verified=V2)
add("Ko-fi","https://ko-fi.com/","monetization",
 "Free with a 5% platform fee on some features; Ko-fi Gold $12/mo for 0% platform fee.",
 "One-off tips from readers who won't commit to a paid subscription",
 "A low-friction tip jar that complements paid subscriptions.",
 free_plan=True, verified=V2)

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
