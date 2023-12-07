from sqlalchemy import ForeignKey, LargeBinary, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.crypto import HASH_SIZE
from lib.rich_text import RichTextMixin
from models.db.base import Base
from models.db.cache_entry import CacheEntry
from models.db.changeset import Changeset
from models.db.created_at_mixin import CreatedAtMixin
from models.db.user import User
from models.text_format import TextFormat


class ChangesetComment(Base.Sequential, CreatedAtMixin, RichTextMixin):
    __tablename__ = 'changeset_comment'
    __rich_text_fields__ = (('body', TextFormat.plain),)

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    user: Mapped[User] = relationship(lazy='raise')
    changeset_id: Mapped[int] = mapped_column(ForeignKey(Changeset.id), nullable=False)
    changeset: Mapped[Changeset] = relationship(lazy='raise')
    body: Mapped[str] = mapped_column(UnicodeText, nullable=False)
    body_rich_hash: Mapped[bytes | None] = mapped_column(LargeBinary(HASH_SIZE), nullable=True, default=None)
    body_rich: Mapped[CacheEntry | None] = relationship(
        CacheEntry,
        primaryjoin=CacheEntry.id == body_rich_hash,
        viewonly=True,
        default=None,
        lazy='raise',
    )
