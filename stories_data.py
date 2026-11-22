"""Per-project stories shown in the 'Read the full story' dialog. Facts come from each project's own README and code."""
import html

STORY = {
    "Agent Invest": dict(
        what="A FastAPI backend and Next.js dashboard. Four AI agents (news, fundamental, technical, sentiment) analyse a symbol in parallel and an orchestrator combines them. Every prediction is stored and later compared with the real price, so accuracy can be tracked per timeframe and symbol. A Telegram bot sends the daily report and answers commands or natural-language questions. Built with a teammate.",
        why=["Agents run in parallel (a pool of 4), so total time is the slowest agent, not the sum.",
             "Scoring is weighted by each agent's confidence instead of a majority vote, so a low-confidence agent counts for less.",
             "The model is a single environment variable (OpenRouter), so swapping it needs no agent changes.",
             "Calibration (Brier score) is tracked apart from direction accuracy, so over-confidence shows even when the call was right.",
             "Costly or risky features (RAG, auto-analysis, local model) are off by default behind flags."],
        probs=[("An agent times out or crashes mid-analysis", "It falls back to a neutral, low-confidence result so one failure does not block the whole analysis."),
               ("Embedding API or pgvector is unavailable", "RAG degrades gracefully: the analysis still runs, just without similar past cases."),
               ("Anyone could post fake updates to the Telegram webhook", "A webhook secret token rejects forged requests, and a separate admin token protects the admin endpoints.")],
        limits=["The target-price formula (price x (1 + confidence x 0.1)) ignores each symbol's volatility. The repo's own analysis flags it, so do not over-read the price-error figures.",
                "Wallet check only identifies the address type and links to an explorer; no balance or risk score yet.",
                "Free versus paid content is two separate Telegram targets, not real membership checks."]),
    "LendLoop": dict(
        what="A neighbourhood tool-lending board. Neighbours list tools, request them for a date range, and lenders approve, decline or mark them returned. Convex holds the data and server functions; n8n sends notifications and a daily overdue reminder. Admins can remove listings and mark Trusted Lenders. It was a take-home project.",
        why=["Access rules live in the Convex functions, never in the UI, because hiding a button is not security.",
             "Roles come from a server-side allowlist, never from the client.",
             "The public query returns only tool name and category; webhook payloads carry only what the message needs (data minimisation).",
             "HMAC-SHA256 in both directions, signing timestamp, method, path and body."],
        probs=[("A signed request could be replayed", "Timestamps older than 5 minutes are rejected, and method plus path are part of the signature, so one endpoint's signature cannot be reused on another."),
               ("Retries could send the same reminder twice", "Each reminder has a deterministic ID (loan + date) stored as a unique key; replays do nothing, and the overdue query skips loans already reminded today."),
               ("n8n re-serialising the JSON would break the signature", "n8n verifies against the exact raw bytes of the request body."),
               ("A failed notification could go unnoticed", "Convex retries up to 5 times with exponential backoff and records sent / retrying / failed on each loan; n8n also has an error workflow.")],
        limits=["Notifications are a logged mock, as the brief allowed. Real email, Slack or Discord is a node swap.",
                "Not production-ready by my own README: secret manager with rotation, rate limiting, pagination, time zones (overdue uses UTC dates) and CI are listed as next steps."]),
    "LINE AI Assistant for a Repair Shop": dict(
        what="One LINE Official Account for a repair shop with two audiences. Staff send a fault code or symptom and get a structured diagnosis (likely cause, things to check, suggestions) and log finished jobs. Customers link their LINE to their phone number and get a service reminder about 6 months later, pushed by a daily scheduler in the same process. A rich menu gives customers quick answers (hours, price, booking).",
        why=["The bottleneck for mechanics is interpreting a code or symptom, not reading it off the car, so the AI does interpretation only.",
             "Real chat history showed most customer questions are about specific parts and prices that need an inventory check, so the bot asks for car model and contact details up front and a person answers.",
             "Service history is an Excel workbook the shop already understands, with a flat 180-day reminder interval as the default.",
             "When a message is unclear or not car-related the bot stays silent rather than force-fitting a reply."],
        probs=[("The free-tier model sometimes returned a valid-looking but empty answer", "Treated as a retryable failure like a rate limit; it retries and usually gets a real answer."),
               ("Rate limits on a single free key", "Several keys are rotated from one environment variable."),
               ("The AI classified greetings and FAQs inconsistently between runs", "Instead of tuning the prompt forever, common greetings and FAQ patterns are caught by deterministic rules before the AI is called."),
               ("Customers send photos of parts", "A vision model gives a best-effort hint for staff; if it is unavailable the plain reply is sent. It never quotes a price from a photo."),
               ("Forged webhook calls", "The LINE signature header is verified on every request and invalid ones are rejected.")],
        limits=["Diagnosis is advice for staff, not a final answer.", "The Excel workbook is simple but would need a database at larger scale."]),
    "AppSec Testing & Remediation (OWASP Juice Shop)": dict(
        what="A hands-on web security exercise on a local copy of OWASP Juice Shop v20.2.0, run like a small engagement: find, document, fix, re-test. Three vulnerabilities were found and written up with full requests and responses, then patched in the code and checked against the original exploit requests.",
        why=["Listing findings is not enough; I wanted to show the fix and prove it held.",
             "A training app on my own machine keeps it legal and safe, and there is no real client."],
        probs=[("SQL injection login bypass (critical)", "Replaced string-built SQL with a parameterised query."),
               ("IDOR on the basket API (high)", "The server now checks ownership from the session token instead of trusting the id in the request."),
               ("SQL injection in search with verbose errors (medium)", "Parameterised the query and return a safe error with no stack trace."),
               ("A fix might break normal use", "Replayed the original exploit requests (now 401/403 or empty) and re-tested normal login, own basket and search.")],
        limits=["Training app only, so it shows method, not production experience.", "Three findings from one app is a small sample."]),
    "Test-Eng Assist": dict(
        what="A local, autonomous command-line agent for test engineers. An agent loop calls tools; documents are ingested and indexed for retrieval (ChromaDB); a scheduler runs recurring jobs; a dashboard shows results. It is packaged as a Windows executable. Demo data is synthetic.",
        why=["Everything runs locally so manuals and test data stay on the machine.",
             "A tool registry is the single dispatch point and owns the confirmation prompts for risky actions.",
             "Documents are split into 500-character chunks with 50 overlap, a simple choice that keeps context across boundaries."],
        probs=[("The embedding model downloads on first use and stalls the file watcher", "A pre-warm step triggers the download before the watcher starts."),
               ("Re-ingesting an edited file leaves stale chunks", "Old chunks for that file are deleted before the new ones are added."),
               ("Retrieval is unavailable if ChromaDB fails", "It falls back to keyword search."),
               ("A packaged exe cannot write next to its own files", "Paths switch to a writable location when running frozen.")],
        limits=["The built-in knowledge base and test data are mock/synthetic, so this demonstrates the design rather than production results."]),
    "AI Content Factory (n8n + Python)": dict(
        what="n8n decides what to make and when (schedule, topic, approval routing, analytics). A Python service turns a topic into a subtitled 9:16 video (script, scenes, video generation, voice-over, FFmpeg) behind a local HTTP API. Facebook Reels publishing was tested with a real post. Nothing publishes without explicit approval.",
        why=["n8n is good at scheduling, branching, retries and waiting for a human; Python is good at FFmpeg, files and deterministic state. Each does what it is best at.",
             "A SQLite-backed state machine (CREATED through UPLOADED) means every step can resume after a restart.",
             "Job IDs live in memory, because the project's own status is already the durable source of truth."],
        probs=[("Facebook's documented upload order did not work", "Live testing showed the status stuck, so the flow was corrected to finish-before-poll from a real published test."),
               ("A publish call can report success without the video being live", "A project is marked uploaded only when Facebook's status explicitly says published; otherwise it reports an unknown status and a retry does not re-upload."),
               ("Facebook puts the access token in the URL, which HTTP logs would print", "HTTP client logging is silenced at INFO level so the token never reaches the logs."),
               ("LLM output is sometimes malformed", "Responses are validated against a schema and retried up to 3 times, then fail clearly instead of inventing missing fields."),
               ("The video model only supports fixed clip lengths", "Scene lengths are rounded to the nearest supported value and FFmpeg handles final timing.")],
        limits=["Default subtitles use scene timing, not speech alignment; a Whisper option exists.", "Mock providers produce placeholder clips; real video generation needs API keys and billing."]),
}


