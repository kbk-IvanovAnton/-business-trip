# type: ignore

from flask import redirect, url_for

from app import db
from app.main import bp
from app.main.models.order import Order


@bp.route("/delete_order/<int:id>")  # dont use now
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("index"))
