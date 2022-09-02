from user.services import get_user_by_id
from blog.models import Page, Post
from user.models import User


def get_page_by_id(page_id):
    try:
        page = Page.objects.get(pk=page_id)
        return page
    except Page.DoesNotExist:
        return None


def get_post_by_id(post_id):
    try:
        post = Post.objects.get(pk=post_id)
        return post
    except Post.DoesNotExist:
        return None


def set_blocking(page, blocking_period):
    page.unblock_date = blocking_period
    page.save()


def follow_page(page, user):
    if page.is_private:
        if user in page.follow_requests.all():
            page.follow_requests.remove(user.pk)
        else:
            page.follow_requests.add(user.pk)
    else:
        if user in page.followers.all():
            page.followers.remove(user.pk)
        else:
            page.followers.add(user.pk)


def like_post(post, user):
    if user in post.users_liked.all():
        post.users_liked.remove(user.pk)
    else:
        post.users_liked.add(user.pk)


def add_user_to_followers(page, user_id):
    try:
        user = get_user_by_id(user_id)
        if user in page.follow_requests.all():
            page.follow_requests.remove(user.pk)
            page.followers.add(user.pk)
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def add_all_users_to_followers(page):
    for user in page.follow_requests.all():
        add_user_to_followers(page, user.pk)


def remove_user_from_requests(page, user_id):
    try:
        user = get_user_by_id(user_id)
        if user in page.follow_requests.all():
            page.follow_requests.remove(user.pk)
            return True
        else:
            return False
    except User.DoesNotExist:
        return False


def remove_all_users_from_requests(page):
    for user in page.follow_requests.all():
        remove_user_from_requests(page, user.pk)
