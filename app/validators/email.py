import logging

from annotated_types import Predicate
from anyio import create_task_group
from dns.asyncresolver import Resolver
from dns.exception import DNSException, Timeout
from dns.rdatatype import RdataType
from dns.resolver import NXDOMAIN, NoAnswer, NoNameservers
from email_validator import EmailNotValidError
from email_validator import validate_email as validate_email_

from app.config import TEST_ENV
from app.limits import EMAIL_DELIVERABILITY_CACHE_EXPIRE, EMAIL_DELIVERABILITY_DNS_TIMEOUT
from app.services.cache_service import CacheService

_cache_context = 'EmailDeliverability'

_resolver = Resolver()
_resolver.timeout = EMAIL_DELIVERABILITY_DNS_TIMEOUT.total_seconds()
_resolver.lifetime = _resolver.timeout + 2
_resolver.cache = None  # using redis cache
_resolver.retry_servfail = True


def validate_email(email: str) -> str:
    """
    Validate and normalize email address.

    Raises ValueError on error.

    >>> validate_email('example@ツ.ⓁⒾⒻⒺ')
    'example@ツ.life'
    """

    try:
        info = validate_email_(
            email,
            check_deliverability=False,
            test_environment=TEST_ENV,
        )
    except EmailNotValidError as e:
        raise ValueError(f'Invalid email address {email!r}') from e

    return info.normalized


async def validate_email_deliverability(email: str) -> None:
    """
    Validate deliverability of an email address.

    Raises ValueError on error.
    """

    try:
        info = validate_email_(
            email,
            check_deliverability=False,
            test_environment=TEST_ENV,
        )
    except EmailNotValidError as e:
        raise ValueError(f'Invalid email address {email!r}') from e

    domain = info.ascii_domain

    async def factory() -> bytes:
        logging.debug('Email domain deliverability cache miss for %r', domain)
        success = await _check_domain_deliverability(domain)
        return b'\xff' if success else b'\x00'

    cache_entry = await CacheService.get_one_by_key(
        key=domain,
        context=_cache_context,
        factory=factory,
        ttl=EMAIL_DELIVERABILITY_CACHE_EXPIRE,
    )

    success = cache_entry.value == b'\xff'
    logging.info('Email domain deliverability for %r: %s', domain, success)

    if not success:
        raise ValueError(f'Undeliverable email domain {domain!r}')


async def _check_domain_deliverability(domain: str) -> bool:
    success = False

    async with create_task_group() as tg:

        async def task(rd: RdataType):
            nonlocal success

            try:
                answer = await _resolver.resolve(domain, rd)
                rrset = answer.rrset
            except NoAnswer:
                rrset = None
            except NXDOMAIN:
                return  # domain does not exist, skip further checks
            except (NoNameservers, Timeout):
                raise  # something's wrong on our side
            except DNSException:
                # some other error, log and proceed gracefully
                logging.warning('DNS error for %r (%r)', domain, rd)
                rrset = None

            if rd == RdataType.MX:
                if not rrset:
                    # on implicit mx, try a/aaaa
                    tg.start_soon(task, RdataType.A)
                    tg.start_soon(task, RdataType.AAAA)
                    return

                # mx - treat not-null answer as success
                # sort answers by preference in descending order
                rrset_by_preference = sorted(rrset, key=lambda r: r.preference, reverse=True)
                exchange = str(rrset_by_preference[0].exchange)
                success = exchange != '.'
            else:
                # a/aaaa - treat any answer as success and cancel other tasks
                if rrset:
                    success = True
                    tg.cancel_scope.cancel()

        tg.start_soon(task, RdataType.MX)

    return success


EmailStrValidator = Predicate(validate_email)
