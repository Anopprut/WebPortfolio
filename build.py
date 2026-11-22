"""Portfolio site for noppruts (นพรุจ). python build.py -> dist/ ; deploy with products/shop-tools/fee-reader/deploy.py.

Portfolio (English) is built from facts read in the author's own project READMEs/docstrings. No invented metrics, clients,
credentials or reviews. Product pages (Thai) target Thai sellers' search queries.
Optional config.json: {"base": "...", "contact": [{"label": "Facebook", "url": "https://..."}], "sameAs": ["https://..."]}
"""
import base64
import html
import json
import shutil
import subprocess
import sys
from datetime import date

from articles import ARTICLES, CHECKED
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
cfg = {"base": "https://nopprut.pages.dev", "contact": [], "sameAs": [], "email": "", "n8n_affiliate_url": "", "store_url": "", "fastwork_url": ""}
if (H / "config.json").exists():
    cfg.update(json.loads((H / "config.json").read_text(encoding="utf-8")))
BASE = cfg["base"].rstrip("/")
TODAY = date.today().isoformat()
HANDLE, THAI = "noppruts", "นพรุจ"
FREE_TOOL = "https://fee-reader-free.pages.dev/"
SRC = "https://flowaccount.com/blog/commission-fees-ecommerce-shopee-lazada-tiktok/"
OUT = H / "dist"
(OUT / "assets").mkdir(parents=True, exist_ok=True)

def hire_box(seller=False):
    u = cfg.get("fastwork_url", "")
    if not u:
        return ""
    what = ("ต้องกรอกยอดขายหรือเช็กออเดอร์ด้วยมือทุกวัน? ผมรับทำระบบสรุปยอดรายวันและแจ้งเตือนออเดอร์ใหม่ (n8n + Google Sheets + LINE/Telegram) ให้ร้านออนไลน์"
            if seller else "รับทำระบบอัตโนมัติ n8n, LINE OA / Telegram Bot และงานเชื่อมระบบสำหรับร้านค้าและทีมเล็ก")
    return ('<div class="box"><b>อยากให้ผมทำให้?</b> ' + what + ' <a href="' + html.escape(u) + '" rel="noopener">ดูบริการของผมบน Fastwork</a> '
            'ส่งโจทย์มาให้ประเมินขอบเขตและราคาก่อนจ้างได้</div>')


# ------------------------------------------------------------------ data (all from the author's own folders)
FEATURED = [
    dict(cat="geo", title="SAR Crop-Damage Verification", sub="Parcel-level flood & crop damage from free satellite radar",
         body="Turns open Sentinel-1 SAR imagery into per-plot flood and crop-damage estimates for Thai rice insurers and lenders. "
              "A rice-transplanting mask avoids flagging normal wet paddy as damage, and every result carries scene IDs, software versions, "
              "parameters and a confidence score so it can be defended in a claims dispute. Flood/damage module implemented; crop and carbon modules are interfaces for later.",
         tags=["Python", "Sentinel-1 SAR", "PostGIS", "Zarr", "Docker"]),
    dict(cat="auto", title="AI Content Factory (n8n + Python)", sub="Idea → finished 9:16 video, with a human gate before publishing",
         body="n8n decides what to make and when (scheduling, topic selection, approval routing, analytics); a Python video factory turns a topic into a subtitled "
              "vertical video (script, video generation, TTS, FFmpeg) behind a local HTTP API with a restart-safe state machine. Nothing publishes without explicit approval.",
         tags=["n8n", "Python", "FFmpeg", "TTS", "Facebook Graph API"]),
    dict(cat="agents", title="LINE AI Assistant for a Repair Shop", sub="Diagnosis help for staff, service reminders for customers",
         body="One LINE Official Account serving two audiences: staff send fault codes or symptoms for an AI diagnosis and log completed jobs; customers link their LINE to their phone "
              "number and receive a reminder when the ~6-month service is due. A daily scheduler inside the same process pushes the reminders.",
         tags=["Python", "LINE Messaging API", "APScheduler", "Flex Messages", "LLM"]),
    dict(cat="agents", title="Agent Invest", sub="Multi-agent investment monitoring · built with a teammate",
         body="Full-stack system: FastAPI backend and Next.js dashboard where several AI agents analyse symbols, store predictions and compare them with later prices to track accuracy per "
              "timeframe. Builds daily reports and talks to users through a Telegram bot by command or natural language.",
         tags=["FastAPI", "Next.js", "Telegram Bot", "Docker", "LLM agents"],
         links=[("https://github.com/nattakit2580/Agent-Invest", "Team repo on GitHub")]),
    dict(cat="auto", title="LendLoop", sub="Tool-lending board with signed, idempotent automation",
         body="Neighbours list tools, request them for a date range, and lenders approve or decline. Next.js and TypeScript with Clerk auth and a Convex backend; n8n sends notifications and daily overdue reminders through HMAC-signed webhooks with retries and backoff, and each reminder is idempotent so nobody is nagged twice. Built as a take-home project.",
         tags=["Next.js", "TypeScript", "Convex", "Clerk", "n8n"],
         links=[("https://github.com/Anopprut/lendloop", "Source on GitHub")]),
    dict(cat="agents", title="Test-Eng Assist", sub="Local RAG agent for test engineers",
         body="Autonomous local CLI agent for test engineers: an agent loop that calls tools, plus document ingestion, RAG, a scheduler and a dashboard; packaged as an executable.",
         tags=["Python", "Typer", "RAG", "Scheduler"]),
]
MORE = [
    dict(cat="agents", title="LangGraph Test-Log Triage (demo)", body="Demo agent that reads test-failure logs, groups them by likely cause and drafts a triage note. Runs on synthetic data only.", tags=["Python", "LangGraph", "Synthetic data"], links=[("https://github.com/Anopprut", "GitHub profile")]),
    dict(cat="tools", title="TypeScript SPC Analyzer (demo)", body="Statistical process control charts and out-of-control rules in TypeScript, the kind of check used on a test line. Demo on synthetic data.", tags=["TypeScript", "SPC", "Synthetic data"], links=[("https://github.com/Anopprut", "GitHub profile")]),
    dict(cat="agents", title="Autonomous Agent Loop", body="Plan → split into sub-tasks → call tools → verify → repeat until done, with a multi-agent orchestrator and a sandboxed workspace.", tags=["Python", "Multi-agent"]),
    dict(cat="agents", title="Windows Computer-Control Agent", body="ReAct loop: capture the screen, ask a vision-language model for the next action, run it through GUI/shell tools, observe, repeat until the goal is met.", tags=["Python", "VLM", "Automation"]),
    dict(cat="auto", title="News Pipeline with Telegram Approval", body="Runs three times a day on Bangkok time and routes each item through a Telegram bot for human approval before it goes out.", tags=["Python", "Telegram", "Scheduler"]),
    dict(cat="auto", title="LINE Slip-OCR Assistant", body="Photo of a trade slip → Thai+English OCR → Flex confirmation card → tax calculation → logged to an Excel workbook that doubles as the database.", tags=["Python", "EasyOCR", "LINE", "Excel"]),
    dict(cat="auto", title="Shop Automation Pack (n8n)", body="Two importable n8n workflows for small online shops: a daily sales summary and a new-order alert with validation. Run end-to-end on a local n8n instance with test data.", tags=["n8n", "Telegram", "Google Sheets"]),
    dict(cat="quant", title="Thai Stock Monitor", body="Watches SET/mai stocks, generates signals from price and indicator thresholds, simulates trades in a paper portfolio, alerts via Telegram/LINE, Next.js dashboard. Live execution deliberately not implemented.", tags=["Python", "Next.js", "yfinance"]),
    dict(cat="quant", title="Quant Signal Engine", body="Market data and news sentiment (FinBERT/VADER) combined with EMA, RSI, ATR and Kelly sizing to output signals with dynamic stop-loss and take-profit levels.", tags=["Python", "NLP", "Quant math"]),
    dict(cat="quant", title="Algorithmic Trading Research (private)", body="Research workflow built around a written edge standard: net-of-cost expectancy, out-of-sample tests, sample-size minimums and regime analysis. Findings are not published.", tags=["Python", "Backtesting", "HMM regimes"]),
    dict(cat="create", title="Character IP Studio", body="An orange-cat character and supporting cast turned into LINE sticker, emoji and theme packs, short animated films and wallpapers. Films come from a deterministic frame-accurate HTML engine rendered with Playwright and FFmpeg, with synthesised audio normalised to -14 LUFS.", tags=["Playwright", "FFmpeg", "NumPy", "LINE Creators"]),
    dict(cat="create", title="1-Minute Product Clip Generator", body="A product JSON and photo become a vertical clip with Thai voice-over in about a minute, without rendering a browser page per frame.", tags=["Python", "Pillow", "edge-tts", "FFmpeg"]),
    dict(cat="tools", title="Shop Fee Reader (live)", body="Mobile web tool that shows where each baht of a Shopee, TikTok Shop or Lazada sale goes, break-even price and break-even ROAS. All data stays in the browser. Free and paid editions are deployed on Cloudflare Pages.", tags=["JavaScript", "Cloudflare Pages"], link=(FREE_TOOL, "Try it")),
    dict(cat="tools", title="Stock & Sales Spreadsheet", body="Excel workbook for small shops with SUMIFS/INDEX-MATCH dashboards, low-stock alerts and charts. Every dashboard value was checked against an independent Python calculation.", tags=["Excel", "openpyxl"]),
    dict(cat="security", title="AppSec Testing & Remediation (OWASP Juice Shop)",
         body="Found and documented 3 real vulnerabilities (SQL injection auth bypass, IDOR, SQL injection + info disclosure) in a locally-run copy of OWASP's own intentionally-vulnerable training app, then patched the vulnerable code and re-verified against the original requests that the fixes held while legitimate use kept working. Full requests/responses and the code diff are in the reports.",
         tags=["AppSec", "SQL Injection", "Access Control", "Node.js/TypeScript"],
         links=[("/security/report-1-juice-shop.pdf", "Findings (PDF)"), ("/security/report-2-remediation.pdf", "Remediation (PDF)")]),
]
FILTERS = [("all", "All"), ("agents", "AI agents"), ("auto", "Automation"), ("geo", "Geospatial"), ("quant", "Quant"), ("create", "Creative"), ("tools", "Tools"), ("security", "Security")]
STACK = ["Python", "FastAPI", "Next.js", "n8n", "Docker", "PostGIS", "LINE Messaging API", "Telegram Bot API", "Playwright", "FFmpeg", "EasyOCR", "APScheduler", "Cloudflare Pages", "Excel / openpyxl"]

