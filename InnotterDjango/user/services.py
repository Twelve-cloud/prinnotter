from user.models import User


def get_user_by_id(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user
    except User.DoesNotExist:
        return None


def set_blocking(user, is_blocked):
    user.is_blocked = is_blocked
    user.save()
