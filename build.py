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

# Head-to-head comparison pages (/compare/<slug>/). Every claim must be checked on the cited sources.
COMPARISONS = [
  dict(slug="datawrapper-vs-flourish-substack", a="datawrapper", b="flourish", checked="2026-10-21",
    title="Datawrapper vs Flourish for Substack: which chart tool actually embeds?",
    h1="Datawrapper vs Flourish for Substack charts",
    desc="Datawrapper vs Flourish for Substack writers: which one embeds natively in Substack posts, what the free plans include, paid pricing, and which to pick for data-driven newsletters.",
    short="Pick Datawrapper if you want interactive charts inside your Substack posts: it's the only one of the two that Substack embeds natively, and its free plan is unlimited. Pick Flourish only if you need animated or scrollytelling visuals and are happy to link out to them from a static image.",
    rows=[
      ("Embeds in Substack posts", "Yes, officially supported. Paste the chart's share link (\"Visualization only\" URL) into your draft and it loads automatically.", "Not in Substack's list of supported embeds. Writers report that pasting the link or embed code doesn't work."),
      ("Interactive for readers", "On the web and in the Substack app. Static in the email version (clicking opens the chart in a browser).", "Only if readers click through to the Flourish-hosted version."),
      ("Free plan", "Create, publish and embed charts, maps and tables without limits; PNG download. Charts carry a \"Created with Datawrapper\" credit.", "Public publishing and embedding with attribution; unpublished projects stay private."),
      ("Image export", "PNG on the free plan; PDF and SVG on Pro.", "Image and SVG export are listed under the paid Presenter plan."),
      ("Paid plans", "Pro $21/user/mo excl. VAT (removes the credit); Business $39/user/mo excl. VAT.", "Presenter via a Canva Business or Enterprise plan; Publisher and Enterprise on request."),
      ("Best at", "Clean, accurate line, bar and table charts and maps that read at a glance.", "Animated, interactive and scrollytelling visuals."),
    ],
    body=[
      ("Why embedding matters on Substack", "Substack doesn't allow custom HTML or scripts in the post editor. It supports a short list of embeds instead, and Datawrapper is on it. That single fact decides most of this comparison: a Datawrapper chart sits inside your post and readers on the web or in the app can hover, zoom and scroll it. A Flourish visual has to live somewhere else, with a picture of it in your post."),
      ("Remember the email version", "Most of your readers meet a post in their inbox, where no chart is interactive. Datawrapper embeds show up as a static image in email, and clicking opens the live chart. Whatever tool you use, design the chart so its main point is readable without hovering: a clear title that states the takeaway, labeled lines and few colors."),
      ("When Flourish is still worth it", "If your story depends on motion, such as a bar chart race, an animated map or a step-by-step scrollytelling piece, Flourish does things Datawrapper doesn't try to do. Publish it on Flourish, put a screenshot in your Substack post, and link the image to the interactive version. On the free plan, Flourish lists image export under its paid Presenter plan, so expect to take that screenshot yourself."),
      ("Our pick", "For almost every Substack writer, Datawrapper. It's free without limits, it's the native option, and its defaults produce honest, readable charts. Consider paying for Pro only if the small credit line under each chart bothers you."),
    ],
    sources=[
      ("Substack Help: How do I embed Datawrapper charts in a Substack post?", "https://support.substack.com/hc/en-us/articles/15722290158100-How-do-I-embed-Datawrapper-charts-in-a-Substack-post"),
      ("Substack Help: How do I embed media in my post? (supported embeds)", "https://support.substack.com/hc/en-us/articles/360037832971-How-do-I-embed-media-in-my-post-e-g-images-video-GIFs"),
      ("Datawrapper Academy: How to embed visualizations in Substack", "https://www.datawrapper.de/academy/how-to-embed-visualizations-in-substack"),
      ("Datawrapper pricing", "https://www.datawrapper.de/pricing"),
      ("Flourish pricing", "https://flourish.studio/pricing/"),
      ("r/Substack: Embed a Flourish visual? (writer reports)", "https://www.reddit.com/r/Substack/comments/1qkyzsn/embed_a_flourish_visualgraphic/"),
    ]),
  dict(slug="substack-insights-vs-notestack", a="substack-insights", b="notestack", checked="2026-10-22",
    title="Substack Insights vs NoteStack: which Substack Notes analytics extension to use",
    h1="Substack Insights vs NoteStack for Substack analytics",
    desc="Substack Insights vs NoteStack compared for Substack writers: Notes and post analytics, pricing ($9.99 one-time vs from $8/mo), scheduling, AI features and what each does with your data.",
    short="Pick Substack Insights if you just want to see which posts and Notes work and when to publish: it's free under 1,000 subscribers and $9.99 one-time above that, and it only reads your data. Pick NoteStack if Notes are your main growth channel and you also want subscriber-conversion rankings, a scheduler and optional AI drafting, from $8/mo.",
    rows=[
      ("What it is", "Chrome extension side panel: post and Notes analytics plus CSV export.", "Chrome extension side panel: Notes analytics, scheduler, competitor research (Spy Mode), media kit and AI tools."),
      ("Price", "Free for publications under 1,000 subscribers; $9.99 one-time above that.", "Starter $8/mo or $60/yr; Pro $12/mo or $99/yr. 7-day free trial."),
      ("Notes analytics", "Top Notes by weighted engagement, best day and time to post Notes (listed under the paid tier on its pricing card).", "Every Note ranked by engagement and subscriber conversion, best-time heatmap, Note-type breakdown and trends."),
      ("Post analytics", "Top posts, top converting posts (free and paid signups), best publishing time and optimal post length.", "Focused on Notes."),
      ("Scheduling", "None (read-only).", "Yes. Auto-publishes through your logged-in Substack session; Starter allows 7 new scheduled Notes a month, Pro is unlimited."),
      ("AI", "Exports a CSV with suggested prompts to paste into ChatGPT, Claude or Gemini yourself.", "Pro adds Ghostwriter (drafts Notes in your voice), AI generation and Post Coach."),
      ("Your data", "Processed in your browser using your existing session; it says it never sees your data.", "Stored in your browser. AI features and license checks call its relay server, and AI requests send your Notes text to Anthropic."),
    ],
    body=[
      ("Start with what Substack already shows you", "Before installing anything, open a recent Note and click View stats: Substack now shows the new free and paid subscribers, followers, clicks and shares each Note produced. Both extensions are most useful once you have enough Notes and posts that patterns are hard to see one at a time."),
      ("Read-only vs a full Notes suite", "Substack Insights only reads. It ranks your posts and Notes, tells you when you tend to get the most engagement, and hands you a CSV to analyze. NoteStack does that for Notes and goes further: it schedules and publishes Notes for you, researches other profiles and offers AI drafting. More features also means more access: anything that publishes on your behalf acts inside your logged-in Substack session."),
      ("About AI-drafted Notes", "Readers follow you for your voice. NoteStack is upfront that its Ghostwriter sends your past Notes to its AI provider to learn your style, and that it never posts AI drafts automatically. If you use it, treat drafts as prompts to rewrite, not posts to publish."),
      ("Our pick", "For most writers, Substack Insights: it answers the main questions (what works, when to post) for free or a one-time $9.99, without posting anything. Choose NoteStack if you post Notes daily and want analytics and a scheduler in one place, and remember that Substack's own Notes scheduler is free if scheduling is all you need."),
    ],
    sources=[
      ("Substack Insights: features, pricing and FAQ", "https://substackinsights.com/"),
      ("Substack Insights on the Chrome Web Store", "https://chromewebstore.google.com/detail/bmeapnigmgnaccpcfgpmifahhddhhihc"),
      ("NoteStack: features and FAQ", "https://notestack.stacktreelabs.com/"),
      ("NoteStack pricing", "https://notestack.stacktreelabs.com/pricing/"),
      ("NoteStack privacy policy (what is sent to its relay and Anthropic)", "https://notestack.stacktreelabs.com/privacy/"),
    ]),
  dict(slug="buffer-vs-typefully-substack-notes", a="buffer", b="typefully", checked="2026-10-26",
    title="Buffer vs Typefully for Substack Notes: which multi-platform scheduler to use",
    h1="Buffer vs Typefully for scheduling Substack Notes",
    desc="Buffer vs Typefully for Substack writers: both free plans schedule Substack Notes. Compare free-plan limits, paid pricing, other platforms, Note analytics and which to pick if Notes are one channel among several.",
    short="Both free plans schedule Substack Notes, so you can try either at no cost. Pick Buffer if Notes are one channel among many (including Instagram, TikTok or Facebook) or you want to see which Notes brought subscribers. Pick Typefully if you write for X or LinkedIn first and want a writing-focused editor. If you only post Notes, Substack's free built-in scheduler may be all you need.",
    rows=[
      ("Substack Notes", "Yes. Connect your Substack account and Notes become a channel in your queue. You can also add your Substack as a feed to pull in published posts for sharing.", "Yes, on every plan. Connect Substack under Settings → Social Sets. Notes only: no long-form posts and no video in Notes."),
      ("Free plan", "Up to 3 channels, 10 scheduled posts per channel at a time (refill as they publish), 30 days of insights.", "10 posts a month, 1 social set, 1 user."),
      ("Paid plans", "Essentials $5/channel/mo billed yearly ($6 monthly); Team $10/channel/mo billed yearly ($12 monthly). 14-day trial.", "Creator $99/yr (annual billing only); Business $18 per social set/mo billed yearly."),
      ("Other platforms", "LinkedIn, X, Threads, Bluesky, Mastodon, Instagram, Facebook, TikTok, YouTube, Pinterest and Google Business Profile.", "X, LinkedIn, Threads, Bluesky and Mastodon."),
      ("Note analytics", "Buffer says it shows free and paid subscribers each Note brought in, plus impressions, follows and engagement.", "Paid analytics are listed for X. Its pricing page doesn't list Substack Note analytics."),
      ("Cross-posting", "Send the same text to Substack and other channels, editing each version.", "Enable Substack alongside other platforms in one draft. Multi-post drafts (threads) are combined into a single Note, so review the Substack version."),
      ("Best at", "One calendar for every channel, with per-channel pricing.", "A distraction-free editor for threads and short posts."),
    ],
    body=[
      ("Start with the free plans", "Unlike most Substack-only Notes tools, both of these include Substack Notes on their free plans. Buffer's free plan caps how many posts can be waiting (10 per channel at once), while Typefully's caps how many you publish in a month (10). If you post a Note a day, Buffer's free plan keeps working as long as you keep your queue short; Typefully's free plan runs out after about ten days."),
      ("How the costs add up", "Buffer charges per channel, so Substack plus LinkedIn on Essentials is about $10/mo billed yearly. Typefully's Creator plan is a flat $99 a year (about $8.25/mo) for one social set. Compare the two at the number of channels you actually use: Buffer's cost grows with every channel you add, Typefully's Creator price doesn't."),
      ("Neither replaces replying", "A scheduler helps you show up consistently, but much of the growth on Notes comes from replying to other writers, which you still do in Substack itself. Treat either tool as a way to free up time for that."),
      ("Our pick", "For most Substack writers who also post elsewhere, Buffer: its free plan covers three channels and it reports subscribers per Note. Choose Typefully if X or LinkedIn is your main channel and you already like writing there. For every other option, including Substack-only batch schedulers, see our Substack Notes schedulers comparison."),
    ],
    sources=[
      ("Buffer: Substack Notes scheduler (features and FAQ)", "https://buffer.com/substack"),
      ("Buffer pricing", "https://buffer.com/pricing"),
      ("Typefully changelog: Publish and Schedule Substack Notes", "https://typefully.com/changelog/substack-notes"),
      ("Typefully Help Center: Publish and Cross-Post to Substack Notes", "https://support.typefully.com/en/articles/16124373-publish-and-cross-post-to-substack-notes"),
      ("Typefully pricing", "https://typefully.com/pricing"),
    ]),
  dict(slug="claude-vs-sudowrite-substack-fiction", a="claude", b="sudowrite", checked="2026-10-27",
    title="Claude vs Sudowrite for Substack fiction writers: general AI assistant or fiction tool?",
    h1="Claude vs Sudowrite for writing serialized fiction on Substack",
    desc="Claude vs Sudowrite for Substack writers who publish fiction: compare free options, monthly pricing, fiction-specific features and which one fits serialized stories versus essays.",
    short="Pick Sudowrite if your Substack is serialized fiction and you want a tool built around story work: its plans include style matching and continuity across a series, with a free trial and no card. Pick Claude if you write essays alongside fiction or mainly want feedback on long drafts: it has a free plan and Pro is $20/mo ($17/mo billed annually). Either way, keep the published prose your own.",
    rows=[
      ("What it is", "A general-purpose AI assistant for chat, drafting, critique and research.", "An AI writing tool built specifically for creative writing and fiction."),
      ("Free option", "Free plan for everyone.", "Free trial, no credit card required. No ongoing free plan."),
      ("Paid plans", "Pro $20/mo billed monthly, or $17/mo with annual billing ($200 up front). Max from $100/mo.", "Hobby & Student $10/mo, Professional $22/mo, Max $44/mo, credit-based. Yearly billing is advertised as up to 50% off."),
      ("Fiction features", "No fiction-specific features listed on its pricing page; you guide it with your own prompts.", "Write, Rewrite, Describe and Expand tools, style matching, continuity across a series, and Sudowrite's own fiction models (Muse and Ballad)."),
      ("Feedback on drafts", "Strong at critiquing long drafts and structure.", "Professional and Max list developmental edits, line edits and beta reads."),
      ("Best for", "Essayists, mixed newsletters, and writers who want one assistant for everything.", "Writers publishing chapters or serialized stories who want a dedicated fiction workspace."),
    ],
    body=[
      ("Start with what you publish", "If most of your Substack is essays, analysis or how-to posts, Sudowrite's fiction tools won't help much and Claude's free plan is the better place to start. If you publish a chapter a week, Sudowrite's series continuity and style matching are built for exactly that job."),
      ("How the costs compare", "Sudowrite's entry plan is $10/mo, half of Claude Pro's monthly price, but it's credit-based, so heavy use can push you to a higher tier. Claude's free plan costs nothing to try for feedback; Sudowrite lets you trial without a card."),
      ("Keep your voice", "Readers subscribe for your writing. Use either tool for brainstorming, critique and getting unstuck, and edit anything it suggests until it sounds like you before it goes out to subscribers."),
      ("Our pick", "Serialized fiction on Substack: Sudowrite. Everything else, or a mix of fiction and essays: Claude. For more options, see the AI Writing & Research category."),
    ],
    sources=[
      ("Claude pricing", "https://claude.com/pricing"),
      ("Sudowrite pricing", "https://sudowrite.com/pricing"),
    ]),
  dict(slug="grammarly-vs-prowritingaid-substack", a="grammarly", b="prowritingaid", checked="2026-10-28",
    title="Grammarly vs ProWritingAid for Substack writers: which editor fits your newsletter?",
    h1="Grammarly vs ProWritingAid for Substack writers",
    desc="Grammarly vs ProWritingAid for Substack writers: free-plan limits, Pro and Premium pricing ($12/mo vs from $10/mo billed yearly), browser extensions for the Substack editor, style reports and which to pick for essays or fiction.",
    short="Pick Grammarly if you want quick, everywhere proofreading: its free browser extension checks spelling and grammar as you type on the web, and Pro (from $12/mo) adds full-sentence rewrites and tone adjustments. Pick ProWritingAid if you write long essays or serialized fiction and want deep style reports: Premium is $10/mo billed yearly ($120) or $30 monthly. Both browser extensions work on web pages, so either can check drafts in the Substack editor.",
    rows=[
      ("Best at", "Fast proofreading and tone as you type, across email, social and web apps.", "Deep line-editing reports (25+ on paid plans) for long-form and fiction."),
      ("Free plan", "Spelling and grammar, tone detection and 100 AI prompts a month.", "Grammar, spelling and punctuation; each report runs on 500 words at a time, twice a day; 10 Rephrases a day."),
      ("Paid plans", "Pro from $12/mo, with a free trial. Enterprise via sales.", "Premium $10/mo billed yearly ($120) or $30 monthly; Premium Pro $12/mo billed yearly ($144) or $36 monthly; lifetime options."),
      ("What paid adds", "Full-sentence rewrites, tone adjustments, plagiarism and AI-text detection, 2,000 AI prompts a month.", "Unlimited reports and Rephrases on any length, custom style guide, Chapter Critique; Premium Pro adds live workshops and community."),
      ("Works in the Substack editor", "Yes, through its browser extensions, which work across web apps.", "Yes, through its Chrome, Edge and Firefox extensions, which work on any web page."),
      ("Refunds and trials", "Free trial on Pro, with an email reminder 2 days before it ends.", "3-day money-back guarantee on yearly and lifetime plans; no refunds on monthly plans."),
    ],
    body=[
      ("Start free with either", "Most Substack writers only need a second pair of eyes for typos before hitting publish. Both free plans catch spelling and grammar. Grammarly's free extension does it as you type; ProWritingAid's free reports cap you at 500 words at a time, which is fine for a Note but tight for a full post."),
      ("Essays and fiction: reports beat rewrites", "If your posts run long, ProWritingAid's reports on repetition, sentence length, pacing, dialogue tags and readability show patterns across a whole draft. That's more useful for a weekly essay or chapter than one-sentence fixes. Its fiction tools (Chapter Critique, Story Canvas) only matter if you publish stories."),
      ("Keep your voice", "Grammarly Pro's full-sentence rewrites and tone adjustments can make every post sound the same. Readers subscribe for how you write, so accept suggestions one at a time and skip the ones that don't sound like you. The same goes for ProWritingAid's Rephrases."),
      ("How the costs compare", "Paying monthly, Grammarly Pro starts at $12 against ProWritingAid Premium's $30. Paying yearly, ProWritingAid Premium works out to $10 a month ($120). Check Grammarly's checkout for its billing options, since its plans page shows the Pro price without a yearly total."),
      ("Our pick", "For most Substack writers, start with Grammarly's free extension for everyday proofreading. Add ProWritingAid Premium (billed yearly) if you publish long essays or serialized fiction and want a deeper edit before each post. For other options, including the free Hemingway web editor and LanguageTool, see the Editing & Proofreading category."),
    ],
    sources=[
      ("Grammarly plans and pricing", "https://www.grammarly.com/plans"),
      ("Grammarly for your browser", "https://www.grammarly.com/browser"),
      ("ProWritingAid pricing (plans, limits, refund policy)", "https://prowritingaid.com/pricing"),
      ("ProWritingAid integrations (browser extensions)", "https://prowritingaid.com/integrations"),
    ]),
  dict(slug="chatgpt-vs-perplexity-substack-research", a="chatgpt", b="perplexity", checked="2026-10-29",
    title="ChatGPT vs Perplexity for Substack research: which AI helps you write better posts?",
    h1="ChatGPT vs Perplexity for Substack research",
    desc="ChatGPT vs Perplexity for Substack writers: free plans, paid pricing (ChatGPT Go $8/mo and Plus $20/mo vs Perplexity Pro $20/mo or $17/mo billed annually), citations, deep research and which to use for brainstorming versus fact-finding.",
    short="Pick Perplexity when you need facts you can check: every answer comes with citations, and the free plan covers light research. Pick ChatGPT when you want a brainstorming and editing partner for angles, outlines and headlines; its free plan includes unlimited everyday text chats, Go is $8/mo and Plus is $20/mo. Perplexity Pro is $20/mo, or $17/mo billed annually.",
    rows=[
      ("Best at", "Brainstorming angles, outlines, headlines and feedback on drafts.", "Research answers with citations you can click through and verify."),
      ("Free plan", "Unlimited everyday text chats, with limited uploads, image creation and deep research.", "Search with citations in every answer, for limited daily use with basic AI models."),
      ("Paid plans", "Go $8/mo (may include ads); Plus $20/mo; Pro from $100/mo. Individual plans are billed monthly.", "Pro $20/mo or $17/mo billed annually ($200/yr); Max $200/mo or $167/mo billed annually."),
      ("What paid adds", "Plus: advanced reasoning models, expanded deep research, memory, projects, scheduled tasks and custom GPTs.", "Pro: deep research, choice of AI models, more usage and memory, and premium data sources."),
      ("Watch out for", "Answers can sound confident without a source, so check any fact before it goes in a post.", "Citations can still be misread or out of date, so open the source before you quote it."),
    ],
    body=[
      ("Use each for what it's good at", "Most Substack writers get the most out of these as two different tools. Perplexity is for questions with a factual answer: a statistic, a date, what a study actually found. ChatGPT is for the thinking around the post: ten possible angles, a tighter outline, five headline options, or a blunt read on a draft."),
      ("Always check the facts", "Readers trust a newsletter that gets details right. Perplexity puts citations in every answer, which makes checking quick, but open the source and read the line yourself before you quote it. Treat any fact from ChatGPT the same way, and look it up before it goes in a post."),
      ("Keep your voice", "Neither tool should write the post for you. Readers subscribe for how you think and write, and AI-drafted prose tends to sound like everyone else's. Use them for research and structure, then write in your own words."),
      ("How the costs compare", "Both free plans are enough to try the workflow. If you pay for one, ChatGPT Go at $8/mo is the cheapest paid step and Plus is $20/mo. Perplexity Pro is also $20/mo, or $17/mo if you pay for a year up front. ChatGPT's individual plans are billed monthly only."),
      ("Our pick", "Start with both free plans: Perplexity for fact-finding and ChatGPT for brainstorming and edits. If you only pay for one, pick the job you do most. Writers who publish researched, data-heavy posts get more from Perplexity Pro; writers who mostly need help shaping ideas get more from ChatGPT. For long-draft feedback, also see Claude in the AI Writing & Research category."),
    ],
    sources=[
      ("ChatGPT plans and pricing", "https://chatgpt.com/pricing"),
      ("What is ChatGPT Plus? (OpenAI Help Center)", "https://help.openai.com/en/articles/6950777-what-is-chatgpt-plus"),
      ("Introducing ChatGPT Go (OpenAI)", "https://openai.com/index/introducing-chatgpt-go/"),
      ("Perplexity pricing", "https://www.perplexity.ai/hub/pricing"),
      ("Perplexity Pro", "https://www.perplexity.ai/pro"),
      ("Perplexity plan prices (Perplexity Help Center)", "https://www.perplexity.ai/help-center/pt-BR/articles/12167980-como-usar-o-conector-para-slack"),
    ]),
]

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
<div><a href="/">Directory</a><br><a href="/guides/{GUIDE_SLUG}/">Best tools to grow your Substack in 2026</a><br><a href="/free-substack-tools/">Free tools for Substack writers</a><br><a href="/substack-notes-schedulers/">Substack Notes schedulers compared</a><br><a href="/guides/substack-seo-guide/">Substack SEO guide</a><br><a href="/guides/substack-recommendations-guide/">Substack recommendations &amp; lists guide</a><br>{''.join(f'<a href="/compare/{c["slug"]}/">{e(BY[c["a"]]["name"])} vs {e(BY[c["b"]]["name"])}</a><br>' for c in COMPARISONS)}<a href="/feature/">Feature your tool</a><br><a href="/about/">About &amp; disclosures</a></div>
<div>Some links may be affiliate links; it never changes our verdicts.<br>Data last updated {e(data['generated'])}.<br><a href="/llms.txt">llms.txt</a> · <a href="/sitemap.xml">sitemap</a></div>
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
<a class="btn" href="/guides/{GUIDE_SLUG}/">Read: Best tools to grow your Substack in 2026 →</a> <a class="btn" href="/free-substack-tools/">Or start with the free tools →</a> <a class="btn" href="/guides/substack-seo-guide/">Get found on Google: Substack SEO guide →</a> <a class="btn" href="/guides/substack-recommendations-guide/">Grow with recommendations and lists →</a></div></section>
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
    cmps = "".join(f'<li><a href="/compare/{x["slug"]}/">{e(BY[x["a"]]["name"])} vs {e(BY[x["b"]]["name"])} for Substack</a></li>' for x in COMPARISONS if BY[x["a"]]["category"] == c["slug"] or BY[x["b"]]["category"] == c["slug"])
    cmps = f"<h2>Comparisons</h2><ul>{cmps}</ul>" if cmps else ""
    others = " · ".join(f'<a href="/category/{o["slug"]}/">{e(o["name"])}</a>' for o in CATS if o["slug"] != c["slug"])
    body = f"""<div class="wrap page"><div class="crumbs"><a href="/">Directory</a> / {e(c['name'])}</div>
<h1>{e(c['name'])} tools for Substack writers</h1><p class="sub">{e(c['desc'])}</p>
<div class="grid">{''.join(card(t) for t in ts)}{FEATURED_PLACEHOLDER}</div>
<h2>Pricing at a glance</h2><div class="table-wrap"><table class="cmp"><thead><tr><th>Tool</th><th>Best for</th><th>Pricing (last checked dates on each tool page)</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Prices change. Always confirm on the vendor's site.</p>
{cmps}{f'<p><a href="/free-substack-tools/#{c["slug"]}">Only want free options? See the free {e(c["name"].lower())} tools →</a></p>' if any(t.get("free_plan") for t in ts) else ""}<p class="small">Other categories: {others}</p></div>{SIGNUP}"""
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
{'<p><a href="/substack-notes-schedulers/">Compare every Substack Notes scheduler, including the free built-in one →</a></p>' if t["slug"] in [x[0] for x in SCHEDULERS] else ''}
{''.join(f'<p><a href="/compare/{x["slug"]}/">Compare: {e(BY[x["a"]]["name"])} vs {e(BY[x["b"]]["name"])} for Substack →</a></p>' for x in COMPARISONS if t["slug"] in (x["a"], x["b"]))}
<h2>Other {e(c['name'].lower())} tools</h2><div class="grid">{''.join(card(o) for o in rel)}</div>
{f'<p><a href="/guides/substack-seo-guide/">How to use {e(t["name"])} in our Substack SEO guide →</a></p>' if t["slug"] in SEO_TOOLS else ''}
{f'<p><a href="/guides/substack-recommendations-guide/">Where {e(t["name"])} fits in our Substack recommendations guide →</a></p>' if t["slug"] in REC_TOOLS else ''}
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
      ("3. Win on Substack Notes", "Notes is where Substack readers discover new writers. Substack now schedules single Notes natively; the tools below add batch queues, cross-posting and, most importantly, attribution: which Notes actually bring subscribers. For every scheduler side by side, see <a href=\"/substack-notes-schedulers/\">Substack Notes schedulers compared</a>.",
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

# ---------------- Free tools hub ----------------
FREE_SLUG = "/free-substack-tools/"
def free_tools():
    ft = [t for t in TOOLS if t.get("free_plan")]
    secs = ""
    for c in CATS:
        ts = [t for t in BYCAT[c["slug"]] if t.get("free_plan")]
        if not ts: continue
        items = "".join(f'<li><strong><a href="/tools/{t["slug"]}/">{e(t["name"])}</a></strong>: {e(t["best_for"])}. <em>Pricing: {e(t["pricing"])}</em></li>' for t in ts)
        secs += f'<h2 id="{c["slug"]}">{e(c["name"])} ({len(ts)})</h2><ul>{items}</ul><p class="small">More: <a href="/category/{c["slug"]}/">all {e(c["name"].lower())} tools, free and paid</a>.</p>'
    ss = [t for t in ft if t.get("substack_specific")]
    starter = [s for s in ["google-analytics", "google-search-console", "canva", "grammarly", "hemingway-editor", "notion", "buffer", "subshack", "sparkloop"] if s in BY and BY[s].get("free_plan")]
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / Free tools</div>
<h1>Free tools for Substack writers</h1>
<p class="small">Updated {e(data['generated'])} · {len(ft)} of our {len(TOOLS)} hand-checked tools have a free plan · Prices and limits checked on each vendor's site</p>
<p>You can grow a Substack without paying for any software. Substack already handles hosting, email, payments, recommendations and Notes, and the gaps that remain (analytics, images, editing, scheduling, planning) all have free options. This page lists every tool in the StackKit directory with a genuine free plan, grouped by what it helps you do, with the paid upgrade next to it so you know where the limits are.</p>
<p><strong>A free starter kit:</strong> {", ".join(L(s) for s in starter)}. That covers traffic sources, search, header images, proofreading, planning, Notes scheduling and recommendations for $0.</p>
<p>"Free plan" here means you can keep using the tool without paying, not just a time-limited trial. Free tiers usually come with limits such as watermarks, monthly credits or a cap on scheduled posts; those limits are in each tool's pricing line below.</p>
<p><strong>Built specifically for Substack and free:</strong> {", ".join(L(t["slug"]) for t in ss)}.</p>
{secs}
<h2>Before you install a free browser extension</h2>
<p>Several free Substack tools are browser extensions that read data through your logged-in Substack session. That's normal, but check each tool's privacy page, prefer read-only modes, and avoid anything that follows, likes or messages people automatically. Our <a href="/guides/{GUIDE_SLUG}/">2026 growth guide</a> explains when paid tools start to make sense.</p>
<p class="small">Free plans change. Always confirm on the vendor's site. See <a href="/about/">how we verify tools</a>.</p></div></div>{SIGNUP}"""
    ld = [{"@context": "https://schema.org", "@type": "CollectionPage", "name": "Free tools for Substack writers", "description": f"{len(ft)} hand-checked tools with free plans for Substack writers.", "dateModified": data["generated"], "url": SITE_URL + FREE_SLUG,
           "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE_URL + f"/tools/{t['slug']}/", "name": t["name"]} for i, t in enumerate(ft)]}},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Can you grow a Substack with only free tools?",
           "acceptedAnswer": {"@type": "Answer", "text": "Yes. Substack includes hosting, email, payments, recommendations and Notes. Free plans from tools like " + ", ".join(BY[s]["name"] for s in starter) + " cover analytics, search, design, editing, planning and Notes scheduling."}}]}]
    write(FREE_SLUG, layout(FREE_SLUG, f"{len(ft)} free tools for Substack writers (checked {data['generated']}) | {BRAND}",
        f"Every free tool in StackKit's hand-checked directory for Substack writers: {len(ft)} tools for analytics, Notes, design, editing, planning, audio and monetization, with free-plan limits and paid prices.", body, ld), "0.9")

