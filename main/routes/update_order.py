# type: ignore


from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.main import bp
from app.main.forms.order import OrderForm
from app.main.models.order import Order


@bp.route("/update_order/<order_id>", methods=["GET", "POST"])
@login_required
def update_order(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        order.name_id = form.user.data
        order.order = form.order.data
        order.order_number = form.order_number.data
        order.detail_number = form.detail_number.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.index"))

    elif request.method == "GET":
        form.user.data = order.name_id
        form.order.data = order.order
        form.order_number.data = order.order_number
        form.detail_number.data = order.detail_number

    return render_template("main/create_order.html", title="Edit Order", form=form)
