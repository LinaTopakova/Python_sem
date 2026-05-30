from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    username: str
    hashed_password: str
    created_at: datetime | None = None


@dataclass
class Prediction:
    id: int
    user_id: int
    input_data: str
    prediction: str
    created_at: datetime | None = None
