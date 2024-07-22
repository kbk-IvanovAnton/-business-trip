# type: ignore

from flask import redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.main import bp
from app.main.forms.order import OrderForm
from app.main.models.order import Order


@bp.route("/create_order", methods=["GET", "POST"])
@login_required
def create_order():
    form = OrderForm()
    if form.validate_on_submit():
        orders = Order(
            name_id=form.user.data,
            order=form.order.data,
            order_number=form.order_number.data,
            detail_number=form.detail_number.data,
        )
        db.session.add(orders)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("main/create_order.html", title="Create Order", form=form)
