import {describe,expect,it} from "vitest";
import {scienceRegistry,validateV8Registry,resolvedV8Cell,gateState,
  type V8Registry,type RegisteredCell,type RegisteredProfile,type RegisteredStructure} from "./v8Registry";
const claimBindings=new Map([["N01","DBE-A01"]]);
const unknown:RegisteredCell={applicability:"UNRESOLVED",availability:"UNKNOWN",outcome:"UNKNOWN",verification_activity_ids:[],scope:""};
function fixture():V8Registry{
 const profile:RegisteredProfile={
   profile_id:"test-profile",claim_id:"N01",concept_id:"DBE-A01",
   assessment_scope:"Synthetic parser fixture",source_snapshot_ref:"test/fixture.json#N01",recorded_at:"2026-10-14",
   cells:{F:{validated:{...unknown},independent:{...unknown},generalized:{...unknown}},
     E:{validated:{...unknown},independent:{...unknown},generalized:{...unknown}},
     A:{validated:{...unknown},independent:{...unknown},generalized:{...unknown}}}
 };
 return {...scienceRegistry,claim_profiles:[profile],structural_graphs:[],verification_activities:[],registered_model_cards:[]};
}
describe("V8 imported evidence contract",()=>{
 it("base registry is empty and passes without manufacturing results",()=>{
   expect(scienceRegistry.claim_profiles).toHaveLength(0);
   expect(scienceRegistry.structural_graphs).toHaveLength(0);
   expect(validateV8Registry(scienceRegistry,claimBindings)).toEqual([]);
 });
 it("rejects profile claim/content mismatches and phantom verification",()=>{
   const r=fixture();
   expect(validateV8Registry(r,claimBindings)).toEqual([]);
   r.claim_profiles[0].concept_id="DBE-D04";
   expect(validateV8Registry(r,claimBindings)).toContain("Unresolved claim/concept binding: test-profile");
   r.claim_profiles[0].concept_id="DBE-A01";
   r.claim_profiles[0].cells.E.validated={applicability:"APPLICABLE",availability:"PRESENT",outcome:"MEETS",verification_activity_ids:[],scope:"lab"};
   expect(validateV8Registry(r,claimBindings).some(x=>x.includes("without scoped receipt"))).toBe(true);
   expect(resolvedV8Cell(r.claim_profiles[0].cells.E.validated,[]).label).toBe("UNVERIFIED");
 });
 it("requires explicit independent replication to mark independent MEETS",()=>{
   const r=fixture();r.verification_activities=[
     {activity_id:"local",activity_type:"SOURCE_REPORTED",performed_by:"source",method:"reported",source_ref:"test"}
   ];
   r.claim_profiles[0].cells.F.independent={applicability:"APPLICABLE",availability:"PRESENT",outcome:"MEETS",scope:"test",verification_activity_ids:["local"]};
   expect(validateV8Registry(r,claimBindings).some(e=>e.includes("Independent evidence lacks"))).toBe(true);
   r.verification_activities[0].activity_type="INDEPENDENT_REPLICATION_CONFIRMED";
   expect(validateV8Registry(r,claimBindings)).toEqual([]);
   expect(resolvedV8Cell(r.claim_profiles[0].cells.F.independent,r.verification_activities).label).toBe("MEETS");
 });
 it("preserves absent evidence, failed evaluation and genuinely irrelevant as different outcomes",()=>{
   expect(resolvedV8Cell({...unknown,applicability:"NOT_APPLICABLE"},[]).label).toBe("N/A");
   expect(resolvedV8Cell({...unknown,applicability:"APPLICABLE",availability:"ABSENT"},[]).label).toBe("ABSENT");
   expect(resolvedV8Cell({...unknown},[]).label).toBe("UNRESOLVED");
 });
 it("evaluates provenance-linked registered structural graphs without creating domain facts",()=>{
   const graph:RegisteredStructure={graph_id:"test",concept_id:"DBE-A01",scope:"fictional",source_snapshot_ref:"fixture",
     closure_status:"CLOSED_WITHIN_DEFINED_ARCHITECTURE",
     predicates:[
       {predicate_id:"p1",label:"P1",knowledge_status:"TRUE_ONLY"},
       {predicate_id:"p2",label:"P2",knowledge_status:"BOTH"},
       {predicate_id:"p3",label:"P3",knowledge_status:"FALSE_ONLY"}
     ],gates:[{gate_id:"g1",operator:"K_OF_N",k:2,input_predicate_ids:["p1","p2","p3"]}]
   };
   const r=fixture();r.structural_graphs=[graph];
   expect(validateV8Registry(r,claimBindings)).toEqual([]);
   expect(gateState(graph,graph.gates[0])).toBe("UNKNOWN");
   graph.gates[0].input_predicate_ids[0]="not-known";
   expect(validateV8Registry(r,claimBindings)).toContain("Unresolved gate input in test");
 });
});
