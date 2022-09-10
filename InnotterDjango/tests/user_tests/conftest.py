import pytest


users = [
    {'email': 'ilya@mail.ru', 'username': 'ilya', 'password': '12341234'},
    {'email': 'artem@mail.ru', 'username': 'artem', 'password': '12341234'},
    {'email': 'gordey@mail.ru', 'username': 'gordey', 'password': '12341234'}
]

user_ids = [f"User: {user['username']}" for user in users]


@pytest.fixture(params=users, ids=user_ids)
def new_user(request):
    return request.param