# ---------------- Notes schedulers hub ----------------
SCHED_SLUG = "/substack-notes-schedulers/"
# (slug, batch queue?, how it publishes). Every claim checked 2026-10-24 on the cited sources / the tool's listing sources.
SCHEDULERS = [
  ("buffer", "Yes, plus every other social channel", "Buffer says it connects to Substack directly; Notes sit in the same calendar as your other channels. Free plan included (checked 2026-10-26)."),
  ("typefully", "Yes, alongside X, LinkedIn, Threads, Bluesky and Mastodon", "You connect Substack in Typefully's settings by authorizing your account on Substack. Notes only (no long-form posts, no video), and included on the free plan (checked 2026-10-26)."),
  ("narrareach", "Yes", "Hands Notes to Substack's own scheduler rather than posting from a stored session."),
  ("subflowai", "Yes (up to 30 at once, visual calendar)", "Chrome extension that schedules Notes on Substack's servers through your logged-in session, so they publish with Chrome closed."),
  ("notesiq", "Weekly queue", "Chrome extension that publishes through Substack's composer in your logged-in session."),
  ("notestack", "Yes (Starter: 7 new scheduled Notes a month; Pro: unlimited)", "Chrome extension that auto-publishes through your logged-in session."),
  ("writestack", "Yes (bulk scheduling, reorderable queue, calendar)", "Chromium browser extension acting in your logged-in session."),
  ("stackbuddy", "Yes (posting slots fill automatically; free plan keeps scheduling)", "Chrome extension syncs each Note into Substack's own scheduler, so Substack publishes it; Chrome only needs to be open while syncing (checked 2026-10-28)."),
  ("stacksweller", "Yes (cloud queue)", "Cloud service that holds your Substack session so the queue runs with your laptop closed."),
]
def schedulers():
    rows = '<tr><td><strong>Substack (built in)</strong></td><td>Free</td><td>No: one Note at a time</td><td>Substack\'s own servers. Scheduled Notes wait in your Drafts tab, where you can still edit them.</td></tr>'
    rows += "".join(f"<tr><td>{L(sl)}</td><td>{P(sl)}</td><td>{e(b)}</td><td>{e(h)}</td></tr>" for sl, b, h in SCHEDULERS if sl in BY)
    verdicts = "".join(f"<li><strong>{L(sl)}</strong>: {e(BY[sl]['verdict'])}</li>" for sl, _, _ in SCHEDULERS if sl in BY)
    names = [BY[sl]["name"] for sl, _, _ in SCHEDULERS if sl in BY]
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / <a href="/category/growth/">Growth &amp; Notes</a> / Notes schedulers</div>
<h1>Substack Notes schedulers compared (2026)</h1>
<p class="small">Updated {e(data['generated'])} · {len(names) + 1} options, including Substack's own scheduler · Prices checked on each vendor's site · Independent, no affiliate links on this page</p>
<p><strong>The short answer:</strong> if you post a few Notes a week, use Substack's built-in scheduler. It's free, and Notes go out from Substack's own servers. Pay for a tool only when you want to batch a week or more at once: {L('buffer')} if Notes are one channel among several, {L('subflowai')} if you want the cheapest batch queue for Substack alone, and {L('writestack')} if you want the most complete Substack-only Notes suite.</p>
<h2>Start with the free built-in scheduler</h2>
<p>Substack schedules Notes natively on the web, iOS and Android. On the web, write your Note, click the calendar icon, choose <em>Schedule</em> and pick a time in your local time zone (on the apps, tap "…" first). Scheduled Notes appear in your Drafts tab, where you can edit them until they publish. The catch: you schedule one Note at a time, with no queue or calendar view. If that's fine for you, you don't need anything on this page.</p>
</div>
<h2>Side by side</h2><div class="table-wrap"><table class="cmp"><thead><tr><th>Tool</th><th>Price</th><th>Batch scheduling</th><th>How it publishes</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="prose">
<h2>How to choose</h2>
<ul>
<li><strong>You post to X, LinkedIn or Threads too:</strong> a multi-platform scheduler saves the most time. {L('buffer')}'s free plan covers up to 3 channels, and {L('typefully')} suits writers who start on X. Both free plans include Notes; see <a href="/compare/buffer-vs-typefully-substack-notes/">Buffer vs Typefully for Substack Notes</a>.</li>
<li><strong>Substack is your whole world and you want to batch cheaply:</strong> {L('subflowai')} (about $1.17/mo on its 5-year plan) or {L('notesiq')} ($4.99 one time, but very new).</li>
<li><strong>You want analytics and scheduling in one place:</strong> {L('notestack')} or {L('writestack')}. Both rank Notes by the subscribers they bring, not just likes.</li>
<li><strong>You start from long-form posts and publish beyond Substack:</strong> {L('narrareach')} turns articles into Notes and cross-posts to other platforms.</li>
<li><strong>You only want to know which Notes work:</strong> skip scheduling and use a read-only tool such as {L('subshack')} (free) or {L('substack-insights')}. See our <a href="/compare/substack-insights-vs-notestack/">Substack Insights vs NoteStack comparison</a>.</li>
</ul>
<h2>Know how a tool publishes before you install it</h2>
<p>Most Substack-only schedulers work through your logged-in Substack session: a browser extension acting as you, or a service holding your session. That's how this category works, not a red flag by itself, but read each tool's privacy page, prefer tools that never post without your approval, and avoid anything that follows, likes or messages people automatically. If a tool stops working after a Substack change, the built-in scheduler is always there as a fallback.</p>
<h2>A note on AI-written Notes</h2>
<p>Several of these tools can draft Notes from your articles "in your voice". Readers follow you for how you think, so treat AI drafts as a starting point and rewrite them before scheduling. Batch scheduling helps you stay consistent; it doesn't replace replying to people, which is where much of the growth on Notes comes from.</p>
<h2>Our verdicts</h2><ul>{verdicts}</ul>
<h2>Sources</h2><ul>
<li><a href="https://substack.com/@substackteam/note/c-232140059" target="_blank" rel="noopener">Substack Team: "Scheduling Notes is officially here" (how to schedule a Note)</a></li>
<li><a href="https://buffer.com/resources/substack-notes-scheduler/" target="_blank" rel="noopener">Buffer: The best Substack Notes schedulers in 2026 (how each tool publishes, per Buffer)</a></li>
<li>Each tool's own site, linked from its StackKit page (pricing and publishing method checked on the dates shown there).</li>
</ul>
<p class="small">Prices change; confirm on each vendor's site. See <a href="/about/">how we verify tools</a>, <a href="/free-substack-tools/">all free tools</a>, and our <a href="/guides/{GUIDE_SLUG}/">2026 growth guide</a>.</p></div></div>{SIGNUP}"""
    faq = [("Can you schedule Substack Notes for free?", "Yes. Substack's built-in scheduler is free on web, iOS and Android: click the calendar icon in the Notes composer, choose Schedule and pick a time. It schedules one Note at a time; scheduled Notes wait in your Drafts tab."),
           ("What is the best Substack Notes scheduler?", "For a few Notes a week, Substack's built-in scheduler. For batching, Buffer if you also post to other networks, SubflowAI for the cheapest Substack-only batch queue, and WriteStack for the most complete Substack-only Notes suite.")]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": "Substack Notes schedulers compared (2026)", "dateModified": data["generated"],
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE_URL + SCHED_SLUG,
           "about": [{"@type": "SoftwareApplication", "name": BY[sl]["name"], "url": BY[sl]["url"]} for sl, _, _ in SCHEDULERS if sl in BY]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    write(SCHED_SLUG, layout(SCHED_SLUG, f"Substack Notes schedulers compared: {len(names) + 1} options with real prices (2026) | {BRAND}",
        "Every way to schedule Substack Notes in 2026, compared: Substack's free built-in scheduler vs " + ", ".join(names[:-1]) + " and " + names[-1] + ". Prices, batch limits and how each tool publishes.", body, ld), "0.9")

