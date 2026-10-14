import { describe, expect, it } from "vitest";
import {evaluateGate,knowledgeToScenario,minimalGateSets,toyTrajectory,toyModelSummary,projectTaxonomyPoint} from "./v8Math";
describe("V8 structural truth and path/cut invariants",()=>{
 it("keeps conflicting and absent knowledge distinct from yes/no",()=>{
   expect(knowledgeToScenario("NEITHER")).toBe("UNKNOWN");
   expect(knowledgeToScenario("BOTH")).toBe("UNKNOWN");
   expect(knowledgeToScenario("TRUE_ONLY")).toBe("TRUE");
   expect(knowledgeToScenario("FALSE_ONLY")).toBe("FALSE");
 });
 it("evaluates ALL, ANY and k-of-n without forcing UNKNOWN to false",()=>{
   expect(evaluateGate("ALL",["TRUE","TRUE"],1)).toBe("TRUE");
   expect(evaluateGate("ALL",["TRUE","UNKNOWN"],1)).toBe("UNKNOWN");
   expect(evaluateGate("ALL",["TRUE","FALSE","UNKNOWN"],2)).toBe("FALSE");
   expect(evaluateGate("ANY",["FALSE","UNKNOWN"],1)).toBe("UNKNOWN");
   expect(evaluateGate("ANY",["FALSE","FALSE"],1)).toBe("FALSE");
   expect(evaluateGate("K_OF_N",["TRUE","TRUE","UNKNOWN","FALSE"],2)).toBe("TRUE");
   expect(evaluateGate("K_OF_N",["TRUE","UNKNOWN","FALSE","FALSE"],2)).toBe("UNKNOWN");
   expect(evaluateGate("K_OF_N",["UNKNOWN","FALSE","FALSE","FALSE"],2)).toBe("FALSE");
   expect(()=>evaluateGate("K_OF_N",["TRUE","FALSE"],3)).toThrow();
   expect(evaluateGate("ALL",[],1)).toBe("UNKNOWN");
 });
 it("returns exact model-relative minimal path/cut sets",()=>{
   expect(minimalGateSets("ALL",3,1)).toEqual({required:3,paths:[[0,1,2]],cuts:[[0],[1],[2]]});
   expect(minimalGateSets("ANY",3,2)).toEqual({required:1,paths:[[0],[1],[2]],cuts:[[0,1,2]]});
   const k=minimalGateSets("K_OF_N",4,2);
   expect(k.required).toBe(2);
   expect(k.paths).toHaveLength(6);
   expect(k.cuts).toHaveLength(4);
   expect(k.paths.every(p=>p.length===2)).toBe(true);
   expect(k.cuts.every(p=>p.length===3)).toBe(true);
   expect(()=>minimalGateSets("K_OF_N",2,0)).toThrow();
 });
});
describe("V8 bounded demonstration dynamics",()=>{
 it("uses correct ordered discrete-time recurrence and baseline",()=>{
   expect(toyTrajectory({retention:.5,control:.4,disturbance:.2,steps:2})).toEqual([
     {k:0,x:0,baseline:0,impulse:1},
     {k:1,x:.2,baseline:-.2,impulse:.5},
     {k:2,x:.3,baseline:-.30000000000000004,impulse:.25}
   ]);
 });
 it("never treats a=1 as a stable finite equilibrium",()=>{
   expect(toyModelSummary({retention:1,control:.5,disturbance:.1,steps:4}).equilibrium).toBeNull();
   expect(toyModelSummary({retention:.5,control:.5,disturbance:.1,steps:4}).equilibrium).toBeCloseTo(.8);
   expect(()=>toyTrajectory({retention:-.1,control:0,disturbance:0,steps:3})).toThrow();
 });
 it("produces deterministic object-kind 3D geometry, not confidence",()=>{
   const p=projectTaxonomyPoint(600,375,75,0,0);
   expect(p.x).toBe(600);expect(p.y).toBe(335);
   expect(projectTaxonomyPoint(600,375,75,0,0)).toEqual(p);
 });
});
