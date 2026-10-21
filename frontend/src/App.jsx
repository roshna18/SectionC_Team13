
import { useEffect, useState } from "react";

const API = "http://127.0.0.1:8000";

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0b1120",
    color: "#f1f5f9",
    padding: "32px 18px",
    fontFamily: "Inter, Segoe UI, Arial, sans-serif",
  },
  container: {
    maxWidth: 1050,
    margin: "0 auto",
  },
  card: {
    background: "#131d30",
    border: "1px solid #29364d",
    borderRadius: 16,
    padding: 22,
    marginBottom: 20,
  },
  button: {
    background: "#38bdf8",
    color: "#082f49",
    border: 0,
    borderRadius: 9,
    padding: "12px 18px",
    fontWeight: 700,
    fontSize: 15,
    cursor: "pointer",
  },
  image: {
    display: "block",
    width: "100%",
    maxHeight: 650,
    objectFit: "contain",
    background: "#080d17",
    borderRadius: 10,
  },
  muted: {
    color: "#a5b4cc",
    lineHeight: 1.6,
  },
};

export default function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!file) {
      setPreview("");
      return;
    }

    const url = URL.createObjectURL(file);
    setPreview(url);

    return () => URL.revokeObjectURL(url);
  }, [file]);

  function handleFileChange(event) {
    const selected = event.target.files?.[0];

    if (!selected) return;

    setResult(null);
    setError("");

    if (!selected.type.startsWith("image/")) {
      setFile(null);
      setError("Please select an image file.");
      return;
    }

    if (selected.size > 15 * 1024 * 1024) {
      setFile(null);
      setError("Please select an image smaller than 15 MB.");
      return;
    }

    setFile(selected);
  }

  async function analyzeImage() {
    if (!file) {
      setError("Please choose a parking-lot image first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API}/api/analyze`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail || `Analysis failed (${response.status}).`
        );
      }

      setResult(data);
    } catch (err) {
      if (
        err instanceof TypeError &&
        /fetch/i.test(err.message)
      ) {
        setError(
          "Cannot connect to the backend. In VS Code, start " +
          "the backend terminal and keep it running at " +
          "http://127.0.0.1:8000."
        );
      } else {
        setError(err.message || "Could not analyze the image.");
      }
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setFile(null);
    setResult(null);
    setError("");
  }

  const stats = [
    {
      label: "Detected spaces",
      value: result?.total_spaces ?? "—",
      color: "#e2e8f0",
    },
    {
      label: "Vacant",
      value: result?.vacant ?? "—",
      color: "#4ade80",
    },
    {
      label: "Occupied",
      value: result?.occupied ?? "—",
      color: "#fb7185",
    },
    {
      label: "Unclassified",
      value: result?.unknown ?? "—",
      color: "#cbd5e1",
    },
  ];

  return (
    <main style={styles.page}>
      <div style={styles.container}>
        <header style={{ marginBottom: 28 }}>
          <div
            style={{
              color: "#38bdf8",
              fontWeight: 800,
              letterSpacing: 2,
              fontSize: 12,
              marginBottom: 10,
            }}
          >
            COMPUTER VISION · SMART PARKING
          </div>

          <h1 style={{ fontSize: 36, margin: "0 0 12px" }}>
            SmartPark AI
          </h1>

          <p style={styles.muted}>
            Upload a parking-lot image. The AI will detect
            parking spaces and classify them as vacant or occupied.
          </p>
        </header>

        <section style={styles.card}>
          <h2 style={{ marginTop: 0 }}>Analyze a parking image</h2>

          <p style={styles.muted}>
            Select a clear image showing parking bays. No manual
            space marking is required for this model.
          </p>

          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            onChange={handleFileChange}
            style={{
              display: "block",
              width: "100%",
              margin: "18px 0",
              color: "#e2e8f0",
            }}
          />

          {preview && !result && (
            <div style={{ marginBottom: 18 }}>
              <p style={{ color: "#cbd5e1" }}>
                Selected image: {file?.name}
              </p>
              <img
                src={preview}
                alt="Selected parking lot"
                style={styles.image}
              />
            </div>
          )}

          <div
            style={{
              display: "flex",
              gap: 12,
              flexWrap: "wrap",
            }}
          >
            <button
              onClick={analyzeImage}
              disabled={!file || loading}
              style={{
                ...styles.button,
                opacity: !file || loading ? 0.55 : 1,
                cursor: !file || loading ? "not-allowed" : "pointer",
              }}
            >
              {loading ? "Analyzing image..." : "Detect Empty Spaces"}
            </button>

            <button
              onClick={reset}
              disabled={loading}
              style={{
                ...styles.button,
                background: "#26344a",
                color: "#e2e8f0",
              }}
            >
              Start over
            </button>
          </div>

          {loading && (
            <p style={styles.muted}>
              The first analysis downloads the model weights if
              needed. This can take several minutes.
            </p>
          )}

          {error && (
            <div
              role="alert"
              style={{
                marginTop: 18,
                padding: 14,
                borderRadius: 10,
                background: "#451a24",
                color: "#fecdd3",
                overflowWrap: "anywhere",
              }}
            >
              {error}
            </div>
          )}
        </section>

        {result && (
          <>
            <section
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
                gap: 14,
                marginBottom: 20,
              }}
            >
              {stats.map((stat) => (
                <div
                  key={stat.label}
                  style={{
                    ...styles.card,
                    marginBottom: 0,
                  }}
                >
                  <div style={{ ...styles.muted, fontSize: 13 }}>
                    {stat.label}
                  </div>
                  <div
                    style={{
                      fontSize: 32,
                      fontWeight: 800,
                      marginTop: 8,
                      color: stat.color,
                    }}
                  >
                    {stat.value}
                  </div>
                </div>
              ))}
            </section>

            <section style={styles.card}>
              <h2 style={{ marginTop: 0 }}>Detection results</h2>

              {result.annotated_image ? (
                <img
                  src={result.annotated_image}
                  alt="Parking spaces detected by SmartPark AI"
                  style={styles.image}
                />
              ) : (
                <p style={styles.muted}>
                  No annotated image was returned.
                </p>
              )}

              <div
                style={{
                  display: "flex",
                  gap: 18,
                  flexWrap: "wrap",
                  marginTop: 18,
                }}
              >
                <span style={{ color: "#4ade80" }}>
                  Green = vacant
                </span>
                <span style={{ color: "#fb7185" }}>
                  Red = occupied
                </span>
                <span style={{ color: "#cbd5e1" }}>
                  Grey = unclassified
                </span>
              </div>

              <p style={styles.muted}>
                Estimated occupancy: {result.occupancy_percent ?? 0}%
              </p>

              <p style={styles.muted}>{result.note}</p>

              {result.total_spaces === 0 && (
                <p style={{ color: "#fbbf24" }}>
                  No spaces were detected. Try a clearer, elevated
                  view of the parking lot.
                </p>
              )}
            </section>

            <section style={styles.card}>
              <h2 style={{ marginTop: 0 }}>Individual predictions</h2>

              {result.results?.length ? (
                <div style={{ overflowX: "auto" }}>
                  <table
                    style={{
                      width: "100%",
                      borderCollapse: "collapse",
                      textAlign: "left",
                    }}
                  >
                    <thead>
                      <tr>
                        {["Space", "Classification", "Confidence"].map(
                          (heading) => (
                            <th
                              key={heading}
                              style={{
                                padding: 12,
                                borderBottom: "1px solid #29364d",
                              }}
                            >
                              {heading}
                            </th>
                          )
                        )}
                      </tr>
                    </thead>
                    <tbody>
                      {result.results.map((item) => (
                        <tr key={item.id}>
                          <td style={{ padding: 12 }}>{item.id}</td>
                          <td
                            style={{
                              padding: 12,
                              color:
                                item.status === "vacant"
                                  ? "#4ade80"
                                  : item.status === "occupied"
                                  ? "#fb7185"
                                  : "#cbd5e1",
                            }}
                          >
                            {item.status}
                          </td>
                          <td style={{ padding: 12 }}>
                            {(item.confidence * 100).toFixed(1)}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <p style={styles.muted}>
                  No parking-space detections to list.
                </p>
              )}
            </section>
          </>
        )}

        <footer style={{ ...styles.muted, fontSize: 12 }}>
          SmartPark AI · Prototype · Predictions may be inaccurate
          under unusual viewpoints, poor lighting, or occlusion.
        </footer>
      </div>
    </main>
  );
}
