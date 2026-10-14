import { useState, type ReactNode } from "react";
import { gateState, registeredStructures, scienceRegistry } from "./v8Registry";
import { inventory, runtime } from "./data";
import type { Concept, ReviewedClaim } from "./types";
import {
  KNOWLEDGE_STATES, evaluateGate, knowledgeToScenario, minimalGateSets,
  toyTrajectory, toyModelSummary,
  type Gate, type KnowledgeTruth,
} from "./v8Math";

function SelectLine({label, value, options, onChange}:{label:string;value:string;options:readonly string[];onChange:(v:string)=>void}){
  return <label className="v8lab-select"><span>{label}</span><select value={value} onChange={e=>onChange(e.target.value)}>
    {options.map(x=><option value={x} key={x}>{x}</option>)}
  </select></label>;
}
function Info({children}:{children:ReactNode}){return <p className="v8lab-note">{children}</p>;}
function PanelHead({title,description}:{title:string;description:string}){
  return <div className="v8lab-head"><strong>{title}</strong><small>{description}</small></div>;
}

/** A source-grounded drilldown into one of the existing V1/V2 review cases. */
export function EvidenceTrace({concept}:{concept:Concept}){
  const all=runtime.reviewed_claims.filter(c=>c.candidate===concept.id);
  const [caseId,setCaseId]=useState("");
  const detail=all.find(c=>c.id===caseId)??all[0];
  return <section className="v8lab-panel" aria-label="Evidence provenance trace">
    <PanelHead title="Evidence trace · direct claim vs. application"
      description="Reviewed case metadata from V1/V2 stress testing. The framework PASS verdict validates a schema check, not scientific truth."/>
    {detail ? <>
      <div className="v8lab-pills">{all.map(c=><button key={c.id} aria-pressed={c.id===detail.id} onClick={()=>setCaseId(c.id)}>{c.id}</button>)}</div>
      <h3>{detail.title}</h3>
      <div className="v8lab-two">
        <article><small>What the source reports within its scope</small><p>{detail.direct_claim}</p></article>
        <article><small>Broader application still under investigation</small><p>{detail.application_claim}</p></article>
      </div>
      <dl className="v8lab-facts">
        <div><dt>Relationship type</dt><dd>{detail.application_relation.replaceAll("_"," ")}</dd></div>
        <div><dt>V1–V4 assessment compatibility</dt><dd>{detail.assessment_result.replaceAll("_"," ")}</dd></div>
        <div><dt>Simulation/transfer boundary</dt><dd>{detail.v4_contract}</dd></div>
        <div><dt>Assessment scope</dt><dd>{detail.assessment_scope}</dd></div>
        <div><dt>Review source</dt><dd>{detail.source_locator.path} · {detail.source_locator.record_id}</dd></div>
      </dl>
      <Info>These records do not include independently validated F/E/A V/I/G cell receipts or a claim-specific numerical probability. Supporting and challenging evidence remain distinct, and a bounded component result is not proof of an integrated energy system.</Info>
    </> : <div className="v8lab-empty">No reviewed case is linked to {concept.id}. The Phase-1 catalog source anchors remain available in the evidence inspector; this does not imply that evidence is absent.</div>}
    <div className="v8lab-two v8lab-evidence-sides">
      <article><small>Source-reported mechanism / candidate rationale</small><p>{concept.mechanism_status}</p></article>
      <article><small>Known gap / challenge to be resolved</small><p>{concept.main_gap}</p></article>
    </div>
    <Info>These two summaries originate in the Phase-1 intake, not newly verified V2 assessment cells. No numeric polarity is inferred from their wording.</Info>
  </section>;
}

