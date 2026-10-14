/** V8 navigation-only analytical projections. Never infer causation, confidence or dynamics from proximity. */
import type { Concept, Relationship, ReviewedClaim } from "./types";

export type KnowledgeLens = "universe" | "evidence" | "dependencies" | "dynamics" | "timeline" | "exploration";
export const LENSES: ReadonlyArray<{id:KnowledgeLens;label:string;description:string}> = [
  {id:"universe",label:"Universe",description:"Domains and concepts"},
  {id:"evidence",label:"Evidence space",description:"Formal, empirical and applied evidence"},
  {id:"dependencies",label:"Dependencies",description:"Reviewed relationships and structural gates"},
  {id:"dynamics",label:"Dynamics",description:"Scoped physical models and research knowledge"},
  {id:"timeline",label:"Time & revision",description:"Knowledge timeline, not physical progress"},
  {id:"exploration",label:"Exploration",description:"Unreviewed cross-field candidates"},
];
export const DOMAIN_PALETTE:Record<string,string> = {A:"#637bc5",B:"#439b91",C:"#ad83b9",D:"#bd8755",E:"#8a91ab",F:"#6c9884"};
export type ConceptPoint = {id:string;domain:string;x:number;y:number};
export type DomainPoint = {id:string;x:number;y:number;count:number;label:string};
export function knowledgeGeometry(concepts:readonly Pick<Concept,"id"|"domain_code"|"domain">[]) {
  const domains = ["A","B","C","D","E","F"].map((code,i)=>{
    const angle = -Math.PI/2 + i*Math.PI/3;
    return {id:code,x:600+320*Math.cos(angle),y:375+230*Math.sin(angle),
      count:concepts.filter(c=>c.domain_code===code).length,
      label:concepts.find(c=>c.domain_code===code)?.domain ?? code};
  });
  const points:ConceptPoint[]=[];
  for (const domain of domains) {
    const members=concepts.filter(c=>c.domain_code===domain.id).slice().sort((a,b)=>a.id.localeCompare(b.id));
    members.forEach((c,i)=>{
      const angle=2.399963229728653*i + Math.PI/6;
      const radius=22 + 16*Math.sqrt(i+1);
      points.push({id:c.id,domain:domain.id,x:domain.x+radius*Math.cos(angle),y:domain.y+radius*Math.sin(angle)});
    });
  }
  return {domains, concepts:points};
}
export function reviewedRelations(conceptId:string,rels:readonly Relationship[],claims:readonly ReviewedClaim[]) {
  const known=new Set(claims.map(c=>c.id));
  return rels.filter(r=>r.target_id===conceptId && known.has(r.source_id) && r.review_status==="REVIEWED");
}
export type EvidenceRow={id:"F"|"E"|"A";label:string;methods:string[];caseIds:string[]};
export function methodCoverage(conceptId:string,claims:readonly (ReviewedClaim&{type?:string[]})[]):EvidenceRow[] {
  const relevant=claims.filter(c=>c.candidate===conceptId);
  const axes=[
    {id:"F" as const,label:"Formal / mathematical",patterns:["formal","theor","proof","mathematical","analytic"]},
    {id:"E" as const,label:"Empirical / experimental",patterns:["empirical","experimental","experiment","observational"]},
    {id:"A" as const,label:"Applied / engineering",patterns:["engineering","prototype","applied","hardware"]},
  ];
  return axes.map(axis=>{
    const matches=relevant.filter(c=>(c.type??[]).some(t=>axis.patterns.some(p=>t.toLowerCase().includes(p))));
    return {id:axis.id,label:axis.label,caseIds:matches.map(c=>c.id),methods:Array.from(new Set(matches.flatMap(c=>c.type??[])))};
  });
}
export type CandidateBridge={a:string;b:string;sharedTags:string[];status:"CATALOG_TAG_OVERLAP_ONLY"};
export function catalogBridgeCandidates(concepts:readonly Pick<Concept,"id"|"domain_code"|"tags">[], cap=16):CandidateBridge[] {
  const out:CandidateBridge[]=[];
  for(let i=0;i<concepts.length;i++) for(let j=i+1;j<concepts.length;j++){
    const a=concepts[i],b=concepts[j];
    if(a.domain_code===b.domain_code)continue;
    const shared=a.tags.filter(t=>b.tags.includes(t)).sort();
    if(shared.length)out.push({a:a.id,b:b.id,sharedTags:shared,status:"CATALOG_TAG_OVERLAP_ONLY"});
  }
  return out.sort((a,b)=>b.sharedTags.length-a.sharedTags.length||a.a.localeCompare(b.a)||a.b.localeCompare(b.b)).slice(0,cap);
}
export function knowledgeTimeline(atlasDate:string,reviewedDate:string,observatoryDate:string){
  return [
    {date:atlasDate,key:"atlas",label:"Concept atlas staged",detail:"90 discovery candidates, not validated scientific claims"},
    {date:observatoryDate,key:"observatory",label:"Observatory snapshot",detail:"Focused research program, no automatic scientific promotions"},
    {date:reviewedDate,key:"workbench",label:"Evidence workbench snapshot",detail:"Research knowledge changed; physical states did not automatically change"},
  ].filter(v=>/^\d{4}-\d{2}-\d{2}$/.test(v.date)).sort((a,b)=>a.date.localeCompare(b.date)||a.key.localeCompare(b.key));
}
