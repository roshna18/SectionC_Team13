import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { StatsPanel } from "./StatsPanel";

describe("StatsPanel component", () => {
  it("renders nothing when result is null", () => {
    const { container } = render(<StatsPanel result={null} />);
    expect(container.firstChild).toBeNull();
  });

  it("renders stats cards with correct values", () => {
    const mockResult = {
      total_spaces: 24,
      vacant: 6,
      occupied: 18,
      occupancy_percent: 75.0,
    };

    render(<StatsPanel result={mockResult} />);

    expect(screen.getByText("Total Spaces")).toBeInTheDocument();
    expect(screen.getByText("24")).toBeInTheDocument();
    expect(screen.getByText("Vacant")).toBeInTheDocument();
    expect(screen.getByText("6")).toBeInTheDocument();
    expect(screen.getByText("Occupied")).toBeInTheDocument();
    expect(screen.getByText("18")).toBeInTheDocument();
    expect(screen.getByText("75%")).toBeInTheDocument();
  });
});
