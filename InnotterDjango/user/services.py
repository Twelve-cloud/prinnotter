from user.models import User


def set_blocking(user: User, is_blocked: bool) -> None:
    """
    set_blocking: set is_blocked parameter to is_blocked field of user.
    if is_blocked == False, user's not blocked, otherwise user's blocked.
    """
    user.is_blocked = is_blocked
    user.save()
