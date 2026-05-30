from flask_app.domain.models import Prediction, User

from .database import db
from .orm import PredictionORM, UserORM


class SQLAlchemyUserRepository:
    def get_by_username(self, username: str) -> User | None:
        orm_user = UserORM.query.filter_by(username=username).first()
        if not orm_user:
            return None
        return User(
            id=orm_user.id,
            username=orm_user.username,
            hashed_password=orm_user.hashed_password,
            created_at=orm_user.created_at,
        )

    def add(self, user: User) -> User:
        orm_user = UserORM(username=user.username, hashed_password=user.hashed_password)
        db.session.add(orm_user)
        db.session.commit()
        user.id = orm_user.id
        return user

    def get_by_id(self, user_id: int) -> User | None:
        orm_user = UserORM.query.get(user_id)
        if not orm_user:
            return None
        return User(
            id=orm_user.id,
            username=orm_user.username,
            hashed_password=orm_user.hashed_password,
            created_at=orm_user.created_at,
        )


class SQLAlchemyPredictionRepository:
    def add(self, prediction: Prediction) -> Prediction:
        orm_pred = PredictionORM(
            user_id=prediction.user_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
        )
        db.session.add(orm_pred)
        db.session.commit()
        prediction.id = orm_pred.id
        return prediction

    def get_by_user(self, user_id: int) -> list[Prediction]:
        orm_preds = (
            PredictionORM.query.filter_by(user_id=user_id)
            .order_by(PredictionORM.created_at.desc())
            .all()
        )
        return [
            Prediction(
                id=p.id,
                user_id=p.user_id,
                input_data=p.input_data,
                prediction=p.prediction,
                created_at=p.created_at,
            )
            for p in orm_preds
        ]
