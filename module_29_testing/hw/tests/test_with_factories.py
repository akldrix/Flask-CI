import factory
from sqlalchemy import func, select

from app.extensions import db
from app.models import Client, Parking
from tests.factories import ClientFactory, ParkingFactory


def test_create_new_client_with_factory(client):
    with client.application.app_context():
        initial_count = db.session.scalar(
            select(func.count()).select_from(Client)) or 0
    client_data = factory.build(dict, FACTORY_CLASS=ClientFactory)
    response = client.post("/clients", json=client_data)

    assert response.status_code == 201

    assert "id" in response.json or response.json.get("success") is True

    with client.application.app_context():
        current_count = db.session.scalar(
            select(func.count()).select_from(Client)) or 0
        assert current_count == initial_count + 1


def test_create_new_parking_with_factory(client):
    with client.application.app_context():
        initial_count = (
            db.session.scalar(select(func.count()).select_from(Parking)) or 0
        )

    parking_data = factory.build(dict, FACTORY_CLASS=ParkingFactory)
    response = client.post("/parkings", json=parking_data)
    assert response.status_code == 201

    with client.application.app_context():
        current_count = (
            db.session.scalar(select(func.count()).select_from(Parking)) or 0
        )
        assert current_count == initial_count + 1

        stmt = select(Parking).order_by(Parking.id.desc())
        new_parking = db.session.scalar(stmt)

        assert new_parking.count_available_places == new_parking.count_places
