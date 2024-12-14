import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects


@pytest.mark.django_db
@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('home_url'),
     pytest.lazy_fixture('login_url'),
     pytest.lazy_fixture('logout_url'),
     pytest.lazy_fixture('signup_url'))
)
def test_base_pages_availability_for_anonymous_user(client, url):
    # Доступ к основным страницам.
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_detail_page_availability_for_anonymous_user(client,
                                                     get_id,
                                                     detail_url):
    # Доступ к странице новости.
    response = client.get(detail_url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('delete_url'))
)
def test_availability_for_comment_edit_and_delete(client,
                                                  parametrized_client,
                                                  expected_status,
                                                  url):
    # Проверка на доступ для редактирования и удаления.
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('delete_url'))
)
def test_redirect_for_anonymous_client(client, url, get_id, login_url):
    # Проверка на переадресацию для анонимного юзера.
    excepted_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, excepted_url)
