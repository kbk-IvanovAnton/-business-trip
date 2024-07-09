# type: ignore

from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, OrderForm, RegistrationForm
from app.models import Currencies, Order, Travel, User


@app.route("/")
@app.route("/index")
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
    return render_template("index.html", orders=orders)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            id=form.id.data,
            username=form.username.data,
            realname=form.realname.data,
            email=form.email.data,
            admin=User.query.first() is None,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/create_order", methods=["GET", "POST"])
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
        return redirect(url_for("index"))
    return render_template("create_order.html", title="Create Order", form=form)


@app.route("/update_order/<order_id>", methods=["GET", "POST"])
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
        return redirect(url_for("index"))

    elif request.method == "GET":
        form.user.data = order.name_id
        form.order.data = order.order
        form.order_number.data = order.order_number
        form.detail_number.data = order.detail_number

    return render_template("create_order.html", title="Edit Order", form=form)


@app.route("/copy_order/<order_id>", methods=["GET", "POST"])
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
        return redirect(url_for("index"))

    elif request.method == "GET":
        form.order.data = order.order
        form.order_number.data = order.order_number
        form.detail_number.data = order.detail_number

    return render_template("create_order.html", title="Copy Order", form=form)


@app.route("/delete_order/<int:id>")  # dont use now
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/hide_order/<int:id>", methods=["POST"])
@login_required
def hide_order(id):
    order = Order.query.get_or_404(id)
    if order.is_hidden is True:
        order.is_hidden = False
    else:
        order.is_hidden = True
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/admin_menu", methods=["GET", "POST"])
@login_required
def admin_menu():
    users = db.session.scalars(sa.select(User)).all()
    return render_template("admin_menu.html", title="Admin Menu", users=users)


@app.route("/admin_menu/currency_table")
@login_required
def currency_table():
    currencies = db.session.scalars(sa.select(Currencies)).all()
    return render_template("currency_table.html", title="Currency Table", currencies=currencies)


@app.route("/admin_menu/travel_table")
@login_required
def travel_table():
    travels = db.session.scalars(sa.select(Travel)).all()
    return render_template("travel_table.html", title="Travel Table", travels=travels)


@app.route("/admin_menu/add_travel", methods=["POST"])
def add_travel():
    data = request.json
    new_travel = Travel(name=data["name"])
    if new_travel:
        db.session.add(new_travel)
        db.session.commit()
        return jsonify(success=True, id=new_travel.id)
    return redirect(url_for("travel_table"))


@app.route("/admin_menu/edit_travel", methods=["POST"])
def edit_travel():
    data = request.json
    travel = Travel.query.get(data["id"])
    if travel:
        travel.name = data["name"]
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/admin_menu/delete_travel", methods=["POST"])
def delete_travel():
    data = request.json
    travel = Travel.query.get(data["id"])
    if travel:
        db.session.delete(travel)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/admin_menu/travel_table/toggle_show", methods=["POST"])
def travel_toggle_show():
    data = request.json
    travel = Travel.query.get(data["id"])
    if travel:
        travel.is_show = bool(data["is_show"])
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/admin_menu/delete_user", methods=["POST"])
def delete_user():
    data = request.get_json()
    user_id = data.get("id")
    user = User.query.get(user_id)
    if user:
        db.session.query(Order).filter(Order.name_id == user_id).delete()
        db.session.delete(user)
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/admin_menu/edit_user", methods=["POST", "GET"])
def edit_user():
    data = request.get_json()
    user_id = data.get("id")
    username = data.get("username")
    realname = data.get("realname")

    user = User.query.get(user_id)
    if user:
        user.username = username
        user.realname = realname
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/admin_menu/toggle_show", methods=["POST"])
def toggle_show():
    data = request.get_json()
    user_id = data.get("id")
    is_show = data.get("is_show")

    if not user_id or is_show is None:
        return jsonify(success=False, message="All fields are required."), 400

    user = User.query.get(user_id)
    if user:
        user.is_show = bool(int(is_show))
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, message="User not found."), 404
