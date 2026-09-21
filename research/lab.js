const NOW = new Date("2026-09-21T10:22:00-05:00");
const KEY = "dbe-observatory-freeze-v2";
const TABS = [
  ["week", "This week"],
  ["month", "Month"],
  ["lookback", "Year lookback"],
  ["catalog", "Catalog"],
  ["engine", "DBE · DBE-S"],
  ["claims", "Claims"],
  ["reviews", "Daily cards"],
  ["versions", "Versions"],
  ["ledger", "Q ledger"],
  ["pillars", "Pillars"],
  ["feeds", "Feeds"],
];
const AUTOGATE = [
  ["A1", "Binds to exactly one existing KEEP or HOLD claim ID."],
  ["A2", "G1–G6 all pass."],
  ["A3", "Action is STRENGTHEN or INCLUDE, not NEW PILLAR, not a CUT reversal."],
  ["A4", "New C ≥ 4, or C stays put and a published numerical bound tightens."],
  ["A5", "Venue is a journal or a replicated hardware result. Bare arXiv cannot auto-raise C."],
  ["A6", "Does not add a new mechanism, bus, fuel, or coupling sentence."],
  ["A7", "Does not increase the number of active HOLD items."],
  ["A8", "Ledger terms, if touched, move in the conservative direction."],
];
const DENY = new Set(["E-HOL", "E-5"]);

let CAT = { papers: [], pillars: [], fields: [], feeds: [], runs: [] };
let CLAIMS = { claims: [], axes: {} };
let VERS = { history: [], buses: [], milestones: [], lines: [], current: {} };
let REVIEWS = { cards: [] };
let LEDGER = {};
let tab = "week", field = "all", q = "", sort = "importance";
let FREEZE = { actions: [], dbe: "DBE-0.1.2", dbes: "DBES-0.1.2", log: [], parkedPaperIds: [] };

