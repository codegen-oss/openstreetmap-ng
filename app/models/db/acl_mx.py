from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db.acl import ACL


class ACLMX(ACL):
    __tablename__ = 'acl_mx'

    mx: Mapped[str] = mapped_column(String, nullable=False)
