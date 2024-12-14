import pytest
from datetime import datetime, timedelta

from django.test.client import Client
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

from news.models import Comment, News


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
def news(author):
    news = News.objects.create(title='Название новости', text='Текст новости')
    return news


@pytest.fixture()
def bulk_news(author):
    all_news = []
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news = News(title=f'Новость {index}',
                    text='Просто текст.',
                    date=today - timedelta(days=index))
        all_news.append(news)
        News.objects.bulk_create(all_news)


@pytest.fixture
def comments_bulk(author, news):
    now = timezone.now()

    all_comments = []
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        all_comments.append(comment)
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def comment_text():
    return 'Новый текст комментария'


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text}


@pytest.fixture
def get_id(news):
    return news.id


@pytest.fixture
def get_comment_id(comment):
    return comment.id


@pytest.fixture
def detail_url(get_id):
    return reverse('news:detail', kwargs={'pk': get_id})


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def edit_url(get_comment_id):
    return reverse('news:edit', kwargs={'pk': get_comment_id})


@pytest.fixture
def delete_url(get_comment_id):
    return reverse('news:delete', kwargs={'pk': get_comment_id})


@pytest.fixture
def comment_url(detail_url):
    url = detail_url + '#comments'
    return url