const esc = (s) => String(s ?? "")
  .replace(/&/g, "&").replace(/</g, "<").replace(/>/g, ">")
  .replace(/"/g, """).replace(/'/g, "&#39;");
const idea = (p) => p.coreIdea || p.plain || "";
const authors = (p) => Array.isArray(p.authors) ? p.authors : String(p.authors || "").split(",").map((s) => s.trim()).filter(Boolean);
const pdate = (p) => p.date || (p.year ? p.year + "-01-01" : "");
const fieldLabel = (id) => (CAT.fields.find((f) => f.id === id) || {}).short || id;
const paperById = (id) => CAT.papers.find((p) => p.id === id || p.arxiv === id);
const claimById = (id) => (CLAIMS.claims || []).find((c) => c.id === id);
const inWeek = (p) => { const t = Date.parse(pdate(p)); return (Number.isFinite(t) && NOW - t <= 7 * 864e5) || p.role === "week"; };
const inMonth = (p) => String(pdate(p)).startsWith("2026-09") || String(pdate(p)).startsWith("2026-08") || p.role === "month" || inWeek(p);
const inLookback = (p) => pdate(p) >= "2025-09-20" || ["lookback", "week", "month"].includes(p.role);
const isFound = (p) => p.foundational || p.role === "pillar" || p.role === "internal";
const high = (p) => (p.importance || 0) >= 85 && (p.confidence || 0) >= 80;
const low = (p) => (p.importance || 0) < 40 && (p.confidence || 0) < 40;
function roleLabel(p) {
  if (p.role === "internal") return "Program source";
  if (isFound(p)) return "Foundational";
  if (inWeek(p)) return "This week";
  if (inMonth(p)) return "This month";
  if (inLookback(p)) return "Year lookback";
  return p.role || "Catalog";
}
function statusClass(s) {
  s = String(s || "").toUpperCase();
  if (["KEEP", "PASS", "INCLUDE", "STRENGTHEN", "AUTO-MERGED", "DONE"].includes(s)) return "ok";
  if (["CUT", "REJECT", "DISCONFIRM"].includes(s)) return "danger";
  if (["HOLD", "QUEUE", "WATCH", "WEAKEN", "NEW PILLAR", "OPEN"].includes(s)) return "warn";
  return "acc";
}
function toast(msg) {
  document.querySelectorAll(".toast").forEach((n) => n.remove());
  const t = document.createElement("div");
  t.className = "toast";
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2800);
}
function bump(v, kind) {
  const m = String(v).match(/^(DBE|DBES)-(\d+)\.(\d+)\.(\d+)$/);
  if (!m) return v;
  return kind === "patch" ? m[1] + "-" + m[2] + "." + m[3] + "." + (+m[4] + 1)
    : m[1] + "-" + m[2] + "." + (+m[3] + 1) + ".0";
}
function lineFor(bind) { return (bind || []).some((b) => String(b).startsWith("S-")) ? "dbes" : "dbe"; }
function applied(id) { return FREEZE.actions.some((a) => a.reviewId === id); }
function gatePass(card) {
  return ["G1", "G2", "G3", "G4", "G5", "G6"].every((g) => String((card.gates || {})[g]).toLowerCase() === "pass");
}
function autoGate(card) {
  const misses = [];
  const bind = (card.bind || []).filter((id) => claimById(id));
  const c = claimById(bind[0]);
  if (bind.length !== 1 || (c && !["KEEP", "HOLD"].includes(c.status))) misses.push("A1");
  if (!gatePass(card)) misses.push("A2");
  if (!["INCLUDE", "STRENGTHEN"].includes(card.action)) misses.push("A3");
  if ((card.bind || []).some((id) => DENY.has(id))) misses.push("A6");
  if (card.action === "NEW PILLAR") misses.push("A7");
  return { pass: misses.length === 0, misses };
}
function inferProposal(p) {
  const binds = p.claimIds || [];
  if (binds.some((id) => DENY.has(id))) return { action: "REJECT", auto: false, reason: "Denylist. Reading is allowed; INCLUDE is not." };
  if (p.suggestedPillar) return { action: "NEW PILLAR", auto: false, reason: "Needs an interface contract at the weekly freeze." };
  const keep = binds.map(claimById).filter((c) => c && ["KEEP", "HOLD"].includes(c.status));
  if (high(p) && keep.length === 1) return { action: "INCLUDE", auto: true, reason: "High harvest rank on a KEEP/HOLD claim. Bibliography only — gauges cannot raise C." };
  if (keep.length === 1) return { action: "INCLUDE", auto: false, reason: "Binds to an existing claim. PATCH bibliography if applied." };
  return { action: "HOLD", auto: false, reason: "Does not bind cleanly to one KEEP claim." };
}
function saveFreeze() { localStorage.setItem(KEY, JSON.stringify(FREEZE)); }
function loadFreeze() {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || "null");
    if (raw && raw.dbe) return raw;
  } catch (e) { /* ignore */ }
  const published = (REVIEWS.cards || []).filter((c) => c.route === "AUTO-MERGED").map((c) => ({
    reviewId: c.id, paperId: c.paperId, action: c.action, route: "AUTO-MERGED", at: c.date, version: c.version,
  }));
  return {
    actions: published,
    dbe: (VERS.current || {}).DBE || "DBE-0.1.3",
    dbes: (VERS.current || {}).DBES || "DBES-0.1.3",
    parkedPaperIds: [],
    log: [],
  };
}
function applyCard(id) {
  const c = (REVIEWS.cards || []).find((x) => x.id === id);
  if (!c) return;
  if (applied(id)) { toast("Already applied to the working freeze."); return; }
  const action = c.action;
  const bind = c.bind || [];
  const gate = autoGate(c);
  if (action === "STRENGTHEN" && !gate.pass) {
    toast("Auto-Gate blocked a C raise (missed " + gate.misses.join(", ") + ").");
    return;
  }
  if (action === "NEW PILLAR" || (c.route === "QUEUE" && action !== "WEAKEN" && action !== "INCLUDE")) {
    FREEZE.actions.push({ reviewId: id, action, route: "QUEUE", at: new Date().toISOString(), paperId: c.paperId });
    saveFreeze(); toast("Queued " + action + " — no auto-bump"); paintFreeze(); render(); return;
  }
  if (action === "REJECT") {
    FREEZE.actions.push({ reviewId: id, action, route: "REJECT", at: new Date().toISOString(), paperId: c.paperId });
    saveFreeze(); toast("Rejected. Not in the paper."); paintFreeze(); render(); return;
  }
  const line = lineFor(bind);
  const kind = action === "INCLUDE" ? "patch" : "minor";
  FREEZE[line] = bump(FREEZE[line], kind);
  FREEZE.actions.push({ reviewId: id, action, route: gate.pass ? "AUTO-MERGED" : "APPLIED", at: new Date().toISOString(), version: FREEZE[line], paperId: c.paperId });
  saveFreeze(); toast("Applied " + action + " → " + FREEZE.dbe + " / " + FREEZE.dbes); paintFreeze(); render();
}
function proposePaper(pid) {
  const p = paperById(pid);
  if (!p) return;
  const prop = inferProposal(p);
  const syn = { id: "local/" + p.id, paperId: p.id, bind: p.claimIds || [], action: prop.action, route: prop.auto ? "AUTO-MERGED" : "QUEUE", gates: { G1: "pass", G2: "pass", G3: "pass", G4: "pass", G5: "pass", G6: "pass" } };
  REVIEWS.cards.push(syn);
  applyCard(syn.id);
}
function resetFreeze() {
  localStorage.removeItem(KEY);
  FREEZE = loadFreeze();
  toast("Working freeze reset to published current");
  paintFreeze(); render();
}
function paintFreeze() {
  const el = document.getElementById("freezeBar");
  if (!el) return;
  el.innerHTML = "<code>" + esc(FREEZE.dbe) + "</code><span>/</span><code>" + esc(FREEZE.dbes) + "</code><span> " + FREEZE.actions.length + " freeze action" + (FREEZE.actions.length === 1 ? "" : "s") + "</span><button class=\"ghost\" type=\"button\" id=\"resetFreeze\">Reset freeze</button>";
  document.getElementById("resetFreeze").onclick = resetFreeze;
  const stats = document.getElementById("stats");
  if (stats) {
    stats.innerHTML = [["Sources", CAT.papers.length], ["Claims", (CLAIMS.claims || []).length], ["DBE", FREEZE.dbe.replace("DBE-", "")], ["DBE-S", FREEZE.dbes.replace("DBES-", "")]].map((kv) => "<div class=\"stat\"><dt>" + kv[0] + "</dt><dd>" + kv[1] + "</dd></div>").join("");
  }
}
function meters(p) {
  const row = (label, n) => "<div><div class=\"lbl\"><span>" + label + "</span><span>" + (n ?? "—") + "</span></div><div class=\"bar\"><i style=\"width:" + Math.max(4, Math.min(100, n || 0)) + "%\"></i></div></div>";
  return "<div class=\"harvest\" title=\"Harvest metadata only. Not C, T, D, or A.\">" + row("Importance", p.importance) + row("Confidence", p.confidence) + row("Popularity", p.popularity) + "</div>";
}
function axisPills(c) {
  return "<span class=\"axis\"><b>C</b>" + (c.C || "—") + " <b>T</b>" + (c.T || "—") + " <b>D</b>" + (c.D || "—") + " <b>A</b>" + (c.A || "—") + "</span>";
}
function pool() {
  let papers = CAT.papers.slice();
  if (tab === "week") papers = papers.filter(inWeek);
  else if (tab === "month") papers = papers.filter(inMonth);
  else if (tab === "lookback") papers = papers.filter(inLookback);
  else if (tab === "pillars") papers = papers.filter(isFound);
  if (field !== "all") papers = papers.filter((p) => (p.fields || []).includes(field));
  if (q) {
    const s = q.toLowerCase();
    papers = papers.filter((p) => [p.title, authors(p).join(" "), idea(p), p.whyItMatters, p.limitation, p.arxiv, ...(p.tags || []), ...(p.claimIds || [])].join(" ").toLowerCase().includes(s));
  }
  papers = papers.filter((p) => !(FREEZE.parkedPaperIds || []).includes(p.id) || tab === "catalog");
  if (tab !== "catalog") papers = papers.filter((p) => p.role !== "off-path" && p.bindAction !== "REJECT");
  papers.sort((a, b) => sort === "date" ? String(pdate(b)).localeCompare(String(pdate(a))) : (b[sort] || 0) - (a[sort] || 0));
  return papers;
}
function openPaper(id) {
  const p = paperById(id);
  if (!p) return;
  const prop = inferProposal(p);
  const bound = (p.claimIds || []).map(claimById).filter(Boolean);
  const pillar = (CAT.pillars || []).find((x) => x.id === p.pillarId || x.id === p.suggestedPillar);
  const overlay = document.createElement("div");
  overlay.className = "overlay";
  overlay.setAttribute("role", "dialog");
  overlay.innerHTML = "<article class=\"panel\"><p class=\"kicker\">" + esc(p.source || p.venue || "Library") + "</p><h2>" + esc(p.title) + "</h2><p class=\"meta\">" + esc(authors(p).join(", ")) + " · " + esc(pdate(p)) + " · " + esc(p.venue || "") + "</p><div>" + (p.fields || []).map((f) => "<span class=\"tag\">" + esc(fieldLabel(f)) + "</span>").join("") + (p.claimIds || []).map((t) => "<span class=\"tag acc\">" + esc(t) + "</span>").join("") + (p.foundational ? "<span class=\"tag acc\">Foundational</span>" : "") + "</div>" + meters(p) + "<p class=\"notice\">Harvest gauges are ingest metadata (0–100). They are not C, T, D, or A and cannot raise a frozen claim.</p>" + bound.map((c) => "<p class=\"meta\"><span class=\"tag " + statusClass(c.status) + "\">" + esc(c.status) + "</span> <b>" + esc(c.id) + "</b> " + axisPills(c) + "<br/>" + esc(c.verdict) + "</p>").join("") + "<p><b>Core idea.</b> " + esc(idea(p)) + "</p><p><b>Why it matters.</b> " + esc(p.whyItMatters || "") + "</p><p><b>One limitation.</b> " + esc(p.limitation || "") + "</p>" + (pillar ? "<p class=\"meta\"><b>" + esc(pillar.engineStatus || pillar.status) + ": " + esc(pillar.name) + "</b><br/>" + esc(pillar.engineNote || pillar.dbeGoal || "") + "</p>" : "") + "<p class=\"meta\">Next-version prompt: <b>" + esc(prop.action) + "</b> — " + esc(prop.reason) + "</p><div style=\"display:flex;flex-wrap:wrap;gap:0.5rem;margin-top:1rem\">" + (p.url && String(p.url).startsWith("http") ? "<a class=\"chip active\" href=\"" + esc(p.url) + "\" target=\"_blank\" rel=\"noreferrer\">Open source</a>" : "") + "<button class=\"btn ok\" type=\"button\" data-propose=\"" + esc(p.id) + "\">Prompt " + esc(prop.action) + "</button><button class=\"ghost\" type=\"button\">Close</button></div></article>";
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay || e.target.closest(".ghost")) overlay.remove();
    const b = e.target.closest("[data-propose]");
    if (b) { proposePaper(b.dataset.propose); overlay.remove(); }
  });
  document.body.appendChild(overlay);
}
function paperRow(p) {
  return "<button class=\"row\" data-id=\"" + p.id + "\"><div><div>" + (p.foundational ? "<span class=\"tag acc\">Foundational</span>" : "<span class=\"tag\">" + roleLabel(p) + "</span>") + (high(p) ? "<span class=\"tag ok\">High signal</span>" : "") + (low(p) ? "<span class=\"tag warn\">Low signal</span>" : "") + (p.claimIds || []).map((id) => "<span class=\"tag acc\">" + id + "</span>").join("") + "<span class=\"meta\"> " + esc(pdate(p)) + "</span></div><h3>" + esc(p.title) + "</h3><p class=\"meta\">" + esc(authors(p).slice(0, 4).join(", ")) + " · " + esc(p.venue || "") + "</p><p>" + esc(idea(p)) + "</p><div>" + (p.fields || []).map((f) => "<span class=\"tag\">" + esc(fieldLabel(f)) + "</span>").join("") + "</div></div>" + meters(p) + "</button>";
}
function renderEngine() {
  const keep = (CLAIMS.claims || []).filter((c) => c.status === "KEEP");
  const hold = (CLAIMS.claims || []).filter((c) => c.status === "HOLD" || c.status === "WATCH");
  const cut = (CLAIMS.claims || []).filter((c) => c.status === "CUT");
  const queued = (REVIEWS.cards || []).filter((c) => c.route === "QUEUE" && !applied(c.id));
  const autoC = (REVIEWS.cards || []).filter((c) => !applied(c.id) && c.action === "INCLUDE" && autoGate(c).pass);
  const cardC = (c) => "<article class=\"card\"><div style=\"display:flex;justify-content:space-between;gap:0.75rem\"><div><span class=\"mono\" style=\"font-size:0.75rem;color:var(--subtle)\">" + esc(c.id) + "</span><h3>" + esc(c.name) + "</h3><p class=\"meta\">" + esc(c.claim) + "</p></div><span class=\"tag " + statusClass(c.status) + "\">" + esc(c.status) + "</span></div><p>" + axisPills(c) + "</p><p>" + esc(c.verdict) + "</p><div>" + (c.evidence || []).map((id) => "<button class=\"chip\" data-open=\"" + id + "\">" + id + "</button>").join("") + "</div></article>";
  return "<p class=\"notice\">Three layers, never mixed. Harvest gauges cannot raise C. Q = 1000 is a ledger stress test, not an output. KEEP claims with C≥3 ride the paper; CUT sections are already out.</p>"
    + "<div class=\"grid\"><article class=\"card\"><p class=\"kicker\">DBE " + esc(FREEZE.dbe) + "</p><h2>Dimensional Braid Engine</h2><p class=\"meta\">Modular quantum-topological processor + plasma controller</p><p>Post-cut stack: Bus A talks to a real plant. Bus B uses the anyon and QEC results we actually have. Bus C is a microphysics campaign, not a coupled engine.</p></article><article class=\"card\"><p class=\"kicker\">DBE-S " + esc(FREEZE.dbes) + "</p><h2>Dynamic Barrier Evasion</h2><p class=\"meta\">Floquet / laser-RF driven tunneling through the Coulomb barrier</p><p>L1–L4 as HOLD except L3 solvers KEEP. Q = 1000 is a stress test of the energy ledger, not an output of the current stack.</p></article></div>"
    + "<h2>Load-bearing</h2><div class=\"grid\">" + keep.map(cardC).join("") + "</div>"
    + "<h2>Hold / watch</h2><div class=\"grid\">" + hold.map(cardC).join("") + "</div>"
    + "<h2>Removed from the paper</h2><div class=\"grid3\">" + cut.map(cardC).join("") + "</div>"
    + "<h2>Buses</h2><div class=\"grid3\">" + (VERS.buses || []).map((b) => "<article class=\"card\"><h3>Bus " + esc(b.id) + " · " + esc(b.name) + "</h3><p class=\"meta\">" + esc(b.C) + " · " + esc(b.D) + "</p><p>" + esc(b.target) + "</p><p class=\"meta\">" + esc(b.interface) + "</p></article>").join("") + "</div>"
    + "<h2>Milestones</h2><div class=\"grid\">" + (VERS.milestones || []).map((m) => "<article class=\"card\"><div style=\"display:flex;justify-content:space-between\"><h3>" + esc(m.id) + " · " + esc(m.name) + "</h3><span class=\"tag " + statusClass(m.status === "done" ? "KEEP" : "OPEN") + "\">" + esc(m.status) + "</span></div><p class=\"meta\">" + esc(m.note) + "</p></article>").join("") + "</div>"
    + "<h2>Prompt the next version</h2><p class=\"meta\">High-signal INCLUDE cards that pass Auto-Gate A1–A8 can merge as PATCH. NEW PILLAR and CUT reversals never auto-bump.</p>"
    + (autoC.length ? autoC.map((c) => { const p = paperById(c.paperId) || {}; return "<article class=\"card\"><span class=\"tag ok\">" + esc(c.action) + "</span> " + (c.bind || []).map((id) => "<span class=\"tag acc\">" + id + "</span>").join("") + "<h3>" + esc(p.title || c.paperId) + "</h3><p>" + esc((c.plain && c.plain.core) || idea(p)) + "</p><div style=\"display:flex;gap:0.5rem\"><button class=\"chip\" data-open=\"" + c.paperId + "\">Open</button><button class=\"btn ok\" data-apply=\"" + c.id + "\">Auto-merge PATCH</button></div></article>"; }).join("") : "<p class=\"meta\">No unpublished Auto-Gate INCLUDE cards waiting.</p>")
    + (queued.length ? "<h3>Weekly queue</h3>" + queued.map((c) => { const p = paperById(c.paperId) || {}; return "<article class=\"card\"><span class=\"tag warn\">" + esc(c.action) + "</span> <span class=\"tag\">QUEUE</span><h3>" + esc(p.title || c.paperId) + "</h3><p>" + esc((c.plain && c.plain.core) || idea(p)) + "</p><p class=\"meta\">" + esc(c.whyQueued || c.gateNote || "") + "</p><button class=\"btn warn\" data-apply=\"" + c.id + "\">Queue on freeze</button></article>"; }).join("") : "")
    + "<h2>Suggested pillars</h2><div class=\"grid\">" + (CAT.pillars || []).filter((p) => p.status === "suggested" || p.engineStatus === "QUEUE").map((p) => "<article class=\"card\"><div style=\"display:flex;justify-content:space-between\"><h3>" + esc(p.name) + "</h3><span class=\"tag warn\">" + esc(p.engineStatus || "QUEUE") + "</span></div><p>" + esc(p.statement) + "</p><p class=\"meta\">" + esc(p.whySuggested || p.engineNote || "") + "</p></article>").join("") + "</div>";
}
function renderClaims() {
  const groups = { DBE: [], "DBE-S": [] };
  (CLAIMS.claims || []).forEach((c) => (groups[c.doc] || (groups[c.doc] = [])).push(c));
  return "<p class=\"notice\">" + esc(CLAIMS.rule || "") + "</p>" + Object.entries(groups).map(([doc, list]) => "<h2>" + doc + "</h2><div class=\"grid\">" + list.map((c) => "<article class=\"card\"><div style=\"display:flex;justify-content:space-between;gap:0.75rem\"><div><span class=\"mono\" style=\"font-size:0.75rem;color:var(--subtle)\">" + esc(c.id) + "</span><h3>" + esc(c.name) + "</h3><p class=\"meta\">" + esc(c.claim) + "</p></div><span class=\"tag " + statusClass(c.status) + "\">" + esc(c.status) + "</span></div><p>" + axisPills(c) + "</p><p>" + esc(c.verdict) + "</p><p class=\"meta\"><b>Disputer.</b> " + esc(c.disputer) + "</p><p class=\"meta\"><b>Kill.</b> " + esc(c.kill) + "</p><div>" + (c.evidence || []).map((id) => "<button class=\"chip\" data-open=\"" + id + "\">" + id + "</button>").join("") + "</div></article>").join("") + "</div>").join("");
}
function renderReviews() {
  return "<p class=\"notice\">One card per paper. Harvest 0–100 numbers are not C. Auto-Gate A1–A8 is the only way a daily run versions the paper without a human.</p><div class=\"grid\">" + AUTOGATE.map((a) => "<p class=\"meta\"><span class=\"mono\" style=\"color:var(--acc)\">" + a[0] + "</span> " + a[1] + "</p>").join("") + "</div>" + (REVIEWS.cards || []).map((c) => {
    const p = paperById(c.paperId) || {};
    const g = autoGate(c);
    return "<article class=\"card\"><span class=\"tag " + statusClass(c.action) + "\">" + esc(c.action) + "</span> <span class=\"tag " + statusClass(c.route) + "\">" + esc(c.route) + "</span> " + (c.bind || []).map((id) => "<span class=\"tag acc\">" + id + "</span>").join("") + "<h3>" + esc(p.title || c.paperId) + "</h3><p>" + esc((c.plain && c.plain.core) || idea(p)) + "</p><p class=\"meta\"><b>Why.</b> " + esc((c.plain && c.plain.why) || p.whyItMatters || "") + "</p><p class=\"meta\"><b>Limitation.</b> " + esc((c.plain && c.plain.limit) || p.limitation || "") + "</p><p class=\"meta\"><b>Disputer.</b> " + esc(c.disputer || "") + "</p><p class=\"mono\" style=\"font-size:0.75rem;color:var(--subtle)\">" + esc(c.claimDelta || c.score || "") + " · Auto-Gate " + (g.pass ? "pass" : "miss " + g.misses.join(",")) + "</p><div style=\"display:flex;gap:0.5rem;margin-top:0.75rem\"><button class=\"chip\" data-open=\"" + c.paperId + "\">Open paper</button><button class=\"btn " + (c.action === "REJECT" ? "danger" : g.pass ? "ok" : "warn") + "\" data-apply=\"" + c.id + "\" " + (applied(c.id) ? "disabled" : "") + ">" + (applied(c.id) ? "Applied" : "Apply " + c.action) + "</button></div></article>";
  }).join("");
}
function renderVersions() {
  const lines = (VERS.lines || []).map((l) => "<article class=\"card\"><div class=\"kicker\">" + esc(l.id) + "</div><h3>" + esc(l.name) + "</h3><p class=\"kicker\">" + esc(l.id === "DBE" ? FREEZE.dbe : FREEZE.dbes) + "</p><p>" + esc(l.meaning) + "</p><p class=\"meta\">" + esc(l.freeze) + "</p></article>").join("");
  const hist = (VERS.history || []).slice().reverse().map((v) => "<article class=\"card\"><span class=\"tag acc\">" + esc(v.kind) + "</span> <span class=\"tag\">" + esc(v.action) + "</span><h3>" + esc(v.version) + " · " + esc(v.title) + "</h3><p class=\"meta\">" + esc(v.date) + "</p><p>" + esc(v.summary) + "</p></article>").join("");
  return "<div class=\"grid\">" + lines + "</div><h2>Version log</h2>" + hist;
}
function renderLedger() {
  const defs = (LEDGER.definitions || []).map((d) => "<article class=\"card\"><div class=\"kicker\">" + esc(d.id) + "</div><h3>" + esc(d.name) + "</h3><p class=\"meta\">" + esc(d.meaning) + "</p><p>" + esc(d.current) + "</p></article>").join("");
  const terms = (LEDGER.terms || []).map((t) => "<article class=\"card\"><b>" + esc(t.id) + "</b> " + esc(t.name) + "<p class=\"meta\">" + esc(t.note) + "</p></article>").join("");
  return "<p class=\"lede\">" + esc(LEDGER.northStar || "") + "</p><div class=\"grid3\">" + defs + "</div><h2>Required terms</h2>" + terms;
}
function renderFeeds() {
  const feeds = (CAT.feeds || []).map((f) => "<article class=\"card\"><h3>" + esc(f.label) + "</h3><p class=\"meta\">" + esc(f.id) + "</p><a href=\"" + esc(f.url) + "\" target=\"_blank\" rel=\"noreferrer\">" + esc(String(f.url).replace("https://", "")) + "</a></article>").join("");
  const fields = (CAT.fields || []).map((f) => "<article class=\"card\"><div class=\"kicker\">" + esc(f.id) + "</div><h3>" + esc(f.label) + "</h3><p>" + esc(f.goal || "") + "</p><p class=\"meta\">" + esc(f.feed || "") + "</p></article>").join("");
  const runs = (CAT.runs || []).map((r) => "<article class=\"card\"><span class=\"tag acc\">" + esc(r.kind) + "</span> <span class=\"meta\">" + esc(r.startedAt || "") + "</span><p>" + esc(r.notes || "") + "</p><p class=\"meta\">" + (r.paperIds || []).length + " papers · " + esc(r.windowStart || "") + " → " + esc(r.windowEnd || "") + "</p></article>").join("");
  return "<h2>Live feeds</h2><div class=\"grid\">" + feeds + "</div><h2>Field goals</h2><div class=\"grid\">" + fields + "</div><h2>Ingest runs</h2>" + runs;
}
function renderPillars() {
  const on = (CAT.pillars || []).filter((p) => ["KEEP", "WATCH", "HOLD", "CUT"].includes(p.engineStatus));
  const queued = (CAT.pillars || []).filter((p) => !on.includes(p));
  const block = (list) => "<div class=\"grid\">" + list.map((p) => "<article class=\"card\"><div style=\"display:flex;justify-content:space-between;gap:0.75rem\"><h3>" + esc(p.name) + "</h3><span class=\"tag " + statusClass(p.engineStatus || p.status) + "\">" + esc(p.engineStatus || p.status) + "</span></div><p>" + esc(p.statement || "") + "</p><p class=\"meta\">" + esc(p.engineNote || p.dbeGoal || "") + "</p><div>" + (p.evidence || []).map((id) => "<button class=\"chip\" data-open=\"" + id + "\">" + id + "</button>").join("") + "</div></article>").join("") + "</div>";
  return "<h2>Engine</h2>" + block(on) + "<h2>Queued / suggested</h2>" + block(queued);
}
function render() {
  const main = document.getElementById("main");
  const tools = document.getElementById("tools");
  const hideTools = ["claims", "versions", "reviews", "ledger", "pillars", "feeds", "engine"].includes(tab);
  tools.style.display = hideTools ? "none" : "block";
  if (tab === "engine") main.innerHTML = renderEngine();
  else if (tab === "claims") main.innerHTML = renderClaims();
  else if (tab === "reviews") main.innerHTML = renderReviews();
  else if (tab === "versions") main.innerHTML = renderVersions();
  else if (tab === "ledger") main.innerHTML = renderLedger();
  else if (tab === "pillars") main.innerHTML = renderPillars();
  else if (tab === "feeds") main.innerHTML = renderFeeds();
  else {
    const papers = pool();
    main.innerHTML = papers.length ? "<div class=\"list\">" + papers.map(paperRow).join("") + "</div>" : "<p class=\"empty\">No papers in this slice.</p>";
  }
  main.querySelectorAll("[data-id], [data-open]").forEach((btn) => btn.addEventListener("click", () => openPaper(btn.dataset.id || btn.dataset.open)));
  main.querySelectorAll("[data-apply]").forEach((btn) => btn.addEventListener("click", () => applyCard(btn.dataset.apply)));
}
function setup() {
  paintFreeze();
  document.getElementById("tabs").innerHTML = TABS.map(([id, label]) => "<button data-tab=\"" + id + "\" class=\"" + (id === tab ? "active" : "") + "\">" + label + "</button>").join("");
  const counts = {};
  CAT.papers.forEach((p) => (p.fields || []).forEach((f) => counts[f] = (counts[f] || 0) + 1));
  document.getElementById("tools").innerHTML = "<div class=\"tools\"><input id=\"q\" placeholder=\"Search title, claim, idea…\"/><select id=\"sort\"><option value=\"importance\">Sort: importance</option><option value=\"confidence\">Sort: confidence</option><option value=\"popularity\">Sort: popularity</option><option value=\"date\">Sort: date</option></select></div><div class=\"chips\" id=\"chips\"></div><p class=\"meta\" id=\"goal\" hidden></p>";
  document.getElementById("chips").innerHTML = "<button class=\"chip " + (field === "all" ? "active" : "") + "\" data-field=\"all\">All fields<span>" + CAT.papers.length + "</span></button>" + CAT.fields.map((f) => "<button class=\"chip " + (field === f.id ? "active" : "") + "\" data-field=\"" + f.id + "\">" + f.short + "<span>" + (counts[f.id] || 0) + "</span></button>").join("");
  document.getElementById("tabs").onclick = (e) => {
    const b = e.target.closest("[data-tab]");
    if (!b) return;
    tab = b.dataset.tab;
    window.scrollTo(0, 0);
    [...document.getElementById("tabs").children].forEach((x) => x.classList.toggle("active", x === b));
    render();
  };
  document.getElementById("chips").onclick = (e) => {
    const b = e.target.closest("[data-field]");
    if (!b) return;
    field = b.dataset.field;
    [...document.getElementById("chips").children].forEach((x) => x.classList.toggle("active", x === b));
    const meta = CAT.fields.find((f) => f.id === field);
    const g = document.getElementById("goal");
    if (meta && meta.goal) { g.hidden = false; g.innerHTML = "<b>" + meta.label + ".</b> " + meta.goal; }
    else g.hidden = true;
    render();
  };
  document.getElementById("q").oninput = (e) => { q = e.target.value; render(); };
  document.getElementById("sort").onchange = (e) => { sort = e.target.value; render(); };
  render();
}
Promise.all([
  fetch("catalog.json").then((r) => r.json()),
  fetch("claims.json").then((r) => r.json()).catch(() => ({ claims: [] })),
  fetch("versions.json").then((r) => r.json()).catch(() => ({ history: [] })),
  fetch("reviews.json").then((r) => r.json()).catch(() => ({ cards: [] })),
  fetch("ledger.json").then((r) => r.json()).catch(() => ({})),
]).then(([cat, claims, versions, reviews, ledger]) => {
  CAT = cat; CLAIMS = claims; VERS = versions; REVIEWS = reviews; LEDGER = ledger;
  FREEZE = loadFreeze();
  setup();
}).catch(() => {
  document.getElementById("main").innerHTML = "<p class='empty'>Serve this folder so catalog.json can load.</p>";
});
