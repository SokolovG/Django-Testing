from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from news.forms import CommentForm
from news.models import News, Comment
from .constants import HOME_URL, DETAIL_URL

User = get_user_model()


class TestContent(TestCase):
    """
    Данный класс отвечает за тестирование
    контента в проекте, а именно количество новостей,
    проверка форм у разных пользователей,
    проверка сортировки по дате.
    """

    @classmethod
    def setUpTestData(cls):
        # Создаем 11 новостей с разными датами.
        today = datetime.today()
        all_news = []
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
            news = News(title=f'Новость {index}',
                        text='Просто текст.',
                        date=today - timedelta(days=index))
            all_news.append(news)
        News.objects.bulk_create(all_news)

    def test_count_news(self):
        # Подсчитываем количество новостей.
        response = self.client.get(HOME_URL)
        objects_list = response.context['object_list']
        news_count = objects_list.count()
        self.assertEqual(news_count, settings.NEWS_COUNT_ON_HOME_PAGE)

    def test_news_order(self):
        # Проверяем сортировку новостей.
        response = self.client.get(HOME_URL)
        objects_list = response.context['object_list']
        all_dates = [news.date for news in objects_list]

        sorted_dates = sorted(all_dates, reverse=True)
        self.assertEqual(all_dates, sorted_dates)


class TestDetailPage(TestCase):
    """
    Данный класс отвечает за тестирование
    конкретной страницы новости.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Создаем новость, формируем на нее сразу маршрут, и создаем автора.
        Дальше меняем даты создания на разные
        для проверки в будущем на сортировку.
        """
        cls.news = News.objects.create(title='Тестовая новость',
                                       text='Просто текст.')
        cls.detail_url = reverse(DETAIL_URL, args=(cls.news.id,))
        cls.author = User.objects.create(username='Комментатор')

        now = timezone.now()
        for index in range(10):
            comment = Comment.objects.create(
                news=cls.news, author=cls.author, text=f'Tекст {index}',
            )
            comment.created = now + timedelta(days=index)
            comment.save()

    def test_comments_order(self):
        # Проверяем что наши комментарии отсортированы.
        response = self.client.get(self.detail_url)
        self.assertIn('news', response.context)
        news = response.context['news']
        all_comments = news.comment_set.all()
        all_timestamps = [comment.created for comment in all_comments]
        sorted_timestamps = sorted(all_timestamps)
        self.assertEqual(all_timestamps, sorted_timestamps)

    def test_anonymous_client_has_no_form(self):
        # Проверяем что у анонимного юзера нет формы.
        response = self.client.get(self.detail_url)
        self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        # Проверяем что у авторизированного юзера есть форма.
        self.client.force_login(self.author)
        response = self.client.get(self.detail_url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], CommentForm)
