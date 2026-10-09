import { v7Report } from "../data";
import { Icon } from "../icons";

export function ScaleRun() {
  const counts = v7Report.counts;
  const maxLoad = Math.max(...v7Report.program_claim_load.map((item) => item.associated_review_count), 1);
  return <details className="scale-run">
    <summary>
      <span><Icon name="info"/><strong>V7 Observatory scale run</strong></span>
      <span>{counts.catalog_papers} papers · {counts.review_cards} reviews · 0 scientific promotions</span>
    </summary>
    <div className="scale-grid">
      <div><strong>{counts.reviewed_catalog_papers}</strong><span>cataloged papers reviewed</span></div>
      <div><strong>{counts.catalog_papers_without_review_card}</strong><span>awaiting a review card</span></div>
      <div><strong>{counts.paper_claim_associations}</strong><span>declared program-claim links</span></div>
      <div><strong>{counts.high_or_critical_findings}</strong><span>quarantined high-severity defects</span></div>
    </div>
    <div className="claim-load" aria-label="Observatory review associations by program claim">
      <strong>Research flow by program claim</strong>
      <div className="claim-load-grid">{v7Report.program_claim_load.map((item) => <div className="claim-load-row" key={item.claim_id}>
        <span>{item.claim_id}</span>
        <i style={{ width: `${Math.max(2, (item.associated_review_count / maxLoad) * 100)}%` }} />
        <b>{item.associated_review_count}</b>
      </div>)}</div>
    </div>
    <p>Associations organize the Observatory program; they do not automatically strengthen claims or create causal edges. V4 scenarios become eligible when a registered scientific model package and authorization receipt exist.</p>
  </details>;
}
