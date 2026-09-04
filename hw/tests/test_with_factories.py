import factory

from app.models import Client, Parking
from tests.factories import ClientFactory, ParkingFactory

def test_create_new_client_with_factory(client):
	with client.application.app_context():
		initial_count = Client.query.count()
	client_data = factory.build(dict, FACTORY_CLASS=ClientFactory)
	response = client.post("/clients", json=client_data)

	assert response.status_code == 201

	assert "id" in response.json or response.json.get("success") is True

	with client.application.app_context():
		assert Client.query.count() == initial_count + 1


def test_create_new_parking_with_factory(client):
	with client.application.app_context():
		initial_count = Parking.query.count()

	parking_data = factory.build(dict, FACTORY_CLASS=ParkingFactory)
	response = client.post("/parkings", json=parking_data)
	assert response.status_code == 201

	with client.application.app_context():
		assert Parking.query.count() == initial_count + 1

		new_parking = Parking.query.order_by(Parking.id.desc()).first()
		assert new_parking.count_available_places == new_parking.count_places