# ---------------- Substack SEO guide (long-form) ----------------
SEO_SLUG = "/guides/substack-seo-guide/"
SEO_TOOLS = ["google-search-console", "google-analytics", "google-trends", "plausible", "subshack", "chatgpt", "claude", "perplexity"]
# Every claim checked 2026-10-25 on the sources listed at the bottom of the page.
def seo_guide():
    tl = "".join(f'<li>{L(s)}: {e(BY[s]["best_for"])}. <em>{e(BY[s]["pricing"])}</em></li>' for s in SEO_TOOLS if s in BY)
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / Guides / Substack SEO</div>
<h1>Substack SEO: how to get your posts found on Google and in AI answers (2026)</h1>
<p class="small">Updated {e(data['generated'])} · Every setting below checked against Substack's own SEO guide · Independent, not affiliated with Substack Inc.</p>
<p><strong>The short version:</strong> Substack already makes your public posts indexable, so SEO on Substack comes down to a few fields and habits you control: a plain-language SEO title and description on each post, a post URL you never change after publishing, links from your popular posts to your new ones, links to your publication from other sites, and keeping your evergreen how-to posts free so search engines and AI crawlers can read them. Connect Google Search Console to see which of those changes are working.</p>
<h2>Why search still matters on a newsletter platform</h2>
<p>Most Substack growth comes from inside Substack: Notes, recommendations and the app. Search is the channel that keeps working on posts you wrote months ago. It also feeds AI assistants: as writer Jenny Ouyang explains in a Code Like a Girl guide, AI tools often answer by asking a search engine and writing from the top results (she names Google for Gemini, Brave for Claude and Bing for ChatGPT), so a page search engines can't find is unlikely to be cited. Ranking well doesn't guarantee an AI will quote you, but not being indexed almost guarantees it won't.</p>

