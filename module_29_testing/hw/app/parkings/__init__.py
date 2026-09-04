from flask import Blueprint

parking_bp = Blueprint("parking", __name__)

from app.parkings import routes as routes  # noqa: F401, E402
