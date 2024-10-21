from datetime import datetime

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from app.lib.crypto import HASH_SIZE
from app.models.db.base import Base
from app.models.db.created_at_mixin import CreatedAtMixin
from app.models.db.user import User


# TODO: validate from address
class UserToken(Base.ZID, CreatedAtMixin):
    __abstract__ = True

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    user_email_hashed: Mapped[bytes] = mapped_column(LargeBinary(HASH_SIZE), nullable=False)
    token_hashed: Mapped[bytes] = mapped_column(LargeBinary(HASH_SIZE), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(True), nullable=False)

    # requires @declared_attr since it is __abstract__
    @declared_attr
    @classmethod
    def user(cls) -> Mapped[User]:
        return relationship(User, foreign_keys=(cls.user_id,), lazy='raise', init=False, innerjoin=True)
