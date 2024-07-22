from flask import Blueprint

bp = Blueprint(
    "main",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/main/static",
)

from app.main.routes import (
    copy_order,
    create_order,
    delete_order,
    hide_order,
    index,
    update_order,
)
