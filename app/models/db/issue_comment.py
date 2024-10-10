from sqlalchemy import ForeignKey, LargeBinary, StringText
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.lib.crypto import HASH_SIZE
from app.lib.rich_text import RichTextMixin, TextFormat
from app.limits import ISSUE_COMMENT_BODY_MAX_LENGTH
from app.models.db.base import Base
from app.models.db.created_at_mixin import CreatedAtMixin
from app.models.db.issue import Issue
from app.models.db.user import User


class IssueComment(Base.Sequential, CreatedAtMixin, RichTextMixin):
    __tablename__ = 'issue_comment'
    __rich_text_fields__ = (('body', TextFormat.markdown),)

    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    user: Mapped[User] = relationship(lazy='raise', innerjoin=True)
    issue_id: Mapped[int] = mapped_column(ForeignKey(Issue.id), nullable=False)
    body: Mapped[str] = mapped_column(StringText, nullable=False)
    body_rich_hash: Mapped[bytes | None] = mapped_column(
        LargeBinary(HASH_SIZE),
        init=False,
        nullable=True,
        server_default=None,
    )

    # runtime
    body_rich: str | None = None

    @validates('body')
    def validate_body(self, _: str, value: str) -> str:
        if len(value) > ISSUE_COMMENT_BODY_MAX_LENGTH:
            raise ValueError(f'Comment body is too long ({len(value)} > {ISSUE_COMMENT_BODY_MAX_LENGTH})')
        return value
