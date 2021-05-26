from app.extensions import csrf
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__)
csrf.exempt(api_bp)
