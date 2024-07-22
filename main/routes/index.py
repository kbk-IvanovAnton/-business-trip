# type: ignore

from flask import render_template
from flask_login import current_user, login_required

from app import db
from app.auth.models.user import User
from app.main import bp
from app.main.models.order import Order


@bp.route("/")
@bp.route("/index")
@login_required  # Only authenticated users can access this route
def index():
    if current_user.admin:
        orders = db.session.query(Order).join(User).filter(User.is_show.is_(True)).all()
    else:
        orders = (
            db.session.query(Order)
            .join(User)
            .filter(User.is_show.is_(True), Order.is_hidden.is_(False))
            .all()
        )
    return render_template("main/index.html", orders=orders)
