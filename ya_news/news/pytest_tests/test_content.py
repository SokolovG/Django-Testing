from django.conf import settings

from news.forms import CommentForm


def test_count_news(client, bulk_news, home_url, db_auto_use):
    """Подсчитываем количество новостей."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = object_list.count()
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


def test_order_news(client, bulk_news, home_url):
    """Проверяем сортировку новостей."""
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    news_sorted = sorted(all_dates)
    assert news_sorted == all_dates


def test_comments(client, get_id, comments_bulk, detail_url):
    """Проверяем что наши комментарии отсортированы."""
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_comments = sorted(all_timestamps)
    assert all_timestamps == sorted_comments


def test_anonymous_client_has_no_form(client, detail_url):
    """Проверяем что у анонимного юзера нет формы."""
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    """Проверяем что у авторизированного юзера есть форма."""
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
