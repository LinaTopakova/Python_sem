import json
from typing import Any, cast

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from flask_app.web.forms import UploadForm

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard() -> Any:
    form = UploadForm()
    return render_template("dashboard.html", form=form)


@main_bp.route("/predict", methods=["POST"])
@login_required
def predict() -> Any:
    form = UploadForm()
    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename or "image.jpg")
        image_bytes = file.read()
        prediction_service = cast(Any, current_app).prediction_service
        try:
            result = prediction_service.request_prediction(
                user_id=current_user.id,
                filename=filename,
                image_bytes=image_bytes,
            )
            return render_template("result.html", result=result, filename=filename)
        except Exception as e:
            flash(f"Ошибка при распознавании: {e}", "danger")
            return redirect(url_for("main.dashboard"))
    flash("Пожалуйста, выберите изображение.", "warning")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/history")
@login_required
def history() -> Any:
    from flask_app.infrastructure.repositories import (
        SQLAlchemyPredictionRepository,
    )

    repo = SQLAlchemyPredictionRepository()
    preds = repo.get_by_user(current_user.id)
    enriched = []
    for p in preds:
        try:
            data = json.loads(p.prediction)
        except Exception:
            data = {}
        enriched.append(
            {
                "input_data": p.input_data,
                "result": data,
                "created_at": p.created_at,
            }
        )
    return render_template("history.html", predictions=enriched)
