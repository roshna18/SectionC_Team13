import React, { useRef } from "react";
import { Upload, Image as ImageIcon, RotateCcw } from "lucide-react";
import { formatFileSize } from "../../utils/formatting";

const MAX_SIZE_MB = 15;
const MAX_BYTES = MAX_SIZE_MB * 1024 * 1024;
const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

export function FileUpload({
  file,
  preview,
  loading,
  hasResult,
  onFileSelect,
  onAnalyze,
  onReset,
  onError,
}) {
  const fileInputRef = useRef(null);

  function handleInputChange(event) {
    const selected = event.target.files?.[0];
    if (!selected) return;

    if (!ALLOWED_TYPES.includes(selected.type)) {
      onError("Please select a valid JPG, PNG, or WEBP image.");
      if (fileInputRef.current) fileInputRef.current.value = "";
      return;
    }

    if (selected.size > MAX_BYTES) {
      onError(`Please select an image smaller than ${MAX_SIZE_MB} MB.`);
      if (fileInputRef.current) fileInputRef.current.value = "";
      return;
    }

    onFileSelect(selected);
  }

  return (
    <section className="upload-section" aria-label="Upload parking lot image">
      <div className="section-intro">
        <h2>Analyze a parking image</h2>
        <p className="section-desc">
          Upload a clear image showing parking bays. The AI automatically identifies spaces and
          calculates occupancy without manual marking.
        </p>
      </div>

      <div
        className="dropzone-card"
        onClick={() => fileInputRef.current?.click()}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            fileInputRef.current?.click();
          }
        }}
        tabIndex={0}
        role="button"
        aria-label="Click or press enter to upload parking lot image"
      >
        <input
          ref={fileInputRef}
          type="file"
          id="parking-file-input"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleInputChange}
          style={{ display: "none" }}
          aria-label="Upload parking lot image"
        />

        <div className="dropzone-content">
          <div className="dropzone-icon">
            <Upload size={24} />
          </div>
          <div>
            <strong>Click to upload</strong> or drag and drop image here
            <div className="file-hints">JPG, PNG, WEBP up to 15 MB</div>
          </div>
        </div>
      </div>

      {preview && !hasResult && (
        <div className="preview-container">
          <div className="preview-header">
            <span className="preview-name">
              <ImageIcon size={16} /> {file?.name} ({formatFileSize(file?.size || 0)})
            </span>
          </div>
          <img src={preview} alt="Selected parking lot preview" className="preview-image" />
        </div>
      )}

      <div className="actions-toolbar">
        <button
          type="button"
          onClick={onAnalyze}
          disabled={!file || loading}
          className="btn-primary"
        >
          {loading ? "Analyzing image..." : "Detect Empty Spaces"}
        </button>

        <button
          type="button"
          onClick={() => {
            if (fileInputRef.current) fileInputRef.current.value = "";
            onReset();
          }}
          disabled={loading || (!file && !hasResult)}
          className="btn-secondary"
        >
          <RotateCcw size={15} /> Start over
        </button>
      </div>
    </section>
  );
}
