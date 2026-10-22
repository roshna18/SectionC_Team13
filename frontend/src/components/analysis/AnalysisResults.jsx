import React from "react";
import { CheckCircle2, AlertTriangle } from "lucide-react";
import { StatsPanel } from "../dashboard/StatsPanel";
import { ResultsTable } from "../dashboard/ResultsTable";

export function AnalysisResults({ result }) {
  if (!result) return null;

  const isAvailable = result.spaces_available;

  return (
    <div className="results-wrapper">
      {/* Availability Banner */}
      <div
        className={`availability-banner ${isAvailable ? "available" : "full"}`}
        role="region"
        aria-label="Parking lot status banner"
      >
        <div className="banner-icon">
          {isAvailable ? <CheckCircle2 size={24} /> : <AlertTriangle size={24} />}
        </div>
        <div className="banner-text">
          <h3>
            {isAvailable
              ? `${result.vacant} ${result.vacant === 1 ? "Space" : "Spaces"} Available`
              : "Parking Lot Full"}
          </h3>
          <p>
            {isAvailable
              ? "Spots were detected and classified as vacant by the AI."
              : "No vacant spaces detected among classified spots."}
          </p>
        </div>
      </div>

      {/* KPI Cards */}
      <StatsPanel result={result} />

      {/* Visual Annotated Canvas Panel */}
      <section className="results-panel" aria-label="Visual detection overlay">
        <div className="panel-title-bar">
          <h2>Visual Detection Results</h2>
          <div className="legend-items">
            <span className="legend-item text-green">
              <span className="legend-dot bg-green" /> Vacant
            </span>
            <span className="legend-item text-red">
              <span className="legend-dot bg-red" /> Occupied
            </span>
            <span className="legend-item text-muted">
              <span className="legend-dot bg-grey" /> Unclassified
            </span>
          </div>
        </div>

        {result.annotated_image ? (
          <div className="annotated-image-wrapper">
            <img
              src={result.annotated_image}
              alt="Parking lot with detected spaces annotated by SmartPark AI"
              className="annotated-image"
            />
          </div>
        ) : (
          <p className="muted-text">No annotated image returned by model.</p>
        )}

        {result.note && <div className="note-box">{result.note}</div>}
      </section>

      {/* Individual Predictions Table */}
      <section className="results-panel" aria-label="Individual bay detections">
        <div className="panel-title-bar">
          <h2>Individual Predictions ({result.results?.length || 0})</h2>
        </div>
        <ResultsTable results={result.results} />
      </section>
    </div>
  );
}
