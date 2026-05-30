from werkzeug.security import check_password_hash, generate_password_hash

from flask_app.domain.models import User
from flask_app.domain.protocols import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def register(self, username: str, password: str) -> User | None:
        if self.user_repo.get_by_username(username):
            return None
        hashed = generate_password_hash(password)
        user = User(id=0, username=username, hashed_password=hashed)
        return self.user_repo.add(user)

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.user_repo.get_by_username(username)
        if user and check_password_hash(user.hashed_password, password):
            return user
        return None
