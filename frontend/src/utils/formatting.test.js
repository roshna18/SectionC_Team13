import { describe, it, expect } from "vitest";
import { formatFileSize, formatConfidence, getStatusBadge } from "./formatting";

describe("Formatting utilities", () => {
  it("formats file sizes accurately", () => {
    expect(formatFileSize(0)).toBe("0 B");
    expect(formatFileSize(1024)).toBe("1 KB");
    expect(formatFileSize(1024 * 1024 * 2.5)).toBe("2.5 MB");
  });

  it("formats confidence percentages", () => {
    expect(formatConfidence(0.954)).toBe("95.4%");
    expect(formatConfidence(0.5)).toBe("50.0%");
    expect(formatConfidence(null)).toBe("—");
  });

  it("returns proper status badge classes", () => {
    expect(getStatusBadge("vacant")).toEqual({ label: "Vacant", colorClass: "text-green" });
    expect(getStatusBadge("occupied")).toEqual({ label: "Occupied", colorClass: "text-red" });
    expect(getStatusBadge("other")).toEqual({ label: "Unclassified", colorClass: "text-muted" });
  });
});
