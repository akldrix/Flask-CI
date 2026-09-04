from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import Base


class Parking(Base):
    __tablename__ = "parking"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    opened: Mapped[bool] = mapped_column(Boolean)
    count_places: Mapped[int] = mapped_column(Integer, nullable=False)
    count_available_places: Mapped[int] = mapped_column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "opened": self.opened,
            "count_places": self.count_places,
            "count_available_places": self.count_available_places,
        }
