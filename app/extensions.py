from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from sqlalchemy import MetaData

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
csrf = CSRFProtect()
ma = Marshmallow()
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
login_manager = LoginManager()
login_manager.login_view = "/"
# login_manager.login_view = 'users_bp.user_form'
