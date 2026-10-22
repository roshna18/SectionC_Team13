/**
 * Centralized API client service for SmartParkAI backend.
 */

const API_BASE = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

export class ApiError extends Error {
  constructor(message, status, detail = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

/**
 * Upload and analyze parking lot image.
 *
 * @param {File} file - Image file to analyze
 * @param {AbortSignal} [signal] - Optional abort signal
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzeParkingImage(file, signal) {
  if (!file) {
    throw new Error("No image file provided.");
  }

  const formData = new FormData();
  formData.append("file", file);

  let response;
  try {
    response = await fetch(`${API_BASE}/api/analyze`, {
      method: "POST",
      body: formData,
      signal,
    });
  } catch (err) {
    if (err.name === "AbortError") {
      throw err;
    }
    throw new ApiError(
      "Cannot connect to the backend server. Ensure the backend is running at " + API_BASE,
      0
    );
  }

  let data = {};
  try {
    data = await response.json();
  } catch {
    // Response was not JSON
  }

  if (!response.ok) {
    const detail = data?.detail || `Analysis failed with HTTP status ${response.status}.`;
    throw new ApiError(detail, response.status, data);
  }

  return data;
}

/**
 * Check backend health status.
 *
 * @returns {Promise<{status: string, model_loaded: boolean}>}
 */
export async function checkBackendHealth() {
  try {
    const response = await fetch(`${API_BASE}/api/health`);
    if (!response.ok) return { status: "unhealthy", model_loaded: false };
    return await response.json();
  } catch {
    return { status: "offline", model_loaded: false };
  }
}
