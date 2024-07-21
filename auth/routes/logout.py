# type: ignore

from flask import redirect, url_for
from flask_login import logout_user

from app.auth import bp


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
