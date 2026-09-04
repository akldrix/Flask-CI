from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import text
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from app import create_app
from app.extensions import db as _db
from app.models import Client, ClientParking, Parking

TEST_DB_URL = "postgresql+psycopg2://admin:admin@localhost:5432/my_db_test"


@pytest.fixture(scope="session")
def app():
    if not database_exists(TEST_DB_URL):
        create_database(TEST_DB_URL)
    app = create_app(
        config_override={"TESTING": True, "SQLALCHEMY_DATABASE_URI": TEST_DB_URL}
    )

    with app.app_context():
        _db.create_all()

        yield app

        _db.drop_all()


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.session.remove()
        _db.session.expunge_all()
        _db.session.execute(
            text(
                "TRUNCATE TABLE client, parking,"
                " client_parking RESTART IDENTITY CASCADE;"
            )
        )
        _db.session.commit()

        test_client = Client(
            name="Ivan",
            surname="Ivanov",
            credit_card="Visa",
            card_number="123",
        )

        test_parking = Parking(
            address="Main St.", opened=True, count_places=20, count_available_places=20
        )

        entry_time = datetime.now(timezone.utc)
        exit_time = entry_time + timedelta(hours=2)

        _db.session.add(test_client)
        _db.session.add(test_parking)
        _db.session.flush()
        test_log = ClientParking(
            client_id=test_client.id,
            parking_id=test_parking.id,
            time_in=entry_time,
            time_out=exit_time,
        )
        _db.session.add(test_log)
        _db.session.commit()

        yield _db
        _db.session.remove()


@pytest.fixture(scope="session")
def client(app, db):
    return app.test_client()
