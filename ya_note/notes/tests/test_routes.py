from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):
    """
    Класс отвечает за тестирование маршрутов, а именно:
    Доступность страниц
    Редирект для анонимны пользователей
    Доступ на страницы редактирования и удаления
    Доступ к страницам, требующие авторизации.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Создаем автора, читателя, и саму заметку,
        для будущего тестирования.
        """
        TITLE = 'Заголовок'
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(title=TITLE, text='Текст',
                                       author=cls.author,
                                       slug='slug')

    def test_pages_availability(self):
        # Доступ к основным страницам.
        urls = (
            ('notes:home', None),
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
        )
        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        # Проверка на редирект для анонимного пользователя.

        urls = (
            ('notes:detail', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:add', None),
            ('notes:success', None),
            ('notes:list', None)
        )

        login_url = reverse('users:login')
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_availability_for_comment_edit_and_delete(self):
        # Проверка на доступ для редактирования и удаления.

        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )

        urls = ('notes:edit', 'notes:delete', 'notes:detail')

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (urls):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_pages_availability_for_auth_user(self):
        # Проверка на доступ для страниц, требующих это.
        urls = ('notes:list', 'notes:add', 'notes:success')
        self.client.force_login(self.author)
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
