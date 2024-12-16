from django.contrib.auth import get_user_model
from django.urls import reverse

from .common import BaseTestClass

User = get_user_model()


class TestRoutes(BaseTestClass):
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
        super().setUpTestData()

    def test_pages_availability(self):
        """Доступ к основным страницам."""
        urls = (
            ('notes:home', None, self.reader, self.OK),
            ('users:login', None, self.reader, self.OK),
            ('users:logout', None, self.reader, self.OK),
            ('users:signup', None, self.reader, self.OK),
            ('notes:edit', self.slug, self.reader, self.NOT_FOUND),
            ('notes:delete', self.slug, self.reader, self.NOT_FOUND),
            ('notes:detail', self.slug, self.reader, self.NOT_FOUND),
            ('notes:edit', self.slug, self.author, self.OK),
            ('notes:delete', self.slug, self.author, self.OK),
            ('notes:detail', self.slug, self.author, self.OK),

            ('notes:list', None, self.author, self.OK),
            ('notes:add', None, self.author, self.OK),
            ('notes:success', None, self.author, self.OK)
        )
        for name, arg, user, status in urls:
            with self.subTest(name=name, user=user):
                self.client.force_login(user)
                url = reverse(name, args=arg)
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка на редирект для анонимного пользователя."""
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
