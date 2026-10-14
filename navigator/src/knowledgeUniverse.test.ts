import { describe, expect, it } from "vitest";
import { catalogBridgeCandidates, knowledgeGeometry, knowledgeTimeline, methodCoverage, reviewedRelations } from "./knowledgeUniverse";
import type { Concept, Relationship, ReviewedClaim } from "./types";
const c = (id:string,domain_code:string,tags:string[]) => ({id,domain_code,domain:"Domain "+domain_code,tags}) as Concept;
const sample=[c("DBE-A01","A",["fusion","materials"]),c("DBE-C01","C",["materials"]),c("DBE-D01","D",["AI"])];
describe("V8 knowledge universe projections",()=>{
 it("uses six stable domain layouts without inventing evidence",()=>{
   const first=knowledgeGeometry(sample); expect(first).toEqual(knowledgeGeometry(sample));
   expect(first.domains).toHaveLength(6); expect(first.concepts).toHaveLength(3);
   expect(first.domains.find(d=>d.id==="C")?.count).toBe(1);
 });
 it("never promotes a tag overlap into a causal or evidence link",()=>{
   expect(catalogBridgeCandidates(sample)).toEqual([{a:"DBE-A01",b:"DBE-C01",sharedTags:["materials"],status:"CATALOG_TAG_OVERLAP_ONLY"}]);
 });
 it("requires reviewed exact claim refs for relationships",()=>{
   const claims=[{id:"N01",candidate:"DBE-A01"}] as ReviewedClaim[];
   const links=[
     {id:"good",source_id:"N01",target_id:"DBE-A01",relation_type:"COMPONENT_EVIDENCE_FOR",review_status:"REVIEWED",gate:null},
     {id:"suggestion",source_id:"N01",target_id:"DBE-C01",relation_type:"SUGGESTED_TOPIC_OVERLAP",review_status:"PROPOSED",gate:null},
     {id:"missing",source_id:"UNKNOWN",target_id:"DBE-A01",relation_type:"DIRECT_EVIDENCE_FOR",review_status:"REVIEWED",gate:null}
   ] as Relationship[];
   expect(reviewedRelations("DBE-A01",links,claims).map(x=>x.id)).toEqual(["good"]);
   expect(reviewedRelations("DBE-C01",links,claims)).toHaveLength(0);
 });
 it("does not upgrade descriptive method tags to formal validation",()=>{
   const claims=[{id:"N01",candidate:"DBE-A01",type:["experimental","engineering"]}] as (ReviewedClaim&{type:string[]})[];
   expect(methodCoverage("DBE-A01",claims).map(row=>row.caseIds)).toEqual([[],["N01"],["N01"]]);
 });
 it("sorts knowledge snapshots without claiming physical change",()=>{
   expect(knowledgeTimeline("2026-10-04","2026-10-09","2026-10-08").map(x=>x.key)).toEqual(["atlas","observatory","workbench"]);
 });
});
