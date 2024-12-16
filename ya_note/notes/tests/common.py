from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from .contstans import DETAIL_URl, LOGIN_URL

User = get_user_model()


class BaseTestClass(TestCase):
    NOTE_TEXT = 'Текст заметки'
    NOTE_TITLE = 'Заметка'
    NOTE_SLUG = 'slug'


    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='admin')
        cls.reader = User.objects.create(username='no_admin')
        cls.note = Note.objects.create(title=cls.NOTE_TITLE,
                                       text=cls.NOTE_TEXT,
                                       slug=cls.NOTE_SLUG,
                                       author=cls.author)

        cls.OK = HTTPStatus.OK
        cls.NOT_FOUND = HTTPStatus.NOT_FOUND
        cls.slug = (cls.note.slug,)
        cls.client_auth = Client()
        cls.client_auth.force_login(cls.author)

        cls.detail_url = reverse(DETAIL_URl, args=(cls.NOTE_SLUG,))
        cls.login_url = reverse(LOGIN_URL)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.reader)