SHOTS = {
    "LendLoop": [("lendloop-dashboard.jpg", "Lender dashboard: incoming requests, with the automation log (notify:request_created and notify:approved, both sent by n8n) on each loan.")],
    "AppSec Testing & Remediation (OWASP Juice Shop)": [("juice-findings.jpg", "Report 1 (findings): proof of concept for the basket IDOR, with the request, root cause and remediation."),
                                                      ("juice-remediation.jpg", "Report 2 (remediation): the same exploit request now returns 401, and a legitimate login still returns 200.")],
}


def story_html(p, DETAILS):
    st = STORY.get(p["title"])
    d = DETAILS.get(p["title"])
    e = html.escape
    if st:
        why = "".join(f"<li>{e(x)}</li>" for x in st["why"])
        pr = "".join(f'<div class="pp"><div class="pq">{e(a)}</div><div class="pa">{e(b)}</div></div>' for a, b in st["probs"])
        lim = "".join(f"<li>{e(x)}</li>" for x in st["limits"])
        fig = "".join(f'<figure class="shot"><img src="/assets/shots/{f}" alt="{e(c)}" loading="lazy"><figcaption>{e(c)}</figcaption></figure>' for f, c in SHOTS.get(p["title"], []))
        body = (f'<h4>What I built</h4><p>{e(st["what"])}</p>{fig}<h4>Why it is built this way</h4><ul>{why}</ul>'
                f'<h4>Problems I hit and how I solved them</h4>{pr}<h4>Limits and honest caveats</h4><ul>{lim}</ul>')
    elif d:
        steps = "".join(f"<li>{e(x)}</li>" for x in d["flow"])
        body = (f'<h4>Problem it addresses</h4><p>{e(d["why"])}</p><h4>How it works</h4><ol>{steps}</ol>'
                f'<h4>Controls and checks</h4><p>{e(d["ctrl"])}</p><h4>When showing it</h4><p>{e(d["show"])}</p>')
    else:
        body = f'<p>{e(p["body"])}</p>'
    return f'<div class="story-body"><h3>{e(p["title"])}</h3><p class="s" style="margin:0 0 4px">{e(p["body"][:0])}</p>{body}</div>'


