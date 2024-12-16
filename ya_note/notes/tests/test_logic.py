from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .contstans import (DELETE_URL,
                        EDIT_URL,
                        ADD_URL,
                        SUCCESS_URL)
from .common import BaseTestClass

User = get_user_model()


class TestNoteCreation(BaseTestClass):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.NOTE_TITLE,
                         'text': cls.NOTE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        """
        Тест проверки запрета создания
        заметки неавторизованному пользователю.
        """
        Note.objects.all().delete()
        self.client.post(reverse(ADD_URL), data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_user_can_create_note(self):
        """
        Тест проверки возможности создания
        заметки авторизованному пользователю.
        """
        note_count = Note.objects.count()
        response = self.client_auth.post(reverse(ADD_URL),
                                         data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        self.assertEqual(Note.objects.count(), note_count + 1)
        note = Note.objects.last()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.NOTE_TITLE)
        self.assertEqual(note.author, self.author)


class TestSlugField(BaseTestClass):
    NEW_NOTE_TEXT = 'Новый текст заметки'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.NEW_NOTE_TEXT,
                         'text': cls.NOTE_TEXT,
                         'slug': cls.NOTE_SLUG}

    def test_not_unique_slug(self):
        """
        Тест проверки уникальности
        поля slug при создании заметки.
        """
        note_count = Note.objects.count()
        response = self.client_auth.post(reverse(ADD_URL),
                                         data=self.form_data)
        self.assertFormError(
            response, 'form', 'slug', errors=(self.note.slug + WARNING))
        assert Note.objects.count() == note_count

    def test_empty_slug(self):
        """Тест проверки отправки формы с пустым полем slug."""
        note_count = Note.objects.count()
        self.form_data.pop('slug')
        response = self.client_auth.post(reverse(ADD_URL),
                                         data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        assert Note.objects.count() == note_count + 1
        new_note = Note.objects.last()
        expected_slug = slugify(self.form_data['title'])
        assert new_note.slug == expected_slug


class TestNoteEditDelete(BaseTestClass):
    NEW_NOTE_TITLE = 'New title'
    NEW_NOTE_TEXT = 'New Text'

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.form_data = {'title': cls.NEW_NOTE_TITLE,
                         'text': cls.NEW_NOTE_TEXT}

    def test_author_can_edit_note(self):
        """
        Тест проверки возможности
        редактирования заметки для ее автора.
        """
        response = self.client_auth.post(reverse(EDIT_URL,
                                                 args=(self.note.slug,)),
                                         data=self.form_data)
        self.assertRedirects(response, reverse(SUCCESS_URL))
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)
        self.assertEqual(self.note.title, self.NEW_NOTE_TITLE)

    def test_reader_cant_edit_note(self):
        """
        Тест проверки запрета
        редактирования заметки для читателя.
        """
        response = self.not_author_client.post(reverse(
            EDIT_URL, args=(self.note.slug,)),
            data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        # self.note.refresh_from_db()
        note_from_db = Note.objects.get(pk=self.note.id)
        self.assertEqual(self.NOTE_TEXT, note_from_db.text)
        self.assertEqual(self.NOTE_TITLE, note_from_db.title)

    def test_author_can_delete_note(self):
        """
        Тест проверки возможности
        удаления заметки для ее автора.
        """
        note_count = Note.objects.count()
        response = self.client_auth.delete(reverse(DELETE_URL,
                                                   args=(self.note.slug,)))
        self.assertRedirects(response, reverse(SUCCESS_URL))
        self.assertEqual(Note.objects.count(), note_count - 1)

    def test_reader_cant_delete_note(self):
        """
        Тест проверки запрета
        удаления заметки для читателя.
        """
        note_count = Note.objects.count()
        response = self.not_author_client.delete(
            reverse(DELETE_URL,
                    args=(self.note.slug,)))
        self.assertEqual(response.status_code, self.NOT_FOUND)
        self.assertEqual(Note.objects.count(), note_count)
