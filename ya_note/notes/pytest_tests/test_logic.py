from pytest_django.asserts import assertRedirects, assertFormError
import pytest

from pytils.translit import slugify
from http import HTTPStatus

from notes.models import Note
from notes.forms import WARNING


def test_user_can_create_note(author_client,
                              author,
                              form_data,
                              add_url,
                              success_url):
    # Проверка на создание заметки для авторизированного пользователя.
    url = add_url
    response = author_client.post(url, form_data)
    assertRedirects(response, success_url)
    assert Note.objects.count() == 1

    new_note = Note.objects.get()
    assert new_note.title == form_data['title']
    assert new_note.text == form_data['text']
    assert new_note.slug == form_data['slug']
    assert new_note.author == author


@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client,
                                         form_data,
                                         login_url,
                                         add_url):
    # Проверка на создание заметки для не авторизированного пользователя.
    url = add_url
    response = client.post(url, data=form_data)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Note.objects.count() == 0


def test_not_unique_slug(author_client, note, form_data, add_url):
    # Проверка на создание нескольких заметок с одинаковым slug.
    url = add_url
    form_data['slug'] = note.slug
    response = author_client.post(url, data=form_data)
    assertFormError(response, 'form', 'slug', errors=(note.slug + WARNING))
    assert Note.objects.count() == 1


def test_empty_slug(author_client, form_data, add_url, success_url):
    # Проверка на создание заметки без указания slug.
    url = add_url
    form_data.pop('slug')
    response = author_client.post(url, data=form_data)
    assertRedirects(response, success_url)
    assert Note.objects.count() == 1
    new_note = Note.objects.get()
    expected_slug = slugify(form_data['title'])
    assert new_note.slug == expected_slug


def test_author_can_edit_note(author_client,
                              form_data,
                              note,
                              edit_url,
                              success_url):
    # Проверка, что авторизированный пользователь может редактировать.
    url = edit_url
    response = author_client.post(url, form_data)
    assertRedirects(response, success_url)
    note.refresh_from_db()
    assert note.title == form_data['title']
    assert note.text == form_data['text']
    assert note.slug == form_data['slug']


def test_other_user_cant_edit_note(not_author_client,
                                   form_data,
                                   note,
                                   edit_url):
    # Проверка, что не авторизированный пользователь не может редактировать.
    url = edit_url
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Note.objects.get(id=note.id)
    assert note.title == note_from_db.title
    assert note.text == note_from_db.text
    assert note.slug == note_from_db.slug


def test_author_can_delete_note(author_client, delete_url, success_url):
    # Проверка, что авторизированный пользователь может удалять заметки.
    url = delete_url
    response = author_client.post(url)
    assertRedirects(response, success_url)
    assert Note.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client, delete_url, login_url):
    # Проверка, что пользователь без авторизации не может удалять заметки.
    url = delete_url
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Note.objects.count() == 1
