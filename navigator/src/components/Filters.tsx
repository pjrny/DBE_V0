import { inventory } from "../data";
import { Icon } from "../icons";

type Props = {
  domain: string;
  classCode: string;
  onDomain: (value: string) => void;
  onClass: (value: string) => void;
  onClose?: () => void;
};

const classes = [
  ["D", "Demonstrated mechanism"],
  ["P", "Physics-compatible frontier"],
  ["S", "Speculative / unknown physics"],
  ["X", "Constraint conflict"],
];

export function Filters({ domain, classCode, onDomain, onClass, onClose }: Props) {
  const domains = Array.from(new Map(inventory.concepts.map((concept) => [concept.domain_code, concept.domain])));
  const domainCount = (code: string) => inventory.concepts.filter((concept) => code === "ALL" || concept.domain_code === code).length;
  const classCount = (code: string) => inventory.concepts.filter((concept) => code === "ALL" || concept.discovery_class === code).length;
  return <aside className="filters" aria-label="Concept filters">
    <div className="filters-title"><span>Filters</span>{onClose && <button className="icon-button" onClick={onClose} aria-label="Close filters"><Icon name="close" /></button>}</div>
    <fieldset>
      <legend>Research domain</legend>
      <FilterRow active={domain === "ALL"} label="All domains" count={domainCount("ALL")} onClick={() => onDomain("ALL")} />
      {domains.map(([code, name]) => <FilterRow key={code} active={domain === code} label={name} count={domainCount(code)} onClick={() => onDomain(code)} />)}
    </fieldset>
    <fieldset>
      <legend>Phase-1 discovery tag</legend>
      <p className="filter-note">Legacy intake metadata; not confidence.</p>
      <FilterRow active={classCode === "ALL"} label="All tags" count={classCount("ALL")} onClick={() => onClass("ALL")} />
      {classes.map(([code, label]) => <FilterRow key={code} active={classCode === code} label={`${code} · ${label}`} count={classCount(code)} onClick={() => onClass(code)} />)}
    </fieldset>
    <div className="integrity-note"><Icon name="info"/><span>90 discovery records. Zero are promoted to assessed concepts by this import.</span></div>
  </aside>;
}

function FilterRow({ active, label, count, onClick }: { active: boolean; label: string; count: number; onClick: () => void }) {
  return <button className={`filter-row ${active ? "active" : ""}`} aria-pressed={active} onClick={onClick}>
    <span>{label}</span><span>{count}</span>
  </button>;
}