const INPUT_IDS=["A","B","C","D"] as const;
const DEFAULT_STATES:KnowledgeTruth[]=["TRUE_ONLY","NEITHER","FALSE_ONLY","BOTH"];
/** Interactively exercises the exact V3 gate truth semantics without registering a scientific dependency. */
export function DependencyGateLab(){
  const [operator,setOperator]=useState<Gate>("K_OF_N");
  const [threshold,setThreshold]=useState(2);
  const [states,setStates]=useState<KnowledgeTruth[]>(DEFAULT_STATES);
  const scenario=states.map(knowledgeToScenario);
  const result=evaluateGate(operator,scenario,threshold);
  const minimal=minimalGateSets(operator,states.length,threshold);
  const stringify=(combos:number[][])=>combos.map(c=>c.map(i=>INPUT_IDS[i]).join(" + ")).join(" OR ");
  const changeState=(i:number,v:KnowledgeTruth)=>setStates(prev=>prev.map((s,j)=>j===i?v:s));
  return <section className="v8lab-panel" aria-label="V3 structural gate sandbox">
    <PanelHead title="V3 structural dependency gate · live demonstration" description="Hypothetical four-input network; NOT the prerequisites of the selected scientific concept."/>
    <div className="v8lab-controls">
      <SelectLine label="Gate logic" value={operator} options={["ALL","ANY","K_OF_N"]} onChange={v=>setOperator(v as Gate)}/>
      {operator==="K_OF_N"&&<label className="v8lab-select"><span>Required inputs (k)</span><input type="number" min={1} max={4} step={1} value={threshold}
        onChange={e=>{const n=Number(e.target.value);if(Number.isInteger(n)&&n>=1&&n<=4)setThreshold(n);}}/></label>}
    </div>
    <div className="v8lab-gate">
      <div className="v8lab-inputs">{states.map((state,i)=><label key={INPUT_IDS[i]}><b>Predicate {INPUT_IDS[i]}</b>
        <select aria-label={"Predicate "+INPUT_IDS[i]+" knowledge status"} value={state} onChange={e=>changeState(i,e.target.value as KnowledgeTruth)}>
          {KNOWLEDGE_STATES.map(s=><option key={s} value={s}>{s}</option>)}
        </select><small>Scenario: {scenario[i]}</small></label>)}</div>
      <div className="v8lab-arrow" aria-hidden="true">→</div>
      <output className={"v8lab-gate-output "+result.toLowerCase()} aria-live="polite">
        <small>{operator==="K_OF_N"?(threshold+" of "+states.length):operator}</small>
        <strong>{result}</strong>
        <small>V3 scenario state</small>
      </output>
    </div>
    <div className="v8lab-two">
      <article><small>Minimal sufficient sets · all others FALSE</small><p>{stringify(minimal.paths)}</p></article>
      <article><small>Minimal cut sets · all others TRUE</small><p>{stringify(minimal.cuts)}</p></article>
    </div>
    <Info>Knowledge statuses preserve contradictions: BOTH is not FALSE or TRUE; NEITHER and BOTH map to UNKNOWN for this demonstration's scenario evaluation. These path and cut sets are exact only for the shown monotone, four-input gate, not global necessity or a claim about nature.</Info>
  </section>;
}

