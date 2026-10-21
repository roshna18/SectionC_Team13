
import base64
import json
import math
import threading
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

app = FastAPI(title="SmartPark AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
STORAGE_DIR = BASE_DIR / "storage"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

SPACES_FILE = STORAGE_DIR / "parking_spaces.json"
MAX_FILE_SIZE = 15 * 1024 * 1024

MODEL_REPO = "simahanyan/parking-lot-yolo26m"
MODEL_FILENAME = "weights/parking_lot.pt"

_model = None
_model_lock = threading.Lock()


def get_model():
    """Download the parking model once and load it."""
    global _model

    with _model_lock:
        if _model is None:
            weights_path = hf_hub_download(
                repo_id=MODEL_REPO,
                filename=MODEL_FILENAME,
            )
            _model = YOLO(weights_path)

    return _model


async def read_uploaded_image(file: UploadFile):
    allowed = {".jpg", ".jpeg", ".png", ".webp"}
    extension = Path(file.filename or "").suffix.lower()

    if extension not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Upload a JPG, JPEG, PNG, or WEBP image.",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if not content:
        raise HTTPException(
            status_code=400,
            detail="The uploaded image is empty.",
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The image must be smaller than 15 MB.",
        )

    image = cv2.imdecode(
        np.frombuffer(content, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )

    if image is None:
        raise HTTPException(
            status_code=400,
            detail="Could not read this image. Try another image.",
        )

    return image


def classify_label(label):
    """Map model class names to the app's status values."""
    name = label.lower().replace("_", "-").replace(" ", "-")

    if "empty" in name or "vacant" in name or "free" in name:
        return "vacant"

    if "occupied" in name or "filled" in name or "taken" in name:
        return "occupied"

    return "unknown"


def encode_image(image):
    success, encoded = cv2.imencode(
        ".jpg",
        image,
        [cv2.IMWRITE_JPEG_QUALITY, 90],
    )

    if not success:
        raise HTTPException(
            status_code=500,
            detail="Could not create the annotated image.",
        )

    encoded_text = base64.b64encode(
        encoded.tobytes()
    ).decode("ascii")

    return f"data:image/jpeg;base64,{encoded_text}"


@app.get("/")
def home():
    return {
        "name": "SmartPark AI",
        "message": "Parking detection API is running.",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "model_loaded": _model is not None,
    }


@app.get("/api/spaces")
def get_spaces():
    """Kept for compatibility with the previous frontend."""
    if not SPACES_FILE.exists():
        return {"spaces": []}

    try:
        spaces = json.loads(
            SPACES_FILE.read_text(encoding="utf-8")
        )
        return {"spaces": spaces if isinstance(spaces, list) else []}
    except (OSError, json.JSONDecodeError):
        return {"spaces": []}


@app.post("/api/spaces")
def save_spaces(payload: dict):
    """Keep the old save-spaces endpoint available."""
    spaces = payload.get("spaces", [])

    if not isinstance(spaces, list):
        raise HTTPException(400, "Spaces must be a list.")

    SPACES_FILE.write_text(
        json.dumps(spaces, indent=2),
        encoding="utf-8",
    )

    return {"message": "Saved.", "count": len(spaces)}


@app.post("/api/lot/upload")
async def upload_lot_image(file: UploadFile = File(...)):
    """Compatibility endpoint for the old interface."""
    image = await read_uploaded_image(file)

    destination = STORAGE_DIR / "reference_image.jpg"

    if not cv2.imwrite(str(destination), image):
        raise HTTPException(500, "Could not save reference image.")

    return {"message": "Image uploaded successfully."}


@app.post("/api/analyze")
async def analyze_image(file: UploadFile = File(...)):
    image = await read_uploaded_image(file)
    height, width = image.shape[:2]

    try:
        detector = get_model()

        # Higher resolution helps detect small parking bays.
        predictions = detector.predict(
            source=image,
            conf=0.25,
            imgsz=1280,
            verbose=False,
        )

    except Exception as error:
        print(f"Parking model error: {error}")
        raise HTTPException(
            status_code=500,
            detail=(
                "The parking model could not run. "
                "Check the backend terminal for details."
            ),
        )

    annotated = image.copy()
    detections = []

    for prediction in predictions:
        if prediction.boxes is None:
            continue

        names = prediction.names

        for box in prediction.boxes:
            class_id = int(box.cls.item())
            label = str(names[class_id])
            status = classify_label(label)
            confidence = float(box.conf.item())

            coordinates = box.xyxy[0].tolist()
            x1, y1, x2, y2 = [
                int(value) for value in coordinates
            ]

            x1 = max(0, min(x1, width - 1))
            x2 = max(0, min(x2, width - 1))
            y1 = max(0, min(y1, height - 1))
            y2 = max(0, min(y2, height - 1))

            # Green = vacant; red = occupied; grey = unknown.
            if status == "vacant":
                color = (0, 200, 0)
            elif status == "occupied":
                color = (0, 0, 255)
            else:
                color = (160, 160, 160)

            display_label = (
                f"{status.upper()} {confidence:.0%}"
                if status != "unknown"
                else f"{label} {confidence:.0%}"
            )

            cv2.rectangle(
                annotated,
                (x1, y1),
                (x2, y2),
                color,
                2,
            )

            text_y = max(22, y1 - 8)

            cv2.putText(
                annotated,
                display_label,
                (x1, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                color,
                2,
                cv2.LINE_AA,
            )

            detections.append({
                "id": f"P{len(detections) + 1}",
                "label": label,
                "status": status,
                "occupied": status == "occupied",
                "confidence": round(confidence, 4),
                "box": [x1, y1, x2, y2],
            })

    occupied = sum(
        1 for item in detections
        if item["status"] == "occupied"
    )
    vacant = sum(
        1 for item in detections
        if item["status"] == "vacant"
    )
    unknown = sum(
        1 for item in detections
        if item["status"] == "unknown"
    )

    total = len(detections)
    classified_total = occupied + vacant

    occupancy_percent = (
        round(occupied / classified_total * 100, 1)
        if classified_total else 0
    )

    if total == 0:
        note = (
            "No parking spaces were detected. Try a clear, "
            "well-lit image from an elevated or fixed viewpoint."
        )
    else:
        note = (
            "Results are predictions from a pretrained model. "
            "Accuracy may vary with camera angle, image quality, "
            "occlusion, and parking layout."
        )

    return {
        "message": "Parking image analyzed successfully.",
        "total_spaces": total,
        "occupied": occupied,
        "vacant": vacant,
        "unknown": unknown,
        "occupancy_percent": occupancy_percent,
        "vehicle_count": None,
        "results": detections,
        "detections": detections,
        "annotated_image": encode_image(annotated),
        "spaces_available": vacant > 0,
        "note": note,
        "image_width": width,
        "image_height": height,
    }
