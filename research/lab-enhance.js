/* Observatory UX pass. Harvest gauges still cannot raise C. */
(function () {
  const TAB_IDS = new Set(["week","month","lookback","catalog","engine","claims","reviews","versions","ledger","pillars","feeds"]);

  function tabCounts() {
    const papers = (window.CAT && CAT.papers) || [];
    const n = (fn) => papers.filter(fn).length;
    return {
      week: n(typeof inWeek === "function" ? inWeek : () => false),
      month: n(typeof inMonth === "function" ? inMonth : () => false),
      lookback: n(typeof inLookback === "function" ? inLookback : () => false),
      catalog: papers.length,
    };
  }

  function paintTabCounts() {
    const counts = tabCounts();
    document.querySelectorAll("#tabs [data-tab]").forEach((b) => {
      const id = b.dataset.tab;
      const base = (b.dataset.baseLabel || b.textContent || "").replace(/\s+\d+$/, "");
      b.dataset.baseLabel = base;
      if (counts[id] != null) b.textContent = base + " " + counts[id];
    });
  }

  function go(id) {
    if (!TAB_IDS.has(id)) return;
    window.tab = id;
    if (location.hash !== "#" + id) history.replaceState(null, "", "#" + id);
    document.querySelectorAll("#tabs [data-tab]").forEach((x) => x.classList.toggle("active", x.dataset.tab === id));
    if (typeof render === "function") render();
    paintTabCounts();
    paintFreezeNotes();
  }

  function paintFreezeNotes() {
    const bar = document.getElementById("freezeBar");
    if (!bar || bar.querySelector("[data-freeze-notes]")) return;
    const wrap = document.createElement("span");
    wrap.setAttribute("data-freeze-notes", "1");
    wrap.innerHTML = ' <a href="papers/DBE-0.2.1.md">DBE-0.2.1 note</a> · <a href="papers/DBES-0.2.0.md">DBES-0.2.0 note</a> · <a href="#engine">Engine</a>';
    bar.appendChild(wrap);
  }

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") document.querySelectorAll(".overlay").forEach((n) => n.remove());
  });

  window.addEventListener("hashchange", () => {
    const id = location.hash.replace("#", "");
    if (TAB_IDS.has(id)) go(id);
  });

  const boot = setInterval(() => {
    if (!document.getElementById("tabs") || !window.CAT || !CAT.papers) return;
    clearInterval(boot);
    const start = location.hash.replace("#", "");
    paintTabCounts();
    paintFreezeNotes();
    if (TAB_IDS.has(start)) go(start);
    document.getElementById("tabs").addEventListener("click", (e) => {
      const b = e.target.closest("[data-tab]");
      if (b) {
        e.stopPropagation();
        go(b.dataset.tab);
      }
    }, true);
  }, 50);
})();