function Plot({points}:{points:ReturnType<typeof toyTrajectory>}){
  const series=[
    {name:"Intervention trajectory",color:"#117aa2",key:"x" as const},
    {name:"Zero-control comparator",color:"#b2774a",key:"baseline" as const},
    {name:"Initial-state response",color:"#8565b7",key:"impulse" as const},
  ];
  const data=points.flatMap(p=>[p.x,p.baseline,p.impulse]);
  const lo=Math.min(-0.1,...data),hi=Math.max(0.1,...data);
  const margin=0.08*(hi-lo)||0.1,yLo=lo-margin,yHi=hi+margin;
  const x=(k:number)=>52+(k/(points.length-1))*628;
  const y=(v:number)=>298-(v-yLo)/(yHi-yLo)*245;
  const path=(key:"x"|"baseline"|"impulse")=>points.map((p,i)=>(i===0?"M":"L")+x(p.k).toFixed(1)+" "+y(p[key]).toFixed(1)).join(" ");
  const format=(v:number)=>v.toFixed(2);
  return <div className="v8lab-plotwrap">
    <svg role="img" aria-label="Unitless toy model time series for intervention, zero-control comparator and initial-state response" viewBox="0 0 730 344">
      <rect x={52} y={38} width={628} height={260} rx={5} fill="#f9fcff" stroke="#d8e5ee"/>
      {[0,.25,.5,.75,1].map(t=><g key={t}><line x1={52} y1={52+t*242} x2={680} y2={52+t*242} stroke="#d9e5ef"/>
        <text x={45} y={55+t*242} fontSize={11} textAnchor="end" fill="#657b8d">{format(yHi-t*(yHi-yLo))}</text></g>)}
      <line x1={52} y1={y(0)} x2={680} y2={y(0)} stroke="#607a8a" strokeDasharray="4 4"/>
      {points.filter((_,i)=>i%3===0).map(p=><text key={p.k} x={x(p.k)} y={319} fill="#607789" fontSize={11} textAnchor="middle">{p.k}</text>)}
      {series.map(s=><path key={s.key} d={path(s.key)} fill="none" stroke={s.color} strokeWidth={2.9} strokeLinejoin="round" strokeLinecap="round"/>)}
      <text x={366} y={338} fontSize={11} textAnchor="middle" fill="#49657c">Discrete time step k · no physical time unit</text>
    </svg>
    <div className="v8lab-legend">{series.map(s=><span key={s.key}><i style={{background:s.color}}/>{s.name}</span>)}</div>
  </div>;
}
export function DynamicsLab(){
  const [retention,setRetention]=useState(.8);
  const [control,setControl]=useState(.35);
  const [disturbance,setDisturbance]=useState(.12);
  const params={retention,control,disturbance,steps:12};
  const trajectory=toyTrajectory(params),summary=toyModelSummary(params);
  const sliders=[{name:"Retention a",value:retention,set:setRetention},{name:"Intervention u",value:control,set:setControl},{name:"Disturbance d",value:disturbance,set:setDisturbance}];
  return <section className="v8lab-panel" aria-label="V4 synthetic dynamics visualization">
    <PanelHead title="V4 numerical dynamics · explicitly synthetic example"
      description="Explore what a local eigenvalue, an intervention and a comparison trajectory mean. This is NOT a fusion model."/>
    <div className="v8lab-equation"><code>x(k+1) = a·x(k) + u − d</code><small>Dimensionless discrete system · x(0)=0 · comparator u=0 · impulse x(0)=1 with u=d=0</small></div>
    <div className="v8lab-sliders">{sliders.map(s=><label key={s.name}><span>{s.name}: <b>{s.value.toFixed(2)}</b></span>
      <input aria-label={s.name} type="range" min={0} max={1} step={.05} value={s.value} onChange={e=>s.set(Number(e.target.value))}/></label>)}</div>
    <Plot points={trajectory}/>
    <div className="v8lab-metrics">
      <div><small>Local eigenvalue (A)</small><strong>{summary.localEigenvalue.toFixed(2)}</strong></div>
      <div><small>One-step response (B)</small><strong>1.00</strong></div>
      <div><small>Linear stability</small><strong>{summary.stable?"|a| < 1":"Marginal a=1"}</strong></div>
      <div><small>Fixed point if stable</small><strong>{summary.equilibrium===null?"Not finite":summary.equilibrium.toFixed(2)}</strong></div>
    </div>
    <Info>Synthetic, unit-free educational example only. No material parameters, calibration, physical operating regime, verification receipts, causal identification, or domain-model authorization are claimed. A real V4 model cannot be run from these controls.</Info>
  </section>;
}

/** Snapshot provenance, without fake claim-by-claim change tracking. */
export function ProvenanceAudit(){
  const snapshots=inventory.source_snapshots??[];
  const [expanded,setExpanded]=useState(false);
  return <section className="v8lab-panel" aria-label="Snapshot source provenance">
    <PanelHead title="Data lineage & snapshot coverage" description="Source records establish what was captured, not the physical truth of the source's claims."/>
    <div className="v8lab-metrics">
      <div><small>Staged concepts</small><strong>{inventory.concepts.length}</strong></div>
      <div><small>Catalog source records</small><strong>{inventory.sources.length}</strong></div>
      <div><small>Reviewed cases</small><strong>{runtime.reviewed_claims.length}</strong></div>
      <div><small>Registered models</small><strong>{runtime.authorized_models.length}</strong></div>
    </div>
    <button className="v8lab-outline" onClick={()=>setExpanded(x=>!x)} aria-expanded={expanded}>{expanded?"Hide":"Inspect"} pinned intake sources and issues</button>
    {expanded && <>
      <div className="v8lab-list">{snapshots.map((s,i)=><article key={String(s.path??i)}><strong>{String(s.path??"Unknown path")}</strong>
        <small>Role: {String(s.role??"Not provided")}</small><code>SHA-256: {String(s.sha256??"UNKNOWN")}</code>
        <small>{String(s.content_status??"No content error flag on source record")}</small></article>)}</div>
      {inventory.source_incidents.map((s,i)=><p key={i} className="v8lab-issue">{String(s.status)}: {String(s.effect??s.path??"Source issue")}</p>)}
    </>}
    <Info>Available source snapshots do not contain enough full historical claim-assessment diffs to animate a real confidence trajectory. The visible time markers are intake/processing events, not a scientific progress curve.</Info>
  </section>;
}

