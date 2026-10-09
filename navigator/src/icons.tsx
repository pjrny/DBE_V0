import type { ReactNode, SVGProps } from "react";

type Name = "search" | "filter" | "download" | "warning" | "source" | "network" | "queue" | "chevron" | "info" | "close";

export function Icon({ name, ...props }: SVGProps<SVGSVGElement> & { name: Name }) {
  const paths: Record<Name, ReactNode> = {
    search: <><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4 4"/></>,
    filter: <path d="M3 5h18l-7 8v6l-4 2v-8Z"/>,
    download: <><path d="M12 3v11m0 0 4-4m-4 4-4-4"/><path d="M5 18v3h14v-3"/></>,
    warning: <><path d="M12 3 2.8 20h18.4Z"/><path d="M12 8v5m0 3v.1"/></>,
    source: <><path d="M6 3h9l4 4v14H6Z"/><path d="M15 3v5h4M9 12h6M9 16h6"/></>,
    network: <><circle cx="5" cy="12" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="19" cy="18" r="2.5"/><path d="m7.3 11 9.2-4m-9.2 6 9.2 4"/></>,
    queue: <><path d="M8 6h13M8 12h13M8 18h13"/><circle cx="3.5" cy="6" r=".8"/><circle cx="3.5" cy="12" r=".8"/><circle cx="3.5" cy="18" r=".8"/></>,
    chevron: <path d="m9 5 7 7-7 7"/>,
    info: <><circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.1"/></>,
    close: <path d="m6 6 12 12M18 6 6 18"/>,
  };
  return <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" {...props}>{paths[name]}</svg>;
}