STORY_CSS = """.shot{margin:14px 0 4px}.shot img{width:100%;height:auto;border:1px solid var(--line);border-radius:10px;background:#fff;display:block}.shot figcaption{font-size:13px;color:var(--mut);margin-top:6px}
.ch{margin:16px 0 6px;font:600 12px ui-monospace,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--acc)}
.cert ul{padding-left:18px;margin:0}.cert li{font-size:15px;line-height:1.55;margin:0 0 5px;color:#cfd6e4}.slink{white-space:nowrap;font-weight:600}
@media(min-width:1100px){.certs{grid-template-columns:repeat(3,1fr)}}
.card[data-sid],.card[data-href]{cursor:pointer}
.story-btn{font-size:14px;padding:8px 14px}
dialog#story{width:min(760px,94vw);max-height:88vh;padding:0;border:1px solid var(--line);border-radius:18px;background:#10141c;color:var(--ink);box-shadow:0 30px 80px rgba(0,0,0,.6)}
dialog#story::backdrop{background:rgba(4,6,10,.72);backdrop-filter:blur(3px)}
#story .sx{position:sticky;top:0;display:flex;justify-content:flex-end;padding:10px 12px 0;background:#10141c}
#story .sx button{background:transparent;border:1px solid var(--line);color:var(--ink);border-radius:10px;padding:6px 12px;cursor:pointer;font:600 13px ui-monospace,Consolas,monospace}
.story-body{padding:0 26px 26px}.story-body h3{margin:0 0 6px;font-size:24px}
.story-body h4{margin:22px 0 8px;font:600 12px ui-monospace,Consolas,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--acc)}
.story-body p,.story-body li{font-size:15.5px;line-height:1.65;color:#cfd6e4}.story-body ul,.story-body ol{padding-left:20px;margin:0}
.pp{border-left:2px solid var(--acc);padding:2px 0 2px 14px;margin:0 0 12px}.pq{font-weight:600;color:var(--ink)}.pa{color:#aeb8cb;font-size:15px}
"""

STORY_JS = """<dialog id="story" aria-label="Project story"><div class="sx"><button type="button" id="sclose">Close (Esc)</button></div><div id="sbody"></div></dialog>
<script>(function(){var d=document.getElementById('story'),b=document.getElementById('sbody'),src=document.getElementById('stories');if(!d||!src||!d.showModal)return;
function open(i){var n=src.querySelector('[data-sid="'+i+'"]');if(!n)return;b.innerHTML=n.innerHTML;d.showModal();d.scrollTop=0;try{history.replaceState(null,'','#story-'+i)}catch(e){}}
document.addEventListener('click',function(e){var sl=e.target.closest('.slink');if(sl){e.preventDefault();open(sl.dataset.sid);return}var t=e.target.closest('.story-btn');if(t){open(t.dataset.sid);return}if(e.target===d){d.close();return}if(e.target.closest('a,button,summary,details,dialog'))return;var c=e.target.closest('.card[data-sid]');if(c){open(c.dataset.sid);return}c=e.target.closest('.card[data-href]');if(c){window.open(c.dataset.href,'_blank','noopener')}});
document.getElementById('sclose').addEventListener('click',function(){d.close()});
d.addEventListener('close',function(){try{history.replaceState(null,'',location.pathname+'#work')}catch(e){}});
var m=/^#story-(\\d+)$/.exec(location.hash);if(m)setTimeout(function(){open(m[1])},50)})()</script>"""
