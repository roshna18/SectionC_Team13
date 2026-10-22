import React from "react";
import { Car, Sparkles } from "lucide-react";
import { useAnalysis } from "./hooks/useAnalysis";
import { FileUpload } from "./components/upload/FileUpload";
import { AnalysisResults } from "./components/analysis/AnalysisResults";
import { LoadingState } from "./components/common/LoadingState";
import { ErrorMessage } from "./components/common/ErrorMessage";

export default function App() {
  const {
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
  } = useAnalysis();

  return (
    <div className="app-shell">
      {/* Header / Brand Topbar */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">
            <Car size={22} />
          </div>
          <span>
            SmartPark <b>AI</b>
          </span>
        </div>

        <div className="status-pill">
          <span className="live-dot" />
          <span>Real-time Occupancy Model</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="content-container">
        {/* Hero Banner */}
        <section className="hero-section">
          <div className="badge-chip">
            <Sparkles size={13} />
            <span>COMPUTER VISION · SMART PARKING</span>
          </div>
          <h1 className="hero-title">
            Intelligent Parking Lot <span>Occupancy Detection</span>
          </h1>
          <p className="hero-subtitle">
            Upload aerial or surveillance parking footage. Pre-trained deep learning models detect
            vacant bays, track occupancy rate, and stream structured analytics instantly.
          </p>
        </section>

        {/* Upload & Control Card */}
        <div className="main-card">
          <FileUpload
            file={file}
            preview={preview}
            loading={loading}
            hasResult={Boolean(result)}
            onFileSelect={handleFileSelect}
            onAnalyze={runAnalysis}
            onReset={reset}
            onError={setError}
          />

          {loading && <LoadingState />}
          {error && <ErrorMessage message={error} onDismiss={clearError} />}
        </div>

        {/* Analysis Results */}
        {result && <AnalysisResults result={result} />}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div>SmartPark AI · Modular Architecture Prototype</div>
        <div className="footer-links">
          <span>FastAPI</span>
          <span>•</span>
          <span>YOLOv8</span>
          <span>•</span>
          <span>React 19</span>
          <span>•</span>
          <span>Vite</span>
        </div>
      </footer>
    </div>
  );
}
