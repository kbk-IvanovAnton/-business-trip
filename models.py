# type: ignore

from datetime import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    realname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, default=None)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    admin: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=False)
    is_show: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)

    orders_rel = db.relationship("Order", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Order(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name_id: so.Mapped[int] = so.mapped_column(
        sa.Integer, db.ForeignKey("user.id"), nullable=False
    )
    order: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    order_number: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    detail_number: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    is_hidden: so.Mapped[bool] = so.mapped_column(sa.Boolean(), nullable=False, default=False)
    year: so.Mapped[int] = so.mapped_column(sa.Integer(), default=lambda: datetime.now().year)

    user = db.relationship("User", back_populates="orders_rel")

    def __repr__(self):
        return "<Order {}>".format(self.id)


class Currencies(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False, default=None)
    prefix: so.Mapped[str] = so.mapped_column(sa.String(), default=None)
    suffix: so.Mapped[str] = so.mapped_column(sa.String(), default=None)
    code: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False, default=None)
    decimal: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=False)
    order: so.Mapped[int] = so.mapped_column(sa.Integer(), nullable=False)
    is_show_japan: so.Mapped[bool] = so.mapped_column(sa.Boolean(), nullable=False, default=True)
    is_show_world: so.Mapped[bool] = so.mapped_column(sa.Boolean(), nullable=False, default=True)

    def __repr__(self):
        return "<Currencies {}>".format(self.id)


class Travel(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(), nullable=False, default=None)
    is_show: so.Mapped[bool] = so.mapped_column(sa.Boolean(), default=True)

    def __repr__(self):
        return "<Travel {}>".format(self.id)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
