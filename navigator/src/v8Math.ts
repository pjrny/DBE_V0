/** V8 transparent educational mathematics. No output is a scientific assessment. */
export type ScenarioTruth = "TRUE" | "FALSE" | "UNKNOWN";
export type KnowledgeTruth = "NEITHER" | "TRUE_ONLY" | "FALSE_ONLY" | "BOTH";
export type Gate = "ALL" | "ANY" | "K_OF_N";
export const KNOWLEDGE_STATES:KnowledgeTruth[]=["NEITHER","TRUE_ONLY","FALSE_ONLY","BOTH"];
export const SCENARIO_STATES:ScenarioTruth[]=["UNKNOWN","TRUE","FALSE"];

export function knowledgeToScenario(knowledge:KnowledgeTruth):ScenarioTruth {
  if(knowledge==="TRUE_ONLY")return "TRUE";
  if(knowledge==="FALSE_ONLY")return "FALSE";
  // Neither observed evidence nor contradictory evidence implies a known scenario state.
  return "UNKNOWN";
}
export function evaluateGate(gate:Gate, states:readonly ScenarioTruth[], k:number):ScenarioTruth {
  if(states.length===0)return "UNKNOWN";
  const required=gate==="ALL"?states.length:gate==="ANY"?1:k;
  if(!Number.isInteger(required)||required<1||required>states.length)throw Error("Invalid k-of-n threshold");
  const trueCount=states.filter(s=>s==="TRUE").length;
  const possibleCount=states.filter(s=>s!=="FALSE").length;
  if(trueCount>=required)return "TRUE";
  if(possibleCount<required)return "FALSE";
  return "UNKNOWN";
}
function combinations(indices:number[], k:number):number[][] {
  if(k===0)return [[]];
  if(k>indices.length)return [];
  if(indices.length===0)return [];
  return [...combinations(indices.slice(1),k-1).map(x=>[indices[0],...x]),...combinations(indices.slice(1),k)];
}
export function minimalGateSets(gate:Gate, n:number, k:number):{paths:number[][];cuts:number[][];required:number}{
  if(!Number.isInteger(n)||n<1||n>10)throw Error("Gate input count must be 1–10");
  const required=gate==="ALL"?n:gate==="ANY"?1:k;
  if(!Number.isInteger(required)||required<1||required>n)throw Error("Invalid gate threshold");
  const indices=Array.from({length:n},(_,i)=>i);
  return {paths:combinations(indices,required),cuts:combinations(indices,n-required+1),required};
}
export type ToyStep={k:number;x:number;baseline:number;impulse:number};
export type ToyParameters={retention:number;control:number;disturbance:number;steps:number};
export function toyTrajectory({retention,control,disturbance,steps}:ToyParameters):ToyStep[]{
  if(![retention,control,disturbance].every(x=>Number.isFinite(x)&&x>=0&&x<=1))throw Error("Toy parameters must be in [0,1]");
  if(!Number.isInteger(steps)||steps<1||steps>40)throw Error("Invalid toy horizon");
  let x=0,baseline=0,impulse=1;
  const result:ToyStep[]=[{k:0,x,baseline,impulse}];
  for(let k=1;k<=steps;k++){
    x=retention*x+control-disturbance;
    baseline=retention*baseline-disturbance;
    impulse=retention*impulse;
    result.push({k,x,baseline,impulse});
  }
  return result;
}
export function toyModelSummary(p:ToyParameters){
  const stable=Math.abs(p.retention)<1;
  const equilibrium=stable?(p.control-p.disturbance)/(1-p.retention):null;
  return {operator:"x(k+1)=a x(k)+u−d",localEigenvalue:p.retention,stable,equilibrium,
    authority:"SYNTHETIC_UNIT_FREE_EXAMPLE" as const};
}
/** Purely visual projection. Z encodes *object kind* (domain 0, concept 75, reviewed case 150). */
export function projectTaxonomyPoint(x:number,y:number,z:number,yaw:number,pitch:number){
  const a=yaw*Math.PI/180,b=pitch*Math.PI/180;
  const dx=x-600,dy=y-375;
  const rotatedX=dx*Math.cos(a)-dy*Math.sin(a);
  const rotatedY=dx*Math.sin(a)+dy*Math.cos(a);
  return {x:600+rotatedX,y:410+rotatedY*Math.sin(b)-z*Math.cos(b)};
}
