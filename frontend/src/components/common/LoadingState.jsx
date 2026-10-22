import React from "react";
import { Loader2 } from "lucide-react";

export function LoadingState({ message = "Analyzing parking lot image..." }) {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "28px 16px",
        gap: 12,
        color: "#a5b4cc",
        textAlign: "center",
      }}
    >
      <Loader2
        size={32}
        className="spin"
        style={{
          color: "#38bdf8",
          animation: "spin 1s linear infinite",
        }}
      />
      <div style={{ fontWeight: 600, color: "#e2e8f0", fontSize: 15 }}>{message}</div>
      <p style={{ margin: 0, fontSize: 13, color: "#8e9bb0", maxWidth: 440 }}>
        The first analysis downloads model weights from HuggingFace if not already cached.
      </p>
    </div>
  );
}
