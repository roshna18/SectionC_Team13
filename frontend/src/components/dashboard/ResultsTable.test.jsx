import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { ResultsTable } from "./ResultsTable";

describe("ResultsTable component", () => {
  it("renders empty fallback message when results array is empty", () => {
    render(<ResultsTable results={[]} />);
    expect(screen.getByText(/No parking space detections to list/i)).toBeInTheDocument();
  });

  it("renders table rows for each space prediction", () => {
    const mockResults = [
      { id: "P1", status: "vacant", confidence: 0.94, box: [10, 20, 100, 150] },
      { id: "P2", status: "occupied", confidence: 0.88, box: [110, 20, 200, 150] },
    ];

    render(<ResultsTable results={mockResults} />);

    expect(screen.getByText("P1")).toBeInTheDocument();
    expect(screen.getByText("Vacant")).toBeInTheDocument();
    expect(screen.getByText("94.0%")).toBeInTheDocument();
    expect(screen.getByText("P2")).toBeInTheDocument();
    expect(screen.getByText("Occupied")).toBeInTheDocument();
    expect(screen.getByText("88.0%")).toBeInTheDocument();
  });
});
