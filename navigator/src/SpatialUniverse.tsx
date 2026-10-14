import { useMemo, useState, type KeyboardEvent } from "react";
import { inventory, runtime } from "./data";
import { DOMAIN_PALETTE, knowledgeGeometry } from "./knowledgeUniverse";
import { projectTaxonomyPoint } from "./v8Math";
import type { Concept } from "./types";

/** Categorical 3D view: height encodes object type ONLY. No measured scientific dimensions. */
export function SpatialUniverse({concepts,selected,onSelect}:{concepts:Concept[];selected:Concept;onSelect:(id:string)=>void}){
  const [yaw,setYaw]=useState(-25),[pitch,setPitch]=useState(50);
  const geometry=useMemo(()=>knowledgeGeometry(inventory.concepts),[]);
  const visible=new Set(concepts.map(c=>c.id));
  const known=new Set(runtime.reviewed_claims.map(c=>c.id));
  const reviewed=runtime.relationships.filter(r=>r.review_status==="REVIEWED" && known.has(r.source_id));
  const conceptPosition=new Map(geometry.concepts.map(p=>[p.id,p]));
  const domainPosition=new Map(geometry.domains.map(d=>[d.id,d]));
  const transformed=(x:number,y:number,z:number)=>projectTaxonomyPoint(x,y,z,yaw,pitch);
  const pointById=new Map(inventory.concepts.map(c=>[c.id,c]));
  const activate=(e:KeyboardEvent<SVGGElement>,id:string)=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();onSelect(id);}};
  return <section className="v8lab-panel v8space" aria-label="Optional three-dimensional taxonomy projection">
    <div className="v8lab-head"><strong>Spatial taxonomy · 3D projection</strong>
      <small>Rotate object-kind layers: domains (ground), concepts (middle), reviewed case records (top). No axis measures physical space, confidence or scientific dimensions.</small></div>
    <div className="v8lab-sliders v8space-controls">
      <label><span>Rotation: <b>{yaw}°</b></span><input aria-label="Spatial rotation" type="range" min={-180} max={180} step={5} value={yaw} onChange={e=>setYaw(Number(e.target.value))}/></label>
      <label><span>Elevation: <b>{pitch}°</b></span><input aria-label="Spatial elevation" type="range" min={15} max={75} step={5} value={pitch} onChange={e=>setPitch(Number(e.target.value))}/></label>
      <button className="v8lab-outline" onClick={()=>{setYaw(-25);setPitch(50);}}>Reset view</button>
    </div>
    <div className="v8space-frame">
      <svg role="group" aria-label="Interactive 3D projection of taxonomy, domain membership, and reviewed case associations" viewBox="0 0 1200 780" className="v8-map">
        <defs><pattern id="v8space-grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#e4edf3"/></pattern></defs>
        <rect x="0" y="0" width="1200" height="780" fill="url(#v8space-grid)"/>
        {geometry.domains.map(d=>{
          const p=transformed(d.x,d.y,0);
          return <g key={"domain-rule-"+d.id}>
            <line x1={600} y1={410} x2={p.x} y2={p.y} stroke={DOMAIN_PALETTE[d.id]} strokeOpacity=".45" strokeWidth="2.5"/>
            <circle cx={p.x} cy={p.y} r={26} fill="#fff" stroke={DOMAIN_PALETTE[d.id]} strokeWidth="3"/>
            <text x={p.x} y={p.y+5} textAnchor="middle" fill="#17314c" fontSize="16" fontWeight="800">{d.id}</text>
          </g>;
        })}
        {geometry.concepts.map(c=>{
          const p=transformed(c.x,c.y,75),d=domainPosition.get(c.domain);
          if(!d)return null;
          const dp=transformed(d.x,d.y,0);
          const present=visible.has(c.id);
          return <line key={"membership-"+c.id} x1={dp.x} y1={dp.y} x2={p.x} y2={p.y}
            stroke={DOMAIN_PALETTE[c.domain]} strokeOpacity={present?.22:.045} strokeWidth=".9"/>;
        })}
        {reviewed.map((rel,i)=>{
          const target=conceptPosition.get(rel.target_id);
          if(!target)return null;
          const p=transformed(target.x,target.y,75);
          const q=transformed(target.x+25+8*(i%3),target.y-10+9*(i%2),155);
          return <g key={rel.id} aria-label={rel.source_id+" reviewed evidence relation to "+rel.target_id}>
            <line x1={p.x} y1={p.y} x2={q.x} y2={q.y} stroke="#59778d" strokeWidth="1.6" strokeDasharray="5 4" strokeOpacity={visible.has(rel.target_id)?1:.2}/>
            <rect x={q.x-16} y={q.y-8} width={32} height={16} rx={3} stroke="#607c91" strokeWidth="1.4" fill="#fff"/>
            <title>{rel.source_id+": "+rel.relation_type+" → "+rel.target_id+". Reviewed case, not structural dependency."}</title>
          </g>;
        })}
        {geometry.concepts.map(c=>{
          const point=pointById.get(c.id);if(!point)return null;
          const p=transformed(c.x,c.y,75);
          const active=visible.has(c.id),selectedFlag=c.id===selected.id;
          return <g key={c.id} tabIndex={0} role="button" aria-label={c.id+": "+point.title+"; select record"}
            onClick={()=>onSelect(c.id)} onKeyDown={e=>activate(e,c.id)} className="v8-point" opacity={active?1:.2}>
            <circle cx={p.x} cy={p.y} r={selectedFlag?10:5.5} fill={DOMAIN_PALETTE[c.domain]} stroke={selectedFlag?"#132c46":"#fff"} strokeWidth={selectedFlag?3:1}/>
            {selectedFlag&&<circle cx={p.x} cy={p.y} r={17} stroke="#122f50" fill="none" strokeWidth="1.5"/>}
            <title>{c.id} · {point.title}</title>
          </g>;
        })}
      </svg>
      <div className="v8lab-legend"><span><i style={{background:"#637bc5"}}/>Domain floor</span><span><i style={{background:"#ad83b9"}}/>Concept layer</span><span><i style={{background:"#607c91"}}/>Reviewed claim-case layer</span></div>
    </div>
    <p className="v8lab-note">{geometry.domains.length} domains · {geometry.concepts.length} concepts · {reviewed.length} reviewed evidence associations. Layout depth encodes object kind; neither Euclidean distance nor apparent height indicates physical dimension, validation, evidence confidence or hierarchy of importance. Every source record is also available in the accessible 2D and list interfaces.</p>
  </section>;
}
