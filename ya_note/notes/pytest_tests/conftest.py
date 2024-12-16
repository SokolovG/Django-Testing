import pytest
from django.test.client import Client
from django.urls import reverse

from notes.models import Note


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    note = Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )
    return note


@pytest.fixture
def form_data():
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }


@pytest.fixture
def slug_for_args(note):
    return (note.slug,)


@pytest.fixture
def notes_url():
    return reverse('notes:list')


@pytest.fixture
def edit_url(slug_for_args):
    return reverse('notes:edit', args=(slug_for_args))


@pytest.fixture
def delete_url(slug_for_args):
    return reverse('notes:delete', args=(slug_for_args))


@pytest.fixture
def add_url():
    return reverse('notes:add')


@pytest.fixture
def success_url():
    return reverse('notes:success')


@pytest.fixture
def home_url():
    return reverse('notes:home')


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture(autouse=True)
def db_auto_use(db):
    return db
