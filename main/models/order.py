# type: ignore

from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db


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
