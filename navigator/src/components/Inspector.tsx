import { useState, type ReactNode } from "react";
import { claimsByConcept, runtime, sourceById } from "../data";
import { Icon } from "../icons";
import type { Concept } from "../types";
import type { DetailTab } from "../useNavigatorState";
import { Neighborhood } from "./Neighborhood";
import { Queue } from "./Queue";

type Props = { concept: Concept; tab: DetailTab; onTab: (tab: DetailTab) => void };

export function Inspector({ concept, tab, onTab }: Props) {
  const [queueExpanded, setQueueExpanded] = useState(true);
  const claims = claimsByConcept.get(concept.id) ?? [];
  const sources = concept.source_refs.map((id) => sourceById.get(id)).filter(Boolean);
  return <aside className="inspector" aria-labelledby="inspector-title">
    <div className="inspector-heading">
      <div><span className="record-id">{concept.id}</span><h2 id="inspector-title">{concept.title}</h2></div>
      <span className="read-only-label">Read-only</span>
    </div>
    <div className="state-line"><span className="status staged">{concept.display_status}</span>{claims.length > 0 && <span className="status reviewed">{claims.length} reviewed claim link{claims.length > 1 ? "s" : ""}</span>}</div>
    <div className="source-warning"><Icon name="warning"/><div><strong>Source verification incomplete</strong><span>Anchors are catalogued, but no primary-result verification receipt is attached.</span></div></div>
    <div className="mobile-tabs" role="tablist" aria-label="Inspector sections">
      {(["evidence", "relations", "queue"] as DetailTab[]).map((value) => <button key={value} role="tab" aria-selected={tab === value} onClick={() => onTab(value)}>{value[0].toUpperCase() + value.slice(1)}</button>)}
    </div>

    <div className={tab === "evidence" ? "tab-active" : "tab-mobile-hidden"}>
      <Section title="Exact assertion" icon="source"><p>{concept.bounded_question}</p></Section>
      <Section title="Bounded scope" icon="info"><p><strong>Domain:</strong> {concept.domain}</p><p><strong>Role:</strong> {concept.role}</p><p><strong>Resource boundary:</strong> {concept.resource_ledger}</p></Section>
      <div className="evidence-grid">
        <Section title="What supports it?" icon="source"><p>{concept.mechanism_status}</p><p className="caveat">Phase-1 summary only; this is not an SDBES verification.</p></Section>
        <Section title="What challenges it?" icon="warning"><p>{concept.main_gap}</p></Section>
        <Section title="What remains unresolved?" icon="info"><p>{concept.main_gap}</p></Section>
        <Section title="What would change this assessment?" icon="network"><p>{concept.next_investigation}</p></Section>
      </div>
      {claims.length > 0 && <Section title="Reviewed claim cases" icon="network">
        {claims.map((claim) => <article className="claim-case" key={claim.id}><strong>{claim.id} · {claim.title}</strong><p>{claim.direct_claim}</p><dl><dt>Application relation</dt><dd>{claim.application_relation.replaceAll("_", " ")}</dd><dt>Result</dt><dd>{claim.assessment_result}</dd><dt>Boundary</dt><dd>{claim.v4_contract}</dd></dl></article>)}
      </Section>}
      <Section title="Source locator" icon="source">
        <p className="caveat">Inventory anchors only. Exact passages, figures, tables, equations, or code locations are not yet recorded.</p>
        <ul className="sources">{sources.map((source) => source && <li key={source.id}><span>{source.id}</span>{source.url ? <a href={source.url} target="_blank" rel="noreferrer">{source.title}</a> : <span>{source.title}</span>}</li>)}</ul>
      </Section>
      <Section title="Model scenarios" icon="network"><div className="disabled-model"><strong>{runtime.scenario_message}</strong><span>V4 outputs appear only after explicit model-use authorization and scope checks.</span></div></Section>
    </div>

    <div className={tab === "relations" ? "tab-active" : "tab-mobile-hidden"}>
      <Section title="Reviewed relationships (neighborhood)" icon="network"><Neighborhood concept={concept}/></Section>
    </div>
    <div className={tab === "queue" ? "tab-active" : "tab-mobile-hidden"}>
      <Queue conceptId={concept.id} expanded={queueExpanded} onToggle={() => setQueueExpanded((value) => !value)}/>
    </div>
  </aside>;
}

function Section({ title, icon, children }: { title: string; icon: "source" | "warning" | "info" | "network"; children: ReactNode }) {
  return <section className="inspector-section"><h3><Icon name={icon}/>{title}</h3><div>{children}</div></section>;
}
