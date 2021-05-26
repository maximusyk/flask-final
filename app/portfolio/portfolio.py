# region IMPORTS

from app.portfolio import portfolio_bp
from flask import render_template

# endregion


# region VARIABLES
menu = [
    ("User", "/register", "user"),
    ("Home", "/", "home"),
    ("About", "/about", "info-circle"),
    ("Portfolio", "/portfolio", "book-content"),
    ("Contact", "/contact", "envelope"),
    ("ToDo List", "/todo", "list-check"),
]
# endregion


# region PORTFOLIO
@portfolio_bp.route("/portfolio")
def portfolio():
    return render_template(
        "portfolio.html",
        menu=menu,
    )
# endregion
