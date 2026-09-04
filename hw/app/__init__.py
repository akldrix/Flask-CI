from flask import Flask
from .extensions import db


def create_app(config_override=None):
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://admin:admin@localhost:5432/my_db"
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	if config_override:
		app.config.update(config_override)
	db.init_app(app)

	with app.app_context():
		from .models import Client, Parking, ClientParking
		db.create_all()

	from app.clients import client_bp
	app.register_blueprint(client_bp)

	from app.parkings import parking_bp
	app.register_blueprint(parking_bp)

	from app.client_parkings import client_parkings_bp
	app.register_blueprint(client_parkings_bp)

	return app
