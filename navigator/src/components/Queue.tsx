import { runtime } from "../data";
import { Icon } from "../icons";

export function Queue({ conceptId, expanded, onToggle }: { conceptId?: string; expanded: boolean; onToggle: () => void }) {
  const items = conceptId ? runtime.research_queue.filter((item) => item.concept_id === conceptId) : runtime.research_queue.slice(0, 10);
  return <section className={`queue ${expanded ? "expanded" : ""}`} aria-labelledby="queue-title">
    <button className="queue-bar" onClick={onToggle} aria-expanded={expanded}>
      <span><Icon name="queue"/><strong id="queue-title">Research queue</strong><small>{conceptId ? `for ${conceptId}` : `${runtime.research_queue.length} proposed investigations`}</small></span>
      <span className="queue-disclosure">{expanded ? "Collapse" : "Expand"}</span>
    </button>
    {expanded && <div className="queue-body">
      <div className="queue-explainer"><strong>Investigations, not fields.</strong><span>No universal score is computed. Missing cost, benefit, or uncertainty stays missing.</span></div>
      {items.map((item) => <article className="queue-row" key={item.id}>
        <div><span className="queue-id">{item.id}</span><strong>{item.title}</strong></div>
        <div><span>Mode</span>{item.activity_mode}</div>
        <div><span>Comparison</span>{item.comparison_state.replaceAll("_", " ")}</div>
        <div><span>Attempts</span>{item.attempts.length} recorded</div>
      </article>)}
    </div>}
  </section>;
}
