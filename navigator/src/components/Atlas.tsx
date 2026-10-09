import { claimsByConcept } from "../data";
import { Icon } from "../icons";
import type { Concept } from "../types";

type Props = { concepts: Concept[]; selectedId: string; onSelect: (id: string) => void; onOpenFilters: () => void; filterCount: number };

const classLabels = { D: "Demonstrated", P: "Frontier", S: "Speculative", X: "Constraint test" };

export function Atlas({ concepts, selectedId, onSelect, onOpenFilters, filterCount }: Props) {
  return <section className="atlas" aria-labelledby="atlas-title">
    <div className="atlas-heading">
      <div><h1 id="atlas-title">Evidence Workbench</h1><p>{concepts.length} of 90 discovery records · 10 reviewed links · 13 separate program cases</p></div>
      <button className="button mobile-filter" onClick={onOpenFilters}><Icon name="filter"/>Filters{filterCount ? ` (${filterCount})` : ""}</button>
    </div>
    <div className="table-wrap">
      <table>
        <thead><tr><th>ID</th><th>Concept</th><th>Discovery tag</th><th>Review workflow</th><th>Source state</th><th><span className="sr-only">Open</span></th></tr></thead>
        <tbody>
          {concepts.map((concept) => {
            const claims = claimsByConcept.get(concept.id) ?? [];
            return <tr key={concept.id} className={selectedId === concept.id ? "selected" : ""} onClick={() => onSelect(concept.id)}>
              <td><button className="row-select" onClick={() => onSelect(concept.id)}>{concept.id}</button></td>
              <td><strong>{concept.title}</strong><span className="mobile-row-meta">{classLabels[concept.discovery_class]} · {claims.length ? `${claims.length} reviewed link${claims.length > 1 ? "s" : ""}` : "Discovery-only"}</span></td>
              <td><span className={`class-mark class-${concept.discovery_class}`}>{concept.discovery_class}</span>{classLabels[concept.discovery_class]}</td>
              <td>{claims.length ? <span className="status reviewed">Reviewed link available</span> : <span className="status staged">Staged only</span>}</td>
              <td><span className="source-state"><Icon name="source"/>{concept.source_refs.length} anchors · unverified</span></td>
              <td><Icon name="chevron"/></td>
            </tr>;
          })}
        </tbody>
      </table>
      {!concepts.length && <div className="empty"><strong>No matching records</strong><span>Clear or broaden the current filters.</span></div>}
    </div>
  </section>;
}
