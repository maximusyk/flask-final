from app.extensions import db
from app.users.models import User
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .controllers import *

admin = Admin(index_view=MyAdminIndexView())


def create_admin(app, **kwargs):
    admin.init_app(app)
    admin.add_view(CustomView(name="Custom"))

    # models = [User]

    # for model in models:
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(UserAdminView(User, db.session))
