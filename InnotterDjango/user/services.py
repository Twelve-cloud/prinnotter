from blog.services import set_blocking as block_page
from datetime import datetime, timedelta
from user.models import User


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
