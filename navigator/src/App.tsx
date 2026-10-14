import { useMemo, useState } from "react";
import { claimsByConcept, inventory, runtime, sourceById } from "./data";
import { Atlas } from "./components/Atlas";
import { Filters } from "./components/Filters";
import { Header } from "./components/Header";
import { Inspector } from "./components/Inspector";
import { Queue } from "./components/Queue";
import { ScaleRun } from "./components/ScaleRun";
import { KnowledgeUniverse } from "./components/KnowledgeUniverse";
import { Icon } from "./icons";
import { useNavigatorState } from "./useNavigatorState";

export function App() {
  const state = useNavigatorState();
  const [surface, setSurface] = useState<"universe" | "records">(() =>
    new URLSearchParams(window.location.search).get("surface") === "records" ? "records" : "universe");
  const changeSurface = (next: "universe" | "records") => {
    setSurface(next);
    const params = new URLSearchParams(window.location.search);
    if (next === "universe") params.delete("surface"); else params.set("surface", "records");
    const query = params.toString();
    window.history.replaceState(null, "", `${window.location.pathname}${query ? `?${query}` : ""}`);
  };
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [queueOpen, setQueueOpen] = useState(false);
  const concepts = useMemo(() => {
    const needle = state.query.trim().toLowerCase();
    return inventory.concepts.filter((concept) => {
      const relatedClaims = (claimsByConcept.get(concept.id) ?? []).flatMap((claim) => [claim.id, claim.title, claim.direct_claim, claim.application_claim]);
      const relatedSources = concept.source_refs.flatMap((id) => {
        const source = sourceById.get(id);
        return source ? [source.id, source.title] : [];
      });
      const queryMatch = !needle || [concept.id, concept.title, concept.domain, concept.bounded_question, ...concept.tags, ...relatedClaims, ...relatedSources].join(" ").toLowerCase().includes(needle);
      return queryMatch && (state.domain === "ALL" || concept.domain_code === state.domain) && (state.classCode === "ALL" || concept.discovery_class === state.classCode);
    });
  }, [state.query, state.domain, state.classCode]);
  const selected = inventory.concepts.find((concept) => concept.id === state.selectedId) ?? concepts[0] ?? inventory.concepts[0];
  const filterCount = Number(state.domain !== "ALL") + Number(state.classCode !== "ALL");

  const exportSession = () => {
    const session = {
      exported_at: new Date().toISOString(),
      mode: runtime.mode,
      filters: { query: state.query, domain: state.domain, discovery_class: state.classCode },
      selected_record: selected.id,
      tab: state.tab,
      surface,
      lens: new URLSearchParams(window.location.search).get("lens") ?? "universe",
      atlas_snapshots: inventory.source_snapshots ?? [],
      note: "Navigation state only; this export is not a scientific assessment.",
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(session, null, 2)], { type: "application/json" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `sdbes-session-${selected.id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  return <div className="app-shell">
    <Header query={state.query} onQuery={state.setQuery} onExport={exportSession}/>
    <div className="integrity-banner"><Icon name="warning"/><strong>Staging boundary:</strong><span>{inventory.warning}</span></div>
    <ScaleRun />
    <div className="v8-switch" aria-label="Research navigation mode">
      <button aria-pressed={surface === "universe"} onClick={() => changeSurface("universe")}>Knowledge universe · V8</button>
      <button aria-pressed={surface === "records"} onClick={() => changeSurface("records")}>Evidence record table</button>
      <span className="v8-switch-note">6 domains · 90 discovery concepts · evidence first</span>
    </div>
    {(state.query || filterCount > 0) && <div className="filter-caution"><Icon name="info"/><span>Current filters may hide relevant challenging or null records. Clear filters before interpreting the evidence set.</span><button onClick={() => { state.setQuery(""); state.setDomain("ALL"); state.setClassCode("ALL"); }}>Clear filters</button></div>}
    <main className={`workspace ${surface === "universe" ? "v8-layout" : ""}`}>
      <div className={`filter-drawer ${filtersOpen ? "open" : ""}`}><Filters domain={state.domain} classCode={state.classCode} onDomain={state.setDomain} onClass={state.setClassCode} onClose={() => setFiltersOpen(false)}/></div>
      <Filters domain={state.domain} classCode={state.classCode} onDomain={state.setDomain} onClass={state.setClassCode}/>
      {surface === "universe" ?
        <KnowledgeUniverse concepts={concepts} selected={selected} onSelect={(id) => { state.setSelectedId(id); state.setTab("evidence"); }} onOpenFilters={() => setFiltersOpen(true)} filterCount={filterCount}/> :
        <Atlas concepts={concepts} selectedId={selected.id} onSelect={(id) => { state.setSelectedId(id); state.setTab("evidence"); }} onOpenFilters={() => setFiltersOpen(true)} filterCount={filterCount}/> }
      <Inspector concept={selected} tab={state.tab} onTab={state.setTab}/>
    </main>
    <div className="desktop-queue"><Queue expanded={queueOpen} onToggle={() => setQueueOpen((value) => !value)}/></div>
  </div>;
}
