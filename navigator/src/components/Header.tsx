import { Icon } from "../icons";

type Props = { query: string; onQuery: (value: string) => void; onExport: () => void };

export function Header({ query, onQuery, onExport }: Props) {
  return <header className="app-header">
    <div className="brand"><strong>SDBES</strong><span>Research Navigator</span></div>
    <label className="global-search">
      <span className="sr-only">Search concepts, claims, or sources</span>
      <Icon name="search" />
      <input value={query} onChange={(event) => onQuery(event.target.value)} placeholder="Search concepts, claims, or sources…" />
    </label>
    <button className="button secondary" onClick={onExport}><Icon name="download" />Export session</button>
    <div className="read-only">Read-only<br/><span>V5/V6 R2</span></div>
  </header>;
}
