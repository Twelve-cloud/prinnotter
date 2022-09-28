from InnotterDjango.tasks import send_email_to_verify_account
from blog.services import set_blocking as block_page
from jwt_auth.services import generate_token
from datetime import datetime, timedelta
from user.models import User
from typing import List


def set_blocking(user: User, is_blocked: bool) -> None:
    """
    set_blocking: set is_blocked parameter to is_blocked field of user.
    if is_blocked == False, user's not blocked, otherwise user's blocked.
    """
    user.is_blocked = is_blocked
    user.save()


def block_all_users_pages(user: User, is_blocked: bool) -> None:
    """
    block_all_users_pages: blocks every page if user will be blocked.
    otherwise unblocks every page of user.
    """
    if is_blocked:
        blocking_period = datetime.now() + timedelta(days=365 * 10)
    else:
        blocking_period = None

    for page in user.pages.all():
        block_page(page, blocking_period)


def search_users_by_params(*args: tuple, **kwargs: dict) -> List[User]:
    """
    search_users_by_params: returns users were found by params.
    """
    return User.objects.filter(**kwargs)


def send_verification_link(link: str, email: str) -> None:
    """
    send_verification_link: send verification link to user email.
    """
    verify_url = link + '?token=' + generate_token(type='access', user_id=email)
    send_email_to_verify_account.delay(email, verify_url)
