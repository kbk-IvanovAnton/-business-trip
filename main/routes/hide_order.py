# type: ignore

from flask import redirect, url_for
from flask_login import login_required

from app import db
from app.main import bp
from app.main.models.order import Order


@bp.route("/hide_order/<int:id>", methods=["POST"])
@login_required
def hide_order(id):
    order = Order.query.get_or_404(id)
    if order.is_hidden is True:
        order.is_hidden = False
    else:
        order.is_hidden = True
    db.session.commit()
    return redirect(url_for("main.index"))
