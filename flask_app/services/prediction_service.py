import json
from typing import Any, cast

import requests

from flask_app.domain.models import Prediction
from flask_app.domain.protocols import PredictionRepository


class PredictionService:
    def __init__(self, prediction_repo: PredictionRepository, ml_api_url: str) -> None:
        self.prediction_repo = prediction_repo
        self.ml_api_url = ml_api_url

    def request_prediction(self, user_id: int, filename: str, image_bytes: bytes) -> dict[str, Any]:
        files = {"file": (filename, image_bytes, "image/jpeg")}
        resp = requests.post(f"{self.ml_api_url}/predict", files=files, timeout=30)
        resp.raise_for_status()
        result: dict[str, Any] = cast(dict[str, Any], resp.json())
        pred = Prediction(id=0, user_id=user_id, input_data=filename, prediction=json.dumps(result))
        self.prediction_repo.add(pred)
        return result
