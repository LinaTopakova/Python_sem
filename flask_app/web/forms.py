from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):  # type: ignore[misc]
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):  # type: ignore[misc]
    username = StringField("Логин", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Зарегистрироваться")


class UploadForm(FlaskForm):  # type: ignore[misc]
    photo = FileField(
        "Фото блюда",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "png", "jpeg"], "Только изображения!"),
        ],
    )
    submit = SubmitField("Распознать")
