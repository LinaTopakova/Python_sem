from datetime import UTC, datetime

from .database import db


class UserORM(db.Model):  # type: ignore
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hashed_password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))


class PredictionORM(db.Model):  # type: ignore
    __tablename__ = "predictions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    input_data = db.Column(db.String(256))
    prediction = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    user = db.relationship("UserORM", backref="predictions")
