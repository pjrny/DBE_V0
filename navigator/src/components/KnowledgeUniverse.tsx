import { useMemo, useState, type KeyboardEvent } from "react";
import { inventory, runtime, v7Report } from "../data";
import type { Concept } from "../types";
import {
  catalogBridgeCandidates, DOMAIN_PALETTE, knowledgeGeometry, knowledgeTimeline,
  LENSES, methodCoverage, reviewedRelations, type KnowledgeLens,
} from "../knowledgeUniverse";
import "../v8.css";

type Props = {
  concepts: Concept[];
  selected: Concept;
  onSelect: (id: string) => void;
  onOpenFilters: () => void;
  filterCount: number;
};
const DOMAIN_TITLES: Record<string, string> = {
  A: "Nuclear & fusion", B: "Planetary energy", C: "Materials & conversion",
  D: "Intelligence & discovery", E: "Fundamental physics", F: "Demand & civilization",
};
const VIG = ["Validated", "Independently checked", "Generalized"] as const;

export function KnowledgeUniverse({ concepts, selected, onSelect, onOpenFilters, filterCount }: Props) {
  const [lens, setLensState] = useState<KnowledgeLens>(() => {
    const lensParam = new URLSearchParams(window.location.search).get("lens");
    return LENSES.some(l => l.id === lensParam) ? lensParam as KnowledgeLens : "universe";
  });
  const [focused, setFocused] = useState<string | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  const [showTaxonomyEdges, setTaxonomyEdges] = useState(false);
  const positions = useMemo(() => knowledgeGeometry(inventory.concepts), []);
  const conceptById = useMemo(() => new Map(inventory.concepts.map(c => [c.id, c])), []);
  const visibleIds = new Set(concepts.map(c => c.id));
  const reviewed = reviewedRelations(selected.id, runtime.relationships, runtime.reviewed_claims);
  const reviewedCases = runtime.reviewed_claims.filter(claim => reviewed.some(edge => edge.source_id === claim.id));
  const methodRows = methodCoverage(selected.id, runtime.reviewed_claims);
  const candidates = useMemo(() => catalogBridgeCandidates(inventory.concepts), []);
  const timeline = knowledgeTimeline(inventory.snapshot_date ?? "2026-10-09", runtime.snapshot_date ?? "2026-10-09", "2026-10-08");
  const v7Models = runtime.authorized_models.length;
  const setLens = (next: KnowledgeLens) => {
    setLensState(next);
    const params = new URLSearchParams(window.location.search);
    if (next === "universe") params.delete("lens"); else params.set("lens", next);
    const query = params.toString();
    window.history.replaceState(null, "", `${window.location.pathname}${query ? `?${query}` : ""}`);
  };
  const selectDomain = (code: string) => {
    setFocused(focused === code ? null : code);
    const target = concepts.find(c => c.domain_code === code) ?? inventory.concepts.find(c => c.domain_code === code);
    if (target) onSelect(target.id);
  };
  const keyboardActivate = (e: KeyboardEvent<SVGGElement>, fn: () => void) => {
    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fn(); }
  };

  return <section className="v8-universe" aria-label="Multidimensional knowledge universe">
    <div className="v8-heading">
      <div>
        <div className="v8-eyebrow">SDBES / V8 · GLOBAL SCIENCE LANDSCAPE</div>
        <h1>Dimensions Beyond Energy Scarcity</h1>
        <p>Explore scientific fields, claims, evidence and possible bridges—without confusing a research map with physical truth.</p>
      </div>
      <button className="button v8-mobile-filters" onClick={onOpenFilters}>Filters{filterCount ? ` (${filterCount})` : ""}</button>
    </div>
    <nav aria-label="Knowledge visualization lenses" className="v8-lenses">
      {LENSES.map(l => <button key={l.id} aria-current={lens === l.id ? "page" : undefined}
        className={lens === l.id ? "active" : ""} onClick={() => setLens(l.id)} title={l.description}>{l.label}</button>)}
    </nav>
    <div className="v8-lens-body">
      {lens === "universe" && <>
        <div className="v8-subheading"><div><strong>Cross-domain universe</strong><span>2D taxonomy projection · not a physical or semantic distance scale</span></div>
          <div className="v8-toolbar"><label><input type="checkbox" checked={showTaxonomyEdges} onChange={(e: {target:{checked:boolean}}) => setTaxonomyEdges(e.target.checked)}/>Show taxonomy membership</label>
            <button onClick={() => setFocused(null)} disabled={!focused}>Show all domains</button></div>
        </div>
        {concepts.length <= 8 && concepts.length < inventory.concepts.length && <div className="v8-visible-results" aria-label="Matching research concepts">
          {concepts.map(c => <button key={c.id} onClick={() => onSelect(c.id)}><b>Record {c.id}</b><span>{c.title}</span></button>)}
          {!concepts.length && <span>No candidates match these filters.</span>}
        </div>}
        <div className="v8-map-wrap">
          <svg className="v8-map" role="group" aria-label="Interactive 2D map of six energy-scarcity research domains and their concept candidates"
            viewBox={(() => { const d = positions.domains.find(d => d.id === focused); return d ? `${d.x - 175} ${d.y - 170} 350 340` : "0 0 1200 760"; })()}>
            <defs><pattern id="v8grid" patternUnits="userSpaceOnUse" width="36" height="36"><path d="M36 0H0V36" fill="none" stroke="#dde6ec" strokeWidth=".75"/></pattern></defs>
            <rect x="0" y="0" width="1200" height="760" fill="url(#v8grid)"/>
            {positions.domains.map(domain => <g key={`field-${domain.id}`}>
              <circle cx={domain.x} cy={domain.y} r="114" fill={DOMAIN_PALETTE[domain.id]} opacity=".055" stroke={DOMAIN_PALETTE[domain.id]} strokeDasharray="4 6" strokeWidth="1.4"/>
              {showTaxonomyEdges && positions.concepts.filter(p=>p.domain===domain.id && visibleIds.has(p.id)).map(p=><line key={`tax-${p.id}`} x1={domain.x} y1={domain.y} x2={p.x} y2={p.y} stroke={DOMAIN_PALETTE[domain.id]} strokeOpacity=".18" strokeWidth=".8"/>)}
            </g>)}
            {positions.concepts.map(point => {
              const c=conceptById.get(point.id); if (!c) return null;
              const active=visibleIds.has(point.id), chosen=point.id === selected.id;
              return <g key={point.id} role="button" tabIndex={0} aria-label={`${point.id}: ${c.title}; ${c.display_status}`}
                onClick={()=>onSelect(point.id)} onKeyDown={(e:KeyboardEvent<SVGGElement>)=>keyboardActivate(e,()=>onSelect(point.id))}
                onMouseEnter={()=>setHovered(point.id)} onMouseLeave={()=>setHovered(null)}
                className={`v8-point ${chosen?"selected":""} ${!active?"dimmed":""}`}>
                <circle cx={point.x} cy={point.y} r={chosen?11:5.6} fill={DOMAIN_PALETTE[point.domain]}
                  fillOpacity={active?1:.18} stroke={chosen?"#132c46":"#fff"} strokeWidth={chosen?3:1.2}/>
                {chosen && <circle cx={point.x} cy={point.y} r="17" fill="none" stroke="#163753" strokeWidth="1.8" strokeDasharray="4 3"/>}
                <title>{`${c.id} · ${c.title} · ${c.display_status}`}</title>
              </g>;
            })}
            {positions.domains.map(domain=><g role="button" tabIndex={0} key={domain.id} className="v8-domain-node"
              onClick={()=>selectDomain(domain.id)} onKeyDown={(e:KeyboardEvent<SVGGElement>)=>keyboardActivate(e,()=>selectDomain(domain.id))}
              aria-label={`Focus ${DOMAIN_TITLES[domain.id]}, ${domain.count} original concepts`}>
              <circle cx={domain.x} cy={domain.y} r="22" fill="#fff" stroke={DOMAIN_PALETTE[domain.id]} strokeWidth="3"/>
              <text x={domain.x} y={domain.y+5} textAnchor="middle" fontSize="15" fontWeight="750" fill="#142946">{domain.id}</text>
              <title>{domain.label}</title>
            </g>)}
          </svg>
          <div className="v8-map-key"><strong>{hovered ? `${hovered} · ${conceptById.get(hovered)?.title}` : `${selected.id} · ${selected.title}`}</strong><span>Circles: discovery concepts · Rings: research domains · Lines: taxonomy only</span></div>
        </div>
        <div className="v8-domain-strip" aria-label="Research domains">
          {positions.domains.map(domain=><button key={domain.id} onClick={()=>selectDomain(domain.id)} aria-pressed={focused===domain.id}>
            <span className="v8-domain-dot" style={{background:DOMAIN_PALETTE[domain.id]}}/>
            <span><strong>{domain.id} · {DOMAIN_TITLES[domain.id]}</strong><small>{domain.count} candidates · {concepts.filter(c=>c.domain_code===domain.id).length} visible</small></span>
          </button>)}
        </div>
        <details className="v8-concept-browser"><summary>Browse {DOMAIN_TITLES[focused ?? selected.domain_code]} concepts in a keyboard/touch list</summary>
          <div>{inventory.concepts.filter(c => c.domain_code === (focused ?? selected.domain_code)).map(c => <button key={c.id} onClick={() => onSelect(c.id)} aria-current={selected.id === c.id ? "true" : undefined}><b>Record {c.id}</b><span>{c.title}</span></button>)}</div>
        </details>
        <div className="v8-guard">The six circles are taxonomic groups, not discovered physical dimensions. Node positions and distances encode no evidence strength, probability, feasibility or causal effect. Selecting a point opens its original evidence inspector.</div>
      </>}
      {lens === "evidence" && <>
        <LensIntro title="Formal · Empirical · Applied" subtitle="V1's 3×3 profile, with V3's structured meaning restored"/>
        <div className="v8-evidence-key">Selected: <strong>{selected.id}</strong> · {reviewedCases.length} related reviewed claim case(s). The current staging export does not contain canonical V/I/G assessment cells for this concept.</div>
        <div className="v8-matrix" role="table" aria-label="Formal Empirical Applied evidence assessment matrix">
          <div className="v8-cell v8-corner" role="columnheader">Method ↓ / Criterion →</div>
          {VIG.map(s=><div key={s} className="v8-cell v8-header" role="columnheader">{s}</div>)}
          {methodRows.map(row=><FragmentRow key={row.id} row={row}/>)}
        </div>
        <div className="v8-methods">
          <h3>Related claim-case method tags</h3>
          {methodRows.map(r=><div key={r.id}><strong>{r.id} · {r.label}</strong><span>{r.caseIds.length ? `${r.caseIds.join(", ")} · source labels: ${r.methods.join(", ")}` : "No matching reviewed-case method tag"}</span></div>)}
          <p>Method tags are imported descriptions. They do not establish validated, independently replicated or generalized results. Unknown is not zero, failure, or inapplicability.</p>
        </div>
      </>}
      {lens === "dependencies" && <>
        <LensIntro title="Typed dependencies & bottlenecks" subtitle="V3 distinguishes epistemic evidence, structural gates and physical causal effects"/>
        <div className="v8-dep-map" aria-label="Reviewed evidence relationship neighborhood">
          <div className="v8-dep-center"><small>Concept candidate</small><strong>{selected.id}</strong><span>{selected.title}</span></div>
          {reviewed.length ? reviewed.map(rel=><div key={rel.id} className="v8-dep-link"><span className="v8-dep-connector">↗ {rel.relation_type.replaceAll("_"," ")}</span><div><strong>{rel.source_id}</strong><span>Reviewed case · {rel.review_status}</span></div></div>) : <div className="v8-empty">No reviewed evidence relations recorded for this concept. Lack of recorded relations is not a claim that none exist.</div>}
        </div>
        <div className="v8-methods"><h3>Structural requirement layer</h3><p>No selected-concept V3 Structural Predicate and Gate assessment is registered in the current read-only projection. A paper-to-concept association is never promoted to a prerequisite or causal edge.</p></div>
        <div className="v8-gate-legend"><span><b>ALL</b> All required</span><span><b>ANY</b> Alternative routes</span><span><b>k-of-n</b> Explicit threshold</span><span><b>NEITHER / TRUE_ONLY / FALSE_ONLY / BOTH</b> Knowledge status</span></div>
      </>}
      {lens === "dynamics" && <>
        <LensIntro title="Physical dynamics versus research knowledge" subtitle="V4 supports bounded causal interventions only with a registered model and a use-specific receipt"/>
        <div className="v8-dynamics-flow">
          <div><small>Physical state</small><strong>x(k)</strong><span>Measured/modelled system</span></div><span className="v8-flow-arrow">→</span>
          <div><small>Domain model</small><strong>F(x,u,z;θ,m)</strong><span>Inputs, disturbances, parameters</span></div><span className="v8-flow-arrow">→</span>
          <div><small>Next state</small><strong>x(k+1)</strong><span>Only in a bounded model</span></div>
        </div>
        <div className="v8-knowledge-flow"><strong>K(t): scientific knowledge and revisions</strong><p>New sources, claim assessments, and corrections change the research ledger—not automatically the physical x(t) state.</p></div>
        <div className="v8-model-state"><strong>{v7Models === 0 ? "No authorized scientific model package registered" : `${v7Models} model receipt(s) registered; inspect use and scope before execution`}</strong>
          <p>{runtime.scenario_message}. No example trajectory, sensitivity, intervention benefit or probability is fabricated.</p>
          <button disabled type="button">Run scenario · requires scoped model authorization</button>
        </div>
      </>}
      {lens === "timeline" && <>
        <LensIntro title="Time, provenance & revision" subtitle="A timeline of what the project recorded, not a graph of how physical laws changed"/>
        <ol className="v8-timeline">{timeline.map(event=><li key={event.key}><time>{event.date}</time><div><strong>{event.label}</strong><p>{event.detail}</p></div></li>)}</ol>
        <div className="v8-methods"><h3>What this timeline does not show</h3><p>Source addition, paper count, and reviewer activity must not be interpreted as a technology maturity curve, confidence gain, or actual physical-world intervention. Full claim-level historical diffs remain a later integration.</p></div>
      </>}
      {lens === "exploration" && <>
        <LensIntro title="Cross-field exploration" subtitle="Catalog co-occurrence suggestions, not approved scientific bridges or prioritized truths"/>
        <div className="v8-guard">Experimental exploration only: shared tags may indicate terminology, not a functional connection. These candidates do not enter the dependency graph or change scientific assessments.</div>
        <div className="v8-candidate-list">{candidates.length ? candidates.map(pair=><button key={`${pair.a}-${pair.b}`} onClick={()=>onSelect(pair.a)}>
          <strong>{pair.a} ↔ {pair.b}</strong><span>{pair.sharedTags.join(", ")}</span><small>Unreviewed catalog-tag overlap</small>
        </button>) : <p>No catalog-tag overlaps found across the six domains.</p>}</div>
        <div className="v8-methods"><h3>Selected concept · next question</h3><p>{selected.next_investigation}</p><p>Suggested investigations are exploratory. V9 may turn reviewed, bounded questions into research campaigns after explicit decisions.</p></div>
      </>}
    </div>
    <footer className="v8-footer"><span>V8 · Read-only visualization</span><span>{concepts.length} visible / {inventory.concepts.length} original candidates · {runtime.relationships.filter(r=>r.review_status==="REVIEWED").length} reviewed case links · {v7Report.counts.catalog_papers} Observatory papers separate</span></footer>
  </section>;
}

function LensIntro({title,subtitle}:{title:string;subtitle:string}) {
  return <div className="v8-subheading"><div><strong>{title}</strong><span>{subtitle}</span></div></div>;
}
function FragmentRow({row}:{row:{id:string;label:string;caseIds:string[]};key?:string}) {
  return <>
    <div className="v8-cell v8-row-label" role="rowheader"><b>{row.id}</b><span>{row.label}</span><small>{row.caseIds.length} method-tagged case(s)</small></div>
    {VIG.map(col=><div key={`${row.id}-${col}`} className="v8-cell v8-unknown" role="cell"><strong>UNKNOWN</strong><small>not yet imported</small></div>)}
  </>;
}
