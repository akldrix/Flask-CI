from flask import Blueprint

client_bp = Blueprint("client", __name__)

from app.clients import routes as routes  # noqa: F401, E402
