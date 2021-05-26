from flask import Blueprint

contact_bp = Blueprint('contact_bp', __name__,
                       template_folder="templates/contact")
