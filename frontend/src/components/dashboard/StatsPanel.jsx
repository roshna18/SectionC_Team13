import React from "react";

export function StatsPanel({ result }) {
  if (!result) return null;

  const stats = [
    {
      label: "Total Spaces",
      value: result.total_spaces ?? 0,
      color: "#e2e8f0",
      description: "Detected parking bays",
    },
    {
      label: "Vacant",
      value: result.vacant ?? 0,
      color: "#4ade80",
      description: "Available spots",
    },
    {
      label: "Occupied",
      value: result.occupied ?? 0,
      color: "#fb7185",
      description: "Vehicles parked",
    },
    {
      label: "Occupancy",
      value: `${result.occupancy_percent ?? 0}%`,
      color: "#38bdf8",
      description: "Current lot capacity",
    },
  ];

  return (
    <section className="stats-grid" aria-label="Occupancy summary statistics">
      {stats.map((stat) => (
        <div key={stat.label} className="stat-card">
          <span className="stat-label">{stat.label}</span>
          <strong className="stat-value" style={{ color: stat.color }}>
            {stat.value}
          </strong>
          <span className="stat-sub">{stat.description}</span>
        </div>
      ))}
    </section>
  );
}
