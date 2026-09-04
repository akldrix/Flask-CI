from flask import jsonify, request

from app.clients import client_bp
from app.extensions import db
from app.models import Client


@client_bp.route('/clients', methods=['GET'])
def get_clients():
	clients = db.session.execute(db.select(Client)).scalars().all()
	if not clients:
		return jsonify({"message": "No clients found"}), 404
	return jsonify({'clients': [client.to_dict() for client in clients]}), 200


@client_bp.route('/clients/<client_id>', methods=['GET'])
def get_client(client_id):
	client = db.session.execute(db.select(Client).where(Client.id == client_id)).scalars().first()
	if not client:
		return jsonify({"message": "No clients with this id found"}), 404
	return jsonify({'client': client.to_dict()}), 200


@client_bp.route('/clients', methods=['POST'])
def create_client():
	client_data = request.get_json()
	if not client_data:
		return jsonify({'error': 'No data provided'}), 400
	client = Client(**client_data)
	db.session.add(client)
	db.session.commit()
	return jsonify({**client.to_dict()}), 201
