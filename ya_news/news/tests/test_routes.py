from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from news.models import Comment, News
from .constants import (
    DELETE_URL, DETAIL_URL, EDIT_URL, HOME_URL,
    LOGIN_URL, LOGOUT_URL, SIGNUP_URL
)

# Получаем модель пользователя.
User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        Создаем автора, читателя, саму новость, и комментарий
        для будущего тестирования.
        """
        cls.news = News.objects.create(title='Заголовок', text='Текст')
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')

        cls.comment = Comment.objects.create(
            news=cls.news,
            author=cls.author,
            text='Текст комментария'
        )

    def test_pages_availability(self):
        """Доступ к основным страницам."""
        urls = (
            (HOME_URL, None),
            (DETAIL_URL, (self.news.id,)),
            (LOGIN_URL, None),
            (LOGOUT_URL, None),
            (SIGNUP_URL, None),
        )

        for name, arg in urls:
            with self.subTest(name=name):
                url = reverse(name, args=arg)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_for_comment_edit_and_delete(self):
        """Проверка на доступ для редактирования и удаления."""
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )

        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (EDIT_URL, DELETE_URL):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.comment.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_for_anonymous_client(self):
        """Проверка на редирект для анонимного пользователя."""
        login_url = reverse('users:login')
        for name in (EDIT_URL, DELETE_URL):
            with self.subTest(name=name):
                url = reverse(name, args=(self.comment.id,))
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