<h2>1. Fill in the SEO fields on every post</h2>
<p>Open a draft, click <strong>Settings</strong>, and expand <strong>SEO options</strong>. There you can set four things: the SEO title, the SEO description, the post URL and the social preview image. According to Substack, these fields don't change how the post looks in subscribers' inboxes, in the app or on your Substack site. They only suggest to search engines how to display the post.</p>
<p>If you leave them blank, Substack fills them in for you: the SEO title from your headline, the description from your subtitle, and the URL from your title. Substack says the defaults are fine for many writers. They fall short when your headline is clever rather than literal, which is common in newsletters.</p>
<h3>SEO title</h3>
<p>This is the clickable headline in search results, and it can differ from the headline your readers see. Keep the reader headline playful if you like, and make the SEO title plain: the words a stranger would actually type. Substack's own advice:</p>
<ul>
<li><strong>Stay under 60 characters</strong>, or search engines may cut it off or rewrite it.</li>
<li><strong>Use keywords naturally.</strong> A stuffed title reads badly and search engines can tell.</li>
<li><strong>Make it unique.</strong> If you run a recurring series with the same name, give each issue a distinct SEO title.</li>
<li><strong>Add your name or brand at the end</strong> if people already search for it.</li>
</ul>
<h3>SEO description</h3>
<p>This is the short summary under the title in search results; by default it's your subtitle. Don't repeat the title. Add the context and the related phrases that didn't fit, and write it like a one-line ad for the reader you want to reach.</p>
<h3>Post URL</h3>
<p>Substack builds the URL from your title (yourname.substack.com/p/post-title), and that's usually fine. If your headline is obscure, you can edit the end of the URL to match your plainer SEO title, <strong>but only before you publish</strong>. Changing the URL of a published post breaks every link already shared. Jenny Ouyang learned this the hard way when changing the address of her most-clicked page turned it into a page-not-found error overnight.</p>
<h3>Social preview image</h3>
<p>The image shown when your post is shared. Substack reports that posts with a social preview image get on average twice as many signups and 40% more clicks than those without. By default it's the first image in your post, or your publication logo if there isn't one. A tool like {L('canva')} makes a consistent template easy.</p>

