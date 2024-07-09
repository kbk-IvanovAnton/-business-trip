# type: ignore

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    id = StringField("Employee ID", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    realname = StringField("Real Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError("Please use a different email address.")

    def validate_id(self, id):
        user = db.session.scalar(sa.select(User).where(User.id == id.data))
        if user is not None:
            raise ValidationError("Please use a different employee ID.")


class OrderForm(FlaskForm):
    user = SelectField("Name", coerce=int, validators=[DataRequired()])
    order = StringField(validators=[DataRequired()])
    order_number = StringField()
    detail_number = StringField()
    submit = SubmitField("Confirm")

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id, user.realname) for user in User.query.all()]
