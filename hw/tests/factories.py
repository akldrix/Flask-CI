import random
import factory
from faker import Faker

from app.extensions import db
from app.models import Client, Parking

fake = Faker()
class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Client
		sqlalchemy_session = db.session
		sqlalchemy_session_persistence = 'commit'

	name = factory.Faker("first_name")
	surname = factory.Faker("last_name")

	credit_card = factory.LazyAttribute(
		lambda _: random.choice(["Visa", "MasterCard", "Mir"])
	)
	card_number = factory.LazyAttribute(
		lambda o: fake.credit_card_number()[:10] if o.credit_card else None
	)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
	class Meta:
		model = Parking
		sqlalchemy_session = db.session
		sqlalchemy_session_persistence = 'commit'

	address = factory.Faker("address")
	opened = factory.Faker("boolean", chance_of_getting_true=80)
	count_places = factory.LazyAttribute(lambda _: random.randint(10, 50))
	count_available_places = factory.LazyAttribute(lambda o: o.count_places)
