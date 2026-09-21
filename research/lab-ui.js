(function () {
  window.paperRow = function (p) {
    return `<button class="row" data-id="${esc(p.id)}" type="button">
      <div>
        <div>${isFound(p) ? `<span class="tag acc">Foundational</span>` : `<span class="tag">${esc(roleLabel(p))}</span>`}
          ${claimIds(p).map(id => `<span class="tag acc">${esc(id)}</span>`).join("")}
          ${p.suggestedPillar ? `<span class="tag warn">new pillar?</span>` : ""}
          <span class="meta">${esc(pdate(p))}</span></div>
        <h3>${esc(p.title)}</h3>
        <p class="meta">${esc(authors(p).slice(0, 4).join(", "))} · ${esc(p.venue || "")}</p>
        <p class="plain"><b>Idea.</b> ${esc(idea(p))}</p>
        <p class="plain"><b>Why.</b> ${esc(why(p))}</p>
        <p class="plain"><b>Limit.</b> ${esc(lim(p))}</p>
      </div>${harvestMeters(p)}
    </button>`;
  };
  window.paintEngine = function () {
    const el = document.getElementById("engine");
    if (!el) return;
    const keep = (CLAIMS.claims || []).filter(c => c.status === "KEEP");
    const cut = (CLAIMS.claims || []).filter(c => c.status === "CUT");
    el.innerHTML = `
      <article class="card">
        <p class="kicker">Published freeze</p>
        <h3 class="mono">${esc(dbeVer())} / ${esc(dbesVer())}</h3>
        <p class="meta">KEEP ${keep.map(c => c.id).join(" · ") || "—"}</p>
        <p class="meta">CUT ${cut.map(c => c.id).join(" · ") || "—"} · Q=1000 is ledger stress, not output.</p>
        <div class="rowish">
          <button class="chip active" data-tabjump="claims" type="button">Open claims</button>
          <button class="chip" data-tabjump="versions" type="button">Version log</button>
          <button class="chip" data-tabjump="ledger" type="button">Q ledger</button>
        </div>
      </article>
      <article class="card">
        <p class="kicker">Protocol</p>
        <p>Harvest 0–100 never moves C. Auto-add only if Auto-Gate A1–A8 pass. CUT / low-C sections stay off the engine.</p>
        <p class="meta">WEAKEN and DISCONFIRM apply immediately. NEW PILLAR and CUT reversal never auto.</p>
      </article>`;
    el.querySelectorAll("[data-tabjump]").forEach(b => {
      b.onclick = () => { tab = b.dataset.tabjump; setupNav(); render(); };
    });
  };
  const origRender = window.render;
  window.render = function () {
    if (typeof origRender === "function") origRender();
    document.querySelectorAll("[data-apply]").forEach(b => {
      b.onclick = () => {
        const d = loadDecisions();
        d[b.dataset.apply] = "queued-for-freeze";
        saveDecisions(d);
        tab = "versions";
        setupNav();
        if (typeof origRender === "function") origRender();
        paintEngine();
      };
    });
    paintEngine();
  };
  if (document.getElementById("engine")) paintEngine();
})();
