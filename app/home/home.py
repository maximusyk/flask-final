# region _IMPORTS

from app.home import home_bp
from flask import render_template

# endregion

# region _VARS
menu = [
    ("User", "/register", "user"),
    ("Home", "/", "home"),
    ("About", "/about", "info-circle"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]
# endregion


# region _ROUTES
@home_bp.route("/")
@home_bp.route("/hero/")
def index():
    return render_template(
        "index.html",
        menu=menu
    )
# endregion
