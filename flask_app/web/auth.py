from typing import Any, cast

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import UserMixin, login_required, login_user, logout_user

from flask_app.domain.models import User as DomainUser
from flask_app.web.forms import LoginForm, RegisterForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> Any:
    form = RegisterForm()
    if form.validate_on_submit():
        auth_service = cast(Any, current_app).auth_service
        user = auth_service.register(form.username.data, form.password.data)
        if user:
            flash("Регистрация успешна! Теперь войдите.", "success")
            return redirect(url_for("auth.login"))
        flash("Пользователь уже существует.", "danger")
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> Any:
    form = LoginForm()
    if form.validate_on_submit():
        auth_service = cast(Any, current_app).auth_service
        user = auth_service.authenticate(form.username.data, form.password.data)
        if user:

            class AuthUser(UserMixin):  # type: ignore[misc]
                def __init__(self, domain_user: DomainUser) -> None:
                    self.id = domain_user.id
                    self.username = domain_user.username

            login_user(AuthUser(user), remember=True)
            flash("Вы вошли в систему.", "success")
            return redirect(url_for("main.dashboard"))
        flash("Неверный логин или пароль.", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout() -> Any:
    logout_user()
    flash("Вы вышли из системы.", "info")
    return redirect(url_for("auth.login"))
