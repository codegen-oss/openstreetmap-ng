from pydantic import SecretStr
from sqlalchemy import ARRAY, Boolean, Enum, ForeignKey, Index, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.crypto import decrypt
from app.lib.image import AvatarType, Image
from app.limits import OAUTH_APP_NAME_MAX_LENGTH, OAUTH_APP_URI_MAX_LENGTH, STORAGE_KEY_MAX_LENGTH
from app.models.db.base import Base
from app.models.db.created_at_mixin import CreatedAtMixin
from app.models.db.updated_at_mixin import UpdatedAtMixin
from app.models.db.user import User
from app.models.scope import Scope
from app.models.types import StorageKey, Uri

_CLIENT_ID_AVATAR_MAP = {
    'SystemApp.web': '/static/img/favicon/256-app.webp',
    'SystemApp.id': '/static/img/brand/id-app.webp',
    'SystemApp.rapid': '/static/img/brand/rapid.webp',
}

_DEFAULT_AVATAR_URL = Image.get_avatar_url(AvatarType.default, app=True)


class OAuth2Application(Base.ZID, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = 'oauth2_application'

    user_id: Mapped[int | None] = mapped_column(ForeignKey(User.id), nullable=True)
    user: Mapped[User | None] = relationship(init=False, lazy='raise')
    name: Mapped[str] = mapped_column(String(OAUTH_APP_NAME_MAX_LENGTH), nullable=False)
    client_id: Mapped[str] = mapped_column(String(50), nullable=False)
    client_secret_encrypted: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    scopes: Mapped[tuple[Scope, ...]] = mapped_column(ARRAY(Enum(Scope), as_tuple=True, dimensions=1), nullable=False)
    is_confidential: Mapped[bool] = mapped_column(Boolean, nullable=False)  # TODO: support
    redirect_uris: Mapped[tuple[Uri, ...]] = mapped_column(
        ARRAY(String(OAUTH_APP_URI_MAX_LENGTH), as_tuple=True, dimensions=1), nullable=False
    )

    # defaults
    # TODO: avatars
    avatar_id: Mapped[StorageKey | None] = mapped_column(
        String(STORAGE_KEY_MAX_LENGTH),
        init=False,
        nullable=True,
        server_default=None,
    )

    __table_args__ = (Index('oauth2_application_client_id_idx', 'client_id', unique=True),)

    @property
    def client_secret(self) -> SecretStr:
        return SecretStr(decrypt(self.client_secret_encrypted))

    @property
    def avatar_url(self) -> str:
        """
        Get the url for the application's avatar image.
        """
        return (
            _CLIENT_ID_AVATAR_MAP.get(self.client_id, _DEFAULT_AVATAR_URL)
            if self.avatar_id is None
            else Image.get_avatar_url(AvatarType.custom, self.avatar_id)
        )

    @property
    def is_system_app(self) -> bool:
        """
        Check if the application is a system app.
        """
        return self.user_id is None

    @property
    def redirect_uris_str(self) -> str:
        """
        Get the application's redirect URIs as a single string.
        """
        return '\n'.join(self.redirect_uris)