<h2>2. Write for the question, not just the idea</h2>
<p>Substack's guide suggests starting with who you want to reach and what they might be searching for, since many searches start as a question. Two practical habits from Jenny Ouyang's playbook:</p>
<ul>
<li><strong>Check ideas against real searches.</strong> Before writing, see whether people actually search for the topic. {L('google-trends')} shows relative interest for free; once you have data, Search Console shows the exact phrases that already bring people to you.</li>
<li><strong>Answer in the first paragraph.</strong> Say what the post is about and name the real things in it (the tool, the problem, the result) in the first few lines, then show how you got there. Skimmers and machines both decide quickly.</li>
</ul>
<p>Don't make several posts compete for the same search. If three of your posts already target it, don't write a fourth.</p>

<h2>3. Link your own posts together</h2>
<p>You can't touch the technical settings a web developer would on Substack, so links between your own posts are one of the few levers you control. When you publish something new, add a sentence and a link to it from your most-visited related post. It helps readers and gives the new page a path for search engines to find it.</p>

<h2>4. Get links from outside Substack</h2>
<p>Substack calls inbound links (links to your publication from other sites) the best way to improve your search ranking. The simple ones:</p>
<ul>
<li>Put your Substack URL on your personal website, or embed a signup form there. Substack's native embed works; {L('supascribe')} adds styled forms and popups.</li>
<li>Put it in every social bio. {L('linktree')} works too, but your Substack homepage can often be the link.</li>
<li>Link generously to other writers in your niche. Links between related writers help readers and search engines see how a topic fits together, and other writers are more likely to link back.</li>
</ul>
<p>On your publication's address: if people search for your name, Substack recommends using it in your subdomain. Substack also notes that the default yourname.substack.com address borrows from Substack's existing search reputation, which is worth weighing before you switch to a custom domain.</p>