from stories_data import STORY_CSS, STORY_JS, story_html
CSS = """
:root{--bg:#0c0e13;--bg2:#12151c;--card:#151a23;--ink:#eef1f6;--mut:#9aa5b8;--line:#232a37;--acc:#ff8a3d;--acc2:#ffc15e;--glow:rgba(255,138,61,.18)}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 Inter,"Segoe UI","Sarabun","Noto Sans Thai",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--acc)}.wrap{max-width:1040px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 86%,transparent);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;height:58px}
.brand{font-weight:800;letter-spacing:.2px;color:var(--ink);text-decoration:none;display:flex;align-items:center;gap:10px}
.brand img{width:30px;height:30px;border-radius:50%;background:var(--glow);object-fit:cover}
nav a{color:var(--mut);text-decoration:none;margin-left:20px;font-weight:600;font-size:.95rem}nav a:hover{color:var(--ink)}
.hero{padding:64px 0 36px;background:radial-gradient(900px 380px at 78% -10%,var(--glow),transparent 70%)}
.hero .wrap{display:grid;grid-template-columns:1.5fr 1fr;gap:28px;align-items:center}
.eyebrow{color:var(--acc);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.78rem}
h1{font-size:clamp(2rem,5vw,3.2rem);line-height:1.12;margin:.35em 0 .4em;letter-spacing:-.02em}
h1 em{font-style:normal;background:linear-gradient(90deg,var(--acc),var(--acc2));-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{color:var(--mut);font-size:1.1rem;max-width:34em}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.btn{display:inline-block;padding:11px 20px;border-radius:12px;font-weight:700;text-decoration:none;border:1px solid var(--line);color:var(--ink);background:var(--card)}
.btn.p{background:linear-gradient(90deg,var(--acc),var(--acc2));color:#1a0f06;border:0}
.avatar{justify-self:center;width:min(300px,70vw);aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 50% 40%,var(--glow),transparent 70%);display:grid;place-items:center}
.avatar img{width:86%;filter:drop-shadow(0 16px 30px rgba(0,0,0,.3))}
section{padding:34px 0}h2{font-size:1.6rem;margin:0 0 6px;letter-spacing:-.01em}.sub{color:var(--mut);margin:0 0 20px}
.grid{display:grid;gap:16px}.g2{grid-template-columns:repeat(2,1fr)}.g3{grid-template-columns:repeat(3,1fr)}
.card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:20px;transition:transform .18s,border-color .18s}
.card:hover{transform:translateY(-3px);border-color:color-mix(in srgb,var(--acc) 55%,var(--line))}
.card h3{margin:0 0 2px;font-size:1.15rem}.card .s{color:var(--acc);font-weight:600;font-size:.9rem;margin-bottom:8px}.card p{color:var(--mut);margin:.4em 0 12px;font-size:.97rem}
.card.big{padding:24px}.card.big h3{font-size:1.3rem}
.tags{display:flex;flex-wrap:wrap;gap:6px}.tag{font-size:.76rem;padding:3px 10px;border-radius:99px;border:1px solid var(--line);color:var(--mut);background:var(--bg2)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 18px}.chip{cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--mut);padding:6px 14px;border-radius:99px;font:inherit;font-size:.9rem}
.chip.on{background:var(--acc);border-color:var(--acc);color:#1a0f06;font-weight:700}
.principles{grid-template-columns:repeat(3,1fr)}.principles .card h3{font-size:1.02rem}
.stack{display:flex;flex-wrap:wrap;gap:8px}.stack .tag{font-size:.88rem;padding:6px 14px}
footer{border-top:1px solid var(--line);margin-top:30px;padding:26px 0;color:var(--mut);font-size:.9rem}
.hide{display:none}
.secgrid{display:grid;grid-template-columns:1.1fr 1fr;gap:26px;margin-top:14px}
.subh{margin:0 0 10px;font-size:1.05rem}
.threats{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:8px}
.threats li{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}
.threats b{display:block;color:var(--acc2);font-size:.9rem;margin-bottom:2px}.threats span{color:var(--mut);font-size:.92rem;line-height:1.45}
.term{background:#07090d;border:1px solid var(--line);border-radius:12px;padding:14px 16px;font:.8rem/1.7 ui-monospace,Consolas,monospace;color:#c9d3e3;overflow:auto;margin:0;white-space:pre}
.term .c{color:#5f6b7e}.term .k{color:#7fb4ff}.term .w{color:#ff7a6b}.term .o{color:#6fdc9a}
.tbl{width:100%;border-collapse:collapse;margin:8px 0 12px;font-size:.88rem}.tbl th,.tbl td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.tbl th{color:var(--mut);font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.06em}
.sev{display:inline-block;border-radius:999px;padding:2px 10px;font-size:.75rem;font-weight:700;border:1px solid}
.sev.critical{color:#ff7a6b;border-color:#ff7a6b}.sev.high{color:#ffb35e;border-color:#ffb35e}.sev.medium{color:#f2dc6b;border-color:#f2dc6b}
@media(max-width:860px){.secgrid{grid-template-columns:1fr}}
.js .rv{opacity:0;transform:translateY(20px);transition:opacity .65s ease,transform .65s ease}.js .rv.in{opacity:1;transform:none}
.hero .hi{opacity:0;transform:translateY(18px)}html:not(.js) .hero .hi{opacity:1;transform:none}
html.go .hero .hi{animation:up .75s cubic-bezier(.2,.7,.2,1) both;animation-delay:calc(var(--d,0)*.12s)}
@keyframes up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.card{transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease}
.card:hover{transform:translateY(-5px);border-color:var(--acc);box-shadow:0 14px 34px -14px var(--glow)}
.photo .cat{transform-origin:50% 100%;animation:catlife 4.8s ease-in-out infinite;cursor:pointer;transition:filter .2s}
@keyframes catlife{0%,38%,100%{transform:translateY(0) rotate(0) scale(1,1)}
44%{transform:translateY(1px) rotate(0) scale(1.07,.9)}
52%{transform:translateY(-16px) rotate(-6deg) scale(.96,1.06)}
60%{transform:translateY(0) rotate(0) scale(1.08,.9)}
66%{transform:translateY(-4px) rotate(3deg) scale(1,1)}
72%{transform:translateY(0) rotate(-3deg)}
80%{transform:translateY(0) rotate(3deg)}
88%{transform:translateY(0) rotate(-2deg)}}
.photo .cat:hover{animation:cathop .55s ease-out 1;filter:drop-shadow(0 8px 16px rgba(255,140,40,.55))}
@keyframes cathop{0%{transform:scale(1,1)}25%{transform:translateY(0) scale(1.12,.86)}55%{transform:translateY(-22px) rotate(8deg) scale(.95,1.08)}80%{transform:translateY(0) scale(1.1,.9)}100%{transform:scale(1,1)}}
.hero.v2{--mx:70%;--my:20%;background-image:radial-gradient(520px circle at var(--mx) var(--my),var(--glow),transparent 65%)}
#sprog{position:fixed;top:0;left:0;height:3px;width:0;background:linear-gradient(90deg,var(--acc),var(--acc2));z-index:60}
.chip,.btn{transition:transform .2s,background .2s,border-color .2s}.btn:hover{transform:translateY(-2px)}
@keyframes upf{from{opacity:0}to{opacity:1}}
@media (prefers-reduced-motion:reduce){.js .rv,.hero .hi{transform:none!important}html.go .hero .hi{animation-name:upf!important}.photo .cat{animation-duration:6s}.card:hover,.btn:hover{transform:none}}
.ships{border:1px solid var(--line);border-radius:16px;background:var(--card);padding:18px 20px 12px;margin-top:14px}
.sbar{height:3px;background:var(--line);border-radius:3px;overflow:hidden;margin-bottom:14px}.sbar i{display:block;height:100%;width:25%;background:linear-gradient(90deg,var(--acc),var(--acc2));transition:width .5s}
.stabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.stab{font:inherit;color:var(--mut);background:transparent;border:1px solid var(--line);border-radius:999px;padding:7px 14px;cursor:pointer}
.stab .mono{color:var(--acc);margin-right:4px}.stab.on{color:var(--ink);border-color:var(--acc);background:var(--glow)}
.spanel{display:none}.spanel.on{display:block;animation:fi .4s}.spanel h3{margin:4px 0 6px}.spanel p{color:var(--mut);max-width:62ch}
@keyframes fi{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.ships .note{font-size:.75rem;color:var(--mut);text-align:right;margin:6px 0 0}


/* article pages */
.page{max-width:760px;margin:0 auto;padding:30px 20px}.page h1{font-size:1.9rem}.page h2{margin-top:1.8em}
table{width:100%;border-collapse:collapse;font-size:.95rem}th,td{border-bottom:1px solid var(--line);padding:8px 6px;text-align:left}.tl{overflow-x:auto}
details{border-bottom:1px solid var(--line);padding:9px 0}summary{cursor:pointer;font-weight:700}.note{color:var(--mut);font-size:.9rem}
pre{background:var(--bg2);border:1px solid var(--line);padding:12px;border-radius:12px;overflow:auto;font-size:.85rem;line-height:1.5}code{font-family:ui-monospace,Consolas,monospace;font-size:.9em}.box{border:1px solid var(--line);border-radius:14px;padding:12px 14px;margin:18px 0;background:var(--card)}ol li,ul li{margin:.3em 0}
@media(max-width:760px){.hero .wrap{grid-template-columns:1fr}.avatar{order:-1;width:170px}.g2,.g3,.principles{grid-template-columns:1fr}nav a{margin-left:12px;font-size:.88rem}}
/* ---- theme v2: aurora + grid, glass cards, cyan/violet accents ---- */
:root{--bg:#06080e;--bg2:#0a0e17;--card:rgba(255,255,255,.04);--line:rgba(255,255,255,.1);--ink:#eef2fa;--mut:#9aa7bd;--acc:#ff8a3d;--acc2:#ffc15e;--cy:#5ad1ff;--vi:#8b7bff;--glow:rgba(255,138,61,.18)}
body{background:radial-gradient(900px 560px at 88% -6%,rgba(139,123,255,.18),transparent 62%),radial-gradient(760px 520px at -4% 8%,rgba(255,138,61,.13),transparent 58%),radial-gradient(700px 500px at 60% 105%,rgba(90,209,255,.08),transparent 60%),var(--bg);background-attachment:fixed}
body::before{content:"";position:fixed;inset:0;z-index:0;pointer-events:none;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:56px 56px;-webkit-mask-image:radial-gradient(ellipse at 50% 18%,#000 15%,transparent 72%);mask-image:radial-gradient(ellipse at 50% 18%,#000 15%,transparent 72%)}
header.top,main,section,footer,.marquee{position:relative;z-index:1}
header.top{backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);background:rgba(6,8,14,.62)!important;border-bottom:1px solid var(--line)}
::selection{background:rgba(255,138,61,.35);color:#fff}
html{scrollbar-color:#2a3345 var(--bg)}
a:focus-visible,button:focus-visible{outline:2px solid var(--cy);outline-offset:3px;border-radius:8px}
h2{background:linear-gradient(90deg,#fff,#c9d3e3);-webkit-background-clip:text;background-clip:text;color:transparent}
h1 em{background:linear-gradient(90deg,var(--acc),var(--acc2) 55%,var(--cy));-webkit-background-clip:text;background-clip:text;color:transparent}
.sechead .n{color:var(--cy)}
.card{position:relative;background:linear-gradient(180deg,rgba(255,255,255,.06),rgba(255,255,255,.02));backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);border:1px solid var(--line);overflow:hidden}
.card::after{content:"";position:absolute;inset:0;pointer-events:none;opacity:0;transition:opacity .3s;background:radial-gradient(360px circle at var(--px,50%) var(--py,50%),rgba(255,160,90,.14),transparent 60%)}
.card:hover::after{opacity:1}
.card:hover{border-color:rgba(255,160,90,.55);box-shadow:0 18px 40px -18px rgba(255,138,61,.35),0 0 0 1px rgba(255,160,90,.08) inset}
.card .idx{color:var(--cy)}
.tag{background:rgba(255,255,255,.03);border-color:rgba(255,255,255,.12)}
.btn{background:rgba(255,255,255,.05);backdrop-filter:blur(6px)}
.btn.p{background:linear-gradient(90deg,var(--acc),var(--acc2));box-shadow:0 10px 30px -10px rgba(255,138,61,.7)}
.btn.p:hover{box-shadow:0 14px 36px -10px rgba(255,138,61,.9)}
.chip.on{background:linear-gradient(90deg,var(--acc),var(--acc2))}
.metabox{background:linear-gradient(180deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1px solid var(--line);box-shadow:0 30px 60px -30px rgba(0,0,0,.8),0 0 60px -20px rgba(139,123,255,.35)}
.photo>img:first-child{box-shadow:0 0 0 1px rgba(255,255,255,.12),0 12px 40px -10px rgba(139,123,255,.45)}
.stats{background:rgba(255,255,255,.035);backdrop-filter:blur(8px)}
.stat b{background:linear-gradient(180deg,#fff,#b8c4da);-webkit-background-clip:text;background-clip:text;color:transparent}
.threats b{color:var(--cy)}
.threats li{background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.02))}
.term{background:#05070b;box-shadow:0 0 40px -18px rgba(90,209,255,.5)}
.ships{background:linear-gradient(180deg,rgba(255,255,255,.05),rgba(255,255,255,.02))}
.stab.on{border-color:var(--cy);background:rgba(90,209,255,.1)}.stab .mono{color:var(--cy)}
.sbar i{background:linear-gradient(90deg,var(--vi),var(--cy))}
.role{border-color:rgba(255,255,255,.14);background:rgba(255,255,255,.04)}
.marquee{background:rgba(255,255,255,.02)}

/* ---- loader v2: boot sequence + curtain ---- */
#loader{position:fixed;inset:0;z-index:99;display:grid;place-items:center;font-family:ui-monospace,Consolas,monospace;color:var(--ink);animation:ldfb .4s 4.6s forwards}
#loader .lpanel{position:absolute;top:0;bottom:0;width:50.2%;background:radial-gradient(700px 500px at 50% 30%,rgba(139,123,255,.16),transparent 65%),#06080e;transition:transform .8s cubic-bezier(.77,0,.18,1)}
#loader .lpanel.l{left:0}#loader .lpanel.r{right:0}
#loader .lpanel::after{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);background-size:48px 48px}
#loader .lscan{position:absolute;left:0;right:0;height:140px;top:-140px;z-index:1;background:linear-gradient(180deg,transparent,rgba(90,209,255,.1),transparent);animation:scan 3s linear infinite}
#loader .lc{position:relative;z-index:2;width:min(380px,86vw);display:flex;flex-direction:column;align-items:center;gap:14px;transition:opacity .4s,transform .6s}
#loader .lring{position:relative;width:104px;height:104px;display:grid;place-items:center}
#loader .lring::before{content:"";position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,var(--acc),var(--cy),var(--vi),var(--acc));-webkit-mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 3px));mask:radial-gradient(farthest-side,transparent calc(100% - 3px),#000 calc(100% - 3px));animation:spin 2.4s linear infinite}
#loader .lring img{width:62px;height:auto;filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))}
#loader .lt{font-size:1.15rem;letter-spacing:.02em}#loader .lt b{color:var(--acc);display:inline-block;min-width:.7em;text-align:center}
#loader .lag{list-style:none;margin:0;padding:0;width:100%;display:grid;gap:6px;font-size:.85rem}
#loader .lag li{display:flex;align-items:center;gap:10px;padding:7px 12px;border:1px solid var(--line);border-radius:10px;background:rgba(255,255,255,.03);color:var(--mut);transition:border-color .3s,color .3s,background .3s}
#loader .lag li i{width:10px;height:10px;border-radius:50%;border:2px solid #4a566c;flex:none;transition:all .3s}
#loader .lag li span{margin-left:auto;font-size:.75rem}
#loader .lag li.run{color:var(--ink);border-color:rgba(90,209,255,.5)}#loader .lag li.run i{border-color:var(--cy);border-top-color:transparent;animation:spin .7s linear infinite}
#loader .lag li.ok{color:var(--ink);border-color:rgba(111,220,154,.45);background:rgba(111,220,154,.06)}#loader .lag li.ok i{background:#6fdc9a;border-color:#6fdc9a;box-shadow:0 0 12px #6fdc9a}#loader .lag li.ok span{color:#6fdc9a}
#loader .lbar{width:100%;height:4px;background:var(--line);border-radius:4px;overflow:hidden}
#loader .lbar i{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--vi),var(--cy),var(--acc));box-shadow:0 0 14px rgba(90,209,255,.6)}
#loader .lpct{font-size:.78rem;color:var(--mut);min-height:1.1em}
#loader button{font:inherit;font-size:.8rem;background:none;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:5px 16px;cursor:pointer;transition:color .2s,border-color .2s}
#loader button:hover{color:var(--ink);border-color:var(--cy)}
#loader.open .lpanel.l{transform:translateX(-101%)}#loader.open .lpanel.r{transform:translateX(101%)}
#loader.open .lc{opacity:0;transform:scale(.96)}#loader.open .lscan{opacity:0}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes scan{to{top:100%}}@keyframes ldfb{to{opacity:0;visibility:hidden;pointer-events:none}}
@media (prefers-reduced-motion:reduce){#loader .lring::before,#loader .lscan,#loader .lag li.run i{animation:none}#loader.open .lpanel.l,#loader.open .lpanel.r{transform:none;opacity:0;transition:opacity .4s}}

.walk{margin:12px 0;border:1px solid var(--line);border-radius:12px;background:rgba(255,255,255,.025)}
.walk summary{cursor:pointer;padding:9px 14px;font:600 13px/1 ui-monospace,Consolas,monospace;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);list-style:none}
.walk summary::-webkit-details-marker{display:none}.walk summary:after{content:" +";float:right}.walk[open] summary:after{content:" -"}
.wk{padding:2px 14px 12px;display:grid;gap:9px;font-size:14.5px;line-height:1.55}
.wr{display:grid;grid-template-columns:104px 1fr;gap:10px}.wr b{color:var(--mut);font:600 12px/1.7 ui-monospace,Consolas,monospace;text-transform:uppercase;letter-spacing:.05em}
.wr ol{margin:0;padding-left:18px}.wr li{margin:0 0 2px}
@media(max-width:560px){.wr{grid-template-columns:1fr;gap:2px}}
.certs{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:26px}

""" + STORY_CSS + """
"""

