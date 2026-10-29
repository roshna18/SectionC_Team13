# SmartPark AI 🚗🅿️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg)](https://fastapi.tiangolo.com)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-8-646CFF.svg)](https://vitejs.dev)
[![Ultralytics](https://img.shields.io/badge/YOLOv8-Ultralytics-FF5722.svg)](https://docs.ultralytics.com)

**SmartPark AI** is an intelligent parking occupancy detection system powered by computer vision. It analyzes surveillance or aerial images of parking facilities, automatically identifies individual parking bays, classifies them as **vacant** or **occupied**, and delivers real-time occupancy analytics through an interactive dashboard.

---

## 🌟 Key Features

- **Automated AI Detection:** Uses a pre-trained YOLO model (`simahanyan/parking-lot-yolo26m`) fine-tuned specifically for parking spaces—no tedious manual spot marking needed.
- **Instant Occupancy Metrics:** Real-time calculation of total detected bays, vacant spots, occupied spots, and percentage utilization.
- **Visual Detection Overlay:** Bounding boxes color-coded in real-time (Green = Vacant, Red = Occupied, Grey = Unclassified) with model confidence scores.
- **Per-Bay Analytics Table:** Tabular inspection of individual bays with bounding coordinates and confidence ratings.
- **Atomic Space Persistence:** Safe, validated storage for manual or detected parking layouts preventing corrupted partial writes.
- **Production Architecture:** Layered, loosely-coupled modular architecture across both backend (FastAPI) and frontend (React 19 + Vite).
- **Security & Reliability:** Built-in rate limiting, strict Pydantic payload validation, configurable CORS origins, and structured error handling.

---

## 🏗️ Architecture & Directory Structure

```
SmartParkAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── router.py             # Central API router & health check
│   │   │   └── routes/
│   │   │       ├── analyze.py        # POST /api/analyze endpoint
│   │   │       └── spaces.py         # GET/POST /api/spaces & /api/lot/upload
│   │   ├── core/
│   │   │   ├── config.py             # Environment-based typed settings
│   │   │   ├── exceptions.py         # Application-specific domain exceptions
│   │   │   ├── logging.py            # Structured logging configuration
│   │   │   └── rate_limit.py         # In-memory sliding window rate limiter
│   │   ├── image_processing/
│   │   │   ├── annotations.py        # OpenCV box & status text rendering
│   │   │   └── encoder.py            # Image decoding, validation & base64 encoding
│   │   ├── ml/
│   │   │   ├── inference.py          # YOLO prediction orchestration
│   │   │   └── model_loader.py       # Thread-safe lazy model weights manager
│   │   ├── schemas/
│   │   │   ├── analyze.py            # Pydantic schemas for detection responses
│   │   │   └── spaces.py             # Pydantic schemas for space persistence
│   │   ├── services/
│   │   │   ├── analysis_service.py   # Full image analysis business workflow
│   │   │   └── spaces_service.py     # Space persistence & atomic file writes
│   │   └── main.py                   # FastAPI application factory & exception handlers
│   ├── tests/
│   │   ├── conftest.py               # Shared pytest fixtures & test client
│   │   ├── integration/              # API endpoint integration tests
│   │   └── unit/                     # Services, image processing & validation tests
│   ├── storage/                      # Local JSON persistence directory
│   ├── Dockerfile
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── .env.example
│   └── main.py                       # Top-level entry point (uvicorn main:app)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── analysis/
│   │   │   │   └── AnalysisResults.jsx # Visualization & results container
│   │   │   ├── common/
│   │   │   │   ├── ErrorMessage.jsx    # Accessible error alert
│   │   │   │   └── LoadingState.jsx    # Accessible spinner & status announcer
│   │   │   ├── dashboard/
│   │   │   │   ├── ResultsTable.jsx    # Individual bays predictions table
│   │   │   │   └── StatsPanel.jsx      # Summary KPI metrics cards
│   │   │   └── upload/
│   │   │       └── FileUpload.jsx      # Drag-and-drop file upload & preview
│   │   ├── hooks/
│   │   │   └── useAnalysis.js          # Encapsulated state & request lifecycle
│   │   ├── services/
│   │   │   └── api.js                  # Centralized HTTP client
│   │   ├── utils/
│   │   │   └── formatting.js           # Pure formatting & badge helpers
│   │   ├── App.jsx                     # Clean page composition
│   │   ├── main.jsx                    # React entry point
│   │   └── style.css                   # Refactored tokenized CSS design system
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### Prerequisites

- **Python:** 3.10 or higher
- **Node.js:** v18 or higher (v20+ recommended)
- **Git**

### 1. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy environment variables
cp .env.example .env

# Start FastAPI server
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The backend API will be available at `http://127.0.0.1:8000`.  
Interactive Swagger documentation is available at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

In a separate terminal tab:

```bash
cd frontend

# Install dependencies
npm install

# (Optional) Copy environment variables
cp .env.example .env

# Start Vite dev server
npm run dev
```

Open your browser at `http://localhost:5173`.

---

## 🐳 Docker Setup

Run both frontend and backend in isolated containers:

```bash
docker compose up --build
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`

---

## 🧪 Running Automated Tests

### Backend Tests (pytest)

```bash
cd backend
source .venv/bin/activate
pytest tests/ -v
```

Tests cover:
- Pydantic validation & malformed payload rejection
- Space persistence and atomic file writes
- Image decoding, validation, and base64 encoding
- Detection annotation rendering
- Mocked ML model inference and error handling
- End-to-end API routes (`/`, `/api/health`, `/api/spaces`, `/api/analyze`)

### Frontend Tests (Vitest + Testing Library)

```bash
cd frontend
npm test
```

Tests cover:
- Utility formatting functions (file sizes, confidence, badges)
- Metric KPI cards rendering
- Detection results table behavior and empty states

---

## ⚙️ Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `ENV` | `development` | Runtime environment (`development`, `production`) |
| `DEBUG` | `true` | Debug mode |
| `HOST` | `127.0.0.1` | Server binding host |
| `PORT` | `8000` | Server binding port |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated allowed origins |
| `MODEL_REPO` | `simahanyan/parking-lot-yolo26m` | HuggingFace repository ID |
| `MODEL_FILENAME` | `weights/parking_lot.pt` | Weights filename |
| `MODEL_CONFIDENCE_THRESHOLD` | `0.25` | Confidence filter for bounding boxes |
| `MODEL_IMAGE_SIZE` | `1280` | Image size passed to YOLO inference |
| `RATE_LIMIT_ENABLED` | `true` | Toggle rate limiting |
| `RATE_LIMIT_REQUESTS` | `30` | Allowed requests per window |
| `RATE_LIMIT_WINDOW_SECONDS` | `60` | Rate limit sliding window (seconds) |

### Frontend (`frontend/.env`)

| Variable | Default | Description |
|---|---|---|
| `VITE_API_URL` | `http://127.0.0.1:8000` | Target backend API base URL |

---

## 🛡️ Security & Reliability Improvements

1. **Strict Input Validation:** Images are validated for mime type, extension, size (< 15 MB), and corrupted byte streams before reaching the ML layer.
2. **Atomic Writes:** Persistence writes to a tempfile before atomically replacing `parking_spaces.json`, eliminating race conditions and partial file corruption.
3. **Model Isolation:** YOLO model weights are managed in a thread-safe singleton with inference execution wrapped in thread locks, preventing concurrency collisions.
4. **Rate Limiting:** Protects the GPU/CPU-heavy `/api/analyze` endpoint against denial-of-service spam.
5. **Request Cancellation:** The frontend uses `AbortController` to cleanly cancel stale or superseded requests.
6. **Graceful Error Handling:** Centralized exception handlers prevent internal tracebacks or system paths from leaking to clients.

## 📄 Project Documentation

## 📄 Project Documentation

- 📘 [Project Report (PDF)](./docs/SmartParkAI_Project_Report.pdf)
- 📊 [Project Presentation (PDF)](./docs/SmartParkAI_Presentation.pdf)