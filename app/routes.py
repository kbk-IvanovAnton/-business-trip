# type: ignore

from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, OrderForm, RegistrationForm
from app.models import Order, User


@app.route("/")
@app.route("/index")
@login_required  # Only authenticated users can access this route
def index():
    orders = db.session.scalars(sa.select(Order)).all()
    return render_template("index.html", title="Home", orders=orders)


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
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@login_required
@app.route("/business", methods=["GET", "POST"])
def business():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            name=form.name.data,
            business=form.business.data,
            order=form.order.data,
            detail=form.detail.data,
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("business.html", title="Business", form=form)


@app.route("/edit_order/<order_id>", methods=["GET", "POST"])
@login_required
def edit_order(order_id):
    order = Order.query.filter_by(id=order_id).first_or_404()
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        order.name = form.name.data
        order.business = form.business.data
        order.order = form.order.data
        order.detail = form.detail.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("index"))

    elif request.method == "GET":
        form.name.data = order.name
        form.business.data = order.business
        form.order.data = order.order
        form.detail.data = order.detail

    return render_template("business.html", title="Edit Order", form=form)
