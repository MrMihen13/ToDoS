import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel

from app import db


class ValidationModel:
    """Модели валидации данных"""

    class InputTask(BaseModel):
        """Модель данных задачи"""
        id: int
        description: str
        body: str
        done: bool
        timestamp: str
        user_id: int
        file: int  # Переделать тип данных для файла

    class UserWithoutPassword(BaseModel):
        """Модель пользователя для FrontEnd"""
        id: int
        name = str
        surname: str
        email: str
        image: int  # Переделать тип данных для изображения

    class InputUser(UserWithoutPassword):
        """Модель данных пользователя для базы данных"""
        password: str


class DBModel:
    """Модели валидации данных"""

    class User(db.Model):
        """Модель пользователя в бозе данных"""
        id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
        name = db.Column(db.String(64), nullable=False, unique=True)
        surname = db.Column(db.String(64), nullable=False, unique=True)
        email = db.Column(db.String(128), nullable=False, unique=True)
        password_hash = db.Column(db.String(128), nullable=False)
        image = db.Column(db.BLOB, unique=False)

        '''__table_args__ = {'extend_existing': True}'''

        def set_password(self, password):
            """Добавление хэша пароля в бозу данных"""
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            """Проверка совпадения пароля"""
            return check_password_hash(self.password_hash, password)

        def __repr__(self):
            return '<User {}>'.format(self.name)

        @property
        def serialize(self):
            """Серилизация данных для Json"""
            return {
                'id': str(self.id),
                'name': self.name,
                'surname': self.surname,
                'email': self.email,
                'image': self.image
            }

    class Task(db.Model):
        """Модель задачи в базе данных"""
        id = db.Column(db.Integer(), primary_key=True)
        description = db.Column(db.String(128))
        body = db.Column(db.Text)
        done = db.Column(db.Boolean())
        timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow())
        user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
        file = db.Column(db.BLOB, unique=True)

        '''__table_args__ = {'extend_existing': True}'''

        def __repr__(self):
            return '<Task {}>'.format(self.body)

        @property
        def serialize(self):
            """Серилизация данных для Json"""
            return {
                'id': self.id,
                'description': self.description,
                'body': self.body,
                'done': self.done,
                'timestamp': str(self.timestamp),
                'user_id': self.user_id,
                'file': self.file,
            }
