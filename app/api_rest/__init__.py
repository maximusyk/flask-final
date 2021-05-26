from app.extensions import csrf
from flask import Blueprint

api_rest_bp = Blueprint("api_rest_bp", __name__)
csrf.exempt(api_rest_bp)
