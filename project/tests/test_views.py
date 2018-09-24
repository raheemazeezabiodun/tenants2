from unittest.mock import patch
import pytest

from project.views import (
    get_initial_session,
    execute_query,
    get_legacy_form_submission,
    fix_newlines,
    LegacyFormSubmissionError
)
from users.tests.factories import UserFactory
from .util import qdict
from frontend.tests import test_safe_mode


def test_get_legacy_form_submission_raises_errors(graphql_client):
    request = graphql_client.request
    with pytest.raises(LegacyFormSubmissionError, match='No GraphQL query found'):
        get_legacy_form_submission(request)

    request.POST = qdict({'graphql': ['boop']})

    with pytest.raises(LegacyFormSubmissionError, match='Invalid GraphQL query'):
        get_legacy_form_submission(request)

    request.POST = qdict({'graphql': ['''
        mutation Foo($input: NonExistentInput!) { foo(input: $input) }
    ''']})

    with pytest.raises(LegacyFormSubmissionError, match='Invalid GraphQL input type'):
        get_legacy_form_submission(request)


def test_execute_query_raises_exception_on_errors(graphql_client):
    with pytest.raises(Exception) as exc_info:
        execute_query(graphql_client.request, 'bloop')
    assert 'bloop' in str(exc_info.value)


def test_get_initial_session_works(graphql_client):
    request = graphql_client.request
    assert len(get_initial_session(request)['csrfToken']) > 0


def test_invalid_post_returns_400(client):
    response = client.post('/')
    assert response.status_code == 400
    assert response.content == b'No GraphQL query found'


# HTML we know will appear in pages only when safe mode is enabled/disabled.
SAFE_MODE_ENABLED_SENTINEL = "navbar-menu is-active"
SAFE_MODE_DISABLED_SENTINEL = "main.bundle.js"


def test_index_works_when_not_in_safe_mode(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'JustFix.nyc' in response.context['title_tag']
    assert '<nav' in response.context['initial_render']

    html = response.content.decode('utf-8')
    assert SAFE_MODE_ENABLED_SENTINEL not in html
    assert SAFE_MODE_DISABLED_SENTINEL in html
    test_safe_mode.assert_html_is_not_in_safe_mode(html)


@pytest.mark.django_db
def test_index_works_when_in_safe_mode(client):
    test_safe_mode.enable_safe_mode(client)
    response = client.get('/')
    assert response.status_code == 200

    html = response.content.decode('utf-8')
    assert SAFE_MODE_ENABLED_SENTINEL in html
    assert SAFE_MODE_DISABLED_SENTINEL not in html
    test_safe_mode.assert_html_is_in_safe_mode(html)


def test_pages_with_redirects_work(client):
    response = client.get('/__example-redirect')
    assert response.status_code == 302
    assert response['location'] == '/'


def test_pages_with_extra_bundles_work(client):
    response = client.get('/__loadable-example-page')
    assert response.status_code == 200
    assert response.context['bundle_urls'] == [
        '/static/frontend/example-loadable-page.bundle.js',
        '/static/frontend/main.bundle.js'
    ]


def test_pages_with_prerendered_modals_work(client):
    response = client.get('/__example-modal')
    assert response.status_code == 200
    assert 'jf-modal-dialog' in response.context['modal_html']

    # We need to make the main content hidden when pre-rendering,
    # or else the content behind the modal will be keyboard-navigable.
    # Perhaps someday when the "inert" attribute is widely supported,
    # we could use that instead.
    assert b'<div id="main" hidden' in response.content


def test_404_works(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404


@patch('project.views.TEST_INTERNAL_SERVER_ERROR', True)
def test_500_works(client):
    response = client.get('/')
    assert response.status_code == 500
    assert response.context['bundle_urls'] == []


def test_fix_newlines_works():
    assert fix_newlines({'boop': 'hello\r\nthere'}) == {'boop': 'hello\nthere'}


def test_form_submission_redirects_on_success(django_app):
    form = django_app.get('/__example-form').forms[0]

    # Sometimes browsers will munge the newlines in our own
    # hidden inputs before submitting; let's make sure that
    # we account for that.
    assert '\r\n' not in form['graphql'].value
    assert '\n' in form['graphql'].value
    form['graphql'] = form['graphql'].value.replace('\n', '\r\n')

    form['exampleField'] = 'hi'
    response = form.submit()
    assert response.status == '302 Found'
    assert response['Location'] == '/'


def test_form_submission_shows_errors(django_app):
    response = django_app.get('/__example-form')
    assert response.status == '200 OK'

    form = response.forms[0]
    form['exampleField'] = 'hello there buddy'
    response = form.submit()

    assert response.status == '200 OK'
    form = response.forms[0]

    # Ensure the form preserves the input from our last submission.
    assert form['exampleField'].value == 'hello there buddy'

    assert 'Ensure this value has at most 5 characters (it has 17)' in response


def test_form_submission_preserves_boolean_fields(django_app):
    form = django_app.get('/__example-form').forms[0]

    assert form['boolField'].value is None
    form['boolField'] = True
    response = form.submit()

    assert response.status == '200 OK'
    form = response.forms[0]

    assert form['boolField'].value == 'on'
    form['boolField'] = False
    response = form.submit()

    assert response.status == '200 OK'
    form = response.forms[0]
    assert form['boolField'].value is None


@pytest.mark.django_db
def test_successful_login_redirects_to_next(django_app):
    UserFactory(phone_number='5551234567', password='test123')
    form = django_app.get('/login?next=/boop').forms[0]

    form['phoneNumber'] = '5551234567'
    form['password'] = 'test123'
    response = form.submit()

    assert response.status == '302 Found'
    assert response['Location'] == 'http://testserver/boop'


@pytest.mark.django_db
def test_unsuccessful_login_shows_error(django_app):
    form = django_app.get('/login?next=/boop').forms[0]

    form['phoneNumber'] = '5551234567'
    form['password'] = 'test123'
    response = form.submit()

    assert response.status == '200 OK'
    assert 'Invalid phone number or password' in response


def test_example_server_error_works(client):
    with pytest.raises(Exception, match="with id 'boop'"):
        client.post('/__example-server-error/boop')


def test_favicon_works(client, staticfiles):
    res = client.get('/favicon.ico', follow=True)
    assert res.status_code == 200
    assert res['Content-Type'] == 'image/x-icon'
