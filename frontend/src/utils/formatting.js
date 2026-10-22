/**
 * Pure data transformation and formatting utilities.
 */

/**
 * Format bytes to readable string (e.g. 1.2 MB).
 * @param {number} bytes
 * @returns {string}
 */
export function formatFileSize(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

/**
 * Format confidence percentage.
 * @param {number} confidence (0.0 to 1.0)
 * @returns {string}
 */
export function formatConfidence(confidence) {
  if (typeof confidence !== "number" || isNaN(confidence)) return "—";
  return `${(confidence * 100).toFixed(1)}%`;
}

/**
 * Get human-readable status badge styling and text.
 * @param {string} status ('vacant', 'occupied', 'unknown')
 * @returns {{ label: string, colorClass: string }}
 */
export function getStatusBadge(status) {
  const norm = (status || "").toLowerCase();
  if (norm === "vacant") {
    return { label: "Vacant", colorClass: "text-green" };
  }
  if (norm === "occupied") {
    return { label: "Occupied", colorClass: "text-red" };
  }
  return { label: "Unclassified", colorClass: "text-muted" };
}
