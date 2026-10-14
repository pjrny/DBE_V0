import registryJson from "../../docs/SDBES/data/V8_VIEW_RECORDS.json";
import { evaluateGate, knowledgeToScenario, type Gate, type KnowledgeTruth, type ScenarioTruth } from "./v8Math";

export type Applicability="APPLICABLE"|"NOT_APPLICABLE"|"UNRESOLVED";
export type Availability="PRESENT"|"ABSENT"|"UNKNOWN";
export type CellOutcome="MEETS"|"DOES_NOT_MEET"|"INCONCLUSIVE"|"UNKNOWN";
export type FEAKey="F"|"E"|"A";
export type Criterion="validated"|"independent"|"generalized";
export const FEA_KEYS:readonly FEAKey[]=["F","E","A"];
export const CRITERIA:readonly Criterion[]=["validated","independent","generalized"];
export type RegisteredCell={
  applicability:Applicability; availability:Availability; outcome:CellOutcome;
  verification_activity_ids:string[]; scope:string; notes?:string;
};
export type RegisteredProfile={
  profile_id:string;claim_id:string;concept_id:string; assessment_scope:string;
  source_snapshot_ref:string;recorded_at:string;
  cells:Record<FEAKey,Record<Criterion,RegisteredCell>>;
};
export type VerificationActivity={
  activity_id:string;activity_type:string;performed_by:string;method:string;source_ref:string;
};
export type StructuralPredicate={predicate_id:string;label:string;knowledge_status:KnowledgeTruth};
export type RegisteredGate={gate_id:string;operator:Gate;k?:number;input_predicate_ids:string[]};
export type RegisteredStructure={
  graph_id:string;concept_id:string;source_snapshot_ref:string;scope:string;closure_status:string;
  predicates:StructuralPredicate[];gates:RegisteredGate[];
};
export type V8Registry={
  schema_name:string;schema_version:string;snapshot_id:string;recording_policy:string;
  verification_activities:VerificationActivity[];
  claim_profiles:RegisteredProfile[];
  structural_graphs:RegisteredStructure[];
  registered_model_cards:unknown[];
};
export const scienceRegistry=registryJson as unknown as V8Registry;

const APPLICABILITY=["APPLICABLE","NOT_APPLICABLE","UNRESOLVED"];
const AVAILABILITY=["PRESENT","ABSENT","UNKNOWN"];
const OUTCOMES=["MEETS","DOES_NOT_MEET","INCONCLUSIVE","UNKNOWN"];
const KSTAT=["NEITHER","TRUE_ONLY","FALSE_ONLY","BOTH"];
const GATES=["ALL","ANY","K_OF_N"];