CSS += """
/* web-portfolio layout (home page) */
.mono{font-family:ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
nav{display:flex;align-items:center;overflow-x:auto;white-space:nowrap}
nav a .n{font-family:ui-monospace,Consolas,monospace;font-size:.7rem;color:var(--acc);margin-right:5px}
.hero.v2{padding:68px 0 24px}
.hero.v2 .wrap{display:block}
.hgrid{display:grid;grid-template-columns:1.55fr 1fr;gap:36px;align-items:center}
.hero.v2 h1{font-size:clamp(2.3rem,6.4vw,4.4rem);line-height:1.02;letter-spacing:-.035em;font-weight:800;margin:.3em 0 .35em}
.hero.v2 .eyebrow{font-size:.78rem}
.roles{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 16px}
.role{font-family:ui-monospace,Consolas,monospace;font-size:.78rem;padding:4px 10px;border:1px solid var(--line);border-radius:6px;color:var(--mut);background:var(--card)}
.metabox{border:1px solid var(--line);border-radius:18px;background:var(--card);padding:18px 18px 8px;position:relative}
.metabox .tagl{position:absolute;top:-11px;left:16px;font-family:ui-monospace,Consolas,monospace;font-size:.7rem;letter-spacing:.12em;background:var(--acc);color:#1a0f06;padding:2px 8px;border-radius:5px;font-weight:700}
.photo{position:relative;width:min(240px,66%);margin:6px auto 12px}
.photo>img:first-child{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;object-position:50% 20%;border-radius:18px;border:1px solid var(--line);background:#fff;display:block}
.photo .cat{position:absolute;right:-18px;bottom:-14px;width:68px;height:auto;filter:drop-shadow(0 6px 12px rgba(0,0,0,.45))}
.metabox .avatar{width:min(220px,60%);margin:4px auto 8px}
.mrow{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);padding:9px 0;font-family:ui-monospace,Consolas,monospace;font-size:.76rem;color:var(--mut);text-transform:uppercase;letter-spacing:.06em}
.mrow b{color:var(--ink);font-weight:600;text-align:right;text-transform:none;letter-spacing:0}
.stats{display:grid;grid-template-columns:repeat(4,1fr);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:34px;background:var(--card)}
.stat{padding:16px 20px;border-right:1px solid var(--line)}.stat:last-child{border-right:0}
.stat b{display:block;font-size:2rem;letter-spacing:-.03em;line-height:1.1}
.stat span{font-family:ui-monospace,Consolas,monospace;font-size:.72rem;color:var(--mut);text-transform:uppercase;letter-spacing:.1em}
.marquee{overflow:hidden;border-block:1px solid var(--line);padding:13px 0;margin:10px 0 6px}
.track{display:flex;gap:36px;width:max-content;animation:mq 42s linear infinite}
.track span{font-family:ui-monospace,Consolas,monospace;font-size:.85rem;color:var(--mut);white-space:nowrap}
@keyframes mq{to{transform:translateX(-50%)}}
@media(prefers-reduced-motion:reduce){.track{animation:none}html{scroll-behavior:auto}}
.sechead{display:flex;align-items:baseline;gap:12px;margin-bottom:4px}
.sechead .n{font-family:ui-monospace,Consolas,monospace;color:var(--acc);font-size:.85rem;font-weight:700}
.sechead h2{margin:0}
.idx{font-family:ui-monospace,Consolas,monospace;font-size:.72rem;color:var(--mut);letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}
.layers{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.layer .num{font-family:ui-monospace,Consolas,monospace;color:var(--acc);font-size:.78rem}
.layer h3{margin:2px 0 2px}.layer .s{color:var(--mut);font-weight:400}
.pn{font-family:ui-monospace,Consolas,monospace;color:var(--acc);font-size:.8rem;margin-bottom:4px}
.tline{display:grid;gap:0}
.trow{display:grid;grid-template-columns:170px 1fr;gap:20px;padding:16px 0;border-top:1px solid var(--line)}
.trow:last-child{border-bottom:1px solid var(--line)}
.trow .when{font-family:ui-monospace,Consolas,monospace;font-size:.78rem;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;padding-top:3px}
.trow h3{margin:0 0 2px;font-size:1.1rem}.trow .org{color:var(--acc);font-size:.9rem;font-weight:600}.trow p{margin:.3em 0 0;color:var(--mut);font-size:.97rem}
.pubs{margin:16px 0 0;padding-left:18px;color:var(--mut);font-size:.93rem}
.cta-big{border:1px solid var(--line);border-radius:22px;padding:34px 26px;background:radial-gradient(700px 260px at 85% -20%,var(--glow),transparent 70%),var(--card);margin-top:18px}
.cta-big h2{font-size:clamp(1.7rem,4vw,2.6rem);letter-spacing:-.025em;margin:0 0 8px}
@media(max-width:760px){.hgrid{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}.stat:nth-child(2){border-right:0}.stat:nth-child(-n+2){border-bottom:1px solid var(--line)}.layers{grid-template-columns:1fr}.trow{grid-template-columns:1fr;gap:4px}}
"""

