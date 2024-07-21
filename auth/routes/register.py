# type: ignore

from flask import flash, redirect, render_template, url_for
from flask_login import current_user

from app import db
from app.auth import bp
from app.auth.forms.register import RegistrationForm
from app.auth.models.user import User


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            id=form.id.data,
            name=form.name.data,
            email=form.email.data,
            admin=User.query.first() is None,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)
