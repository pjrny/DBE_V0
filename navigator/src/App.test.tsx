import { fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import { App } from "./App";

describe("SDBES Research Navigator", () => {
  beforeEach(() => window.history.replaceState(null, "", "/"));

  it("preserves the staging boundary and disabled model gate", () => {
    render(<App />);
    expect(screen.getByText(/Discovery records are not scientific assessments/)).toBeInTheDocument();
    expect(screen.getByText("Discovery-only — not assessed")).toBeInTheDocument();
    expect(screen.getByText("No registered scientific model package available")).toBeInTheDocument();
    expect(screen.getByText(/405 papers · 291 reviews · 0 scientific promotions/)).toBeInTheDocument();
    fireEvent.click(screen.getByText("V7 Observatory scale run"));
    expect(screen.getByLabelText("Observatory review associations by program claim")).toHaveTextContent("E-QEC74");
  });

  it("filters the atlas without changing evidence status", () => {
    render(<App />);
    fireEvent.change(screen.getByPlaceholderText(/Search concepts/), { target: { value: "quantum energy teleportation" } });
    expect(screen.getByText("DBE-E04")).toBeInTheDocument();
    expect(screen.getByText(/Current filters may hide relevant challenging or null records/)).toBeInTheDocument();
  });

  it("shows only reviewed relationships and no topic-overlap graph", () => {
    render(<App />);
    fireEvent.click(screen.getByRole("tab", { name: "Relations" }));
    expect(screen.getAllByText(/N01/).length).toBeGreaterThan(0);
    expect(screen.queryByText(/topic overlap/i)).not.toBeInTheDocument();
  });

  it("opens the V8 global universe and preserves unassessed science", () => {
    render(<App />);
    expect(screen.getByText("Dimensions Beyond Energy Scarcity")).toBeInTheDocument();
    expect(screen.getByRole("navigation", { name: "Knowledge visualization lenses" })).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Evidence space" }));
    expect(screen.getByRole("table", { name: "Formal Empirical Applied evidence assessment matrix" })).toBeInTheDocument();
    expect(screen.getAllByText("UNKNOWN")).toHaveLength(9);
    fireEvent.click(screen.getByRole("button", { name: "Dynamics" }));
    expect(screen.getByRole("button", { name: /Run scenario/ })).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: "Evidence record table" }));
    expect(screen.getByText("Evidence Workbench")).toBeInTheDocument();
  });

  it("can switch to 3D taxonomy and return to the accessible 2D map", () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Explore 3D layers" }));
    expect(screen.getByLabelText("Optional three-dimensional taxonomy projection")).toBeInTheDocument();
    expect(screen.getByLabelText("Spatial rotation")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Switch to accessible 2D" }));
    expect(screen.getByLabelText("Interactive 2D map of six energy-scarcity research domains and their concept candidates")).toBeInTheDocument();
  });

  it("separates live logical sandbox from registered V3 science", () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Dependencies" }));
    expect(screen.getByLabelText("Registered V3 structural snapshot")).toBeInTheDocument();
    expect(screen.getByLabelText("V3 structural gate sandbox")).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("Predicate B knowledge status"), { target: {value:"TRUE_ONLY"} });
    expect(screen.getByText("V3 scenario state")).toBeInTheDocument();
  });

  it("renders the synthetic dynamic plot, but cannot run any unregistered physical model", () => {
    render(<App />);
    fireEvent.click(screen.getByRole("button", { name: "Dynamics" }));
    expect(screen.getByLabelText("V4 synthetic dynamics visualization")).toBeInTheDocument();
    expect(screen.getByRole("img", {name:/Unitless toy model time series/})).toBeInTheDocument();
    expect(screen.getByRole("button", {name:/Run scenario/})).toBeDisabled();
  });

});