NAV = [("/#work", '<span class="n">001</span>Work'), ("/#security", '<span class="n">002</span>AI security'), ("/#approach", '<span class="n">003</span>Approach'), ("/#ships", '<span class="n">004</span>How it ships'), ("/#toolkit", '<span class="n">005</span>Toolkit'),
       ("/#about", '<span class="n">006</span>About'), ("/#tools", '<span class="n">007</span>Tools'), ("/guides/", "Guides (TH)")]
if cfg["contact"]:
    NAV.append(("/#contact", "Contact"))


LOADER = ("""<div id="loader" role="status" aria-live="polite"><div class="lpanel l"></div><div class="lpanel r"></div><div class="lscan"></div>
<div class="lc"><div class="lring"><img src="/assets/cat.png" alt="" width="62" height="76"></div>
<div class="lt">Loading agents <b id="lc">0</b>/3</div>
<ul class="lag"><li id="ag0"><i></i>planner<span>idle</span></li><li id="ag1"><i></i>builder<span>idle</span></li><li id="ag2"><i></i>checker<span>idle</span></li></ul>
<div class="lbar"><i id="lb"></i></div><div class="lpct" id="lp">0%</div><button type="button" id="lskip">Skip</button></div></div>
<script>(function(){var l=document.getElementById('loader');if(!l)return;var g=document.documentElement;setTimeout(function(){g.classList.add('go')},4800);
try{if(sessionStorage.getItem('seen')){l.remove();g.classList.add('go');return}}catch(e){}
var lc=document.getElementById('lc'),lb=document.getElementById('lb'),lp=document.getElementById('lp'),ag=[0,1,2].map(function(i){return document.getElementById('ag'+i)}),st=['planner online','builder online','checker online'],n=0,fin=false,t0=performance.now(),D=2700,raf;
function done(){if(fin)return;fin=true;clearInterval(raf);try{sessionStorage.setItem('seen','1')}catch(e){}g.classList.add('go');l.classList.add('open');setTimeout(function(){l.remove()},900)}
function set(i,cls,txt){ag[i].className=cls;ag[i].lastChild.textContent=txt}
function tick(now){var p=Math.min(1,(now-t0)/D),e=1-Math.pow(1-p,2.2);lb.style.width=(e*100)+'%';lp.textContent=Math.round(e*100)+'%';
var k=Math.floor(p*3+0.001);for(var i=0;i<3;i++){if(i<k&&ag[i].className!=='ok'){set(i,'ok',st[i]);n=Math.max(n,i+1);lc.textContent=n}else if(i===k&&i<3&&ag[i].className!=='run'&&ag[i].className!=='ok'){set(i,'run','booting...')}}
if(p>=1){clearInterval(raf);lc.textContent=3;set(2,'ok',st[2]);setTimeout(done,380)}}
raf=setInterval(function(){tick(performance.now())},33);document.getElementById('lskip').onclick=done})()</script>""")


MOTION = """<script>(function(){var d=document,r=d.documentElement,rm=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
if(!r.classList.contains('go')){setTimeout(function(){r.classList.add('go')},60)}
var bar=d.getElementById('sprog');function sp(){var h=d.documentElement.scrollHeight-innerHeight;bar.style.width=(h>0?scrollY/h*100:0)+'%'}addEventListener('scroll',sp,{passive:true});sp();
var els=d.querySelectorAll('main .card,.sechead,.sub,.layer,.trow,.ships,.pubs li,.chips,.stat'.replace('main ',''));
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.12});
els.forEach(function(el,i){if(el.closest('.hero'))return;el.classList.add('rv');el.style.transitionDelay=((i%3)*90)+'ms';io.observe(el)});
var co=new IntersectionObserver(function(es){es.forEach(function(e){if(!e.isIntersecting)return;co.unobserve(e.target);var b=e.target;var mm=/^(\d+)(.*)$/.exec(b.textContent);if(!mm)return;var t=parseInt(mm[1],10),sf=mm[2];var s=performance.now();(function f(n){var p=Math.min(1,(n-s)/1100);b.textContent=Math.round(t*(1-Math.pow(1-p,3)))+sf;if(p<1)requestAnimationFrame(f)})(s)})},{threshold:.6});
d.querySelectorAll('.stats .stat b').forEach(function(b){co.observe(b)});
d.addEventListener('pointermove',function(e){var c=e.target.closest&&e.target.closest('.card');if(c){var q=c.getBoundingClientRect();c.style.setProperty('--px',(e.clientX-q.left)+'px');c.style.setProperty('--py',(e.clientY-q.top)+'px')}},{passive:true});
var h=d.querySelector('.hero.v2');if(h&&!rm&&matchMedia('(hover:hover)').matches){h.addEventListener('pointermove',function(e){var q=h.getBoundingClientRect();h.style.setProperty('--mx',(e.clientX-q.left)+'px');h.style.setProperty('--my',(e.clientY-q.top)+'px')})}
})()</script>"""


def shell(path, title, desc, body, schema, lang="en", article=False, og="/og.png"):
    url = f"{BASE}{path}"
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schema)
    nav = "".join(f'<a href="{h}">{t}</a>' for h, t in NAV)
    doc = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta name="theme-color" content="#0c0e13"><link rel="icon" href="/assets/cat.png">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{og}"><meta name="twitter:card" content="summary_large_image">
