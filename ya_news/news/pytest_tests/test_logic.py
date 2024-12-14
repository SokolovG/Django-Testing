from pytest_django.asserts import assertRedirects, assertFormError

from http import HTTPStatus

from news.models import Comment
from news.forms import BAD_WORDS, WARNING


def test_anonymous_user_cant_create_comment(client, detail_url, form_data):
    """
    Тест проверки запрета создания
    комментария для анонимного пользователя.
    """
    url = detail_url
    client.post(url, form_data)
    assert Comment.objects.count() == 0


def test_user_can_create_comment(author_client,
                                 form_data,
                                 detail_url,
                                 comment_text,
                                 news, author):
    """
    Тест проверки создания
    комментария для анонимного пользователя.
    """
    url = detail_url
    response = author_client.post(url, form_data)
    assertRedirects(response, f'{detail_url}#comments')
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == comment_text
    assert comment.news == news
    assert comment.author == author


def test_user_cant_use_bad_words(author_client, detail_url):
    """
    Тест проверки запрета создания
    комментария для анонимного пользователя.
    """
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    url = detail_url
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    assert Comment.objects.count() == 0


def test_author_can_delete_comment(author_client,
                                   news,
                                   delete_url,
                                   comment_url):
    """Тест проверки запрета отправки запрещенных слов."""
    url = delete_url
    response = author_client.delete(url)
    assertRedirects(response, comment_url)
    assert Comment.objects.count() == 0


def test_user_cant_delete_comment_of_another_user(not_author_client,
                                                  delete_url):
    """Тест проверки запрета удаления чужого комментария."""
    url = delete_url
    response = not_author_client.delete(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


def test_author_can_edit_comment(edit_url,
                                 author_client,
                                 form_data,
                                 comment,
                                 comment_text,
                                 comment_url):
    """Тест проверки редактирования комментария."""
    url = edit_url
    response = author_client.post(url, form_data)
    assertRedirects(response, comment_url)
    comment.refresh_from_db()
    assert comment.text == comment_text


def test_user_cant_edit_comment_of_another_user(edit_url,
                                                not_author_client,
                                                form_data,
                                                comment):
    """Тест проверки запрета редактирования чужого комментария."""
    url = edit_url
    response = not_author_client.post(url, form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
