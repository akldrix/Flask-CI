from app.extensions import Base

from .parking import Parking
from .client import Client
from .client_parking import ClientParking

__all__ = ["Base", "Client", "Parking", "ClientParking"]
