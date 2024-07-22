# type: ignore

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from app.auth.models.user import User


class OrderForm(FlaskForm):
    user = SelectField("Name", coerce=int, validators=[DataRequired()])
    order = StringField(validators=[DataRequired()])
    order_number = StringField()
    detail_number = StringField()
    submit = SubmitField("Confirm")

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.user.choices = [(user.id, user.name) for user in User.query.all()]
