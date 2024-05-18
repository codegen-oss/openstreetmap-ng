from sqlalchemy import (
    BigInteger,
    Enum,
    ForeignKey,
    Index,
    PrimaryKeyConstraint,
    SmallInteger,
    Unicode,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db.base import Base
from app.models.db.element import Element
from app.models.element_type import ElementType


class ElementMember(Base.NoID):
    __tablename__ = 'element_member'

    sequence_id: Mapped[int] = mapped_column(ForeignKey(Element.sequence_id), init=False, nullable=False)
    order: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    type: Mapped[ElementType] = mapped_column(Enum('node', 'way', 'relation', name='element_type'), nullable=False)
    id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role: Mapped[str] = mapped_column(Unicode(255), nullable=False)

    __table_args__ = (
        # could make primary key client-sided, and switch to brim index (to reduce disk use)
        # preparing data would require sorting by sequence_id
        PrimaryKeyConstraint(sequence_id, order, name='element_member_pkey'),
        Index('element_member_idx', type, id, sequence_id),
    )