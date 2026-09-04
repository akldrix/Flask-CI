from flask import Blueprint

client_parkings_bp = Blueprint('client_parkings', __name__)

from app.client_parkings import routes