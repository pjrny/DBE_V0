import { useCallback, useMemo, useState } from "react";

export type DetailTab = "evidence" | "relations" | "queue";

function readParams() {
  const params = new URLSearchParams(window.location.search);
  return {
    query: params.get("q") ?? "",
    domain: params.get("domain") ?? "ALL",
    classCode: params.get("class") ?? "ALL",
    selectedId: params.get("selected") ?? "DBE-A01",
    tab: (params.get("tab") as DetailTab) ?? "evidence",
  };
}

export function useNavigatorState() {
  const initial = useMemo(readParams, []);
  const [query, setQueryState] = useState(initial.query);
  const [domain, setDomainState] = useState(initial.domain);
  const [classCode, setClassState] = useState(initial.classCode);
  const [selectedId, setSelectedState] = useState(initial.selectedId);
  const [tab, setTabState] = useState<DetailTab>(initial.tab);

  const sync = useCallback((patch: Record<string, string>) => {
    const params = new URLSearchParams(window.location.search);
    Object.entries(patch).forEach(([key, value]) => value && value !== "ALL" ? params.set(key, value) : params.delete(key));
    window.history.replaceState(null, "", `${window.location.pathname}?${params.toString()}`);
  }, []);

  return {
    query,
    domain,
    classCode,
    selectedId,
    tab,
    setQuery: (value: string) => { setQueryState(value); sync({ q: value }); },
    setDomain: (value: string) => { setDomainState(value); sync({ domain: value }); },
    setClassCode: (value: string) => { setClassState(value); sync({ class: value }); },
    setSelectedId: (value: string) => { setSelectedState(value); sync({ selected: value }); },
    setTab: (value: DetailTab) => { setTabState(value); sync({ tab: value }); },
  };
}
