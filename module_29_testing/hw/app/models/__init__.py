from app.extensions import Base

from .client import Client
from .client_parking import ClientParking
from .parking import Parking

__all__ = ["Base", "Client", "ClientParking", "Parking"]