<script>document.documentElement.classList.add("js")</script><style>{CSS}</style>{ld}</head><body><div id="sprog"></div>
<header class="top"><div class="wrap"><a class="brand" href="/"><img src="/assets/cat.png" alt="" width="30" height="30">{HANDLE}</a><nav>{nav}</nav></div></header>
{LOADER if path == "/" else ""}{body}
<footer><div class="wrap">© {date.today().year} {HANDLE} ({THAI}) · Updated {TODAY}</div></footer></body></html>"""
    f = OUT / path.strip("/") / "index.html" if path != "/" else OUT / "index.html"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding="utf-8")


def tags(ts):
    return '<div class="tags">' + "".join(f'<span class="tag">{html.escape(t)}</span>' for t in ts) + "</div>"


def card(p, big=False):
    link_list = p.get("links") or ([p["link"]] if p.get("link") else [])
    link = ("<p>" + " &nbsp; ".join(f'<a href="{u}">{html.escape(t)} →</a>' for u, t in link_list) + "</p>") if link_list else ""
    sub = f'<div class="s">{html.escape(p["sub"])}</div>' if p.get("sub") else ""
    return (f'<article class="card{" big" if big else ""}" data-cat="{p["cat"]}"><h3>{html.escape(p["title"])}</h3>{sub}'
            f'<p>{html.escape(p["body"])}</p>{link}{tags(p["tags"])}</article>')


person = {"@context": "https://schema.org", "@type": "Person", "@id": f"{BASE}/#person", "name": HANDLE, "alternateName": THAI, "url": f"{BASE}/",
          "jobTitle": "AI engineer (agents, automation, application security)", "image": f"{BASE}/assets/cat.png",
          "knowsAbout": ["AI agents", "workflow automation", "n8n", "LINE bots", "SAR remote sensing", "quantitative research", "Python"]}
if cfg["sameAs"]:
    person["sameAs"] = cfg["sameAs"]
if cfg.get("email"):
    person["email"] = cfg["email"]
site_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": HANDLE, "url": f"{BASE}/", "publisher": {"@id": f"{BASE}/#person"}}

# ------------------------------------------------------------------ home (English portfolio)
chips = "".join(f'<button class="chip{" on" if k == "all" else ""}" data-f="{k}">{html.escape(v)}</button>' for k, v in FILTERS)
contact = ""
if cfg["contact"]:
    btns = "".join(f'<a class="btn{" p" if i == 0 else ""}" href="{html.escape(c["url"])}">{html.escape(c["label"])}</a>' for i, c in enumerate(cfg["contact"]))
    services = [("AI video creation", "Short vertical videos (Reels, TikTok, Shorts) with Thai voice-over and subtitles."),
                ("LINE OA bots & chatbots", "LINE Official Account bots with automation: replies, reminders, staff tools."),
                ("n8n workflow automation", "Connect Sheets, LINE, Telegram and APIs so repetitive work runs itself."),
                ("AI object detection (YOLO)", "Counting and quality-control from images, e.g. product counting.")]
    svc = "".join(f'<div class="card"><h3>{html.escape(a)}</h3><p>{html.escape(b)}</p></div>' for a, b in services)
    contact = (f'<section id="contact"><div class="wrap"><h2>Work with me</h2><p class="sub">Services listed on my Fastwork profile. Tell me what is slow, manual or unreliable in your process.</p>'
               f'<div class="grid g2">{svc}</div><div class="cta">{btns}</div></div></section>')
principles = [("Verify before claiming", "Numbers get checked against an independent calculation before they ship. Every fee table here cites its source and date."),
              ("Humans stay in the loop", "Publishing, payments and anything irreversible wait for an explicit approval step. Automation drafts; people decide."),
              ("Ship small, measure", "Start with the smallest version a real user can try, put it online, and let usage decide what gets built next.")]
LAYERS = [("01", "AI & agents", "Agents that plan, call tools and verify", ["LLM agents", "RAG", "Vision-language models", "FinBERT / VADER", "EasyOCR"]),
          ("02", "Automation", "Workflows where people approve what matters", ["n8n", "LINE Messaging API", "Telegram Bot API", "APScheduler"]),
          ("03", "Backend & data", "Pipelines whose numbers can be checked", ["Python", "FastAPI", "PostGIS", "Zarr", "Excel / openpyxl"]),
          ("04", "Delivery", "Small things that are online and usable", ["Next.js", "Docker", "Cloudflare Pages", "Playwright", "FFmpeg"])]
TIMELINE = [("Sep 2025 - now", "Test Engineer", "Electronics manufacturing", "Debug board and system test failures, write Failure Analysis reports, and build the Python tools that cut manual log review by over 80%."),
            ("Apr 2025 - now", "Freelance AI & software developer", "Fastwork and direct clients", "LINE and Telegram bots, n8n workflows and data tools, delivered from requirements to deployment."),
            ("2024 - now", "Undergraduate research assistant", "Rajamangala University of Technology Rattanakosin", "MATLAB and reinforcement-learning work behind three IEEE publications (second author)."),
            ("2020 - 2025", "B.Eng. Electrical Engineering", "Rajamangala University of Technology Rattanakosin", "Harvard CS50's Introduction to AI with Python (2026); OPSWAT cybersecurity fundamentals (2026).")]
PUBS = [("Metaheuristic-based optimal scheduling of appliances and EV charging (IEEE OAJPE, 2026)", "https://doi.org/10.1109/OAJPE.2026.3676351"),
        ("Decentralized microgrid energy management with multi-agent deep reinforcement learning (iEECON, 2026)", "https://doi.org/10.1109/iEECON68065.2026.11707083"),
        ("Appliance scheduling with EV charging load using metaheuristics (ICPEI, 2024)", "https://doi.org/10.1109/ICPEI61831.2024.10748852")]
_pool = FEATURED + MORE
_by = {p["title"]: p for p in _pool}
_order = ["Agent Invest", "LendLoop", "LINE AI Assistant for a Repair Shop", "AppSec Testing & Remediation (OWASP Juice Shop)", "Test-Eng Assist", "AI Content Factory (n8n + Python)"]
FEATURED = [_by[t] for t in _order]
MORE = [p for p in _pool if p["title"] not in _order]
ALL = FEATURED + MORE
more_counts = {k: sum(1 for p in MORE if p["cat"] == k) for k, _ in FILTERS if k != "all"}



# ------------------------------------------------------------------ walkthrough details (shown on each card so a viewer can follow along)
# keys: why (problem), flow (ordered steps), ctrl (controls/checks), show (what to point at when presenting)
DETAILS = {
 "Agent Invest": dict(why="Following many symbols by hand is slow, and nobody knows whether an AI's calls were any good.",
   flow=["Several AI agents analyse each symbol", "Predictions are stored with their timeframe", "Later prices are compared with the stored predictions", "Accuracy is tracked per timeframe on the Next.js dashboard", "A daily report is built; users ask the Telegram bot by command or natural language"],
   ctrl="Predictions are judged against real later prices instead of trusting the model's own confidence.",
   show="Team project: open the dashboard, then the repo linked on the card."),
 "LendLoop": dict(why="Neighbours lending tools to each other need approvals, notifications and overdue reminders without anyone chasing by hand.",
   flow=["A neighbour lists a tool; another requests it for a date range (Clerk sign-in)", "The lender approves or declines; Convex enforces who may do what", "Convex signs a webhook and calls n8n to notify (retries with backoff, up to 5 times)", "n8n runs daily at 09:00 and asks Convex which loans are overdue", "n8n writes each reminder back with a unique ID, so a replay never duplicates it"],
   ctrl="Signed requests, timestamps older than 5 minutes rejected, idempotent handlers so a retry never sends a second reminder.",
   show="Built as a take-home project: show the webhook handler and the retry log in the repo."),
 "LINE AI Assistant for a Repair Shop": dict(why="Staff lose time diagnosing faults, and customers forget their 6-month service.",
   flow=["Staff message the LINE account with a fault code or symptom", "An LLM drafts a diagnosis for staff to use", "Staff log the completed job", "Customers link their LINE to their phone number", "A daily scheduler in the same process pushes the service reminder when due"],
   ctrl="The AI only advises staff; customers get scheduled reminders, not free-form AI answers. Several API keys are rotated to survive rate limits.",
   show="Show the two audiences: a staff diagnosis chat, then a customer reminder message."),
 "AppSec Testing & Remediation (OWASP Juice Shop)": dict(why="Show I can find, fix and re-verify web vulnerabilities, not only list them.",
   flow=["Run OWASP Juice Shop v20.2.0 locally", "Find and document 3 vulnerabilities with full requests and responses", "Patch the vulnerable code", "Replay the original exploit requests against the fix", "Confirm normal login, own basket and search still work"],
   ctrl="Fixes use parameterised queries and a server-side ownership check from the session token; exploits now fail safely with 401/403 or an empty result and no stack trace.",
   show="Open the two PDFs: Findings first, then Remediation with the code diff. Training app only, no real client."),
 "Test-Eng Assist": dict(why="Test engineers dig through manuals and past failures to answer the same questions repeatedly.",
   flow=["Ingest the engineer's own documents", "Index them for retrieval (RAG, ChromaDB)", "The agent loop picks tools and answers from the documents", "A scheduler runs recurring jobs", "Results appear in a dashboard; packaged as an executable"],
   ctrl="Runs locally so documents stay on the machine.",
   show="Ask a question and point to the retrieved source chunks."),
 "AI Content Factory (n8n + Python)": dict(why="Making short vertical videos on a schedule is repetitive, but publishing blindly is risky.",
   flow=["n8n schedules and picks a topic", "A Python factory writes the script", "Video generation and TTS voice-over", "FFmpeg assembles the 9:16 video with subtitles", "A person approves; only then does n8n publish"],
   ctrl="A restart-safe state machine behind a local HTTP API, and nothing publishes without explicit approval.",
   show="Walk the n8n workflow left to right, then the approval step."),
 "SAR Crop-Damage Verification": dict(why="Insurers and lenders need defensible, parcel-level flood and crop-damage numbers.",
   flow=["Pull open Sentinel-1 radar scenes", "Apply a rice-transplanting mask so normal wet paddy is not flagged", "Estimate flood and damage per plot", "Attach scene IDs, versions, parameters and a confidence score"],
   ctrl="Every result is reproducible and carries its evidence for a claims dispute.", show="Flood/damage module is implemented; crop and carbon are interfaces only."),
 "LangGraph Test-Log Triage (demo)": dict(why="Failure logs pile up and engineers read them one by one.", flow=["Read test-failure logs", "Group them by likely cause", "Draft a triage note"], ctrl="Synthetic data only.", show="Run it on the sample logs."),
 "TypeScript SPC Analyzer (demo)": dict(why="A test line needs to notice when a process drifts.", flow=["Load measurements", "Draw control charts", "Apply out-of-control rules"], ctrl="Synthetic data only.", show="Load a sample series and trigger a rule."),
 "Autonomous Agent Loop": dict(why="Complex tasks need planning, not one prompt.", flow=["Plan", "Split into sub-tasks", "Call tools", "Verify", "Repeat until done"], ctrl="Sandboxed workspace; multi-agent orchestrator.", show="Show one task's plan and verify steps."),
 "Windows Computer-Control Agent": dict(why="Automate desktop apps that have no API.", flow=["Capture the screen", "Ask a vision-language model for the next action", "Run it through GUI or shell tools", "Observe the result", "Repeat until the goal is met"], ctrl="Loop stops when the goal is met.", show="Give it a small goal and watch the loop."),
 "News Pipeline with Telegram Approval": dict(why="Automated posting needs a human gate.", flow=["Runs three times a day (Bangkok time)", "Collects items", "Sends each to a Telegram bot", "Posts only what a person approves"], ctrl="Human approval before anything goes out.", show="Show an approval message in Telegram."),
 "LINE Slip-OCR Assistant": dict(why="Typing trade slips into a spreadsheet by hand.", flow=["Photo of the slip in LINE", "Thai + English OCR (EasyOCR)", "Flex confirmation card for the user", "Tax calculation", "Row logged to an Excel workbook that acts as the database"], ctrl="The user confirms before anything is logged.", show="Send a sample slip image."),
 "Shop Automation Pack (n8n)": dict(why="Small shops need daily sales and order alerts without a developer.", flow=["Import the workflow into n8n", "Daily sales summary from Google Sheets to Telegram", "New-order alert with validation"], ctrl="Tested end-to-end on a local n8n with test data.", show="Import the JSON and run it."),
 "Thai Stock Monitor": dict(why="Watch SET/mai stocks without staring at charts.", flow=["Fetch prices (yfinance)", "Generate signals from indicator thresholds", "Simulate trades in a paper portfolio", "Alert by Telegram/LINE", "Show it in a Next.js dashboard"], ctrl="Live execution deliberately not implemented.", show="Open the dashboard and the paper portfolio."),
 "Quant Signal Engine": dict(why="Combine price and news into one disciplined signal.", flow=["Market data plus news sentiment (FinBERT/VADER)", "EMA, RSI, ATR indicators", "Kelly sizing", "Signal with dynamic stop-loss and take-profit"], ctrl="Position size comes from a formula, not a guess.", show="Print one signal with its inputs."),
 "Algorithmic Trading Research (private)": dict(why="Most backtests flatter themselves.", flow=["Write the edge standard first", "Net-of-cost expectancy", "Out-of-sample tests and minimum sample sizes", "Regime analysis (HMM)"], ctrl="Findings are not published.", show="Describe the method only."),
 "Character IP Studio": dict(why="Turn one character into many products.", flow=["Design the orange-cat cast", "Export LINE sticker, emoji and theme packs", "Render short films from a frame-accurate HTML engine (Playwright + FFmpeg)", "Synthesise audio normalised to -14 LUFS"], ctrl="Deterministic rendering, so a film re-renders identically.", show="Play a short film."),
 "1-Minute Product Clip Generator": dict(why="Product clips take too long to edit.", flow=["Input: product JSON and a photo", "Thai voice-over (edge-tts)", "Compose frames with Pillow", "Assemble with FFmpeg into a vertical clip"], ctrl="No browser page is rendered per frame, which keeps it near a minute.", show="Run it on a sample product."),
 "Shop Fee Reader (live)": dict(why="Sellers cannot see where each baht of a sale goes.", flow=["Choose platform (Shopee, TikTok Shop, Lazada)", "Enter price and costs", "See fees, break-even price and break-even ROAS"], ctrl="All data stays in the browser.", show="Open the live tool and try a sample sale."),
 "Stock & Sales Spreadsheet": dict(why="Small shops track stock in messy sheets.", flow=["Enter stock and sales", "SUMIFS / INDEX-MATCH dashboards", "Low-stock alerts and charts"], ctrl="Every dashboard value was checked against an independent Python calculation.", show="Change a stock number and watch the dashboard."),
}


def walk(p, open_=False):
    d = DETAILS.get(p["title"])
    if not d:
        return ""
    steps = "".join(f"<li>{html.escape(x)}</li>" for x in d["flow"])
    inner = (f'<div class="wk"><div class="wr"><b>Problem</b><span>{html.escape(d["why"])}</span></div>'
             f'<div class="wr"><b>How it works</b><ol>{steps}</ol></div>'
             f'<div class="wr"><b>Controls</b><span>{html.escape(d["ctrl"])}</span></div>'
             f'<div class="wr"><b>When showing it</b><span>{html.escape(d["show"])}</span></div></div>')
    return f'<details class="walk"{" open" if open_ else ""}><summary>Walkthrough</summary>{inner}</details>'


def pcard(p, i, n, big=False):
    link_list = p.get("links") or ([p["link"]] if p.get("link") else [])
    link = ("<p>" + " &nbsp; ".join(f'<a href="{u}">{html.escape(t)} →</a>' for u, t in link_list) + "</p>") if link_list else ""
    sub = f'<div class="s">{html.escape(p["sub"])}</div>' if p.get("sub") else ""
    idx = f'<div class="idx">{i:02d} / {n:02d} · {html.escape(CAT_NAME[p["cat"]])}</div>'
    sid = ALL.index(p)
    return (f'<article class="card{" big" if big else ""}" data-cat="{p["cat"]}">{idx}<h3>{html.escape(p["title"])}</h3>{sub}'
            f'<p>{html.escape(p["body"])}</p>{walk(p, big)}<p><button class="btn story-btn" type="button" data-sid="{sid}">Read the full story</button></p>{link}{tags(p["tags"])}</article>')


CAT_NAME = dict(FILTERS)
chips2 = "".join(f'<button class="chip{" on" if k == "all" else ""}" data-f="{k}">{html.escape(v)}'
                 f'{"" if k == "all" else " " + str(more_counts.get(k, 0))}</button>' for k, v in FILTERS if k == "all" or more_counts.get(k, 0))
marquee_items = "".join(f"<span>{html.escape(s)}</span>" for s in STACK) * 2
meta_rows = [("Focus", "AI agents · AppSec"), ("Based", "Thailand"), ("Core", "Python · FastAPI · LLM"), ("Status", "Open to AI / security roles")]
metabox = ('<div class="metabox hi" style="--d:2"><span class="tagl">PROFILE</span><div class="photo"><img src="/assets/me.jpg" alt="Portrait of Nopprut Saeli" width="240" height="300"><img class="cat" src="/assets/cat.png" alt="Orange cat mascot" width="64" height="78"></div>'
           + "".join(f'<div class="mrow"><span>{a}</span><b>{html.escape(b)}</b></div>' for a, b in meta_rows) + "</div>")
stats = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for v, k in
                [("80%+", "Manual log review cut"), ("4", "AI apps built end to end"), ("3", "Vulns found and fixed"), ("3", "IEEE papers")])

CERTS = [("OPSWAT Academy · Issued 14 Nov 2026 · 0.50 CPE", "Introduction to Critical Infrastructure Protection",
          "Basic ideas behind protecting critical infrastructure, what a critical network is, and how the OPSWAT Academy certification programme is structured. Valid to 14 Nov 2027.",
          "https://learn.opswatacademy.com/certificate/ekojQN1SPg", "Verify certificate"),
         ("OPSWAT Academy · Issued 15 Nov 2026 · 1.25 CPE", "Cybersecurity Fundamentals Associate (OCFA)",
          "Per the course overview (a third-party source): types of security and the technologies behind them, career paths and skills, strategies for entry-level work, and an end-of-course assessment. Valid to 14 Nov 2027.",
          "https://learn.opswatacademy.com/certificate/X6yY89u_nw", "Verify certificate"),
         ("Harvard CS50 · 2026", "Introduction to Artificial Intelligence with Python", "Search, knowledge, uncertainty, optimisation, machine learning, neural networks and language.",
          "https://cs50.harvard.edu/certificates/8d30649f-b896-4f19-80f4-7b0da1badeff", "Verify certificate")]
certs_html = '<h3 class="subh" style="margin-top:34px">Certifications</h3><div class="certs">' + "".join(
    f'<div class="card"><div class="idx">{html.escape(a)}</div><h3>{html.escape(b)}</h3><p>{html.escape(c)}</p><p><a href="{u}" rel="noopener">{html.escape(t)} →</a></p></div>' for a, b, c, u, t in CERTS) + "</div>"
stories_html = '<div id="stories" hidden>' + "".join(f'<div data-sid="{i}">{story_html(p, DETAILS)}</div>' for i, p in enumerate(ALL)) + '</div>'
featured_html = "".join(pcard(p, i, len(FEATURED), True) for i, p in enumerate(FEATURED, 1))
more_html = "".join(pcard(p, i, len(MORE)) for i, p in enumerate(MORE, 1))
approach_html = "".join(f'<div class="card"><div class="pn">0{i}</div><h3>{html.escape(a)}</h3><p>{html.escape(b)}</p></div>' for i, (a, b) in enumerate(principles, 1))
layers_html = "".join(f'<div class="card layer"><div class="num">LAYER {n}</div><h3>{html.escape(t)}</h3><p class="s">{html.escape(s)}</p>{tags(ts)}</div>' for n, t, s, ts in LAYERS)
timeline_html = "".join(f'<div class="trow"><div class="when">{w}</div><div><h3>{html.escape(t)}</h3><div class="org">{html.escape(o)}</div><p>{html.escape(d)}</p></div></div>' for w, t, o, d in TIMELINE)
pubs_html = "".join(f'<li><a href="{u}" rel="noopener">{html.escape(t)}</a></li>' for t, u in PUBS)
contact_html = contact.replace('<section id="contact"><div class="wrap"><h2>Work with me</h2>',
                               '<section id="contact"><div class="wrap"><div class="sechead"><span class="n">008</span><h2>Work with me</h2></div>') if contact else ""


STAGES = [("Plan", "Pin down the pain", "Write down what is slow, manual or unreliable, who approves what, and what 'done' means. Agree the smallest version worth trying.", ["Scope note", "Approval points", "Success check"]),
          ("Design", "Draw the flow and the guardrails", "Choose the pieces (n8n, FastAPI, a bot), decide where a human must approve, and define how every number will be verified.", ["Flow diagram", "Data checks", "Failure handling"]),
          ("Build", "Small steps, tested as I go", "Ship a thin working slice first. Retries, idempotency and logging go in early, then features. Tests compare results with an independent calculation.", ["Thin slice", "Tests", "Logs"]),
          ("Deliver", "Online, documented, handed over", "Deploy with Docker or Cloudflare Pages, write the README and a short runbook, and watch real usage before adding more.", ["Deployed", "Docs", "Follow-up"])]
ships_tabs = "".join(f'<button class="stab{" on" if i == 0 else ""}" data-i="{i}" type="button"><span class="mono">0{i + 1}</span> {html.escape(a)}</button>' for i, (a, *_r) in enumerate(STAGES))
ships_panels = "".join(f'<div class="spanel{" on" if i == 0 else ""}" data-i="{i}"><h3>{html.escape(b)}</h3><p>{html.escape(c)}</p>{tags(d)}</div>' for i, (a, b, c, d) in enumerate(STAGES))
SHIPS_HTML = (f'<div class="ships" id="ships-box"><div class="sbar"><i id="sfill"></i></div><div class="stabs" role="tablist">{ships_tabs}</div><div class="spanels">{ships_panels}</div><p class="note mono">Illustrative process</p></div>'
              """<script>(function(){var b=document.getElementById('ships-box');if(!b)return;var t=b.querySelectorAll('.stab'),p=b.querySelectorAll('.spanel'),f=document.getElementById('sfill'),cur=0,auto=true,tm;
function go(i){cur=i;t.forEach(function(x,k){x.classList.toggle('on',k===i)});p.forEach(function(x,k){x.classList.toggle('on',k===i)});f.style.width=((i+1)*25)+'%'}
t.forEach(function(x,k){x.addEventListener('click',function(){auto=false;clearInterval(tm);go(k)})});
if(!window.matchMedia('(prefers-reduced-motion:reduce)').matches){tm=setInterval(function(){if(auto)go((cur+1)%4)},4200)}go(0)})()</script>""")


THREATS = [("Prompt injection", "Contain the blast radius: read-only tools by default, untrusted text kept apart from instructions."),
           ("Excessive agency", "Human approval for anything that writes, sends or spends; a kill switch; risky actions off by default."),
           ("Forged webhooks", "HMAC-signed requests both ways, timestamps older than 5 minutes rejected (built into LendLoop)."),
           ("Duplicate side effects", "Idempotent handlers and retries with backoff, every attempt logged (LendLoop: 5 retries)."),
           ("Leaked keys and cost abuse", "Keys stay server-side, rotated across several keys (LINE repair bot), rate and token limits."),
           ("Cross-user data access", "Authorization checked on the server from the session, never from request parameters (Juice Shop fix).")]
FINDINGS = [("Critical", "SQL injection login bypass", "Parameterised query"), ("High", "IDOR on basket API", "Ownership check from session token"), ("Medium", "SQL injection in search + verbose errors", "Parameterised query, safe error response")]
threat_html = "".join(f'<li><b>{html.escape(a)}</b><span>{html.escape(b)}</span></li>' for a, b in THREATS)
find_rows = "".join(f'<tr><td><span class="sev {a.lower()}">{a}</span></td><td>{html.escape(b)}</td><td>{html.escape(c)}</td></tr>' for a, b, c in FINDINGS)
TERM = """<pre class="term" aria-label="Illustrative agent guardrail trace"><span class="c"># illustrative trace: a guarded agent step</span>
<span class="k">agent</span>  &gt; tool_call  send_email(to="customer", body=...)
<span class="k">policy</span> &gt; tenant=A  scope=read_only  <span class="w">BLOCKED: write action</span>
<span class="k">policy</span> &gt; route to human approval
<span class="k">human</span>  &gt; <span class="o">approved</span>  (logged: user, time, inputs)
<span class="k">agent</span>  &gt; executed once  (idempotency key checked)</pre>"""
SECURITY_HTML = (f'<div class="secgrid"><div><h3 class="subh">Threat model for a tool-calling agent</h3><ul class="threats">{threat_html}</ul>{TERM}</div>'
                 f'<div><h3 class="subh">Hands-on: OWASP Juice Shop</h3><p class="s">A deliberately vulnerable training app on my own machine, assessed like a client engagement, then fixed and re-tested.</p>'
                 f'<table class="tbl"><thead><tr><th>Severity</th><th>Finding</th><th>Fix</th></tr></thead><tbody>{find_rows}</tbody></table>'
                 f'<p class="s">Exploit requests fail safely after the patch (401/403 or empty result, no stack trace) and normal login, own basket and search still work. Training app only, no real client.</p>'
                 f'<p><a class="btn p" href="/security/report-1-juice-shop.pdf">Findings (PDF)</a> &nbsp; <a class="btn" href="/security/report-2-remediation.pdf">Remediation (PDF)</a></p></div></div>')


def sec(n, title, sub, inner, sid):
    return f'<section id="{sid}"><div class="wrap"><div class="sechead"><span class="n">{n}</span><h2>{title}</h2></div><p class="sub">{sub}</p>{inner}</div></section>'


home = (f"""<section class="hero v2"><div class="wrap"><div class="hgrid"><div>
<div class="eyebrow mono hi" style="--d:0">Web portfolio / {date.today().year}</div>
<h1 class="hi" style="--d:1">Building AI agents that <em>stay under control</em>.</h1>
<div class="roles hi" style="--d:2"><span class="role">AI agents</span><span class="role">AI security</span><span class="role">Automation</span></div>
<p class="lead hi" style="--d:3">Hi, I'm {HANDLE} ({THAI}), an AI engineer with a test-engineering background. I build agents and automation with the controls built in: least-privilege tools, human approval, signed webhooks, and tests that try to break them.</p>
<div class="cta hi" style="--d:4"><a class="btn p" href="#work">Explore my work</a><a class="btn" href="#security">AI security work</a></div></div>
{metabox}</div><div class="stats">{stats}</div></div></section>
<div class="marquee" aria-hidden="true"><div class="track">{marquee_items}</div></div>
"""
        + sec("001", "Selected work", "Six projects that show the range, from agents to AppSec. Details come from each project's own documentation.", f'<div class="grid g2">{featured_html}</div>', "work")
        + sec("002", "AI security", "Agents that call tools need controls the model cannot talk its way around. This is how I design them, and what I have tested hands-on.", SECURITY_HTML, "security")
        + sec("", "More projects", "Filter by area.", f'<div class="chips" id="chips">{chips2}</div><div class="grid g3" id="more">{more_html}</div>', "more-work")
        + sec("003", "Approach", "Three habits that show up across the projects above.", f'<div class="grid principles">{approach_html}</div>', "approach")
        + sec("004", "How a build ships", "Four stages I follow on every project. Click a stage; this is an illustrative walk-through of my process, not a live system.", SHIPS_HTML, "ships")
        + sec("005", "Engineering toolkit", "Grouped by what each layer does. Taken from the projects above, not a wish list.", f'<div class="layers">{layers_html}</div>', "toolkit")
        + sec("006", "About", "Engineer by training, builder by habit.", f'<div class="tline">{timeline_html}</div><ul class="pubs">{pubs_html}</ul>{certs_html}', "about")
        + f"""<section id="tools"><div class="wrap"><div class="sechead"><span class="n">007</span><h2>Live tools</h2></div><p class="sub">Things you can open right now (Thai interface, built for online sellers).</p>
