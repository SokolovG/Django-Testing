import pytest

from notes.forms import NoteForm


@pytest.mark.parametrize(
    'parametrized_client, note_in_list',
    (
        (pytest.lazy_fixture('author_client'), True),
        (pytest.lazy_fixture('not_author_client'), False)
    )
)
def test_note_for_different_users(parametrized_client,
                                  note,
                                  note_in_list,
                                  notes_url):
    """Проверяем, что если пользователь автор, то ему видны заметки."""
    url = notes_url
    response = parametrized_client.get(url)
    object_list = response.context['object_list']
    assert (note in object_list) is note_in_list


@pytest.mark.parametrize(
    'name',
    (
        (pytest.lazy_fixture('edit_url')),
        (pytest.lazy_fixture('add_url'))
    )
)
def test_pages_contains_form(author_client, name):
    # Проверка, что у автора есть форма.

    response = author_client.get(name)
    assert 'form' in response.context
    assert isinstance(response.context['form'], NoteForm)
