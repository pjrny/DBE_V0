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
});