<div class="grid g2">
<article class="card big"><h3>Shop Fee Reader</h3><div class="s">Free · Shopee, TikTok Shop, Lazada</div><p>See where each baht of a sale goes, the break-even price and break-even ROAS. Data stays in your browser.</p><p><a class="btn p" href="{FREE_TOOL}">Open the free tool</a> &nbsp; <a href="/tools/fee-reader/">Details (TH)</a></p></article>
<article class="card big"><h3>Marketplace Fee Guide 2569</h3><div class="s">Thai article · sourced rates</div><p>Fee table for the three platforms with a worked example and an FAQ on checking unexpected deductions.</p><p><a class="btn" href="/guide/shopee-lazada-tiktok-fees-2569/">Read the guide (TH)</a></p></article></div></div></section>
"""
        + contact_html
        + """<script>document.getElementById('chips').addEventListener('click',function(e){var f=e.target.dataset.f;if(!f)return;this.querySelectorAll('.chip').forEach(function(c){c.classList.toggle('on',c===e.target)});document.querySelectorAll('#more .card').forEach(function(c){c.classList.toggle('hide',f!=='all'&&c.dataset.cat!==f)})})</script>""")
home = home + stories_html + STORY_JS + MOTION
home = home.replace('<span class="n"></span>', '<span class="n">&middot;</span>')
shell("/", f"{HANDLE} — AI engineer: secure AI agents, automation & AppSec",
      f"{HANDLE} ({THAI}) is an AI engineer building agents and automation with security controls built in: LINE/Telegram bots, n8n pipelines, RAG assistants and hands-on AppSec (OWASP Juice Shop). Portfolio and live tools.",
      home, [person, site_ld])

# ------------------------------------------------------------------ Thai product pages (target Thai search queries)
faq = [
 ("ค่าธรรมเนียม Shopee รวมกี่ %?", "ไม่มีตัวเลขเดียวสำหรับทุกร้าน ขึ้นกับประเภทร้าน หมวดสินค้า และโปรแกรมที่เข้าร่วม ตามตารางของ FlowAccount ปี 2569 Shopee มีค่าคอมมิชชั่น 7.49–19.26% ค่าธุรกรรม 3.21–7.49% ค่าบริการโปรแกรม 5.35–8.56% (เฉพาะร้านที่เข้าร่วม) และค่าแพลตฟอร์ม 1.07 บาทต่อออเดอร์ กรณีต่ำสุดที่ไม่เข้าโปรแกรมเท่ากับประมาณ 10.70% บวก 1.07 บาท ให้ตรวจอัตราจริงของร้านใน Seller Center"),
 ("ทำไมถูกหักเงินที่ไม่รู้ที่มา ตรวจอย่างไร?", "เปิดหน้ารายได้ของออเดอร์ใน Seller Center จดยอดที่ถูกหักแต่ละบรรทัด หารด้วยราคาขายเพื่อดูเป็น % แล้วเทียบกับอัตราของร้านคุณ ถ้ามีรายการที่ไม่ตรงหรือไม่รู้ที่มา ให้ถ่ายภาพหน้าจอแล้วสอบถามแพลตฟอร์มผ่านศูนย์ช่วยเหลือ ผู้ขายบางคนรายงานว่าเจอการหักที่ไม่คาดคิด เช่น ค่า Affiliate เครื่องมือเปรียบเทียบเป็นเพียงตัวช่วยตรวจ ไม่ได้ยืนยันว่าแพลตฟอร์มผิดพลาด"),
 ("ราคาเสมอตัว (break-even) คิดอย่างไร?", "ราคาที่กำไรเท่ากับศูนย์ คือ (ต้นทุน + ค่าส่งที่ร้านออก + ค่าแพ็ก + ค่าแพลตฟอร์มคงที่) ÷ (1 − อัตราค่าธรรมเนียมรวมเป็นสัดส่วน − สัดส่วนค่าโฆษณา) ถ้ามีเพดานค่าธรรมเนียมต่อชิ้น เช่น ค่า Commerce Growth ของ TikTok Shop ที่มีเพดาน 199 บาท ต้องคิดแยกเมื่อราคาสูง เครื่องมือฟรีคำนวณให้อัตโนมัติ"),
 ("ROAS เสมอตัวคืออะไร?", "ค่า ROAS ต่ำสุดที่ยิงโฆษณาแล้วไม่ขาดทุน คำนวณจากราคาขายหารกำไรก่อนหักค่าโฆษณา เช่น ตัวอย่างด้านล่างได้ประมาณ 2.4 ถ้า ROAS จริงต่ำกว่านี้ ออเดอร์จากแอดทำให้ขาดทุน"),
 ("เครื่องมือฟรีหรือเปล่า ข้อมูลไปไหน?", "ฉบับพื้นฐาน (คำนวณกำไร ตั้งอัตรา) ใช้ฟรี ไม่ต้องสมัคร ข้อมูลที่กรอกเก็บในเบราว์เซอร์ของคุณเท่านั้น ไม่ส่งขึ้นเซิร์ฟเวอร์ ฉบับเต็มราคา 99 บาท เพิ่มตรวจยอดที่ถูกหักเทียบอัตรา บันทึกหลายสินค้า และส่งออก CSV"),
]
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
article_ld = {"@context": "https://schema.org", "@type": "Article", "headline": "ค่าธรรมเนียม Shopee, Lazada, TikTok Shop ปี 2569 คิดยังไง (พร้อมตัวอย่างคำนวณ)", "inLanguage": "th",
              "datePublished": TODAY, "dateModified": TODAY, "author": {"@id": f"{BASE}/#person"}, "mainEntityOfPage": f"{BASE}/guide/shopee-lazada-tiktok-fees-2569/", "citation": SRC}
faq_html = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in faq)
guide = f"""<div class="page"><h1>ค่าธรรมเนียม Shopee, Lazada, TikTok Shop ปี 2569 คิดยังไง</h1>
<p class="note">ตัวเลขอ้างอิงจากบทความของ <a href="{SRC}" rel="nofollow noopener">FlowAccount</a> ตรวจเมื่อ {TODAY} (รวม VAT) แพลตฟอร์มปรับอัตราบ่อยและแต่ละร้านต่างกัน ให้ยืนยันกับ Seller Center ของร้านคุณก่อนตัดสินใจ</p>
<p><b>คำตอบสั้น:</b> ไม่มีตัวเลข % เดียวที่ใช้ได้ทุกร้าน ค่าธรรมเนียมแยกเป็นหลายก้อน (คอมมิชชั่น ค่าธุรกรรม ค่าโปรแกรม ค่าคงที่ต่อออเดอร์) ที่รวมกันเป็นสิบกว่า % ของราคาขาย ใช้ตารางด้านล่างประมาณการ แล้วคำนวณของร้านคุณด้วยเครื่องมือฟรี</p>
<h2>ตารางอัตราค่าธรรมเนียม (ปี 2569)</h2><div class="tl"><table>
<tr><th>แพลตฟอร์ม</th><th>ค่าธรรมเนียม</th><th>อัตรา</th><th>เงื่อนไข</th></tr>
<tr><td rowspan="4">Shopee</td><td>คอมมิชชั่น</td><td>7.49–19.26%</td><td>ตามประเภทร้านและหมวด</td></tr>
<tr><td>ค่าบริการโปรแกรม</td><td>5.35–8.56%</td><td>เฉพาะร้านที่เข้าร่วมโปรแกรม</td></tr>
<tr><td>ค่าธุรกรรมการชำระเงิน</td><td>3.21–7.49%</td><td>ต่างกันตามวิธีชำระ</td></tr>
<tr><td>ค่าแพลตฟอร์ม</td><td>1.07 บาท</td><td>ทุกออเดอร์</td></tr>
<tr><td rowspan="4">TikTok Shop</td><td>คอมมิชชั่นการตลาด</td><td>5.35–7.49%</td><td>ตามหมวดสินค้า</td></tr>
<tr><td>ค่าธุรกรรม</td><td>3.21%</td><td>ทุกคำสั่งซื้อ</td></tr>
<tr><td>ค่า Commerce Growth</td><td>5.35–6.42%</td><td>เพดาน 199 บาทต่อชิ้น</td></tr>
<tr><td>ค่าแพลตฟอร์ม</td><td>1.07 บาท</td><td>เฉพาะร้านขาย &gt;100 ชิ้นใน 30 วัน</td></tr>
<tr><td rowspan="2">Lazada</td><td>ค่าธรรมเนียมการขาย</td><td>6.96–18.73%</td><td>ตามประเภทร้านและหมวด</td></tr>
<tr><td>ค่าชำระเงิน</td><td>3.21%</td><td>ทุกช่องทาง</td></tr></table></div>
<h2>ตัวอย่างคำนวณ: ขายสินค้า 199 บาทบน Shopee</h2>
<p>สมมติ (เป็นตัวอย่างเท่านั้น): ร้านไม่เข้าโปรแกรมบริการ ใช้อัตราต่ำสุดในตาราง ต้นทุนสินค้า 90 บาท ค่าแพ็ก 5 บาท ไม่ซื้อโฆษณา</p>
<div class="tl"><table><tr><th>รายการ</th><th>บาท</th><th>% ของราคา</th></tr>
<tr><td>ราคาขาย</td><td>199.00</td><td>100.0%</td></tr><tr><td>− คอมมิชชั่น 7.49%</td><td>14.91</td><td>7.5%</td></tr>
<tr><td>− ค่าธุรกรรม 3.21%</td><td>6.39</td><td>3.2%</td></tr><tr><td>− ค่าแพลตฟอร์ม</td><td>1.07</td><td>0.5%</td></tr>
<tr><td>− ต้นทุนสินค้า</td><td>90.00</td><td>45.2%</td></tr><tr><td>− ค่าแพ็ก</td><td>5.00</td><td>2.5%</td></tr>
<tr><td><b>= กำไร</b></td><td><b>81.64</b></td><td><b>41.0%</b></td></tr></table></div>
<p>ค่าธรรมเนียมรวม 22.36 บาท (11.2%) ราคาเสมอตัวประมาณ 107.59 บาท และ ROAS เสมอตัวประมาณ 2.4 ถ้าร้านเข้าโปรแกรมบริการหรือหมวดมีคอมมิชชั่นสูงกว่านี้ ตัวเลขจะต่างมาก จึงควรใส่อัตราจริงของร้าน</p>
<p><a class="btn p" href="{FREE_TOOL}">คำนวณของร้านคุณฟรี</a></p>
<h2>คำถามที่พบบ่อย</h2>{faq_html}
<h2>ข้อจำกัดที่ควรรู้</h2><ul><li>อัตราในตารางเป็นค่าสาธารณะ ไม่ใช่ข้อเสนอเฉพาะของร้านคุณ</li><li>ไม่ครอบคลุมภาษี (เช่น VAT หรือภาษีเงินได้) กรุณาปรึกษาผู้ทำบัญชี</li><li>ไม่ได้ดึงข้อมูลจากแพลตฟอร์มอัตโนมัติ ต้องกรอกตัวเลขเอง</li></ul>
{hire_box(True)}<p class="note">เขียนโดย <a href="/">{HANDLE} ({THAI})</a> · ปรับปรุงล่าสุด {TODAY}</p></div>"""
shell("/guide/shopee-lazada-tiktok-fees-2569/", "ค่าธรรมเนียม Shopee, Lazada, TikTok Shop 2569 คิดยังไง",
      "สรุปอัตราค่าธรรมเนียม Shopee, Lazada, TikTok Shop ปี 2569 พร้อมวิธีตรวจยอดที่ถูกหัก ตัวอย่างคำนวณกำไรต่อออเดอร์ ราคาเสมอตัว และ ROAS เสมอตัว",
      guide, [article_ld, faq_ld, person], lang="th")

app_ld = {"@context": "https://schema.org", "@type": "WebApplication", "name": "ตัวอ่านค่าธรรมเนียมร้านออนไลน์", "url": f"{BASE}/tools/fee-reader/",
          "applicationCategory": "BusinessApplication", "operatingSystem": "Any (web browser)", "inLanguage": "th",
          "description": "คำนวณกำไรหลังหักค่าธรรมเนียม Shopee, TikTok Shop, Lazada ราคาเสมอตัว และ ROAS เสมอตัว", "author": {"@id": f"{BASE}/#person"},
          "offers": [{"@type": "Offer", "name": "ฉบับฟรี", "price": "0", "priceCurrency": "THB"}, {"@type": "Offer", "name": "ฉบับเต็ม", "price": "99", "priceCurrency": "THB"}]}
tool = f"""<div class="page"><h1>ตัวอ่านค่าธรรมเนียมร้านออนไลน์</h1>
<p>เครื่องมือเว็บสำหรับผู้ขาย Shopee, TikTok Shop และ Lazada ใช้บนมือถือหรือคอมได้ทันที ไม่ต้องสมัคร ไม่ต้องติดตั้ง</p>
<p><a class="btn p" href="{FREE_TOOL}">เปิดฉบับฟรี</a></p>
<h2>ทำอะไรได้</h2><ul><li>แยกให้เห็นว่าราคาขายถูกหักเป็นคอมมิชชั่น ค่าธุรกรรม ค่าแพลตฟอร์มเท่าไร เหลือกำไรกี่บาทและกี่ %</li>
<li>บอกราคาเสมอตัวและราคาที่ได้กำไรตามเป้า (รวมเพดานค่า Commerce Growth ของ TikTok Shop)</li><li>บอก ROAS เสมอตัว ก่อนซื้อโฆษณา</li><li>แก้อัตราเองเมื่อแพลตฟอร์มปรับค่าธรรมเนียม</li></ul>
<h2>ฉบับฟรี และฉบับเต็ม 99 บาท</h2><div class="tl"><table><tr><th></th><th>ฟรี</th><th>เต็ม 99 บาท</th></tr>
<tr><td>คำนวณกำไร ราคาเสมอตัว ROAS</td><td>✓</td><td>✓</td></tr><tr><td>ตั้งอัตราเอง</td><td>✓</td><td>✓</td></tr>
<tr><td>ตรวจยอดที่ถูกหักเทียบอัตรา (แจ้งเตือนเมื่อหักเกิน)</td><td>–</td><td>✓</td></tr><tr><td>บันทึกหลายสินค้า และส่งออก CSV</td><td>–</td><td>✓</td></tr></table></div>
<h2>ข้อจำกัด</h2><ul><li>อัตราตั้งต้นเป็นข้อมูลสาธารณะ (ดู<a href="/guide/shopee-lazada-tiktok-fees-2569/">คู่มือค่าธรรมเนียม</a>) ต้องแก้ให้ตรงกับร้านคุณ</li><li>ไม่ดึงข้อมูลจากแพลตฟอร์มอัตโนมัติ</li><li>ไม่ใช่คำแนะนำภาษีหรือบัญชี</li><li>ข้อมูลเก็บในเบราว์เซอร์เครื่องนี้ ควรส่งออก CSV เก็บไว้</li></ul>{hire_box(True)}</div>"""
shell("/tools/fee-reader/", "ตัวอ่านค่าธรรมเนียมร้านออนไลน์ — คำนวณกำไรฟรี",
      "เครื่องมือฟรีบนมือถือ ดูว่าแต่ละบาทที่ขายถูกหักเป็นอะไร เหลือกำไรเท่าไร ราคาเสมอตัว ROAS เสมอตัว แก้อัตราเองได้ ข้อมูลอยู่ในเครื่องคุณ", tool, [app_ld, person], lang="th")

# ------------------------------------------------------------------ security reports (PDFs, sourced from the author's own auto-facebook/career/portfolio)
SECURITY_SRC = ROOT.parent / "auto-facebook" / "career" / "portfolio"
(OUT / "security").mkdir(parents=True, exist_ok=True)
_sec_files = [
    (SECURITY_SRC / "report-01-juice-shop" / "Portfolio-Report-1-Juice-Shop-Security-Assessment.pdf", "report-1-juice-shop.pdf"),
    (SECURITY_SRC / "report-02-remediation" / "Portfolio-Report-2-From-Finding-to-Fix.pdf", "report-2-remediation.pdf"),
]
for src, name in _sec_files:
    fixed = H / "src" / "reports" / name  # regenerated with the author name filled in
    if fixed.exists():
        shutil.copyfile(fixed, OUT / "security" / name)
    elif src.exists():
        shutil.copyfile(src, OUT / "security" / name)

# ------------------------------------------------------------------ n8n + LINE guides (Thai)
def affiliate_box():
    u = cfg.get("n8n_affiliate_url", "")
    if not u:
        return ""
    return ('<div class="box"><b>ลิงก์แนะนำ n8n Cloud</b><br>ถ้าคุณสมัครผ่าน <a href="' + html.escape(u) + '" rel="sponsored noopener">ลิงก์นี้</a> '
            'ผมอาจได้รับค่าคอมมิชชันจาก n8n โดยราคาที่คุณจ่ายไม่เปลี่ยนแปลง ผมเขียนเนื้อหาตามข้อมูลที่ตรวจได้ ไม่ว่าคุณจะใช้ลิงก์นี้หรือไม่</div>')


def store_box():
    u = cfg.get("store_url", "")
    if not u:
        return ""
    return '<div class="box">มีชุดแม่แบบและเครื่องมือสำหรับร้านค้า: <a href="' + html.escape(u) + '">ดูที่ร้าน</a></div>'



guide_urls = []
for a in ARTICLES:
    path = f"/guides/{a['slug']}/"
    guide_urls.append(path)
    body = a["body"].replace("{CHECKED}", CHECKED).replace("{AFFILIATE}", affiliate_box())
    page = (f'<div class="page"><h1>{html.escape(a["title"])}</h1>{body}{store_box()}{hire_box()}'
            f'<p class="note">เขียนโดย <a href="/">{HANDLE} ({THAI})</a> · ตรวจข้อมูลล่าสุด {CHECKED} · <a href="/guides/">คู่มือทั้งหมด</a></p></div>')
    art_ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "inLanguage": "th", "datePublished": TODAY,
              "dateModified": TODAY, "author": {"@id": f"{BASE}/#person"}, "mainEntityOfPage": f"{BASE}{path}"}
    faq_ld2 = {"@context": "https://schema.org", "@type": "FAQPage",
               "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": t}} for q, t in a["faq"]]}
    faq_html2 = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(t)}</p></details>" for q, t in a["faq"])
    page = page.replace('<p class="note">เขียนโดย', f'<h2>คำถามที่พบบ่อย</h2>{faq_html2}<p class="note">เขียนโดย', 1)
    shell(path, a["title"], a["desc"], page, [art_ld, faq_ld2, person], lang="th")

hub_items = "".join(f'<div class="card"><h3 style="margin:0 0 4px"><a href="/guides/{a["slug"]}/">{html.escape(a["title"])}</a></h3><p class="note" style="margin:0">{html.escape(a["desc"])}</p></div>' for a in ARTICLES)
shell("/guides/", "คู่มือ n8n + LINE ภาษาไทย", "รวมคู่มือภาษาไทยเรื่อง n8n และ LINE Messaging API: ย้ายจาก LINE Notify, Reply/Push/Multicast/Broadcast, บอตตอบอัตโนมัติ, Rich Menu และการเลือก n8n Cloud หรือโฮสต์เอง",
      f'<div class="page"><h1>คู่มือ n8n + LINE (ภาษาไทย)</h1><p class="note">ทุกเรื่องตรวจกับเอกสารทางการ ณ {CHECKED} และบอกชัดเจนว่าส่วนไหนยังไม่ได้ทดสอบกับบัญชีจริง</p><div class="grid g2">{hub_items}</div>{hire_box()}</div>',
      [person], lang="th")

# ------------------------------------------------------------------ assets, og, robots, sitemap
from PIL import Image  # noqa: E402
cat = Image.open(ROOT / "films/ep02-hot-desk/assets/cat_12.png").convert("RGBA")
cat.thumbnail((520, 640))
cat.save(OUT / "assets" / "cat.png", optimize=True)
from PIL import Image as _I
_me = _I.open(str(H / "src" / "me.jpg")).convert("RGB"); _me.thumbnail((480, 600)); _me.save(OUT / "assets" / "me.jpg", quality=88, optimize=True)

sys.path.insert(0, str(ROOT / "tools"))
from thai_text import find_chrome  # noqa: E402
cat64 = base64.b64encode((OUT / "assets" / "cat.png").read_bytes()).decode()
og = f"""<!doctype html><meta charset=utf-8><style>body{{margin:0;width:1200px;height:630px;background:radial-gradient(900px 500px at 85% 0%,#4a2a14,#0c0e13 70%);font-family:Segoe UI,Arial,sans-serif;color:#eef1f6;display:flex;align-items:center}}
.t{{padding:0 70px;width:760px}}.e{{color:#ff8a3d;font-weight:700;letter-spacing:.16em;font-size:26px}}h1{{font-size:96px;margin:10px 0;letter-spacing:-2px}}p{{font-size:34px;margin:0;color:#9aa5b8;line-height:1.35}}img{{height:500px}}</style>
<div class=t><div class=e>PORTFOLIO</div><h1>noppruts</h1><p>AI agents · automation<br>· data tools</p></div><img src="data:image/png;base64,{cat64}">"""
tmp = H / "og.html"
tmp.write_text(og, encoding="utf-8")
subprocess.run([find_chrome(), "--headless", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630", "--force-device-scale-factor=1",
                "--virtual-time-budget=2000", f"--screenshot={(OUT / 'og.png').resolve()}", tmp.resolve().as_uri()], check=True, capture_output=True, timeout=90)
tmp.unlink()

urls = ["/", "/guides/", "/guide/shopee-lazada-tiktok-fees-2569/", "/tools/fee-reader/", "/security/report-1-juice-shop.pdf", "/security/report-2-remediation.pdf"] + guide_urls
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                 + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls) + "</urlset>", encoding="utf-8")
(OUT / "llms.txt").write_text(f"# {HANDLE} ({THAI})\n> Builds AI agents, workflow automation and data tools. Portfolio and live tools.\n\n- [Portfolio]({BASE}/)\n- [Thai fee guide 2569]({BASE}/guide/shopee-lazada-tiktok-fees-2569/)\n- [Shop fee reader tool]({BASE}/tools/fee-reader/)\n- [Security findings report]({BASE}/security/report-1-juice-shop.pdf)\n- [Security remediation report]({BASE}/security/report-2-remediation.pdf)\n", encoding="utf-8")
print("built", sorted(str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()))
