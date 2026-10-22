"""Parking lot image analysis service."""

from typing import Optional
from fastapi import UploadFile
import numpy as np

from app.core.exceptions import ImageValidationError, ModelInferenceError
from app.core.logging import logger
from app.image_processing.annotations import draw_detection_annotations
from app.image_processing.encoder import encode_image_to_base64, read_uploaded_image
from app.ml.inference import predict_parking_spaces
from app.schemas.analyze import AnalyzeResponse, DetectionItem


class AnalysisService:
    async def analyze_image_file(
        self,
        file: UploadFile,
        confidence_threshold: Optional[float] = None,
    ) -> AnalyzeResponse:
        """
        Orchestrate the end-to-end analysis of an uploaded parking image.
        1. Validates and decodes image bytes
        2. Executes YOLO model inference
        3. Computes summary metrics (vacant, occupied, unknown, percent)
        4. Renders visual bounding boxes and status labels
        5. Encodes annotated image to base64 Data URL
        """
        # 1. Read & validate image
        image: np.ndarray = await read_uploaded_image(file)

        # 2. Predict spaces
        detections, height, width = predict_parking_spaces(
            image=image,
            confidence_threshold=confidence_threshold,
        )

        # 3. Compute metrics
        occupied = sum(1 for item in detections if item.status == "occupied")
        vacant = sum(1 for item in detections if item.status == "vacant")
        unknown = sum(1 for item in detections if item.status == "unknown")
        total = len(detections)
        classified_total = occupied + vacant

        occupancy_percent = (
            round(occupied / classified_total * 100, 1)
            if classified_total > 0
            else 0.0
        )

        # 4. Generate user advisory note
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

        # 5. Render annotated visualization
        annotated_image = draw_detection_annotations(image, detections)
        encoded_image_str = encode_image_to_base64(annotated_image)

        logger.info(
            f"Image analyzed: {width}x{height}, total={total}, vacant={vacant}, "
            f"occupied={occupied}, occupancy={occupancy_percent}%"
        )

        return AnalyzeResponse(
            message="Parking image analyzed successfully.",
            total_spaces=total,
            occupied=occupied,
            vacant=vacant,
            unknown=unknown,
            occupancy_percent=occupancy_percent,
            vehicle_count=None,
            results=detections,
            detections=detections,
            annotated_image=encoded_image_str,
            spaces_available=vacant > 0,
            note=note,
            image_width=width,
            image_height=height,
        )


analysis_service = AnalysisService()
