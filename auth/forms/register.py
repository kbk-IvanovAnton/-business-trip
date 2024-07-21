# type: ignore

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db
from app.auth.models.user import User


class RegistrationForm(FlaskForm):
    id = StringField("Employee ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")

    def validate_id(self, id):
        user = db.session.scalar(sa.select(User).where(User.id == id.data))
        if user is not None:
            raise ValidationError("Please use a different employee ID.")