<h2>5. Keep evergreen guides free</h2>
<p>Search engine and AI crawlers don't have subscriptions, so anything behind your paywall is invisible to them. A useful rule from Jenny Ouyang: "sell narrow, talk broad." Keep the how-to posts that stay useful for years free and public, and put the paywall on deep dives and member-only material your existing readers pay for.</p>

<h2>6. Measure with Google Search Console</h2>
<p>{L('google-search-console')} is free and shows which of your pages Google has indexed, the searches people used to find you, and how often they clicked. Substack's help center says Search Console verification becomes available as a publication grows, so it may not be offered on a brand-new Substack. Once connected:</p>
<ul>
<li><strong>Find pages with many impressions and few clicks.</strong> Those are shown in results but skipped, and a better SEO title and description usually help them first.</li>
<li><strong>Look at the queries.</strong> They tell you how readers phrase your topics, which feeds back into step 2.</li>
<li><strong>Check after a few months.</strong> Search data builds slowly, so connect it early.</li>
</ul>
<p>Add {L('google-analytics')} (free) or {L('plausible')} if you want to see what visitors do after they land. Jenny Ouyang also recommends adding <a href="https://www.bing.com/webmasters/" target="_blank" rel="noopener">Bing Webmaster Tools</a> (free), which can import your site from Search Console, since some AI tools search the web through Bing.</p>

<h2>A one-hour starter checklist</h2>
<ol>
<li>Connect Google Search Console if your publication can.</li>
<li>Rewrite the SEO title and description on your three most-read posts.</li>
<li>Add a link from your most-visited post to your newest related post.</li>
<li>Make sure your best evergreen how-to is free and public.</li>
<li>Add your Substack URL to your website and social bios.</li>
<li>From now on, set the SEO fields (and settle the URL) before you hit publish.</li>
</ol>

<h2>Using AI to draft SEO titles</h2>
<p>An AI assistant such as {L('chatgpt')}, {L('claude')} or {L('perplexity')} can suggest options if you paste in your draft and ask for a few SEO titles under 60 characters and descriptions of roughly 155 characters or less. Treat the output as suggestions: check that each one is accurate, sounds like you, and doesn't promise more than the post delivers.</p>

<h2>Tools mentioned in this guide</h2><ul>{tl}</ul>
<h2>Sources</h2><ul>
<li><a href="https://on.substack.com/p/substack-seo-guide" target="_blank" rel="noopener">Substack: A guide to SEO on Substack</a> (SEO options, title length, URL and social preview advice, inbound links, subdomain advice)</li>
<li><a href="https://support.substack.com/hc/en-us/articles/4407702258836-How-can-I-optimize-my-Substack-publication-for-SEO" target="_blank" rel="noopener">Substack Help Center: How can I optimize my Substack publication for SEO?</a> (Search Console availability)</li>
<li><a href="https://codelikeagirl.substack.com/p/substack-seo-google-ai-search" target="_blank" rel="noopener">Code Like a Girl with Jenny Ouyang: Your Best Post is Hiding From Google</a> (search and AI answers, internal links, "sell narrow, talk broad", Bing Webmaster Tools, the changed-URL lesson)</li>
</ul>
<p class="small">Substack's settings change; if something here no longer matches what you see, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. More: our <a href="/guides/{GUIDE_SLUG}/">2026 growth guide</a>, the <a href="/guides/substack-recommendations-guide/">Substack recommendations and lists guide</a>, <a href="/free-substack-tools/">free tools for Substack writers</a> and the <a href="/category/analytics/">analytics tools</a> category.</p></div></div>{SIGNUP}"""
    faq = [("Do Substack posts show up on Google?", "Yes. Public Substack posts can be indexed by search engines. Paywalled content can't be read by crawlers, so keep the posts you want found free and public."),
           ("How do I change the SEO title on a Substack post?", "Open the post's Settings, expand SEO options, and edit the SEO title. It only changes how the post appears in search results, not in email, the app or on your Substack site. Substack recommends keeping it under 60 characters."),
           ("Can I change a Substack post URL after publishing?", "You can, but Substack advises against it: editing the URL after publishing breaks every existing link to the post. Settle the URL before you publish."),
           ("Should I use a custom domain for Substack SEO?", "Either works. Substack notes that the default substack.com subdomain benefits from Substack's existing search reputation; if people search for your name, use it in your subdomain.")]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": "Substack SEO: how to get your posts found on Google and in AI answers (2026)", "dateModified": data["generated"],
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE_URL + SEO_SLUG},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    write(SEO_SLUG, layout(SEO_SLUG, f"Substack SEO guide: get found on Google and AI search (2026) | {BRAND}",
        "How to do SEO on Substack in 2026: set SEO titles and descriptions, never change a published URL, link posts together, earn inbound links, keep evergreen posts free, and measure with Google Search Console.", body, ld, current=SEO_SLUG), "0.9")

# ---------------- Substack recommendations & lists guide (long-form) ----------------
REC_SLUG = "/guides/substack-recommendations-guide/"
REC_TOOLS = ["stackbuddy", "stackstats", "sparkloop"]
# Every Substack claim checked 2026-10-30 on the Substack sources listed at the bottom of the page (help articles updated Oct 29, 2026; lists launched Oct 29, 2026).
def rec_guide():
    tl = "".join(f'<li>{L(s)}: {e(BY[s]["best_for"])}. <em>{e(BY[s]["pricing"])}</em></li>' for s in REC_TOOLS if s in BY)
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / Guides / Substack recommendations</div>
<h1>Substack recommendations and lists: how to use them to grow (2026)</h1>
<p class="small">Updated {e(data['generated'])} · Every setting below checked against Substack's own help center, including the lists feature launched Oct 29, 2026 · Independent, not affiliated with Substack Inc.</p>
<p><strong>The short version:</strong> recommendations are free, built into Substack, and one of the main ways publications grow there. Recommend a handful of publications your readers would genuinely like, write a one-or-two-sentence reason for each, and keep "Include in recommendation digests" switched on. Since Oct 29, 2026 you can also sort recommendations into themed lists that readers can save, which puts the posts and Notes of everyone on the list into their Home feed. Check your Recommendations page every month or so to see which publications send you subscribers and which you send subscribers to.</p>

