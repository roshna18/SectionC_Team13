import { useState, useCallback, useRef, useEffect } from "react";
import { analyzeParkingImage, ApiError } from "../services/api";

export function useAnalysis() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const abortControllerRef = useRef(null);

  // Maintain local object URL for instant preview
  useEffect(() => {
    if (!file) {
      setPreview("");
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreview(objectUrl);

    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [file]);

  // Clean up any ongoing fetch on unmount
  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  const handleFileSelect = useCallback((selectedFile) => {
    setFile(selectedFile);
    setResult(null);
    setError("");
  }, []);

  const clearError = useCallback(() => {
    setError("");
  }, []);

  const reset = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setFile(null);
    setResult(null);
    setError("");
    setLoading(false);
  }, []);

  const runAnalysis = useCallback(async () => {
    if (!file) {
      setError("Please choose a parking-lot image first.");
      return;
    }

    // Cancel prior request if still pending
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    const controller = new AbortController();
    abortControllerRef.current = controller;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeParkingImage(file, controller.signal);
      setResult(data);
    } catch (err) {
      if (err.name === "AbortError") {
        return; // Request was cleanly cancelled
      }
      setError(err.message || "Could not analyze the image.");
    } finally {
      setLoading(false);
    }
  }, [file]);

  return {
    file,
    preview,
    result,
    loading,
    error,
    handleFileSelect,
    runAnalysis,
    reset,
    clearError,
    setError,
  };
}
