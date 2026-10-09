import inventoryJson from "../../docs/SDBES/data/V6_CONCEPT_INVENTORY.json";
import runtimeJson from "../../docs/SDBES/data/V5_RUNTIME_VIEW.json";
import type { Concept, QueueItem, Relationship, ReviewedClaim, SourceRecord } from "./types";

export const inventory = inventoryJson as unknown as {
  warning: string;
  concepts: Concept[];
  sources: SourceRecord[];
  derived_counts: Record<string, number>;
  source_incidents: Array<Record<string, string>>;
};

export const runtime = runtimeJson as unknown as {
  mode: string;
  reviewed_claims: ReviewedClaim[];
  relationships: Relationship[];
  research_queue: QueueItem[];
  authorized_models: unknown[];
  scenario_message: string;
};

export const sourceById = new Map(inventory.sources.map((source) => [source.id, source]));
export const claimById = new Map(runtime.reviewed_claims.map((claim) => [claim.id, claim]));
export const claimsByConcept = new Map<string, ReviewedClaim[]>();
for (const claim of runtime.reviewed_claims) {
  const existing = claimsByConcept.get(claim.candidate) ?? [];
  claimsByConcept.set(claim.candidate, [...existing, claim]);
}