export function validateV8Registry(reg:V8Registry,knownClaimBindings:Map<string,string>):string[]{
  const errors:string[]=[];
  if(reg.schema_name!=="SDBES_V8_TYPED_VISUAL_REGISTRY"||reg.recording_policy!=="STRICT_RECEIPT_BACKED_ONLY")errors.push("Unrecognized registry contract");
  const activities=new Map<string,VerificationActivity>();
  for(const a of reg.verification_activities){
    if(!a.activity_id ||activities.has(a.activity_id)||!a.activity_type||!a.performed_by||!a.method||!a.source_ref)errors.push("Missing, duplicate or untraceable verification activity");
    else activities.set(a.activity_id,a);
  }
  const profileIds=new Set<string>();
  for(const p of reg.claim_profiles){
    if(!p.profile_id||profileIds.has(p.profile_id))errors.push("Duplicate or blank profile ID");
    profileIds.add(p.profile_id);
    if(knownClaimBindings.get(p.claim_id)!==p.concept_id)errors.push("Unresolved claim/concept binding: "+p.profile_id);
    if(!p.assessment_scope||!p.source_snapshot_ref||!p.recorded_at)errors.push("Profile missing scope/source/date: "+p.profile_id);
    for(const axis of FEA_KEYS)for(const col of CRITERIA){
      const c=p.cells?.[axis]?.[col];
      if(!c||!APPLICABILITY.includes(c.applicability)||!AVAILABILITY.includes(c.availability)||!OUTCOMES.includes(c.outcome)){
        errors.push("Invalid FEA cell: "+p.profile_id+" "+axis+"_"+col);continue;
      }
      if(c.applicability!=="APPLICABLE"&&(c.availability==="PRESENT"||c.outcome==="MEETS"))errors.push("Nonapplicable cell cannot be reported as verified: "+p.profile_id+" "+axis+"_"+col);
      if(c.availability!=="PRESENT"&&c.outcome!=="UNKNOWN")errors.push("Absent/unknown evidence with a definitive outcome: "+p.profile_id+" "+axis+"_"+col);
      if(c.availability==="PRESENT"&&(!c.scope||!c.verification_activity_ids?.length))errors.push("Present evidence without scoped receipt: "+p.profile_id+" "+axis+"_"+col);
      for(const id of c.verification_activity_ids??[])if(!activities.has(id))errors.push("Dangling verification activity "+id+" in "+p.profile_id);
      if(c.availability==="PRESENT"&&col==="independent"&&c.outcome==="MEETS"&&!c.verification_activity_ids.some(id=>activities.get(id)?.activity_type==="INDEPENDENT_REPLICATION_CONFIRMED"))
        errors.push("Independent evidence lacks independent replication receipt: "+p.profile_id);
    }
  }
  const graphs=new Set<string>();
  for(const g of reg.structural_graphs){
    if(!g.graph_id||graphs.has(g.graph_id)||!g.source_snapshot_ref||!g.scope||!g.closure_status||!g.concept_id)errors.push("Missing or duplicate structural snapshot provenance");
    graphs.add(g.graph_id);
    const nodes=new Set<string>();
    for(const p of g.predicates){
      if(nodes.has(p.predicate_id)||!p.predicate_id||!p.label||!KSTAT.includes(p.knowledge_status))errors.push("Invalid structural predicate in "+g.graph_id);
      nodes.add(p.predicate_id);
    }
    for(const gate of g.gates){
      if(!GATES.includes(gate.operator)||!gate.gate_id||!gate.input_predicate_ids.length)errors.push("Invalid structural gate in "+g.graph_id);
      if(gate.input_predicate_ids.some(id=>!nodes.has(id)))errors.push("Unresolved gate input in "+g.graph_id);
      const k=gate.operator==="K_OF_N"?(gate.k??NaN):1;
      if(gate.operator==="K_OF_N"&&(!Number.isInteger(k)||k<1||k>gate.input_predicate_ids.length))errors.push("Invalid k-of-n gate in "+g.graph_id);
    }
  }
  return errors;
}
export function resolvedV8Cell(cell:RegisteredCell|undefined,activities:VerificationActivity[]){
  if(!cell)return {label:"UNKNOWN",kind:"unknown" as const,detail:"No structured assessment or verification receipt is registered"};
  if(cell.applicability==="NOT_APPLICABLE")return {label:"N/A",kind:"na" as const,detail:cell.notes??"Criterion not applicable to this scoped claim"};
  if(cell.applicability!=="APPLICABLE")return {label:"UNRESOLVED",kind:"unknown" as const,detail:"Applicability is unresolved"};
  if(cell.availability==="ABSENT")return {label:"ABSENT",kind:"unknown" as const,detail:"Relevant evidence is recorded absent; this is not a failed test"};
  if(cell.availability==="UNKNOWN")return {label:"UNKNOWN",kind:"unknown" as const,detail:"Evidence not assessed"};
  const receipts=new Set(activities.map(a=>a.activity_id));
  if(!cell.scope||!cell.verification_activity_ids?.length||cell.verification_activity_ids.some(id=>!receipts.has(id)))return {label:"UNVERIFIED",kind:"unknown" as const,detail:"Required scope or provenance receipt is missing"};
  return {label:cell.outcome,kind:"recorded" as const,detail:cell.notes??"Scoped assessment outcome with activity receipts; not a universal probability"};
}
export function gateState(graph:RegisteredStructure,gate:RegisteredGate):ScenarioTruth{
  const nodes=new Map(graph.predicates.map(x=>[x.predicate_id,x.knowledge_status]));
  const inputs=gate.input_predicate_ids.map(id=>nodes.has(id)?knowledgeToScenario(nodes.get(id)!):"UNKNOWN");
  return evaluateGate(gate.operator,inputs,gate.k??1);
}
export function registeredProfiles(conceptId:string,reg:V8Registry=scienceRegistry){
  return reg.claim_profiles.filter(p=>p.concept_id===conceptId).sort((a,b)=>a.profile_id.localeCompare(b.profile_id));
}
export function registeredStructures(conceptId:string,reg:V8Registry=scienceRegistry){
  return reg.structural_graphs.filter(g=>g.concept_id===conceptId).sort((a,b)=>a.graph_id.localeCompare(b.graph_id));
}
