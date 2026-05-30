import os
from typing import Any

from flask import Flask
from flask_login import LoginManager

from flask_app.infrastructure.database import db, init_db
from flask_app.infrastructure.repositories import (
    SQLAlchemyPredictionRepository,
    SQLAlchemyUserRepository,
)
from flask_app.services.auth_service import AuthService
from flask_app.services.prediction_service import PredictionService


def create_app() -> Flask:
    app = Flask(__name__, template_folder="web/templates")
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-secret")

    init_db(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    user_repo = SQLAlchemyUserRepository()
    prediction_repo = SQLAlchemyPredictionRepository()
    ml_api_url = os.getenv("ML_API_URL", "http://fastapi:8000")

    app.auth_service = AuthService(user_repo)  # type: ignore[attr-defined]
    app.prediction_service = PredictionService(  # type: ignore[attr-defined]
        prediction_repo, ml_api_url
    )

    @login_manager.user_loader
    def load_user(user_id: str) -> Any | None:
        from flask_login import UserMixin

        user = user_repo.get_by_id(int(user_id))
        if user:

            class AuthUser(UserMixin):  # type: ignore[misc]
                def __init__(self, domain_user: Any) -> None:
                    self.id = domain_user.id
                    self.username = domain_user.username

            return AuthUser(user)
        return None

    with app.app_context():
        db.create_all()

    from flask_app.web.auth import auth_bp
    from flask_app.web.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
