from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.extensions import Base


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    credit_card: Mapped[str] = mapped_column(String(50))
    card_number: Mapped[str] = mapped_column(String(10))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "credit_card": self.credit_card,
            "card_number": self.card_number,
        }
