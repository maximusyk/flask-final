# region _IMPORTS

from app.about import about_bp
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

# region _ROUTES


@about_bp.route("/about")
def about():
    return render_template(
        "about.html",
        menu=menu,
    )
# endregion
