from enum import Enum
from flask_login import UserMixin
from utils import AuthenticationError, Util, db
from .base_model import BaseModel


class Role(BaseModel):

    class Tier(Enum):

        ADMIN = (1, "Admin")
        SELLER = (2, "Seller")
        CASHIER = (3, "Cashier")

        def __new__(cls, value, label):
            obj = object.__new__(cls)
            obj._value_ = value
            obj.label = label
            return obj


class User(UserMixin, BaseModel):

    def __init__(self, data: dict):
        self.id = data['user_id']
        self.username = data['username']
        self.password = data['password']
        self.role = data['role_id']
        self.last_login_dttm = data['last_login_dttm']

    def __str__(self):

        return f"ID: {self.id}, USERNAME: {self.username}, ROLE: {self.get_role()}"

    def __repr__(self):

        return {'id': self.id, 'username': self.username, 'role_id': self.role}

    def get_id(self):
        return str(self.id)

    def get_role(self):
        return {'role': Role.Tier(self.role).label}

    @staticmethod
    def login(data: dict) -> dict:
        from werkzeug.security import check_password_hash

        username, password = Util.split_dict(data)
        user_row = db.query.get_many_rows_by_att(User, username)

        if user_row:
            user_row = Util.handle_row_data(user_row, User)[0]

        if not user_row or not check_password_hash(user_row['password'],
                                                   password['password']):
            raise AuthenticationError(
                "Invalid username or password.",
                context=AuthenticationError.get_error_context(
                    user_row=user_row, data=data))

        else:
            return User(user_row)

    @staticmethod
    def load(user_id):
        user_data = User.get_data(user_id)
        return User(user_data) if user_data else None
