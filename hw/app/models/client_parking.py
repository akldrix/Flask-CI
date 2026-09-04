from typing import Optional

from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint, DateTime, ForeignKey
from datetime import datetime


class ClientParking(db.Model):
	__tablename__ = 'client_parking'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	client_id: Mapped[Optional[int]] = mapped_column(ForeignKey('client.id'))
	parking_id: Mapped[Optional[int]] = mapped_column(ForeignKey('parking.id'))
	time_in: Mapped[Optional[datetime]] = mapped_column(DateTime)
	time_out: Mapped[Optional[datetime]] = mapped_column(DateTime)

	__table_args__ = (
		UniqueConstraint('client_id', 'parking_id'),
	)

	def to_dict(self):
		return {
			'id': self.id,
			'client_id': self.client_id,
			'parking_id': self.parking_id,
			'time_in': self.time_in,
			'time_out': self.time_out,
		}