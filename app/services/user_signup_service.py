from fastapi import Request

from app.db import DB
from app.lib_cython.auth import auth_user, manual_auth_context
from app.lib_cython.email import validate_email_deliverability
from app.lib_cython.message_collector import MessageCollector
from app.lib_cython.password_hash import PasswordHash
from app.lib_cython.translation import t, translation_languages
from app.models.db.user import User
from app.models.mail_from_type import MailFromType
from app.models.msgspec.user_token_struct import UserTokenStruct
from app.models.str import EmailStr, PasswordStr, UserNameStr
from app.models.user_status import UserStatus
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.services.mail_service import MailService
from app.services.user_token_account_confirm_service import UserTokenAccountConfirmService
from app.utils import parse_request_ip


class UserSignupService:
    @staticmethod
    async def signup(
        request: Request,
        collector: MessageCollector,
        *,
        display_name: UserNameStr,
        email: EmailStr,
        password: PasswordStr,
    ) -> UserTokenStruct:
        """
        Create a new user.

        Returns a new user session token.
        """

        # some early validation
        if not await UserRepository.check_display_name_available(display_name):
            collector.raise_error('display_name', t('user.display_name_already_taken'))
        if not await UserRepository.check_email_available(email):
            collector.raise_error('email', t('user.email_already_taken'))
        if not await validate_email_deliverability(email):
            collector.raise_error('email', t('user.invalid_email'))

        # precompute values to reduce transaction time
        password_hashed = PasswordHash.default().hash(password)
        created_ip = parse_request_ip(request)
        languages = translation_languages()

        # create user
        async with DB() as session:
            user = User(
                email=email,
                display_name=display_name,
                password_hashed=password_hashed,
                created_ip=created_ip,
                status=UserStatus.pending,
                auth_provider=None,  # TODO: support
                auth_uid=None,
                languages=languages,
            )
            session.add(user)

        with manual_auth_context(user):
            await UserSignupService.send_confirm_email()

        return await AuthService.create_session(user.id)

    @staticmethod
    async def send_confirm_email() -> None:
        """
        Send a confirmation email for the account.
        """

        token = await UserTokenAccountConfirmService.create()

        await MailService.schedule(
            from_user=None,
            from_type=MailFromType.system,
            to_user=auth_user(),
            subject='TODO',  # TODO:
            template_name='TODO',
            template_data={'token': str(token)},
        )