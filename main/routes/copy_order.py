# type: ignore


from flask import redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.main import bp
from app.main.forms.order import OrderForm
from app.main.models.order import Order


@bp.route("/copy_order/<order_id>", methods=["GET", "POST"])
@login_required
def copy_order(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    form = OrderForm(obj=order)
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

    elif request.method == "GET":
        form.order.data = order.order
        form.order_number.data = order.order_number
        form.detail_number.data = order.detail_number

    return render_template("main/create_order.html", title="Copy Order", form=form)