export function CompareConcepts({selected,onSelect}:{selected:Concept;onSelect:(id:string)=>void}){
  const [otherId,setOtherId]=useState("DBE-F01");
  const other=inventory.concepts.find(c=>c.id===otherId)??inventory.concepts[0];
  const cols=[selected,other];
  return <section className="v8lab-panel" aria-label="Cross-domain concept comparison">
    <PanelHead title="Compare concepts without collapsing dimensions" description="Two independent candidate records; no synthetic overall ranking or similarity-as-dependency."/>
    <SelectLine label="Comparison record" value={other.id}
      options={inventory.concepts.map(c=>c.id)} onChange={setOtherId}/>
    <div className="v8lab-two">{cols.map(c=><article key={c.id}><small>{c.domain}</small>
      <h3>{c.id} · {c.title}</h3>
      <dl><dt>Discovery tag</dt><dd>{c.discovery_class} (Phase 1 only)</dd>
      <dt>Function</dt><dd>{c.role}</dd>
      <dt>Principal unresolved gap</dt><dd>{c.main_gap}</dd>
      <dt>Next investigation</dt><dd>{c.next_investigation}</dd>
      <dt>Catalog sources</dt><dd>{c.source_refs.length} linked source record(s), not independently assessed evidence</dd></dl>
      <button className="v8lab-outline" onClick={()=>onSelect(c.id)}>Inspect {c.id}</button>
    </article>)}</div>
  </section>;
}

/** Registered graph snapshot view. The empty baseline renders NO scientific dependency claims. */
export function RegisteredGraphPanel({conceptId}:{conceptId:string}){
  const graphs=registeredStructures(conceptId);
  return <section className="v8lab-panel" aria-label="Registered V3 structural snapshot">
    <PanelHead title="V3 registered structural networks" description={"Registry "+scienceRegistry.snapshot_id+" · scope-specific predicate and gate records only"}/>
    {graphs.length===0 ? <div className="v8lab-empty">No receipt-backed Structural Predicate snapshot registered for {conceptId}. The separate interactive gate sandbox below is a mathematical demonstration, not a model of this candidate.</div> :
      graphs.map(graph=><article className="v8lab-list" key={graph.graph_id}>
        <h3>{graph.graph_id}</h3>
        <p>Scope: {graph.scope} · Closure: {graph.closure_status} · Source: {graph.source_snapshot_ref}</p>
        <div className="v8lab-two">{graph.gates.map(g=><article key={g.gate_id}>
          <small>{g.gate_id} · {g.operator}{g.operator==="K_OF_N"?" ("+g.k+" of "+g.input_predicate_ids.length+")":""}</small>
          <p>Inputs: {g.input_predicate_ids.join(", ")}</p>
          <p>Scenario result: <strong>{gateState(graph,g)}</strong></p>
        </article>)}</div>
        <div className="v8lab-list">{graph.predicates.map(p=><article key={p.predicate_id}><strong>{p.predicate_id} · {p.label}</strong><small>Knowledge state: {p.knowledge_status}</small></article>)}</div>
      </article>)}
    <Info>Graph results are scoped to their source snapshot and declared closure. A TRUE gate does not establish global technological feasibility, and a FALSE gate does not prove physical impossibility outside the modeled architecture.</Info>
  </section>;
}
