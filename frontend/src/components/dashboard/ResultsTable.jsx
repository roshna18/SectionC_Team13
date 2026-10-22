import React from "react";
import { formatConfidence, getStatusBadge } from "../../utils/formatting";

export function ResultsTable({ results }) {
  if (!results || results.length === 0) {
    return (
      <div className="empty-results-box">
        <p className="muted-text">No parking space detections to list.</p>
      </div>
    );
  }

  return (
    <div className="table-responsive-container">
      <table className="results-table" aria-label="Individual space predictions">
        <thead>
          <tr>
            <th scope="col">Space</th>
            <th scope="col">Status</th>
            <th scope="col">Confidence</th>
            <th scope="col">Bounding Box [x1, y1, x2, y2]</th>
          </tr>
        </thead>
        <tbody>
          {results.map((item) => {
            const badge = getStatusBadge(item.status);
            return (
              <tr key={item.id}>
                <td className="font-mono">{item.id}</td>
                <td>
                  <span className={`status-tag ${badge.colorClass}`}>
                    <span className="dot" />
                    {badge.label}
                  </span>
                </td>
                <td className="font-mono">{formatConfidence(item.confidence)}</td>
                <td className="font-mono text-muted text-xs">
                  {item.box ? item.box.join(", ") : "—"}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
