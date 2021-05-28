from app.extensions import db
from run import app

db.init_app(app)
db.create_all()
