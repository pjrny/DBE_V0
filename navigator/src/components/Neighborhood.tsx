import { claimById, claimsByConcept, runtime } from "../data";
import type { Concept } from "../types";

export function Neighborhood({ concept }: { concept: Concept }) {
  const claims = claimsByConcept.get(concept.id) ?? [];
  const links = runtime.relationships.filter((rel) => rel.target_id === concept.id && claimById.has(rel.source_id));
  if (!links.length) {
    return <div className="graph-empty"><strong>No reviewed relationships yet</strong><p>Topic similarity and shared tags are deliberately not drawn as dependencies.</p></div>;
  }
  return <div className="neighborhood">
    <svg role="img" aria-labelledby="graph-title graph-desc" viewBox="0 0 620 230">
      <title id="graph-title">Reviewed relationships for {concept.id}</title>
      <desc id="graph-desc">Reviewed claim cases connect to the selected concept using typed evidence relations.</desc>
      {links.map((link, index) => {
        const y = 58 + index * 100;
        return <g key={link.id}>
          <path d={`M170 ${y} H290`} className="graph-edge" />
          <rect x="194" y={y - 16} width="112" height="31" rx="3" className="edge-label" />
          <text x="250" y={y - 2} textAnchor="middle" className="edge-label-text">{link.relation_type.replaceAll("_", " ")}</text>
          <circle cx="120" cy={y} r="34" className="node claim-node" />
          <text x="120" y={y - 3} textAnchor="middle" className="node-id">{link.source_id}</text>
          <text x="120" y={y + 14} textAnchor="middle" className="node-kind">claim</text>
        </g>;
      })}
      <circle cx="430" cy="108" r="42" className="node concept-node" />
      <text x="430" y="104" textAnchor="middle" className="node-id">{concept.id}</text>
      <text x="430" y="121" textAnchor="middle" className="node-kind">concept</text>
      {links.map((link, index) => <path key={`${link.id}-tail`} d={`M306 ${58 + index * 100} C350 ${58 + index * 100}, 350 108, 386 108`} className="graph-edge" />)}
    </svg>
    <ul className="relationship-list">
      {claims.map((claim) => <li key={claim.id}><strong>{claim.title}</strong><span>{claim.application_relation.replaceAll("_", " ")} · {claim.assessment_result}</span></li>)}
    </ul>
  </div>;
}
