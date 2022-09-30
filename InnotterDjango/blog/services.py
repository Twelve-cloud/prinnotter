from InnotterDjango.tasks import send_notification_about_new_post
from django.shortcuts import get_object_or_404
from blog.models import Page, Post
from user.models import User
from typing import List
import datetime


def set_blocking(page: Page, blocking_period: datetime) -> None:
    """
    set_blocking: set blocking_period parameter to unblock_date field of page.
    if blocking_period == None then page's not blocked.
    """
    page.unblock_date = blocking_period
    page.save()


def follow_page(page: Page, user: User) -> None:
    """
    follow_page: if page is private, request will be in follow_requests.
    if page is not private request will be accepted and it will be in followers.
    if request has already in followers or follow_requests it will be canceled.
    """
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


def like_or_unlike_post(post: Post, user: User) -> None:
    """
    like_or_unlike_post: if like has already been on the post it will
    be canceled, otherwise post will be liked.
    """
    if user in post.users_liked.all():
        post.users_liked.remove(user.pk)
    else:
        post.users_liked.add(user.pk)


def add_user_to_followers(page: Page, user_id: int) -> None:
    """
    add_user_to_followers: remove user request from follow_requests and
    add it to followers.
    """
    user = get_object_or_404(User, pk=user_id)
    if user in page.follow_requests.all():
        page.follow_requests.remove(user.pk)
        page.followers.add(user.pk)


def add_all_users_to_followers(page: Page) -> None:
    """
    add_all_users_to_followers: remove all user requests from follow_requests
    and add all users to followers.
    """
    for user in page.follow_requests.all():
        add_user_to_followers(page, user.pk)


def remove_user_from_requests(page: Page, user_id: int) -> None:
    """
    remove_user_from_requests: remove user request from follow_requests.
    """
    user = get_object_or_404(User, pk=user_id)
    if user in page.follow_requests.all():
        page.follow_requests.remove(user.pk)


def remove_all_users_from_requests(page: Page) -> None:
    """
    remove_all_users_from_requests: remove all user requests
    from follow_requests.
    """
    for user in page.follow_requests.all():
        remove_user_from_requests(page, user.pk)


def search_pages_by_params(*args: tuple, **kwargs: dict) -> List[Page]:
    """
    search_pages_by_params: returns pages were found by params.
    """
    return Page.objects.filter(**kwargs)


def send_notification_to_followers(parent_page_id: int, posts_url: str) -> None:
    """
    send_notification_to_followers: send notification to all followers
    of a page about new post.
    """
    page = Page.objects.get(pk=parent_page_id)
    user_emails = list(page.followers.values_list('email', flat=True))
    send_notification_about_new_post.delay(page.name, user_emails, posts_url)
