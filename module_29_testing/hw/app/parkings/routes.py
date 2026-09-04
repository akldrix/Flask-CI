from flask import jsonify, request

from app.extensions import db
from app.models import Parking
from app.parkings import parking_bp


@parking_bp.route("/parkings", methods=["POST"])
def create_parking():
    parking_data = request.get_json()
    if not parking_data:
        return jsonify({"error": "No data provided"}), 400
    parking = Parking(**parking_data)
    db.session.add(parking)
    db.session.commit()
    return jsonify({"parking": parking.to_dict()}), 201