<h2>What a recommendation actually does</h2>
<p>When you recommend a publication, Substack shows it to your readers in several places (per Substack's help center):</p>
<ul>
<li><strong>Right after someone subscribes to you.</strong> New subscribers may see your recommendations straight after signing up, with up to 3 ready to subscribe to for free in one click. This is the big one, because it happens at the moment a reader is most open to trying something new.</li>
<li><strong>On your homepage</strong>, in the sidebar, and on your recommendations page at your.substack.com/recommendations.</li>
<li><strong>In recommendation digest emails</strong> that Substack sends to your subscribers now and then.</li>
<li><strong>On your Substack profile</strong>, on the web and in the app.</li>
</ul>
<p>It works in both directions. Every writer who recommends you puts your publication in front of their new subscribers, and that's why recommendations are one of the main ways writers grow on Substack. Substack's announcement of lists makes another point worth repeating: recommendations are free and nobody pays to be on a list, so a spot on one carries real weight with readers.</p>

<h2>1. Set up your first recommendations</h2>
<p>You need to be an owner or admin of your publication. Then:</p>
<ol>
<li>In your dashboard, open <strong>Audience</strong>, then <strong>Recommendations</strong>.</li>
<li>Click <strong>Add recommendation</strong> and search for a person or publication.</li>
<li>Write a reason for recommending (optional, up to 500 characters). Substack suggests a sentence or two about why you love it, to help your readers decide.</li>
<li>Click <strong>Add recommendation</strong>.</li>
</ol>
<p>There are shortcuts too. After you publish a post that links to other Substacks, Substack offers to recommend them. On any creator's profile you can click the three-dot menu and choose <strong>Recommend</strong>. And when you subscribe to a publication, Substack may ask whether you want to recommend it. You can't recommend your own publication or a private one.</p>

<h2>2. Choose recommendations your readers will thank you for</h2>
<p>A recommendation is a small promise to your readers: "if you like this, you'll like that." A few rules of thumb (our advice, not Substack's):</p>
<ul>
<li><strong>Recommend what you actually read.</strong> Your readers trust your taste; a list of strangers you swapped with spends that trust.</li>
<li><strong>Pick neighbors, not clones.</strong> A publication on a related topic gives your readers something new without competing for the same inbox slot.</li>
<li><strong>Lead with your strongest few.</strong> New subscribers may be offered up to 3 at sign-up, so the first impression comes from a small set.</li>
<li><strong>Make sure they're active.</strong> A publication only appears in digest emails if it has at least 3 published posts and has posted in the last 30 days, so a dormant pick does less for your readers and for the writer.</li>
</ul>

<h2>3. Write a reason, every time</h2>
<p>The reason (up to 500 characters) appears with your recommendation and is part of what Substack sends the writer you recommended. Say who it's for and what they'll get: "If you liked my post on pricing, Jane's weekly teardown of real creator offers is the next thing to read" does more than "Great newsletter!" If a publication is on several of your lists, its reason is the same on every list, so update it in one place and it changes everywhere.</p>

<h2>4. Turn your recommendations into lists (new, Oct 2026)</h2>
<p>Substack launched lists on Oct 29, 2026 as "the next generation of recommendations." You can sort the publications you recommend into themed lists, like "My favorite food writers" or "Mood boosters," each with its own name, description, link and chronological activity feed of posts and Notes from everyone on it.</p>
<h3>How to make a list</h3>
<ol>
<li>On the web version of your Substack, click <strong>Recommendations</strong> in the left sidebar.</li>
<li>Under <strong>Your lists</strong>, click <strong>New list</strong>.</li>
<li>Give it a <strong>Name</strong> (up to 100 characters) and a <strong>Description</strong> that says what ties the list together.</li>
<li>Check the pre-filled public link or make your own (custom list links can only be made on the web).</li>
<li>Click <strong>Save changes</strong>, then <strong>Add publication</strong> for each publication, with an optional reason.</li>
</ol>
<p>In the app, go to your profile, tap <strong>Recommendations and Subscriptions</strong>, open the <strong>Lists</strong> tab and tap <strong>Create new list</strong>. You can also add a publication from its profile with the three-dot menu and <strong>Add to list</strong>.</p>
<h3>What to know about lists</h3>
<ul>
<li><strong>Your existing recommendations become your first list</strong>, called Recommendations. It keeps the your.substack.com/recommendations link, so nothing you've shared breaks, and it can't be renamed or deleted. You can create up to 50 more.</li>
<li><strong>Every list is public</strong> to anyone with the link (if your publication is in private mode, only subscribers see your recommendations). All your lists appear together at your.substack.com/lists and on your profile.</li>
<li><strong>Saving a list changes a reader's feed.</strong> When a reader saves your list, new posts and Notes from the publications on it start showing up in their Home feed. Lists are dynamic, so if you add a publication later, people who saved the list see its new work too.</li>
<li><strong>Share them.</strong> A list can be shared on Notes, where it shows up as a card in the feed, or off Substack with a link.</li>
<li><strong>Measure them.</strong> The Your lists table shows Saves (all time) and Saves (30 days). You see how many people saved a list, not who. Substack's launch post adds that you can see how much traffic your list sent to each writer on it.</li>
</ul>
<h3>Lists that work</h3>
<p>Our suggestions: make lists around a reader's need rather than your social circle ("Substacks for first-time freelancers," "Weekly reads for small-business owners"). A list is the kind of thing a reader saves and shares, so a well-named niche list is also a reason for someone outside your audience to find your profile. Keep the main Recommendations list short and your best, and use themed lists for the longer tail.</p>

<h2>5. Check what's working</h2>
<p>Your Recommendations page shows how many publications recommend you and how many of your subscribers came from recommendations. Two tables break it down:</p>
<ul>
<li><strong>Incoming recommendations:</strong> Substacks that recommend you, with the subscriptions each sent you in the last 30 days and since they started.</li>
<li><strong>Outgoing recommendations:</strong> Substacks you recommend, with the subscriptions you've sent them.</li>
</ul>
<p>These numbers count free subscriptions. If you remove a recommendation that sent you subscribers in the past, it moves to the Inactive tab, and you can bring it back with <strong>Recommend</strong>. For deeper analysis of where subscribers come from, {L('stackstats')} works from your own Substack exports.</p>

<h2>6. Digests, notifications and the settings that matter</h2>
<p>Three settings in your Recommendations settings apply to all your recommendations at once:</p>
<ul>
<li><strong>Include in recommendation digests.</strong> Digests are occasional emails introducing your subscribers to publications you recommend. Each subscriber gets one about once a month at most, featuring up to 4 publications. A publication is only included if both you and it have this setting on, it has at least 3 posts and posted in the last 30 days, and the reader doesn't already subscribe. Turning it off also removes you from digests of recommendations others make of you, so leave it on unless you have a reason.</li>
<li><strong>Show recommendations on homepage</strong> controls the sidebar on your website.</li>
<li><strong>Manage recommendation blurbs</strong> lets you choose which blurbs other writers have written about you appear on your welcome page. A good blurb from a respected writer is social proof at sign-up, so pick your best.</li>
</ul>
<p><strong>Will they know?</strong> Substack emails a creator about your recommendation if they subscribe to you, or once your recommendation has brought them a meaningful share of their new subscribers. The email includes your reason and, when available, how many subscribers you've sent. If neither happens within two months, no email is sent. Creators can turn these emails off with the New recommenders setting.</p>
<p><strong>Removing yourself:</strong> the only way to take your publication off someone else's recommendations and lists is to block them, which also unsubscribes and unfollows you from each other and removes any recommendation you made of them.</p>

<h2>7. Earn recommendations without begging for them</h2>
<p>Recommendations follow relationships. The approaches we see work (our advice):</p>
<ul>
<li><strong>Recommend first, with a real reason.</strong> Substack may email the writer with your reason once you send them subscribers, which is a far better introduction than a cold DM asking for a swap.</li>
<li><strong>Link to other writers in your posts.</strong> It helps your readers, and Substack offers to turn those links into recommendations when you publish.</li>
<li><strong>Be useful in comments and Notes.</strong> Thoughtful replies on other writers' posts are how most writers meet the people who later recommend them.</li>
<li><strong>Make a list worth being on.</strong> A carefully curated niche list is something writers are glad to share, which brings readers to your profile too.</li>
</ul>
<p>If you'd like help finding writers to cross-promote with, {L('stackbuddy')} includes a creator network. Outside Substack's own system, {L('sparkloop')} runs a separate recommendation network with paid referrals; see its page for how that works and what it costs.</p>

<h2>A 20-minute starter checklist</h2>
<ol>
<li>Open Audience → Recommendations and look at your incoming and outgoing numbers.</li>
<li>Add 3 to 5 publications your readers would genuinely like, each with a one- or two-sentence reason.</li>
<li>Check that "Include in recommendation digests" and "Show recommendations on homepage" are on.</li>
<li>Make one themed list around a reader's need, with a clear name and description.</li>
<li>Share the list in a Note so it appears as a card in the feed.</li>
<li>Set a monthly reminder to review what recommendations sent you and what you sent others.</li>
</ol>

<h2>Tools mentioned in this guide</h2><ul>{tl}</ul>
<h2>Sources</h2><ul>
<li><a href="https://support.substack.com/hc/en-us/articles/5036794583828-How-can-I-recommend-other-publications-on-Substack" target="_blank" rel="noopener">Substack Help Center: How can I recommend other publications on Substack?</a> (updated Oct 29, 2026: setup, where recommendations appear, digests, stats, notifications, blocking, up to 50 more lists)</li>
<li><a href="https://support.substack.com/hc/en-us/articles/54727840919700-How-do-I-create-a-list-of-recommended-publications" target="_blank" rel="noopener">Substack Help Center: How do I create a list of recommended publications?</a> (updated Oct 29, 2026: creating lists on web and app, public links, saves, your.substack.com/lists)</li>
<li><a href="https://support.substack.com/hc/en-us/articles/7208782994580-What-are-recommendations-digests" target="_blank" rel="noopener">Substack Help Center: What are recommendations digests?</a> (opting out)</li>
<li><a href="https://on.substack.com/p/introducing-lists-on-substack" target="_blank" rel="noopener">On Substack: Introducing lists on Substack</a> (Oct 29, 2026: activity feeds, dynamic lists, sharing on Notes, traffic per writer, "nobody pays to be on a list")</li>
</ul>
<p class="small">Substack's settings change; if something here no longer matches what you see, email <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>. More: our <a href="/guides/{GUIDE_SLUG}/">2026 growth guide</a>, the <a href="/guides/substack-seo-guide/">Substack SEO guide</a>, <a href="/substack-notes-schedulers/">Substack Notes schedulers compared</a> and the <a href="/category/growth/">growth tools</a> category.</p></div></div>{SIGNUP}"""
    faq = [("How do recommendations work on Substack?", "When you recommend a publication, Substack can show it to your new subscribers right after they sign up (up to 3, one click to subscribe for free), in your homepage sidebar and recommendations page, in occasional digest emails to your subscribers, and on your profile. Writers who recommend you do the same for your publication."),
           ("How do I recommend another publication on Substack?", "In your dashboard, open Audience, then Recommendations, click Add recommendation, search for the publication, optionally write a reason (up to 500 characters) and click Add recommendation. You need to be an owner or admin of your publication."),
           ("What are Substack lists?", "Launched Oct 29, 2026, lists let you sort the publications you recommend into themed, public lists with their own link and activity feed. When a reader saves a list, new posts and Notes from the publications on it show up in their Home feed. Your existing recommendations become your first list, and you can create up to 50 more."),
           ("How often do Substack recommendation digests go out?", "Each subscriber gets a digest about once a month at most, featuring up to 4 publications. A publication is only included if both writers have digests turned on, it has at least 3 posts and has posted in the last 30 days, and the reader doesn't already subscribe."),
           ("Does it cost money to be recommended on Substack?", "No. Substack says recommendations are free and nobody pays to be on a list.")]
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": "Substack recommendations and lists: how to use them to grow (2026)", "dateModified": data["generated"],
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE_URL + REC_SLUG},
          {"@context": "https://schema.org", "@type": "HowTo", "name": "How to create a list of recommended publications on Substack",
           "step": [{"@type": "HowToStep", "text": t} for t in ["On the web version of your Substack, click Recommendations in the left sidebar.", "Under Your lists, click New list.", "Give the list a name (up to 100 characters) and a description.", "Check the public link or create your own, then click Save changes.", "Click Add publication, search for a publication, optionally write a reason, and click Add to list."]]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    write(REC_SLUG, layout(REC_SLUG, f"Substack recommendations and lists guide: grow with recommendations (2026) | {BRAND}",
        "How Substack recommendations and the new lists (Oct 2026) work: where recommendations appear, how to set them up, writing reasons, creating lists, digests, stats and how to earn recommendations.", body, ld, current=REC_SLUG), "0.9")

# ---------------- Comparisons ----------------
def compare(x):
    a, b = BY[x["a"]], BY[x["b"]]
    rows = "".join(f"<tr><th scope=\"row\">{e(k)}</th><td>{e(va)}</td><td>{e(vb)}</td></tr>" for k, va, vb in x["rows"])
    secs = "".join(f"<h2>{e(h)}</h2><p>{e(ptxt)}</p>" for h, ptxt in x["body"])
    srcs = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></li>' for n, u in x["sources"])
    cat = CAT[a["category"]]
    body = f"""<div class="wrap page"><div class="prose"><div class="crumbs"><a href="/">Directory</a> / <a href="/category/{cat['slug']}/">{e(cat['name'])}</a> / Comparison</div>
<h1>{e(x['h1'])}</h1>
<p class="small">Checked {e(x['checked'])} on the vendors' sites and Substack's help center · Independent, no affiliate relationship with either tool</p>
<p><strong>The short answer:</strong> {e(x['short'])}</p></div>
<h2>Side by side</h2><div class="table-wrap"><table class="cmp"><thead><tr><th></th><th><a href="/tools/{a['slug']}/">{e(a['name'])}</a></th><th><a href="/tools/{b['slug']}/">{e(b['name'])}</a></th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="prose">{secs}
<h2>Our verdicts</h2><ul><li><strong><a href="/tools/{a['slug']}/">{e(a['name'])}</a>:</strong> {e(a['verdict'])}</li><li><strong><a href="/tools/{b['slug']}/">{e(b['name'])}</a>:</strong> {e(b['verdict'])}</li></ul>
<h2>Sources</h2><ul>{srcs}</ul>
<p class="small">Prices change; confirm on each vendor's site. See <a href="/about/">how we verify tools</a>. More tools like these: <a href="/category/{cat['slug']}/">{e(cat['name'])}</a>.</p></div></div>{SIGNUP}"""
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": x["title"], "dateModified": x["checked"], "description": x["desc"],
           "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}, "mainEntityOfPage": SITE_URL + f"/compare/{x['slug']}/",
           "about": [{"@type": "SoftwareApplication", "name": a["name"], "url": a["url"]}, {"@type": "SoftwareApplication", "name": b["name"], "url": b["url"]}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": f"{a['name']} or {b['name']}: which is better for Substack?",
           "acceptedAnswer": {"@type": "Answer", "text": x["short"]}}]}]
    write(f"/compare/{x['slug']}/", layout(f"/compare/{x['slug']}/", f"{x['title']} | {BRAND}", x["desc"], body, ld), "0.8")

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
             f"- [Free tools for Substack writers]({SITE_URL}/free-substack-tools/): every listed tool with a free plan ({sum(1 for t in TOOLS if t.get('free_plan'))}), grouped by category, with free-plan limits and paid prices",
             f"- [Substack SEO guide]({SITE_URL}/guides/substack-seo-guide/): how to get Substack posts found on Google and in AI answers: SEO title, description and URL settings, internal and inbound links, keeping evergreen posts free, and measuring with Google Search Console",
             f"- [Substack recommendations and lists guide]({SITE_URL}/guides/substack-recommendations-guide/): how Substack recommendations and the new lists (launched Oct 29, 2026) work: where recommendations appear, setup, writing reasons, creating themed lists, digest rules, stats, and how to earn recommendations",
             f"- [Substack Notes schedulers compared]({SITE_URL}/substack-notes-schedulers/): Substack's free built-in Notes scheduler vs every third-party scheduler in the directory, with prices, batch limits and how each one publishes",
             *[f"- [{x['title']}]({SITE_URL}/compare/{x['slug']}/): {x['short']}" for x in COMPARISONS],
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
    for x in COMPARISONS: compare(x)
    feature(); about(); guide(); free_tools(); schedulers(); seo_guide(); rec_guide(); extras()
    open(os.path.join(OUT, "CNAME"), "w").write(SITE_URL.split("://", 1)[1] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"Built {len(pages)} pages into {OUT} (SITE_URL={SITE_URL})")

if __name__ == "__main__": main()
