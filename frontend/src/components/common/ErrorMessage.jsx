import React from "react";
import { AlertCircle } from "lucide-react";

export function ErrorMessage({ message, onDismiss }) {
  if (!message) return null;

  return (
    <div
      role="alert"
      className="error-banner"
      style={{
        display: "flex",
        alignItems: "flex-start",
        gap: 12,
        marginTop: 18,
        padding: 14,
        borderRadius: 10,
        background: "#451a24",
        border: "1px solid #f43f5e55",
        color: "#fecdd3",
        fontSize: 14,
        lineHeight: 1.5,
        overflowWrap: "anywhere",
      }}
    >
      <AlertCircle size={18} style={{ flexShrink: 0, marginTop: 2, color: "#fb7185" }} />
      <div style={{ flex: 1 }}>{message}</div>
      {onDismiss && (
        <button
          type="button"
          onClick={onDismiss}
          aria-label="Dismiss error"
          style={{
            background: "transparent",
            border: 0,
            color: "#fecdd3",
            cursor: "pointer",
            fontSize: 16,
            padding: "0 4px",
          }}
        >
          ×
        </button>
      )}
    </div>
  );
}
