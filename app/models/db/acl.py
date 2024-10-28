from sqlalchemy import ARRAY, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db.base import Base


class ACL(Base.ZID):
    __abstract__ = True

    restrictions: Mapped[list[str]] = mapped_column(ARRAY(String, dimensions=1), nullable=False)
