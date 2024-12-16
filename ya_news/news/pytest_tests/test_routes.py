from http import HTTPStatus

import pytest
from django.test import Client
from pytest_django.asserts import assertRedirects


anonym = Client()
not_author = pytest.lazy_fixture('not_author_client')
author = pytest.lazy_fixture('author_client')

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND


@pytest.mark.parametrize(
    'url, user, status',
    (
        (pytest.lazy_fixture('home_url'), anonym, OK),
        (pytest.lazy_fixture('login_url'), anonym, OK),
        (pytest.lazy_fixture('logout_url'), anonym, OK),
        (pytest.lazy_fixture('signup_url'), anonym, OK),
        (pytest.lazy_fixture('detail_url'), anonym, OK),
        (pytest.lazy_fixture('edit_url'), not_author, NOT_FOUND),
        (pytest.lazy_fixture('edit_url'), author, OK),
        (pytest.lazy_fixture('delete_url'), not_author, NOT_FOUND),
        (pytest.lazy_fixture('delete_url'), author, OK),
    )
)
def test_base_pages_availability_for_anonymous_user(client,
                                                    url,
                                                    user,
                                                    status,
                                                    db_auto_use):
    """Доступ к основным страницам."""
    response = user.get(url)
    assert response.status_code == status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('delete_url'))
)
def test_redirect_for_anonymous_client(client, url, get_id, login_url):
    """Проверка на переадресацию для анонимного юзера."""
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)
