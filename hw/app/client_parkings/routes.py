from flask import jsonify, request

from app.client_parkings import client_parkings_bp
from app.extensions import db
from app.models import ClientParking, Client, Parking
from datetime import datetime


@client_parkings_bp.route('/client_parkings', methods=['POST'])
def create_client_parking():
	client_id = request.json.get('client_id')
	parking_id = request.json.get('parking_id')

	if not client_id:
		return jsonify({'error': 'Missing client_id'}), 400
	if not parking_id:
		return jsonify({'error': 'Missing parking_id'}), 400

	client = db.session.query(Client).where(Client.id == client_id).one_or_none()
	if client is None:
		return jsonify({'error': 'Client not found'}), 404

	parking = db.session.query(Parking).where(Parking.id == parking_id).one_or_none()
	if parking is None:
		return jsonify({'error': 'Parking not found'}), 404

	if parking.count_available_places == 0:
		return jsonify({'error': 'Parking not available'}), 400

	client_parking = ClientParking(client_id=client_id, parking_id=parking_id, time_in=datetime.now())
	db.session.add(client_parking)
	parking.count_available_places -= 1
	db.session.commit()
	return jsonify({'success': True, "client-parking": client_parking.to_dict()}), 201


@client_parkings_bp.route('/client_parkings', methods=['DELETE'])
def delete_client_parking():
	client_id = request.json.get('client_id')
	parking_id = request.json.get('parking_id')
	if not client_id:
		return jsonify({'error': 'Missing client_id'}), 400
	if not parking_id:
		return jsonify({'error': 'Missing parking_id'}), 400

	client = db.session.query(Client).where(Client.id == client_id).one_or_none()
	if client is None:
		return jsonify({'error': 'Client not found'}), 404

	parking = db.session.query(Parking).where(Parking.id == parking_id).one_or_none()
	if parking is None:
		return jsonify({'error': 'Parking not found'}), 404

	if client.credit_card is None:
		return jsonify({'error': 'Credit card not found'}), 404

	client_parking = db.session.query(ClientParking).where(
		ClientParking.client_id == client_id,
		ClientParking.parking_id == parking_id
	).one_or_none()
	if client_parking is None:
		return jsonify({'error': 'Client-parking not found'}), 404
	parking.count_available_places += 1
	client_parking.time_out = datetime.now()
	response = client_parking.to_dict()
	db.session.delete(client_parking)
	db.session.commit()
	return jsonify({'success': True, "client-parking": response}), 200
