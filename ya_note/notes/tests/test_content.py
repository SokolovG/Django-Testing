from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestListPage(TestCase):
    """
    Класс проверяет наполнение страницы
    для авторизованного и анонимного пользователя.
    """
    @classmethod
    def setUpTestData(cls):
        # Создаем автора, читателя, и саму заметку.
        cls.author = User.objects.create(username='admin')
        cls.reader = User.objects.create(username='no_admin')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='zag',
                                       author=cls.author)

    def test_note_in_list(self):
        # Проверяем что у анонимного юзера нет заметок.
        url = reverse('notes:list')
        users_note_in_list = (
            (self.author, True),
            (self.reader, False)
        )

        for user, note_in_list in users_note_in_list:
            with self.subTest(user=user, note_in_list=note_in_list):
                self.client.force_login(user)
                response = self.client.get(url)
                objets_list = response.context['object_list']
                assert (self.note in objets_list) is note_in_list


class TestContainForm(TestCase):
    """
    Класс проверяет, что у авторизированного
    пользователя есть форма.
    """
    @classmethod
    def setUpTestData(cls):
        # Создаем автора и саму заметку.
        cls.author = User.objects.create(username='admin')
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='zag',
                                       author=cls.author)

    def test_pages_contain_form(self):
        # Проверяем что у авторизированного юзера есть форма.
        self.client.force_login(self.author)
        urls = (
            ('notes:edit', (self.note.slug,)),
            ('notes:add', None)
        )
        for name, args in urls:
            with self.subTest(name=name, args=args):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
