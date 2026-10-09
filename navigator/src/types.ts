export type Concept = {
  id: string;
  title: string;
  domain_code: string;
  domain: string;
  discovery_class: "D" | "P" | "S" | "X";
  discovery_class_label: string;
  role: string;
  bounded_question: string;
  mechanism_status: string;
  resource_ledger: string;
  main_gap: string;
  next_investigation: string;
  coverage: string;
  formal_confidence: string;
  source_refs: string[];
  tags: string[];
  review_workflow: string;
  work_disposition: string;
  context_compatibility: string;
  display_status: string;
};

export type SourceRecord = {
  id: string;
  title: string;
  record_type: string;
  url: string | null;
  doi_url: string | null;
  verification: { status: string; receipt: string | null; note: string };
};

export type ReviewedClaim = {
  id: string;
  title: string;
  candidate: string;
  direct_claim: string;
  application_claim: string;
  application_relation: string;
  assessment_result: string;
  assessment_scope: string;
  v4_contract: string;
  source_locator: { path: string; record_id: string; status: string };
};

export type Relationship = {
  id: string;
  source_id: string;
  target_id: string;
  relation_type: string;
  review_status: string;
  gate: string | null;
};

export type QueueItem = {
  id: string;
  concept_id: string;
  title: string;
  activity_mode: string;
  origin: string;
  comparison_state: string;
  attempts: unknown[];
  preregistration: unknown | null;
  decision_rule: unknown | null;
  work_status: string;
};
